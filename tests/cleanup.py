#!/usr/bin/env python
"""
Clean up test objects created by test cases
"""
import asyncio
import logging
import os
import re
import sys
import time
from collections import defaultdict
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from itertools import chain, zip_longest
from re import Pattern
from typing import Union

from tests.base import get_tokens
from wxc_sdk import WebexSimpleApi
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.common import NumberState
from wxc_sdk.telephony import NumberType, NumberListPhoneNumber
from wxc_sdk.telephony.callqueue import CallQueue

TO_DELETE = re.compile(r'^(?:(?:\w{2}_|many_|test_|test_ann_|test_user_|workspace test |CPE |cpe_|cp)\d{3})|National Holidays$')
DRY_RUN = False


def filtered(targets, name_getter=None, alternate_matches: Union[Pattern, str] = None):
    def default_name_getter(item):
        return item.name

    name_getter = name_getter or default_name_getter

    if isinstance(alternate_matches, str):
        alternate_matches = re.compile(alternate_matches)

    for t in targets:
        name = name_getter(t)
        if alternate_matches and alternate_matches.match(name) or TO_DELETE.match(name):
            yield t
        else:
            print(f'Keeping {t.__class__.__name__}({name})')


async def main():
    tokens = get_tokens()
    if not tokens:
        print('Failed to get tokens', file=sys.stderr)
        exit(1)
    api = WebexSimpleApi(tokens=tokens)
    # get calling locations
    locations = list(api.locations.list())
    async with AsWebexSimpleApi(tokens=tokens) as as_api:
        details = await asyncio.gather(*[as_api.telephony.location.details(location_id=loc.location_id)
                                         for loc in locations], return_exceptions=True)
    locations = [loc for loc, detail in zip(locations, details)
                 if not isinstance(detail, Exception)]

    log_name = f'{os.path.splitext(__file__)[0]}.log'

    fmt = logging.Formatter(fmt='%(asctime)s %(threadName)s %(message)s')
    fmt.converter = time.gmtime

    fh = logging.FileHandler(log_name, mode='w')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    rest_logger = logging.getLogger('wxc_sdk.rest')
    rest_logger.addHandler(fh)
    rest_logger.setLevel(logging.DEBUG)

    rest_logger = logging.getLogger('wxc_sdk.as_rest')
    rest_logger.addHandler(fh)
    rest_logger.setLevel(logging.DEBUG)

    with ThreadPoolExecutor() as pool:

        # MPPs with mac DEADEAD mac or stll in "activating"
        mpp_devices = [device for device in api.devices.list(product_type='phone')
                       if device.mac and device.mac.startswith('DEADDEAD') or
                       device.connection_status and device.connection_status == 'activating']
        print(f'deleting {len(mpp_devices)} MPP phones: {", ".join(mpp.display_name for mpp in mpp_devices)}')
        if not DRY_RUN:
            list(pool.map(lambda mpp: api.devices.delete(device_id=mpp.device_id),
                          mpp_devices))

        # remove Dustin Harris from Call Queues
        if False:
            dustins = list(api.people.list(display_name='Dustin Harris'))
            if dustins:
                dustin = dustins[0]
                call_queues = list(api.telephony.callqueue.list())
                details = list(
                    pool.map(lambda cq: api.telephony.callqueue.details(location_id=cq.location_id, queue_id=cq.id),
                             call_queues))
                remove_from = [cq for cq in details
                               if next((agent for agent in cq.agents
                                        if agent.agent_id == dustin.person_id), None) is not None]

                def queue_wo_dustin(cq: CallQueue) -> CallQueue:
                    wo_dustin = cq.model_copy(deep=True)
                    wo_dustin.agents = [agent for agent in cq.agents if agent.agent_id != dustin.person_id]
                    return wo_dustin

                if remove_from:
                    list(pool.map(lambda cq: api.telephony.callqueue.update(location_id=cq.location_id, queue_id=cq.id,
                                                                            update=queue_wo_dustin(cq)), remove_from))

        # auto attendants
        ata = api.telephony.auto_attendant
        aa_list = list(filtered(ata.list()))
        print(f'deleting {len(aa_list)} auto attendants: {", ".join(aa.name for aa in aa_list)}')
        if not DRY_RUN:
            list(pool.map(lambda aa: ata.delete_auto_attendant(location_id=aa.location_id,
                                                               auto_attendant_id=aa.auto_attendant_id),
                          aa_list))
        # call parks
        atc = api.telephony.callpark
        cp_list = list(filtered(chain.from_iterable(
            pool.map(lambda l: atc.list(location_id=l.location_id),
                     locations)), alternate_matches=r'CPG\d'))
        print(f'deleting {len(cp_list)} call parks: {", ".join(cp.name for cp in cp_list)}')
        if not DRY_RUN:
            list(pool.map(lambda cp: atc.delete_callpark(location_id=cp.location_id, callpark_id=cp.callpark_id),
                          cp_list))

        # call pickups
        atp = api.telephony.pickup
        cpu_list = list(filtered(chain.from_iterable(
            pool.map(lambda l: atp.list(location_id=l.location_id),
                     locations))))
        print(f'deleting {len(cpu_list)} call pickups: {", ".join(cp.name for cp in cpu_list)}')
        if not DRY_RUN:
            list(pool.map(lambda cp: atp.delete_pickup(location_id=cp.location_id, pickup_id=cp.pickup_id),
                          cpu_list))

        # call queues
        atq = api.telephony.callqueue
        cq_list = list(filtered(atq.list()))
        print(f'deleting {len(cq_list)} call queues: {", ".join(cq.name for cq in cq_list)}')
        if not DRY_RUN:
            list(pool.map(lambda cq: atq.delete_queue(location_id=cq.location_id, queue_id=cq.id),
                          cq_list))

        # hunt groups
        ath = api.telephony.huntgroup
        hg_list = list(filtered(chain.from_iterable(
            pool.map(lambda l: ath.list(location_id=l.location_id),
                     locations))))
        print(f'deleting {len(hg_list)} hunt groups: {", ".join(hg.name for hg in hg_list)}')
        if not DRY_RUN:
            list(pool.map(lambda hg: ath.delete_huntgroup(location_id=hg.location_id, huntgroup_id=hg.id),
                          hg_list))

        # paging groups
        atpg = api.telephony.paging
        pg_list = list(filtered(atpg.list()))
        print(f'deleting {len(pg_list)} paging groups: {", ".join(pg.name for pg in pg_list)}')
        if not DRY_RUN:
            list(pool.map(lambda pg: atpg.delete_paging(location_id=pg.location_id, paging_id=pg.paging_id),
                          pg_list))

        # schedules
        ats = api.telephony.schedules
        schedule_list = list(filtered(chain.from_iterable(
            pool.map(lambda l: ats.list(obj_id=l.location_id),
                     locations)), alternate_matches=r'\w+ \d{2}'))
        print(f'deleting {len(schedule_list)} schedules: {", ".join(schedule.name for schedule in schedule_list)}')
        if not DRY_RUN:
            list(pool.map(lambda schedule: ats.delete_schedule(obj_id=schedule.location_id,
                                                               schedule_type=schedule.schedule_type,
                                                               schedule_id=schedule.schedule_id),
                          schedule_list))

        # person schedules
        aps = api.person_settings.schedules
        users = [user for user in api.people.list(calling_data=True)
                 if user.location_id]

        schedule_lists = list(pool.map(lambda user: list(aps.list(obj_id=user.person_id)),
                                       users))
        users_and_schedules = list(chain.from_iterable(((user, schedule)
                                                        for schedule in filtered(schedules))
                                                       for user, schedules in zip(users, schedule_lists)))
        print(f'deleting {len(users_and_schedules)} user schedules:'
              f' {", ".join(f"{user.display_name}-{schedule.name}" for user, schedule in users_and_schedules)}')

        if not DRY_RUN:
            list(pool.map(
                lambda user_and_schedule: aps.delete_schedule(
                    obj_id=user_and_schedule[0].person_id,
                    schedule_type=user_and_schedule[1].schedule_type,
                    schedule_id=user_and_schedule[1].schedule_id),
                users_and_schedules))

        # groups
        groups = list(filtered(api.groups.list(),
                               name_getter=lambda g: g.display_name))
        groups.sort(key=lambda g: g.display_name)
        print(f'Deleting {len(groups)} groups')
        if not DRY_RUN:
            list(pool.map(lambda g: api.groups.delete_group(group_id=g.group_id),
                          groups))

        # workspaces
        workspaces = list(filtered(api.workspaces.list(),
                                   name_getter=lambda w: w.display_name))
        print(f'Deleting {len(workspaces)} workspaces')
        if not DRY_RUN:
            list(pool.map(lambda ws: api.workspaces.delete_workspace(workspace_id=ws.workspace_id),
                          workspaces))

        # voicemail groups
        groups = list(filtered(api.telephony.voicemail_groups.list()))
        print(f'Deleting {len(groups)} voicemail groups')
        if not DRY_RUN:
            list(pool.map(lambda g: api.telephony.voicemail_groups.delete(location_id=g.location_id,
                                                                          voicemail_group_id=g.group_id),
                          groups))

        # inactive unused numbers
        numbers = [number
                   for number in api.telephony.phone_numbers(state=NumberState.inactive, number_type=NumberType.number)
                   if number.owner is None and not number.main_number]
        print(f'Deleting {len(numbers)} phone numbers')
        numbers_by_location: dict[str, list[NumberListPhoneNumber]] = reduce(
            lambda red, number: red[(number.location.id, number.location.name)].append(number) or red,
            numbers,
            defaultdict(list))
        if numbers_by_location:
            loc_len = max(map(lambda k: len(k[1]), numbers_by_location))
            print('\n'.join(f'  {l_name:{loc_len}} ({len(numbers)} numbers): '
                            f'{", ".join(number.phone_number for number in numbers)}'
                            for (l_id, l_name), numbers in numbers_by_location.items()))
        if not DRY_RUN:
            # delete numbers in batches of 5
            def batches_to_delete() -> Generator[tuple[str, list[str]]]:
                for (l_id, l_name), numbers in numbers_by_location.items():
                    n_iter = iter(numbers)
                    for batch in zip_longest(*([n_iter] * 5),
                                             fillvalue=None):
                        batch = [n.phone_number for n in batch if n]
                        yield l_id, batch

            batches = list(batches_to_delete())
            list(pool.map(
                lambda v: api.telephony.location.number.remove(
                    location_id=v[0],
                    phone_numbers=v[1]),
                batches))

        # dial plans
        dial_plans = list(filtered(list(api.telephony.prem_pstn.dial_plan.list())))
        print(f'Deleting {len(dial_plans)} dialplans')
        if not DRY_RUN:
            list(pool.map(lambda dp: api.telephony.prem_pstn.dial_plan.delete_dial_plan(dial_plan_id=dp.dial_plan_id),
                          dial_plans))

        # call park extensions
        cpe_list = list(filtered(api.telephony.callpark_extension.list(), alternate_matches=r'\w\d{4}'))
        print(f'Deleting {len(cpe_list)} call park extensions')
        if not DRY_RUN:
            list(pool.map(lambda cpe: api.telephony.callpark_extension.delete(location_id=cpe.location_id,
                                                                              cpe_id=cpe.cpe_id),
                          cpe_list))

        # teams
        teams = list(filtered(api.teams.list(),
                              alternate_matches=r'Team Test \d{3}'))
        print(f'Deleting {len(teams)} teams')
        if not DRY_RUN:
            list(pool.map(lambda team: api.teams.delete(team_id=team.id), teams))

    async with AsWebexSimpleApi(tokens=tokens) as as_api:
        # workspace locations
        # we can only delete workspace locations which are not enabled for calling
        if False:
            locations = [loc for loc in api.workspace_locations.list()
                         if re.search(r'\b(\w{2})\b (\d+) USA', loc.address)]
            print(f'Deleting {len(locations)} locations')
            if not DRY_RUN:
                await asyncio.gather(*[as_api.workspace_locations.delete(location_id=loc.id)
                                       for loc in locations],
                                     return_exceptions=True)

        # spaces
        spaces = list(filtered(api.rooms.list(),
                               alternate_matches=r'(Test Space \d{3})||(public \w{8}-\w{4}-\w{4}-\w{4}-\w{12})',
                               name_getter=lambda i: i.title))
        print(f'Deleting {len(spaces)} spaces')
        if not DRY_RUN:
            await asyncio.gather(*[as_api.rooms.delete(room_id=space.id) for space in spaces],
                                 return_exceptions=True)

        # try deleting all announcements and ignore any errors
        anns = list(filtered(await as_api.telephony.announcements_repo.list()))
        try:
            await asyncio.gather(
                *[api.telephony.announcements_repo.delete(announcement_id=ann.id) for ann in anns],
                return_exceptions=True)
        except Exception:
            pass


if __name__ == '__main__':
    asyncio.run(main())
