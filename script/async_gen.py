#!/usr/bin/env python
import logging
import os
import re
from collections.abc import Generator, Iterable
from dataclasses import dataclass, field, fields, is_dataclass
from importlib import import_module
from itertools import chain
from pathlib import Path
from typing import ClassVar, Dict, Optional, Any, Union

from wxc_sdk import WebexSimpleApi

log = logging.getLogger(__name__)

# file name for auto generated async api source
AS_API_SOURCE = 'as_api.py'

# preamble for autogenerated async API
PREAMBLE = """# auto-generated. DO NOT EDIT
import csv
import json
import logging
import mimetypes
import os
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from dateutil import tz
from enum import Enum
from io import BufferedReader
from typing import Union, Dict, Optional, Literal, List

from aiohttp import MultipartWriter, FormData
from pydantic import parse_obj_as

from wxc_sdk.all_types import *
from wxc_sdk.as_rest import AsRestSession
from wxc_sdk.base import to_camel, StrOrDict, dt_iso_str

log = logging.getLogger(__name__)


class MultipartEncoder(FormData):
    \"""
    Compatibility class for requests toolbelt MultipartEncoder
    \"""

    def __init__(self, body):
        super().__init__()
        for name, value in body.items():
            if isinstance(value, str):
                self.add_field(name, value)
            elif isinstance(value, tuple):
                self.add_field(name, value=value[1], content_type=value[2], filename=value[0])
            else:
                raise NotImplementedError

    @property
    def content_type(self) -> str:
        return self._writer.content_type


# there seems to be a problem with getting too many users with calling data at the same time
# this is the maximum number the SDK enforces
MAX_USERS_WITH_CALLING_DATA = 10


"""




# identify sync calls to be translated to "await .." calls
RE_SYNC_CALLS = re.compile(r"""
    (?:(?:self\.(?:(?:_)?session\.)?)|  # self., self._session., self.session.
       (?:super\(\)\.))                 # super().
    (?:rest_)?(?:get|put|post|delete|patch|close|list)""",
                           flags=re.VERBOSE)

# start of a class until the 1st method
RE_CLASS_START = re.compile(r"""
    (?:^@\w+(?:\(.+\))?$\n)?            # optional decorator before the class definition with optinal parameters
    ^class\s(?P<class_name>\w+).*:$     # the 1st line of the class including the class name
    (?s:.*?)                            # non greedy match on arbitrary characters
                                        # modfier ?s: -> matches on \n, ? at the end -> non greedy
    \n+                                 # a sequence of empty lines, end of class_start
    (?=^[ ]+(?:def)|@)                  # a line starting with spaces and "def" -> 1st method
    """, flags=re.VERBOSE + re.MULTILINE)

# source of method
RE_METHOD = re.compile(r"""
    (?:^[ ]+@\w+(?:\(.+\))?$\n)?    # optional decorator
    (?P<indent>^[ ]+)def            # start of line with "def"
    \s+(?P<method_name>\S+)         # white space(s) followed by non white spaces (method name)
    \(.+$                           # .. until opening bracket until end of line.
                                    # This is end of the 1st line of the method
    (?s:.+?)                        # non greedy match on arbitrary characters
    (?=\s*                          # non capturing, (potentially empty) sequence of white spaces (empty lines)
        (?:                         # followed by one of ...
            \Z|                     # ... end of string
            ^(?P=indent)def|         # ... line with def with same indent as initial def
            # (?P=indent)@|           # ... or line starting with @ with same indent as initial def
            ^[ ]*@))                # .. or just a line starting with a @ indicating the start of a decoration
    """, flags=re.VERBOSE + re.MULTILINE)

# method def
RE_METHOD_DEF = re.compile(r"""
    def         # def
    \s+\S+?     # followed by white spaces and non-greedy sequence of non-whitespaces
    \(      # ..until opening bracket
    """, flags=re.VERBOSE)

