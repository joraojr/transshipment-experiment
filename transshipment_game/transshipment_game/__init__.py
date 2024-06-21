from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'transshipment_game'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10


class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    # Assign Treatments from the Previous app to the players
    for player in subsession.get_players():
        player.treatment = player.participant.treatment

    # Randomly assign players to groups but keep the same id_in_group for all rounds
    subsession.group_randomly(fixed_id_in_group=True)


class Group(BaseGroup):
    transfer_engagement = models.BooleanField()
    transfer_engagement_message_text = models.StringField()

    def all_transfer_engagement_yes(self):
        # Check if all players in the group have answered 'yes' to transfer_engagement
        return all(player.transfer_engagement for player in self.get_players())

    def set_transfer_engagement_message(self):
        if self.all_transfer_engagement_yes():
            self.transfer_engagement = True
            self.transfer_engagement_message_text = (
                "You and the other retailer decided to engage in a transfer this round. <b>There will be a transfer in this round</b> if there is "
                "excess demand or excess inventory."
            )
        else:
            self.transfer_engagement = False
            self.transfer_engagement_message_text = (
                "You or the other retailer decided not to engage in a transfer this round. <b>There will be no transfer in this round</b> if "
                "there is excess demand or excess inventory."
            )


class Player(BasePlayer):
    treatment = models.StringField()
    transfer_engagement = models.BooleanField(
        label="Decide whether you want to engage in a transfer with the other retailer, in case you face excess demand or excess inventory.",
        blank=False
    )


# PAGES
class TransferEngagement(Page):
    form_model = 'player'
    form_fields = ['transfer_engagement']

    @staticmethod
    def is_displayed(player):
        return player.session.config['treatments'][player.treatment]["decision_frequency"] == "PER_ROUND"

    @staticmethod
    def vars_for_template(self):
        return {
            'CURRENT_ROUND': self.round_number,
        }


class TransferEngagementResultsWaitPage(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.session.config['treatments']["decision_frequency"] == "PER_ROUND"

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_transfer_engagement_message()


class TransferEngagementResult(Page):
    @staticmethod
    def is_displayed(player):
        return player.session.config['treatments']["decision_frequency"] == "PER_ROUND"

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return {
            'engagement_message': group.transfer_engagement_message_text,
            'CURRENT_ROUND': player.round_number,
        }


class ProcurementPhase(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


# class RandomDraw(Page):
#     @staticmethod
#     def is_displayed(player):
#         return player.round_number == C.num_rounds
#
#     @staticmethod
#     def before_next_page(player, timeout_happened):
#         drawn_indices = [x - 1 for x in player.participant.drawn_rounds]
#         earnings_list = player.participant.earnings_list
#         player.drawn_earnings = str([earnings_list[i] for i in drawn_indices])
#         player.participant.drawn_earnings = [earnings_list[i] for i in drawn_indices]
#         player.participant.account_balance = round(sum(player.participant.drawn_earnings),2)
#
# class RandomDrawResult(Page):
#     @staticmethod
#     def is_displayed(player):
#         return player.round_number == C.num_rounds
#
#     @staticmethod
#     def vars_for_template(player: Player):
#         return dict(total_payoff=round(player.participant.account_balance+2.50,2))

# TODO ADD group matching waiting page as 1st

page_sequence = [TransferEngagement, TransferEngagementResultsWaitPage, TransferEngagementResult]
# ProcurementPhase, ResultsWaitPage, Results]
# RandomDraw,RandomDrawResult]
