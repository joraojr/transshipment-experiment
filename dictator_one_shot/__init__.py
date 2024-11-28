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
    INSTRUCTIONS_TEMPLATE = 'dictator_one_shot/instructions.html'
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

def custom_export(players):
    # header row
    yield ['session', 'participant_code', 'round_number', 'id_in_group', 'payoff', 'participant_label']
    for p in players:
        participant = p.participant
        session = p.session
        yield [session.code, participant.code, p.round_number, p.id_in_group, p.payoff, participant.label]

def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = group.kept
    p2.payoff = C.ENDOWMENT - group.kept
    p1.participant.vars['earning_1'] = p1.payoff
    p2.participant.vars['earning_1'] = p2.payoff

# def get_results_offers(subsession):
#     # offers_list = []
#     for p in subsession.get_players():
#         # if p.experiment_finished:
#         group = p.group
#         offer = C.ENDOWMENT - group.kept
#         # offers_list.append(offer)
#
#     # catch the case where no player has finished yet
#     # if len(linda_banking_list) >0:
#     #     average_rank_banking = round(statistics.mean(linda_banking_list),2)
#     #     average_rank_banking_feminist = round(statistics.mean(linda_banking_feminist_list), 2)
#     # else:
#     #     average_rank_banking = average_rank_banking_feminist = None
#     return offer

def get_players(player: Player):
    participant_name = player.participant
    return dict(participant_name=participant_name)


def vars_for_admin_report(subsession):
    all_offers = []
    for subsession in subsession.in_all_rounds():
       # this_group = subsession.group
       # offer = C.ENDOWMENT - this_group.kept
       # all_offers.append(offer)
       # payoffs = sorted([p.payoff for p in subsession.get_players()])
        for group in subsession.get_groups():
            offer = C.ENDOWMENT - group.kept
            all_offers.append(offer)
        payoffs = sorted([p.payoff for p in subsession.get_players()])
    return dict(payoffs=payoffs, all_offers=all_offers)

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


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(offer=C.ENDOWMENT - group.kept)

    @staticmethod
    def js_vars(player: Player):
        group = player.group
        return dict(
            taken=group.kept,
        )

    @staticmethod
    def vars_for_admin_report(subsession):
        payoffs = sorted([p.payoff for p in subsession.get_players()])
        return dict(payoffs=payoffs)




page_sequence = [Introduction, Offer, ResultsWaitPage, Results]