# Generator return annotation
RE_GENERATOR = re.compile(r'->\s*Generator\[(?P<gen_type>\w+)(?P<post>.+)')

RE_FOLLOW_PAGINATION = re.compile("""
    return\s(?P<follow>\S+?follow_pagination\((?s:.+)?\))
""", flags=re.VERBOSE)

# block comment with async code to put in for method
RE_ASYNC_SOURCE = re.compile("'''async(.*?)$(?P<async_source>.+?)'''", flags=re.VERBOSE + re.DOTALL + re.MULTILINE)


@dataclass
class Module:
    #: project relative module name
    module_name: str = field(init=False)
    #: absolute path
    abs_path: Path
    #: project relative path
    proj_path: Path = field(init=False)
    #: set of names of modules importing from this module
    imported_by_module_names: set[str] = field(init=False)
    #: list of imports in this module
    imports: list['Import'] = field(init=False)
    #: imported module
    imported_module: Any = field(init=False)

    #: module registry
    registry: ClassVar[Dict[str, 'Module']] = {}

    def __post_init__(self):
        """
        Initialize module from path
        """
        parts = list(self.abs_path.parts)
        parts.reverse()
        # forget the parts before the project root directory
        parts = parts[:parts.index('wxc_sdk') + 1]
        self.proj_path = Path(os.path.join(*(reversed(parts))))

        self.module_name = self.module_name_from_path(path=self.abs_path)
        self.imported_module = import_module(self.module_name)
        self.registry[self.module_name] = self
        self.imports = []
        self.imported_by_module_names = set()

    @classmethod
    def module(cls, module_name: str) -> 'Module':
        try:
            return cls.registry[module_name]
        except KeyError:
            raise

    @classmethod
    def init_imports(cls):
        """
        Initialize imported_by and imports attributes of all registered modules
        """
        for module in cls.registry.values():
            module: Module
            module.imports = list(module.imported())
            imported_from = set(imp.module_name for imp in module.imports)
            for imported_from_module_name in imported_from:
                cls.module(module_name=imported_from_module_name).imported_by_module_names.add(module.module_name)

    @staticmethod
    def module_name_from_path(*, path: Path) -> str:
        """
        Create a module name from a path
        :param path:
        :return:
        """
        parts = list(path.parts)
        parts.reverse()
        # forget the parts before the project root directory
        parts = parts[:parts.index('wxc_sdk') + 1]
        # remove the file extension from the last part
        parts[0] = os.path.splitext(parts[0])[0]
        # __init__ takes the package name
        if parts[0] == '__init__':
            parts = parts[1:]
        mod_name = '.'.join(reversed(parts))
        log.debug(f'_module_name_from_path(\'{path}\'): {mod_name}')
        return mod_name

    def source(self) -> str:
        """
        Get Python source of module
        :return: source
        """
        with open(self.abs_path, mode='r') as f:
            return f.read()

    def imported(self) -> Generator['Import', None, None]:
        source = self.source()
        import_re = re.compile(r'^from\s+(?P<module>(?:wxc)?\.\S+)\s+import\s+(?P<imports>.+)$', flags=re.MULTILINE)
        for m in import_re.finditer(source):
            module_name = m.group('module')
            imports = m.group('imports').strip()
            if module_name.startswith('.'):
                # create absolute module name; relative to project path of current module
                mod_path = list(self.proj_path.parts)[:-1]
                mod_path.append('.')
                # drop parts of the path for each leading "."; climb up one directory for each "."
                while module_name.startswith('.'):
                    module_name = module_name[1:]
                    mod_path = mod_path[:-1]
                module_name = f'{".".join(mod_path)}.{module_name}'
            log.debug(f'imported({self.proj_path}): {m.group(0)} -> module {module_name}')
            for imported_item in imports.split(','):
                imported_item = imported_item.strip()
                one_import = Import.register(module_name=module_name, name=imported_item, imported_in=self)
                yield one_import

    @classmethod
    def module_order(cls) -> Generator['Module', None, None]:
        """
        yield modules in order so that all imported modules comme before modules that depend on them
        """
        visited = set()

        def visit(module: Module) -> Generator['Module', None, None]:
            if module.module_name in visited:
                return
            visited.add(module.module_name)
            yield from chain.from_iterable(map(lambda i: visit(i.module), module.imports))
            yield module

        yield from chain.from_iterable(map(visit, cls.registry.values()))

    def dependants_gen(self) -> Generator['Module', None, None]:
        """
        Generator for all modules that depend on this module
        :return:
        """
        visited = set()

        def visit(module_name: str) -> Generator['Module', None, None]:
            mod = self.registry[module_name]
            mod: Module
            if mod.module_name in visited:
                return
            visited.add(mod.module_name)
            yield from chain.from_iterable(map(visit, mod.imported_by_module_names))
            yield mod

        yield from chain.from_iterable(map(visit, self.imported_by_module_names))

    @property
    def dependants(self) -> list['Module']:
        return list(self.dependants_gen())


