from otree.api import *

doc = """
Post Survey to the Transshipment Game
"""


class C(BaseConstants):
    NAME_IN_URL = 'Questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

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

    POSITIVE_RECIPROCITY = [
        [5, ''],
        [10, ''],
        [15, ''],
        [20, ''],
        [25, ''],
        [30, ''],
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(
        label="How old are you?",
        choices=[
            [1, '18-24'],
            [2, '25-34'],
            [3, '35-44'],
            [4, '45-54'],
            [5, '55-64'],
            [6, '65-74'],
            [7, '75 or over'],
        ],
    )

    gender = models.StringField(
        label="With which gender do you identify yourself most?",
        choices=["Male", "Female", "Prefer not to say"]
    )

    subject = models.StringField(
        label="Which subject are you primarily enrolled in?",
        choices=["Economics/Business", "Law", "Humanities", "Science/Engineering", "None"]
    )

    religion = models.StringField(
        label="Do you consider yourself a religious person?",
        choices=["Strongly Disagree", "Disagree", "Neither Agree nor Disagree", "Agree", "Strongly Agree"]
    )

    """
        LEGEND:
        RT = Risk Taking
        T = TRUST
        A - Altruism
        NR = Negative reciprocity 
        PR = Positive reciprocity
        
    """

    RT_QA1 = models.IntegerField(
        label='How do you see yourself: Are you a person who is generally willing to take risks, or do you try to avoid taking risks?',
        choices=C.LIKERT,
        widget=widgets.RadioSelectHorizontal()
    )

    T_QA1 = models.IntegerField(
        label='How well does the following statement describe you as a person? As long as I am not convinced otherwise, I assume that people have '
              'only the best intentions.   ',
        choices=C.LIKERT,
        widget=widgets.RadioSelectHorizontal()
    )

    A_QA1 = models.IntegerField(
        label='How do you assess your willingness to share with others without expecting anything in return when it comes to charity?',
        choices=C.LIKERT,
        widget=widgets.RadioSelectHorizontal()
    )

    NR_QA1 = models.IntegerField(
        label='How do you see yourself: Are you a person who is generally willing to punish unfair behavior even if this is costly?',
        choices=C.LIKERT,
        widget=widgets.RadioSelectHorizontal()
    )

    PR_QA1 = models.IntegerField(
        label='Imagine the following situation: you are shopping in an unfamiliar city and realize you lost your way. You ask a stranger for '
              'directions. The stranger offers to take you with their car to your destination. The ride takes about 20 minutes and costs the '
              'stranger about 20 Euro in total. The stranger does not want money for it. You carry six bottles of wine with you. The cheapest '
              'bottle costs 5 Euro, the most expensive one 30 Euro. You decide to give one of the bottles to the stranger as a thank-you gift. '
              'Which bottle do you give?',
        choices=C.POSITIVE_RECIPROCITY,
        widget=widgets.RadioSelectHorizontal()
    )


class Demographics(Page):
    form_model = 'player'
    form_fields = [
        'gender',
        'age',
        'subject',
        'religion'
    ]


# PAGES
class Introduction(Page):
    pass


class Q1(Page):
    form_model = 'player'
    form_fields = ['RT_QA1', 'T_QA1', 'A_QA1', 'NR_QA1']


class Q2(Page):
    form_model = 'player'
    form_fields = ['PR_QA1']


class FinalPage(Page):
    def vars_for_template(player: Player):
        return dict(
            DRAW_EARNINGS_NUM_ROUNDS=player.session.config['draw_earnings_num_rounds'],
            payoff=player.participant.payoff_in_real_world_currency(),
            total_payoff=player.participant.payoff_plus_participation_fee(),
            show_up_fee=player.session.config['participation_fee']

        )


page_sequence = [Introduction, Q1, Q2, Demographics, FinalPage]
