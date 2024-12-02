from otree.api import *

from welcome import Welcome

doc = """
Post Survey to the Transshipment Game
"""


class C(BaseConstants):
    NAME_IN_URL = 'pre_questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # Initial amount allocated to the dictator
    ENDOWMENT = cu(1000)

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

    Br1 = make_risk_decision("To help somebody is the best policy to be certain that s/he will help you in the future.",
                             C.PoDIRS_6_SCALES)
    Br2 = make_risk_decision("I do not behave badly with others so as to avoid them behaving badly with me.",
                             C.PoDIRS_6_SCALES)
    Br3 = make_risk_decision("I fear the reactions of a person I have previously treated badly.",
                             C.PoDIRS_6_SCALES)
    Br4 = make_risk_decision("If I work hard, I expect it will be repaid.",
                             C.PoDIRS_6_SCALES)
    Br5 = make_risk_decision("When I pay someone compliments, I expect that s/he in turn will reciprocate.",
                             C.PoDIRS_6_SCALES)
    Br6 = make_risk_decision("I avoid being impolite because I do not want others being impolite with me.",
                             C.PoDIRS_6_SCALES)
    Br7 = make_risk_decision("If I help tourists, I expect that they will thank me nicely.",
                             C.PoDIRS_6_SCALES)
    Br8 = make_risk_decision("It is obvious that if I treat someone badly s/he will look for revenge.",
                             C.PoDIRS_6_SCALES)
    Br9 = make_risk_decision("If I don’t leave a good tip in a restaurant, I expect that in future I will not get good service.",
                             C.PoDIRS_6_SCALES)

    Pr1 = make_risk_decision("I am ready to undergo personal costs to help somebody who helped me before.",
                             C.PoDIRS_6_SCALES)
    Pr2 = make_risk_decision("If someone does a favour for me, I am ready to return it.",
                             C.PoDIRS_6_SCALES)
    Pr3 = make_risk_decision("If someone is helpful with me at work, I am pleased to help him/her.",
                             C.PoDIRS_6_SCALES)
    Pr4 = make_risk_decision("I’m ready to do a boring job to return someone’s previous help.",
                             C.PoDIRS_6_SCALES)
    Pr5 = make_risk_decision("When someone does me a favour, I feel committed to repay him/her.",
                             C.PoDIRS_6_SCALES)
    Pr6 = make_risk_decision("If someone asks me politely for information, I’m really happy to help him/her.",
                             C.PoDIRS_6_SCALES)
    Pr7 = make_risk_decision("If someone lends me money as a favour, I feel I should give him/her back something more than what is strictly due.",
                             C.PoDIRS_6_SCALES)
    Pr8 = make_risk_decision(
        "If somebody suggests to me the name of the winning horse at the race, I would certainly give him/her part of my winnings.",
        C.PoDIRS_6_SCALES)
    Pr9 = make_risk_decision("I go out of my way to help somebody who has been kind to me before.",
                             C.PoDIRS_6_SCALES)

    Nr1 = make_risk_decision("If I suffer a serious wrong, I will take my revenge as soon as possible, no matter what the costs.",
                             C.PoDIRS_6_SCALES)
    Nr2 = make_risk_decision("I am willing to invest time and effort to reciprocate an unfair action.",
                             C.PoDIRS_6_SCALES)
    Nr3 = make_risk_decision("I am kind and nice if others behave well with me, otherwise it’s tit-for-tat.",
                             C.PoDIRS_6_SCALES)
    Nr4 = make_risk_decision("If somebody puts me in a difficult position, I will do the same to him/he.",
                             C.PoDIRS_6_SCALES)
    Nr5 = make_risk_decision("If somebody offends me, I will offend him/her back.",
                             C.PoDIRS_6_SCALES)
    Nr6 = make_risk_decision("If someone is unfair to me, I prefer to give him/her what s/he deserves instead of accepting his/her apologies.",
                             C.PoDIRS_6_SCALES)
    Nr7 = make_risk_decision("I would not do a favour for somebody who behaved badly with me, even if it meant foregoing some personal gains.",
                             C.PoDIRS_6_SCALES)
    Nr8 = make_risk_decision("If somebody is impolite to me, I become impolite.",
                             C.PoDIRS_6_SCALES)
    Nr9 = make_risk_decision("The way I treat others depends much on how they treat me.",
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
class Welcome(Page):
    pass


class IntroductionDictatorGame(Page):
    def vars_for_template(self):
        return {
            'conversion_rate': 1 / self.session.config['real_world_currency_per_point'],  # 1EUR * conversion_rate
        }


class BeliefsReciprocity(Page):
    form_model = 'player'
    form_fields = ['Br1', 'Br2', 'Br3', 'Br4', 'Br5', 'Br6', 'Br7', 'Br8', 'Br9']


class PositiveReciprocity(Page):
    form_model = 'player'
    form_fields = ['Pr1', 'Pr2', 'Pr3', 'Pr4', 'Pr5', 'Pr6', 'Pr7', 'Pr8', 'Pr9']


class NegativeReciprocity(Page):
    form_model = 'player'
    form_fields = ['Nr1', 'Nr2', 'Nr3', 'Nr4', 'Nr5', 'Nr6', 'Nr7', 'Nr8', 'Nr9']


class PoDIRSReciprocity(Page):
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


page_sequence = [Welcome, Trust, IntroductionDictatorGame]
