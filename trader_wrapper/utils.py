from django.core.management.base import BaseCommand
import logging
from trader_wrapper.models import Event, Constants, AttrDict, Player, EventType, Direction
from dateparser import parse
from dateutil.relativedelta import relativedelta
import random
from itertools import cycle
from enum import Enum
from django.utils import timezone
import pytz

utc = pytz.utc
logger = logging.getLogger(__name__)

import pandas as pd
import numpy as np


def pp(start, end, n):
    """Taken from: https://stackoverflow.com/questions/50559078/generating-random-dates-within-a-given-range-in-pandas.
    Just generate a sorted list of N random timestamps between two dates from two python datetimes"""
    start_u = pd.Timestamp(start).value // 10 ** 6
    end_u = pd.Timestamp(end).value // 10 ** 6
    return sorted(pd.to_datetime(
        pd.DatetimeIndex(
            (10 ** 6 * np.random.randint(start_u, end_u, n, dtype=np.int64)).view('M8[ns]'),
            tz=utc, ),
        unit='ms'),
    )


class MockPlayer:
    attainable_events = dict(
        work=[EventType.task, EventType.change_tab],
        trade=[EventType.change_tab, EventType.transaction, EventType.change_stock_tab]
    )

    def __init__(self, owner, num_events):
        self.owner = owner
        self.num_events = num_events
        start = self.owner.start_time
        end = self.owner.end_time
        event_timestamps = pp(start, end, num_events)
        for i in event_timestamps:
            self.generate_random_event(i)

    def generate_random_event(self, timestamp):
        if timezone.is_naive(timestamp):
            timezone.make_aware(timestamp, timezone=utc)

        self.current_timestamp = timestamp

        attainable_tasks = self.attainable_events[self.owner.current_tab]
        ev = random.choice(attainable_tasks)
        params = getattr(self, ev)()
        # this if condition is only valid for transactions (which can be unattainable due to monetary/depository reasons
        if params:
            self.register_event(event_name=ev, params=params)

    def register_event(self, event_name, params, ):
        data = dict(name=event_name,
                    body=params,
                    timestamp=self.current_timestamp)
        self.owner.register_event(data=data)

    def change_tab(self):
        tab = [t for t in Constants.tabs if t != self.owner.current_tab][0]
        return dict(tab_name=tab)

    def transaction(self):
        o = self.owner
        stonks = o.deposit.all()
        direction = random.choice([Direction.buy, Direction.sell])
        if direction == Direction.sell:
            stonks = stonks.filter(quantity__gt=0)
            # we have nothing to sell - action impossible :( :
            if not stonks.exists():
                return
            r = random.choice(stonks)
            q = random.randint(1, r.quantity) * direction

        if direction == Direction.buy:
            b = o.ending_balance
            r = random.choice(stonks)
            p = o.get_price(timestamp=self.current_timestamp, stock_name=r.name)
            max_q = b // p
            if max_q < 1:
                return
            q = random.randint(1, max_q) * direction
        return dict(quantity=q, name=r.name, direction=direction)

    def submit_task(self):
        task = self.owner.get_current_task(self.current_timestamp)
        is_correct = random.choice([False, True])
        if is_correct:
            return dict(answer=task.correct_answer, task_id=task.id)
        else:
            return dict(answer=task.correct_answer + '666', task_id=task.id)

    def change_stock_tab(self):
        current_tab = self.owner.current_stock_shown
        n = random.choice([i for i in Constants.stocks if i != current_tab])
        return dict(tab_name=n)


def creating_events(session):
    logger.info(f'Gonna generate a mocked data in trading platform for session {session.code}')
    for p in session.get_participants():
        age = random.randint(18, 100)
        gender = random.choice(['Male', 'Female'])
        income = random.randint(0, 7)

        pls = Player.objects.filter(participant=p)
        for i in pls:
            i.age = age
            i.gender = gender
            i.income = income
            nevents = random.randint(50, 100)
            m = MockPlayer(owner=i, num_events=nevents)
