from otree.api import Currency as c, currency_range

import settings
from ._builtin import Page, WaitPage
from .models import Constants

from pretrade.pages import GeneralPage


class AnnounceTrader(GeneralPage):
    pass


class Trader(GeneralPage):
    live_method = 'register_event'


    def vars_for_template(self):
        return dict()

    def before_next_page(self):
        self.player.set_payoffs()


page_sequence = [
    # AnnounceTrader,
    Trader,
]
