from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
import json


class GeneralPage(Page):
    def vars_for_template(self):
        return dict()

class Consent(GeneralPage):
    form_model = 'player'
    form_fields = ['consent']

class CQPage(GeneralPage):
    form_model = 'player'
    form_fields = ['cq1', 'cq2', 
    # 'cq3',
     'cq4','cq5']

class Instructions(GeneralPage):
    pass

class KnowledgeP(GeneralPage):
    def post(self):
        try:
            survey_data = json.loads(self.request.POST.get('surveyholder'))
            knowledge = survey_data.get('knowledge')
            self.player.knowledge= knowledge
        except Exception as e:
            print('SOMETHING WENT WRONG:: ', e)
        return super().post()

    

page_sequence = [
    Consent,
    Instructions,
    # CQPage,
    KnowledgeP,
]