@dataclass
class Import:
    """
    an imported item
    """
    #: module the item was imported from
    module_name: str
    #: name of imported item
    name: str
    #: fully qualified identifier
    qualident: str = field(init=False)

    registry: ClassVar[dict[str, 'Import']] = {}

    #: imported into which modules
    imported_in_module_names: set[str] = field(init=False)

    def __post_init__(self):
        self.imported_in_module_names = set()
        self.qualident = f'{self.module_name}.{self.name}'
        self.registry[self.qualident] = self

    @classmethod
    def register(cls, module_name: str, name: str, imported_in: Module) -> 'Import':
        """
        Register an import
        :param module_name: module name of imported item
        :param name: name of imported item
        :param imported_in: module the item is imported in
        :return: Import object
        """
        qualident = f'{module_name}.{name}'
        import_obj = cls.registry.get(qualident)
        if import_obj is None:
            import_obj = Import(module_name=module_name, name=name)
        import_obj.imported_in_module_names.add(imported_in.module_name)
        return import_obj

    @property
    def module(self) -> Module:
        return Module.module(self.module_name)


def source_paths() -> list[Path]:
    """
    Get list of Python source files that are part of the project

    :return: list of absolute paths
    """

    # project root path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'wxc_sdk'))
    py_files = list(Path(project_root).rglob('*.py'))
    py_files.sort()
    # don't look at the file we are about to create
    py_files = [path for path in py_files
                if os.path.basename(path) != AS_API_SOURCE]
    return py_files


