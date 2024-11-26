from otree.api import *

doc = """
Post Survey to the Transshipment Game
"""


class C(BaseConstants):
    NAME_IN_URL = 'Pre_Questionnaire'
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

    @staticmethod
    def make_risk_decision(label, choices):
        return models.StringField(
            choices=choices,
            label=label,
            widget=widgets.RadioSelectHorizontal(),
            blank=False  # Make sure the choice is required
        )

    PDIRS_1 = make_risk_decision("In helping others, we help ourselves, for whatever good we give out completes the circle and comes back to us",
                                 C.PoDIRS_6_SCALES)
    PDIRS_2 = make_risk_decision("Life is like an echo, we get back what we give.",
                                 C.PoDIRS_6_SCALES)
    PDIRS_3 = make_risk_decision("When we help somebody, somebody else will help us.",
                                 C.PoDIRS_6_SCALES)
    PDIRS_4 = make_risk_decision("It is worth being good towards others because it will come back to us sooner or later.",
                                 C.PoDIRS_6_SCALES)
    PDIRS_5 = make_risk_decision("Good done to somebody else comes back all of a sudden, sometimes even stronger.",
                                 C.PoDIRS_6_SCALES)
    PDIRS_6 = make_risk_decision("Good done to others always comes back.",
                                 C.PoDIRS_6_SCALES)

    T_QA1 = models.IntegerField(
        label='How well does the following statement describe you as a person? As long as I am not convinced otherwise, I assume that people have only the best intentions.',
        choices=C.LIKERT,
        widget=widgets.RadioSelectHorizontal()
    )

    A_QA1 = models.IntegerField(
        label='Imagine the following situation: you won 1,000 Euro in a lottery. Considering your current situation, how much would you donate to charity?',
        blank=False,
        min=0,
        max=1000,
    )

    A_QA2 = models.IntegerField(
        label='How do you assess your willingness to share with others without expecting anything in return when it comes to charity?',
        choices=C.LIKERT,
        widget=widgets.RadioSelectHorizontal()
    )


# PAGES
class Introduction(Page):
    pass


class Reciprocity(Page):
    form_model = 'player'
    form_fields = ['PDIRS_1', 'PDIRS_2', 'PDIRS_3', 'PDIRS_4', 'PDIRS_5', 'PDIRS_6']


class Trust(Page):
    form_model = 'player'
    form_fields = ['T_QA1']


class Altruism1(Page):
    form_model = 'player'
    form_fields = ['A_QA1']


class Altruism2(Page):
    form_model = 'player'
    form_fields = ['A_QA2']


page_sequence = [Introduction, Reciprocity, Trust, Altruism1, Altruism2]
