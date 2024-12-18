from otree.api import *

import settings
from welcome import Welcome

doc = """
Post Survey to the Transshipment Game
"""


class C(BaseConstants):
    NAME_IN_URL = 'pre_questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # Initial amount allocated to the dictator
    ENDOWMENT = cu(settings.SESSION_CONFIG_DEFAULTS['draw_dictator_endowments'])

    LIKERT = [
        [0, ''],
        [1, ''],
        [2, ''],
        [3, ''],
        [4, ''],
        [5, ''],
        [6, ''],
        [7, ''],
        [8, ''],
        [9, ''],
        [10, '']
    ]

    PoDIRS_6_SCALES = [
        [1, "I strongly disagree"],
        [2, "I disagree"],
        [3, "I rather disagree"],
        [4, "It is indifferent to me"],
        [5, "I rather agree"],
        [6, "I agree"],
        [7, "I strongly agree"],
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    """
        LEGEND:
        RT = Risk Taking
        T = TRUST
        A - Altruism
        NR = Negative reciprocity
        PR = Positive reciprocity
        PDIRS = Positive Downstream Indirect Reciprocity Scale

    """
    sent = models.CurrencyField(
        doc="""Amount Participant A decided to send to Participant B""",
        min=0,
        max=C.ENDOWMENT,
    )

    T_QA1 = models.IntegerField(
        label='As long as I am not convinced otherwise, I assume that people have only the best intentions.',
        choices=C.LIKERT,
        widget=widgets.RadioSelectHorizontal()
    )


# PAGES
class Welcome(Page):
    pass


class Q2(Page):
    """
    Dictator Game
    """
    form_model = 'player'
    form_fields = ['sent']

    def vars_for_template(self):
        return {
            'conversion_rate': round(1 / self.session.config['real_world_currency_per_point']),  # 1EUR * conversion_rate,
            'draw_earnings_dictator': self.session.config['draw_earnings_dictator']

        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.earning_dictator = C.ENDOWMENT - player.sent


class Q1(Page):
    """
    Trust
    """
    form_model = 'player'
    form_fields = ['T_QA1']


page_sequence = [Welcome, Q1, Q2]
