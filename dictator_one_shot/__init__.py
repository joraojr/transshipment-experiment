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
    ENDOWMENT = cu(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    kept = models.CurrencyField(
        doc="""Amount dictator decided to keep for himself""",
        min=0,
        max=C.ENDOWMENT,
        label="I will keep",
    )


class Player(BasePlayer):
    pass


# FUNCTIONS

def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = group.kept
    p2.payoff = C.ENDOWMENT - group.kept
    p1.participant.vars['earning_1'] = p1.payoff
    p2.participant.vars['earning_1'] = p2.payoff


def get_players(player: Player):
    participant_name = player.participant
    return dict(participant_name=participant_name)


def js_vars(player: Player):
    group = player.group
    return dict(
        taken=group.kept,
    )


# PAGES
class Introduction(Page):
    pass


class Offer(Page):
    form_model = 'group'
    form_fields = ['kept']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class RecipientWait(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(offer=C.ENDOWMENT - group.kept)


page_sequence = [Introduction, Offer, RecipientWait, ResultsWaitPage, Results]
