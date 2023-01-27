from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Player, FinQ
from django.forms import inlineformset_factory
from django import forms
import json
from otree.api import widgets
from django.shortcuts import redirect


# form for fin qs

class FinQForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        jchoices = json.loads(self.instance.choices)

        exchoices = [(i, j) for i, j in enumerate(jchoices)]

        self.fields['answer'] = forms.ChoiceField(widget=widgets.RadioSelect(attrs={'required': True}),
                                                  choices=exchoices,
                                                  required=True)


# formset for fin qs
finq_formset = inlineformset_factory(parent_model=Player,
                                     model=FinQ,
                                     fields=['answer'],
                                     extra=0,
                                     can_delete=False,
                                     form=FinQForm,
                                     )


class SelfReflection1(Page):
    form_model = 'player'
    form_fields = ['sr_prefs', ]


class SelfReflection2(Page):
    form_model = 'player'
    form_fields = ['sr_better_decs', ]

class SelfReflection3(Page):
    form_model = 'player'
    form_fields = ['sr_better_have_option', ]


class SelfReflection4(Page):
    form_model = 'player'
    form_fields = ['sr_notifications', 'sr_badges', 'sr_confetti']


class FinQuiz(Page):
    def get_formset(self, data=None):
        return finq_formset(instance=self.player,
                            data=data, )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.get_formset()

        return context

    def get_form(self, data=None, files=None, **kwargs):
        if data and data.get('timeout_happened'):
            return super().get_form(data, files, **kwargs)
        if not data:
            return self.get_formset()
        formset = self.get_formset(data=data)
        return formset

    def before_next_page(self):
        self.player.payoff = self.player.get_correct_quiz_questions_num() * Constants.fee_per_correct_answer


class Results(Page):
    def vars_for_template(self):
        return dict(
            chosen_round=self.participant.vars.get('payable_round', ''),
            trading_payoff=self.participant.vars.get('trading_payoff', ''),
            correct_quiz_questions=self.player.get_correct_quiz_questions_num(),
            quiz_bonus=self.player.payoff
        )

class Debriefing(Page):
   pass


class Q(Page):
    form_model = 'player'
    form_fields = ['gender',
                   'age',
                   'nationality',
                #    'email',
                   'education',
                   'study_major',
                   'course_financial',
                   'experiment_before',
                   'trading_experience',
                   'online_trading_experience',
                   'trading_frequency',
                   'portfolio_frequency',
                   'asset_class',
                   'use_leverage',
                   'purpose',
                   'difficulty']


class FinalForProlific(Page):
    def is_displayed(self):
        return self.session.config.get('for_prolific')

    def get(self):
        return redirect(self.session.config.get('prolific_redirect_url'))


page_sequence = [
    SelfReflection1,
    SelfReflection2,
    SelfReflection3,
    SelfReflection4,
    FinQuiz,
    Q,
    Results,
    Debriefing,
    FinalForProlific
]