@dataclass
class ClassDef:
    class_name: str
    decorator: Optional[str]
    module_name: Optional[str]
    source: Optional[str]
    base_classes: set[str] = field(default_factory=set)
    is_base_of: set[str] = field(default_factory=set)

    #: registry of classes. Key is the unqualified class name
    registry: ClassVar[dict[str, 'ClassDef']] = {}

    def derived_classes(self) -> Generator['ClassDef', None, None]:
        """
        Recursively determine all classes derived from given class
        """
        visited = set()
        visited.add(self.class_name)

        def visit(*, base: ClassDef, skip_super=False) -> Generator['ClassDef', None, None]:
            if skip_super or base.class_name in visited:
                return
            visited.add(base.class_name)
            yield from chain.from_iterable(visit(base=self.registry[class_name])
                                           for class_name in base.is_base_of)

        return visit(base=self, skip_super=True)

    @classmethod
    def register_class(cls, *, class_name: str, module_name: str = None, decorator: Optional[str] = None,
                       bases: Optional[str] = None, source: str = None) -> 'ClassDef':
        cd = cls.registry.get(class_name)
        if cd is None:
            cd = ClassDef(class_name=class_name, decorator=decorator, module_name=module_name,
                          source=source)
            cls.registry[class_name] = cd
        cd.source = cd.source or source
        cd.decorator = cd.decorator or decorator
        cd.module_name = cd.module_name or module_name
        if bases:
            parsed_bases = bases.split(',')
            parsed_bases = [b.strip() for b in parsed_bases]
            parsed_bases = [b for b in parsed_bases if re.match(r'^\w+$', b)]
            for base in parsed_bases:
                cls.register_as_base(class_name=base, is_base_of=class_name)
        return cd

    @classmethod
    def register_as_base(cls, *, class_name: str, is_base_of: str):
        cd = cls.registry.get(is_base_of)
        if cd:
            cd: ClassDef
            cd.base_classes.add(class_name)
        else:
            cls.register_class(class_name=is_base_of, bases=class_name, source=None, module_name=None, decorator=None)
        base = cls.register_class(class_name=class_name, bases=None, source=None, module_name=None, decorator=None)
        base.is_base_of.add(is_base_of)

    @classmethod
    def from_path(cls, path: Union[str, Path]) -> Generator['ClassDef', None, None]:
        class_re = re.compile(r'(?:^@(?P<decorator>\w+).*$\n)?^class\s+(?P<class_name>\w+)(?:\((?P<bases>.+)\))?:\s*$('
                              r'?:\n^(?:\W.*)?$)+',
                              flags=re.MULTILINE)
        with open(path, mode='r') as f:
            source = f.read()
        module_name = Module.module_name_from_path(path=path)
        for m in class_re.finditer(source):
            cd = ClassDef.register_class(module_name=module_name, source=m.group(0), **m.groupdict())
            yield cd


VISITED_FOR_CLASS_SOURCES = set()


def class_sources(*, target: type) -> Generator[str, None, None]:
    """
    Dump source for one class. Descend into all dependencies before dumping the source for this class
    :param target: class to dump source of
    """
    # pretend we already visited RestSession
    VISITED_FOR_CLASS_SOURCES.add('RestSession')

    def act_on(*, target_class_name: str, level: int = 0) -> Generator[str, None, None]:
        def logger(message: str):
            log.debug(f'{" " * (level * 2)}act_on ({target_class_name}): {message}')

        logger('start')

        # assert that each class is only visited once
        if target_class_name in VISITED_FOR_CLASS_SOURCES:
            logger('already visited -> done')
            return
        VISITED_FOR_CLASS_SOURCES.add(target_class_name)

        # get target class
        class_def = ClassDef.registry.get(target_class_name)
        if not class_def:
            raise KeyError(f'No ClassDef for {target_class_name}')
        class_def: ClassDef

        # load module the target
        module_name = class_def.module_name
        if module_name is None:
            logger('not defined within project. We are done here')
            return

        logger(f'defined in module {module_name}')

        try:
            module_info = Module.registry[module_name]
        except KeyError:
            logger(f'no module infor for module {module_name}')
            raise
        module_info: Module

        imported_module = module_info.imported_module
        try:
            target_class = imported_module.__dict__[target_class_name]
        except KeyError:
            logger(f'class "{target_class_name}" not found in module {module_name}, {imported_module.__file__}')
            raise

        # check for attributes of the class
        if is_dataclass(target_class):
            attributes = fields(target_class)
            attributes = sorted(attributes, key=lambda a: a.name)
            logger(f'attributes {", ".join(f"{a.name}: {a.type.__name__}" for a in attributes)}')
        else:
            attributes = []

        depends_on_class_names = set(attribute.type.__name__ for attribute in attributes)
        # check base classes
        bases = class_def.base_classes
        logger(f'base classes: {", ".join(sorted(bases)) or "None"}')
        depends_on_class_names.update(bases)

        # make sure to cover the classes we depend on 1st
        yield from chain.from_iterable(map(lambda class_name: act_on(target_class_name=class_name, level=level + 1),
                                           sorted(depends_on_class_names)))

        logger('dependencies addressed')

        yield class_def.source

    return act_on(target_class_name=target.__name__)


