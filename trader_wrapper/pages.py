from otree.api import Currency as c, currency_range

import settings
from ._builtin import Page, WaitPage
from .models import Constants

from pretrade.pages import GeneralPage


class AnnounceTrader(GeneralPage):
    pass


class ChoosingGamification(GeneralPage):
    def is_displayed(self):
        return self.round_number==Constants.num_rounds
    form_model = 'player'
    form_fields = ['gamified']


class Trader(GeneralPage):
    live_method = 'register_event'
    def vars_for_template(self):
        if self.round_number == 1:
            return dict(prediction_at=1,
                        trading_at=0)

        return dict(prediction_at=self.session.config.get('prediction_at'),
                    trading_at=self.session.config.get('trading_at'))

    def before_next_page(self):
        self.player.set_payoffs()


page_sequence = [
    # AnnounceTrader,
    ChoosingGamification,
    Trader,
]
