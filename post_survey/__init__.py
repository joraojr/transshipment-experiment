import random

from otree.api import *
from sqlalchemy.testing.plugin.plugin_base import options

doc = """
Post Survey to the Transshipment Game
"""


class C(BaseConstants):
    NAME_IN_URL = 'post_questionnaire'
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
    random_selected_dictator = models.IntegerField(initial=0)


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
        widget=widgets.RadioSelectHorizontal()

    )

    gender = models.StringField(
        label="With which gender do you identify yourself most?",
        choices=["Male", "Female", "Prefer not to say", "Other"],
        widget=widgets.RadioSelectHorizontal()

    )

    economics = models.StringField(
        label="How would you rate your expertise in Economics on a scale of 1 (not knowledgeable at all) to 10 (expert)?",
        choices=range(1, 11),
        widget=widgets.RadioSelectHorizontal()

    )

    logistics = models.StringField(
        label="How would you rate your expertise in Logistics on a scale of 1 (not knowledgeable at all) to 10 (expert)?",
        choices=range(1, 11),
        widget=widgets.RadioSelectHorizontal()

    )

    """
        LEGEND:
        RT = Risk Taking
        T = TRUST
        A - Altruism
        NR = Negative reciprocity 
        PR = Positive reciprocity
        
    """

    @staticmethod
    def make_risk_decision(label, choices=['Option A', 'Option B']):
        return models.StringField(
            choices=choices,
            label=label,
            widget=widgets.RadioSelectHorizontal(),
            blank=False  # Make sure the choice is required
        )

    rq1 = make_risk_decision("Option A: 1/10 of $2.00, 9/10 of $1.60 | Option B: 1/10 of $3.85, 9/10 of $0.10")
    rq2 = make_risk_decision("Option A: 2/10 of $2.00, 8/10 of $1.60 | Option B: 2/10 of $3.85, 8/10 of $0.10")
    rq3 = make_risk_decision("Option A: 3/10 of $2.00, 7/10 of $1.60 | Option B: 3/10 of $3.85, 7/10 of $0.10")
    rq4 = make_risk_decision("Option A: 4/10 of $2.00, 6/10 of $1.60 | Option B: 4/10 of $3.85, 6/10 of $0.10")
    rq5 = make_risk_decision("Option A: 5/10 of $2.00, 5/10 of $1.60 | Option B: 5/10 of $3.85, 5/10 of $0.10")
    rq6 = make_risk_decision("Option A: 6/10 of $2.00, 4/10 of $1.60 | Option B: 6/10 of $3.85, 4/10 of $0.10")
    rq7 = make_risk_decision("Option A: 7/10 of $2.00, 3/10 of $1.60 | Option B: 7/10 of $3.85, 3/10 of $0.10")
    rq8 = make_risk_decision("Option A: 8/10 of $2.00, 2/10 of $1.60 | Option B: 8/10 of $3.85, 2/10 of $0.10")
    rq9 = make_risk_decision("Option A: 9/10 of $2.00, 1/10 of $1.60 | Option B: 9/10 of $3.85, 1/10 of $0.10")
    rq10 = make_risk_decision("Option A: 10/10 of $2.00, 0/10 of $1.60 | Option B: 10/10 of $3.85, 0/10 of $0.10")

    Pr1 = make_risk_decision("If someone does me a favor, I am prepared to return it.", C.PoDIRS_6_SCALES)
    Pr2 = make_risk_decision("I go out of my way to help somebody who has been kind to me in the past.", C.PoDIRS_6_SCALES)
    Pr3 = make_risk_decision("I am ready to assume personal costs to help somebody who helped me in the past.", C.PoDIRS_6_SCALES)

    Nr1 = make_risk_decision("If I suffer a serious wrong, I will take revenge as soon as possible, no matter what the cost.", C.PoDIRS_6_SCALES)
    Nr2 = make_risk_decision("If somebody puts me in a difficult position, I will do the same to him/her.", C.PoDIRS_6_SCALES)
    Nr3 = make_risk_decision("If somebody offends me, I will offend him/her back.", C.PoDIRS_6_SCALES)


def calculate_risk_reward(player: Player):
    import random

    options = {
        'Option A': [200.00, 160.00],
        'Option B': [385.00, 10.00]
    }

    # TODO deal with it when the player does not select any option

    i = random.randint(1, 10)
    selected_risk = 'rq' + str(i)
    choice_option = options[getattr(player, selected_risk)]
    player.participant.selected_risk = "Decision {}, {}".format(str(i), getattr(player, selected_risk))

    chance = random.randint(1, 10)
    player.participant.earning_risk = choice_option[0] if chance <= i else choice_option[1]

    player.participant.payoff += cu(player.participant.earning_risk)


# PAGES
class Welcome(Page):
    pass


class Risk(Page):
    form_model = 'player'
    form_fields = ['rq1', 'rq2', 'rq3', 'rq4', 'rq5', 'rq6', 'rq7', 'rq8', 'rq9', 'rq10']

    @staticmethod
    def before_next_page(player, timeout_happened):
        calculate_risk_reward(player)


class Reciprocity(Page):
    form_model = 'player'
    form_fields = ['Pr1', 'Pr2', 'Pr3', 'Nr1', 'Nr2', 'Nr3']


class Demographics(Page):
    form_model = 'player'
    form_fields = [
        'gender',
        'age',
        'economics',
        'logistics'
    ]

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.finished = True
        # Select 5 random players to earn the dictator game

        subsession = player.subsession
        number_selected = subsession.random_selected_dictator
        player.participant.selected_for_earning_dictator = False

        if number_selected < 5:
            if random.choice([True]):
                player.participant.selected_for_earning_dictator = True
                player.participant.payoff += cu(player.participant.earning_dictator)
                subsession.random_selected_dictator += 1


class FinalPage(Page):
    def vars_for_template(player: Player):
        return dict(
            DRAW_EARNINGS_NUM_ROUNDS=player.session.config['draw_earnings_num_rounds'],
            payoff=player.participant.payoff_in_real_world_currency(),
            total_payoff=player.participant.payoff_plus_participation_fee(),
            show_up_fee=player.session.config['participation_fee'],
            draw_earnings_dictator=player.session.config['draw_earnings_dictator'],
            result_part1_selected=player.participant.selected_for_earning_dictator,
            result_part1_currency=cu(player.participant.earning_dictator).to_real_world_currency(player.session),
            result_part3_currency=cu(max(player.participant.avg_earnings, 0)).to_real_world_currency(player.session),
            result_part3_rounds=sorted([x + 1 for x in player.participant.draw_earnings_indexes]),
            result_part4_currency=cu(player.participant.earning_risk).to_real_world_currency(player.session),
            result_part4_selection=player.participant.selected_risk,
        )


page_sequence = [Welcome, Risk, Reciprocity, Demographics, FinalPage]