@dataclass
class ClassTransform:
    class_name: str
    regex: re.Pattern
    replacement: str

    registry: ClassVar[dict[str, 'ClassTransform']] = dict()

    def __post_init__(self):
        self.registry[self.class_name] = self

    def apply(self, *, source: str) -> tuple[str, int]:
        """
        Apply the transform

        :param source:
        :return:
        """
        return self.regex.subn(repl=self.replacement, string=source)

    @staticmethod
    def from_class_name(class_name: str) -> 'ClassTransform':
        """
        Transform for given class name

        :param class_name:
        :return:
        """
        log.debug(f'New ClassTransform: {class_name} -> As{class_name}')
        return ClassTransform(class_name=class_name,
                              regex=re.compile(f'(\\b){class_name}(\\b)'),
                              replacement=f'\g<1>As{class_name}\g<2>')

    @classmethod
    def appy_all(cls, *, source: str) -> tuple[str, int]:
        """
        Apply all registered class name transforms

        :param source:
        :return:
        """
        total_subs = 0
        for transform in cls.registry.values():
            transform: ClassTransform
            source, subs = transform.apply(source=source)
            total_subs += subs
        return source, total_subs


def transform_classes_to_async(sources: Iterable[str]) -> Generator[str, None, None]:
    def transform_method(*, class_name: str, method_match: re.Match) -> str:
        """
        Transform source of one method

        :param class_name:
        :param method_match:
        :return:
        """
        method_name = method_match.group('method_name')
        source = method_match.group(0)
        # replace all known class names
        source, subs = ClassTransform.appy_all(source=source)
        log.debug(f'transform_method ({class_name}.{method_name}): class name transformations: {subs}')

        # see if there is a a """:async block which as the async code
        if async_code_match := RE_ASYNC_SOURCE.search(source):
            log.debug(f'transform_method ({class_name}.{method_name}): using async code from async block comment')
            async_code = async_code_match.group('async_source').strip('\n')
            return async_code

        # see if there is a call that "smells" like async
        source, subs = RE_SYNC_CALLS.subn(repl='await \g<0>', string=source)
        if subs:
            log.debug(f'transform_method ({class_name}.{method_name}): async call added, change method to "async '
                      f'def {method_name}"')
            # found a sync call --> also need to change the method signature to "async"
            source = re.sub(r'(^[ ]+)def', '\g<1>async def', source)

        source, subs = re.subn(r'(?:async )?def __(enter|exit)__', 'async def __a\g<1>__', source)
        if subs:
            log.debug(f'transform_method ({class_name}.{method_name}): converted enter/exit to __aenter__/__aexit__')

        if RE_GENERATOR.search(source):
            log.debug(f'transform_method ({class_name}.{method_name}): generator detected')

            # this is a method which returns a generator
            # -> generate two_methods:
            #   * def <method>_gen(...) -> AsyncGenerator[...
            #   * async def <method>(...) -> list[
            #       * switch return self.session.follow_pagination(url=ep, model=Person, params=params)
            #       * to: return [o async for o in self.session.follow_pagination(url=ep, model=Person, params=params)]

            # switch Generator[ to AsyncGenerator for async generator
            gen_source, subs = RE_GENERATOR.subn('-> AsyncGenerator[\g<gen_type>\g<post>', source)
            if not subs:
                raise ValueError(f'Changing "Generator" to "AsyncGenerator" failed for {class_name}.{method_name}')

            # rename generator method name to _gen; only 1st occurrence
            gen_source, subs = RE_METHOD_DEF.subn(f'def {method_name}_gen(', gen_source, count=1)
            if not subs:
                raise ValueError(f'Changing method name to *_gen failed for {class_name}.{method_name}')
            log.debug(f'transform_method ({class_name}.{method_name}): created {class_name}.{method_name}_gen')

            # now change signature to 'async def'
            source, subs = RE_METHOD_DEF.subn(f'async def {method_name}(', source, count=1)
            if not subs:
                raise ValueError(f'creating "async def {method_name}" failed for'
                                 f' {class_name}.{method_name}')
            # update return signature
            source, subs = RE_GENERATOR.subn('-> List[\g<gen_type>]:', source)
            if not subs:
                raise ValueError(f'updating return signature to "-> list[..]"failed for'
                                 f' {class_name}.{method_name}')
            source, subs = RE_FOLLOW_PAGINATION.subn('return [o async for o in \g<follow>]', source)
            if not subs:
                raise ValueError(f'updating return return failed for'
                                 f' {class_name}.{method_name}')
            log.debug(f'transform_method ({class_name}.{method_name}): created {class_name}.{method_name} -> list[...')
            source = '\n\n'.join((gen_source, source))
        return source

    def transform_class(*, source: str) -> str:
        """
        transform source of one method to async

        * each class has a part before the 1st method and some methods
        * not all methods have a call to an async method
        * properties remain unchanged
        :param source:
        :return:
        """
        m = RE_CLASS_START.match(source)
        if not m:
            raise ValueError('No class name?')
        class_name = m.group('class_name')
        log.debug(f'transform_class({class_name}): start')
        # create and register new transform
        ClassTransform.from_class_name(class_name)

        # apply transforms to start of class def
        class_start = m.group(0)
        class_start, subs = ClassTransform.appy_all(source=class_start)
        log.debug(f'transform_class({class_name}): replacements in class start: {subs}')
        class_start, subs = re.subn(r':class:`.+\.As', ':class:`As', class_start)
        log.debug(f'transform_class({class_name}): replacements for ":class:" declarations: {subs}')

        # get all methods
        method_matches = list(RE_METHOD.finditer(source))
        log.debug(f'transform_class({class_name}): methods: '
                  f'{", ".join(m.group("method_name") for m in method_matches)}')

        # new source: transformed class start followed by transformed methods
        transformed_methods = "\n\n".join(map(lambda m: transform_method(class_name=class_name,
                                                                         method_match=m),
                                              method_matches))
        source = f'{class_start}{transformed_methods}'
        return source

    # we suppressed the source for RestSession, but the class name still needs to be translated
    ClassTransform.from_class_name('RestSession')
    for class_source in sources:
        yield transform_class(source=class_source)


