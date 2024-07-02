from otree.api import *

doc = """
Post Survey to the Transshipment Game
"""


class C(BaseConstants):
    NAME_IN_URL = 'Questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    LIKERT = [
        [1, 'Strongly disagree'],
        [2, 'Disagree'],
        [3, 'Neither Agree nor Disagree'],
        [4, 'Agree'],
        [5, 'Strongly agree']
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(
        label="How old are you?",
        min=18,
        max=100
    )

    gender = models.StringField(
        label="With which gender do you identify yourself most?",
        choices=["Male", "Female", "Other", "Prefer not to say"]
    )

    subject = models.StringField(
        label="Which subject are you primarily enrolled in?",
        choices=["Economics/Business", "Law", "Humanities", "Science/Engineering", "None", "Other"]
    )

    religion = models.StringField(
        label="Do you consider yourself a religious person?",
        choices=["Strongly Disagree", "Disagree", "Neither Agree nor Disagree", "Agree", "Strongly Agree"]
    )

    QA1 = models.IntegerField(label='Testing Testing Testing Testing Testing Testing Testing Testing Testing Testing Testing Testing',
                              choices=C.LIKERT, widget=widgets.RadioSelectHorizontal())


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
    form_fields = ['QA1']


class FinalPage(Page):
    def vars_for_template(player: Player):
        return dict(
            DRAW_EARNINGS_NUM_ROUNDS=player.session.config['draw_earnings_num_rounds'],
            payoff=player.participant.payoff_in_real_world_currency(),
            total_payoff=player.participant.payoff_plus_participation_fee(),
            show_up_fee=player.session.config['participation_fee']

        )


page_sequence = [Introduction, Q1, Demographics, FinalPage]
