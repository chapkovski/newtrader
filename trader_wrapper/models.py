from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from pprint import pprint
from otree.models import Session
import random
from django.db import models as djmodels
from django.utils import timezone
from itertools import cycle
import json
import csv
import yaml
author = 'Philipp Chapkovski, University of Bonn'

doc = """
Backend for trading platform 
"""
def conv(x): return [float(i.strip()) for i in x.split(',')]


class Constants(BaseConstants):
    name_in_url = 'trader_wrapper'
    players_per_group = None
    training_rounds = [1]
    num_rounds = 5
    tick_frequency = 6
    tick_num = 10
    with open(r'./data/blocks.yaml') as file:
        blocks = yaml.load(file, Loader=yaml.FullLoader)
    with open(r'./data/treatments.yaml') as file:
        treatments = yaml.load(file, Loader=yaml.FullLoader)
    num_blocks = len(blocks)
    num_treatments = len(treatments)
    blocked_treatments = []
    for b in blocks:
        for t in treatments:
            bc = b.copy()
            bc.update(t)
            blocked_treatments.append(bc)
    
    def price_reader(stub, i):
        def pathfinder(x): return f'data/{x}'
        price_path = pathfinder(f'{stub}{i}.csv')
        with open(price_path, newline='') as csvfile:
            stockreader = csv.DictReader(csvfile, delimiter=',')
            stockreader = [float(i.get('stock')) for i in stockreader]
            return stockreader
    prices_normal = []
    prices_martingale = []

    for i in range(5):
        prices_normal.append(price_reader('prices_markov_main_', i))
        prices_martingale.append(price_reader('prices_markov_robust_', i))


def flatten(t):
    return [item for sublist in t for item in sublist]


class Subsession(BaseSubsession):
    tick_frequency = models.FloatField()
    max_length = models.FloatField()

    def creating_session(self):
        awards_at = conv(self.session.config.get('awards_at', ''))
        assert len(
            awards_at) == 5, 'Something is wrong with awards_at settings. Check again'
        self.session.vars['awards_at'] = awards_at

        if self.round_number == 1:
            params = {}
            params['game_rounds'] = Constants.num_rounds
            params['exchange_rate'] = self.session.config.get(
                'real_world_currency_per_point')
            max_tick_frequency = Constants.tick_frequency
            params['round_length'] = Constants.tick_frequency * \
                Constants.tick_num
            training_rounds = [1]
            self.session.vars['training_rounds'] = training_rounds
            treatment_order = [True] + [False]
            tcycle = cycle([-1, 1])
            for p in self.session.get_participants():
                p.vars['treatments'] = treatment_order[::next(tcycle)]
                p.vars['payable_round'] = random.randint(
                    2, Constants.num_rounds)

        self.tick_frequency = Constants.tick_frequency
        for p in self.get_players():
            _id = (p.id_in_subsession-1) % len(Constants.blocked_treatments)
            block = Constants.blocked_treatments[_id]
            martingale = block.get('martingale')
            p.treatment_name = block.get('treatment_name')
            p.inner_treatment_name = block.get('inner_name')
            p.participant.vars['treatment'] = block.get('inner_name')
            p.block_name = block.get('block_name')
            p.participant.vars['martingale']= martingale
            if martingale:
                price = Constants.prices_martingale[self.round_number-1]
            else:
                price = Constants.prices_normal[self.round_number-1]
            p.stock_prices_A = json.dumps(price)
            p.payable_round = p.participant.vars['payable_round'] == p.round_number
            if self.round_number == 1:
                p.martingale=martingale
                p.training = True
                p.gamified = False
                p.salient = False
                p.hedonic = False
                p.notifications = False
            else:
                p.training = False
                p.martingale=martingale
                p.gamified = block.get('gamified')[self.round_number-2]
                p.salient = block.get('salient')[self.round_number-2]
                p.notifications = block.get('notifications')
                p.hedonic = block.get('hedonic')


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    martingale = models.BooleanField()
    def get_stock_prices_A(self):
        return json.loads(self.stock_prices_A)

    """In production we may not need theses two fields, but it is still useful to have them
    as natural limits after which the player should proceed to the next trading day.
    """
    stock_prices_A = models.LongStringField()

    def formatted_prob(self):
        return f"{self.crash_probability:.0%}"
    intermediary_payoff = models.IntegerField()
    gamified = models.BooleanField()
    salient = models.BooleanField()
    notifications = models.BooleanField()
    hedonic = models.BooleanField()
    treatment = models.StringField()
    block = models.StringField()
    training = models.BooleanField()
    start_time = djmodels.DateTimeField(null=True, blank=True)
    end_time = djmodels.DateTimeField(null=True, blank=True)
    payable_round = models.BooleanField()
    day_params = models.LongStringField()
    block_name = models.StringField()
    treatment_name = models.StringField()
    inner_treatment_name = models.StringField()
    def register_event(self, data):
        timestamp = timezone.now()
        action = data.get('action', '')
        print('DATA', data)
        if hasattr(self, action):
            method = getattr(self, action)
            method(data, timestamp)
        self.events.create(
            part_number=self.round_number,
            owner=self,
            timestamp=timestamp,
            name=data.pop('name', ''),
            n_transactions=data.pop('nTransactions', None),
            tick_number=data.pop('tick_number', None),
            balance=data.pop('balance', None),
            body=json.dumps(data),
        )

        return {
            self.id_in_group: dict(timestamp=timestamp.strftime('%m_%d_%Y_%H_%M_%S'), action='getServerConfirmation')}

    def set_payoffs(self):
        if self.payable_round:
            self.payoff = self.intermediary_payoff
            self.participant.vars['payable_round'] = self.round_number
            self.participant.vars['trading_payoff'] = self.payoff


class Event(djmodels.Model):
    class Meta:
        ordering = ['timestamp']
        get_latest_by = 'timestamp'

    part_number = models.IntegerField()
    owner = djmodels.ForeignKey(
        to=Player, on_delete=djmodels.CASCADE, related_name='events')
    name = models.StringField()
    timestamp = djmodels.DateTimeField(null=True, blank=True)
    body = models.StringField()
    balance = models.FloatField()  # to store the current state of bank account
    tick_number = models.IntegerField()
    n_transactions = models.IntegerField()


def custom_export(players):
    session = players[0].session
    all_fields = Event._meta.get_fields()
    field_names = [i.name for i in all_fields]

    player_fields = ['participant_code',
                     'session_code',
                     'treatment']
    yield field_names + player_fields
    for q in Event.objects.all().order_by('owner__session', 'owner__round_number',
                                          'timestamp'):
        yield [getattr(q, f) or '' for f in field_names] + [q.owner.participant.code,

                                                            q.owner.session.code,
                                                            q.owner.session.config.get('display_name')]
