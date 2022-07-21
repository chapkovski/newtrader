from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage



class GeneralPage(Page):
    def vars_for_template(self):
        return dict()

class CQPage(GeneralPage):
    form_model = 'player'
    form_fields = ['cq1', 'cq2', 'cq3', 'cq4','cq5']

class Instructions(GeneralPage):
    pass

page_sequence = [
    Instructions,
    CQPage
]
