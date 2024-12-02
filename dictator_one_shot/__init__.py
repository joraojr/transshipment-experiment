from otree.api import *

# from .admin_report_functions import *

doc = """
One player decides how to divide a certain amount between himself and the other
player.
See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.
"""


class C(BaseConstants):
    NAME_IN_URL = 'dictator_one_shot'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    # Initial amount allocated to the dictator
    ENDOWMENT = cu(1000)
    PARTICIPANT_A_ROLE = 'Participant A'
    PARTICIPANT_B_ROLE = 'Participant B'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent = models.CurrencyField(
        doc="""Amount Participant A decided to send to Participant B""",
        min=0,
        max=C.ENDOWMENT,
    )


class Player(BasePlayer):
    pass


# FUNCTIONS

def set_payoffs(group: Group):
    p1 = group.get_player_by_role(C.PARTICIPANT_A_ROLE)
    p2 = group.get_player_by_role(C.PARTICIPANT_B_ROLE)

    p1.participant.earning_dictator = C.ENDOWMENT - group.sent
    p2.participant.earning_dictator = group.sent


# PAGES

class Offer(Page):
    form_model = 'group'
    form_fields = ['sent']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.PARTICIPANT_A_ROLE


class ParticipantB(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.PARTICIPANT_B_ROLE


class ParticipantA(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.PARTICIPANT_A_ROLE


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(offer=C.ENDOWMENT - group.sent,
                    conversion_rate=1 / player.session.config['real_world_currency_per_point']  # 1EUR * conversion_rate)
                    )


class MatchingWaitPage(WaitPage):
    group_by_arrival_time = True


class ResultsWaitPageParticipantA(WaitPage):
    after_all_players_arrive = set_payoffs

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.PARTICIPANT_A_ROLE


class ResultsWaitPageParticipantB(WaitPage):
    after_all_players_arrive = set_payoffs
    body_text = "Please wait for Participant A to make a proposal."

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.PARTICIPANT_B_ROLE


page_sequence = [MatchingWaitPage, ParticipantA, ParticipantB, Offer, ResultsWaitPageParticipantA, ResultsWaitPageParticipantB, Results]