def gen():
    # start with WebexSimpleApi
    as_api_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'wxc_sdk', AS_API_SOURCE))
    with open(as_api_path, mode='w') as combined:
        combined.write(PREAMBLE)
        converted_classes_source = '\n\n\n'.join(transform_classes_to_async(class_sources(target=WebexSimpleApi)))
        visited_classes = sorted(VISITED_FOR_CLASS_SOURCES)

        # created nicely formatted __all__ section
        line = '__all__ = ['
        max_line = 120
        for name in visited_classes:
            entry = f"'As{name}', "
            if len(line) + len(entry) >= max_line:
                print(line.rstrip(), file=combined)
                line = ' ' * 11

            line = f'{line}{entry}'
        print(f'{line.rstrip(" ,")}]', file=combined)
        print('\n', file=combined)
        combined.write(converted_classes_source)
    return


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    paths = source_paths()

    # register all classes in all source paths
    list(chain.from_iterable(ClassDef.from_path(p) for p in paths))

    # register all modules
    modules = list(map(Module, paths))
    Module.init_imports()

    # names of modules that use rest (depend on rest)
    uses_rest = set(m.module_name for m in Module.registry['wxc_sdk.rest'].dependants_gen())

    # modules depending on rest
    mo = list(m for m in Module.module_order()
              if m.module_name in uses_rest)

    for module in Module.registry.values():
        imported = import_module(module.module_name)
        foo = 1
    modules = list(Module.registry)
    for import_qualident in sorted(Import.registry):
        import_item: Import = Import.registry[import_qualident]
        print(f'{import_qualident}: {", ".join(sorted(import_item.imported_in_module_names))}')
    gen()
