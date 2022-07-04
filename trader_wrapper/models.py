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

from otree.models import Session
import random
from django.db import models as djmodels
from django.utils import timezone
from itertools import cycle
import json
import csv
from django.conf import settings

author = 'Philipp Chapkovski, WZB'

doc = """
Backend for trading platform 
"""


class Constants(BaseConstants):
    name_in_url = 'trader_wrapper'
    players_per_group = None
    training_rounds = [1]
    num_rounds = 4
    tick_frequency = 6
    tick_num = 10


def flatten(t):
    return [item for sublist in t for item in sublist]


class Subsession(BaseSubsession):
    tick_frequency = models.FloatField()
    max_length = models.FloatField()
    stock_prices_A = models.LongStringField()
    stock_prices_B = models.LongStringField()

    def get_stock_prices_A(self):
        return json.loads(self.stock_prices_A)

    def get_stock_prices_B(self):
        return json.loads(self.stock_prices_B)

    def creating_session(self):

        stock_price_path_A = f'data/prices_markov_A_{self.round_number-1}.csv'
        stock_price_path_B = f'data/prices_markov_B_{self.round_number-1}.csv'
        with open(stock_price_path_A, newline='') as csvfile:
            stockreader = csv.DictReader(csvfile, delimiter=',')
            stockreader = [float(i.get('stock')) for i in stockreader]
            self.stock_prices_A = json.dumps(stockreader)
        with open(stock_price_path_B, newline='') as csvfile:
            stockreader = csv.DictReader(csvfile, delimiter=',')
            stockreader = [float(i.get('stock')) for i in stockreader]
            self.stock_prices_B = json.dumps(stockreader)

        if self.round_number == 1:
            params = {}
            params['game_rounds'] = Constants.num_rounds
            params['exchange_rate'] = self.session.config.get('real_world_currency_per_point')
            max_tick_frequency = Constants.tick_frequency
            params['round_length'] = Constants.tick_frequency * Constants.tick_num
            training_rounds = [1]

            self.session.vars['training_rounds'] = training_rounds

            treatment_order = [True] + [False]
            tcycle = cycle([-1, 1])
            for p in self.session.get_participants():
                p.vars['treatments'] = treatment_order[::next(tcycle)]
                lb = max(Constants.training_rounds)
                p.vars['payable_round'] = random.randint(lb + 1, Constants.num_rounds)

        self.tick_frequency = Constants.tick_frequency
        for p in self.get_players():
            p.payable_round = p.participant.vars['payable_round'] == p.round_number
            p.training = p.round_number in self.session.vars['training_rounds']
            if self.round_number !=Constants.num_rounds:
                if p.training:
                    p.gamified = False
                else:
                    p.gamified = p.participant.vars['treatments'][self.round_number - len(Constants.training_rounds) - 1]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    """In production we may not need theses two fields, but it is still useful to have them
    as natural limits after which the player should proceed to the next trading day.
    """

    def formatted_prob(self):
        return f"{self.crash_probability:.0%}"

    gamified = models.BooleanField(label='Which of the two designs above do you prefer?',
                                   choices=[(False, 'Design 1'), (True, 'Design 2')])
    training = models.BooleanField()
    start_time = djmodels.DateTimeField(null=True, blank=True)
    end_time = djmodels.DateTimeField(null=True, blank=True)
    payable_round = models.BooleanField()
    day_params = models.LongStringField()
    stock_up_A = models.IntegerField()
    stock_up_B = models.IntegerField()
    confidence_A = models.IntegerField()
    confidence_B = models.IntegerField()

    def predictions_send(self, data, timestamp):
        print('predictions_send registered', data)
        self.stock_up_A = data.get('stockUpA')
        self.stock_up_B = data.get('stockUpB')
        self.confidence_A = data.get('confidenceA')
        self.confidence_B = data.get('confidenceB')

    def register_event(self, data):
        timestamp = timezone.now()
        action = data.get('action', '')
        if hasattr(self, action):
            method = getattr(self, action)
            method(data, timestamp)

        self.events.create(
            part_number=self.round_number,
            owner=self,
            timestamp=timestamp,
            name=data.pop('name', ''),
            tick_number=data.pop('tick_number', None),
            balance=data.pop('balance', None),
            body=json.dumps(data),
        )

        return {
            self.id_in_group: dict(timestamp=timestamp.strftime('%m_%d_%Y_%H_%M_%S'), action='getServerConfirmation')}

    def set_payoffs(self):
        if self.payable_round:
            self.payoff = 1
            self.participant.vars['payable_round'] = self.round_number
            self.participant.vars['trading_payoff'] = self.payoff


class Event(djmodels.Model):
    class Meta:
        ordering = ['timestamp']
        get_latest_by = 'timestamp'

    part_number = models.IntegerField()
    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name='events')
    name = models.StringField()
    timestamp = djmodels.DateTimeField(null=True, blank=True)
    body = models.StringField()
    balance = models.FloatField()  # to store the current state of bank account
    tick_number = models.IntegerField()


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
