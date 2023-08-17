#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Generate fake data.
"""

from datetime import datetime, timedelta
import meerschaum as mrsm
from meerschaum.utils.misc import iterate_chunks, round_time
from typing import Any, Iterator, List, Dict

required = ['Faker', 'python-dateutil']

def fetch(
        pipe: mrsm.Pipe,
        begin: datetime | None = None,
        end: datetime | None = None,
        debug: bool = False,
        **kwargs: Any,
    ) -> Iterator[List[Dict[str, Any]]]:
    """
    For each day in the interval, yield a chunk of documents.
    """
    from dateutil.rrule import rrule, DAILY, HOURLY

    begin = begin or pipe.get_sync_time(debug=debug) or datetime(2023, 1, 1)
    end = end or round_time(datetime.utcnow(), timedelta(days=1))
    days = rrule(DAILY, dtstart=begin, until=end)

    fake = build_faker()

    for chunk_begin, chunk_end in iterate_chunks(days, 2, days[-1]):
        fake.seed_instance(int(chunk_begin.timestamp()))
        hours = rrule(HOURLY, dtstart=chunk_begin, until=chunk_end)
        
        docs = [
            {
                'timestamp': hour,
                'username': fake.user_name(),
                'attributes': {
                    'name': fake.name(),
                    'address': fake.address(),
                    'email': fake.email(),
                    'phone': fake.phone_number(),
                },
                'review': fake.text(),
                'reaction': fake.emoji(),
            }
            for hour in list(hours)[:-1]
        ]
        if docs:
            yield docs


def build_faker() -> 'faker.Faker':
    """
    Build and return an instance of `Faker`.
    """
    with mrsm.Venv('fake'):
        from faker import Faker
        from faker.providers import emoji, internet, phone_number
    fake = Faker()
    fake.add_provider(emoji)
    fake.add_provider(internet)
    fake.add_provider(phone_number)
    return fake
