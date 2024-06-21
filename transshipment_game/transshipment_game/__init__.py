from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'transshipment_game'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
    TREATMENTS = {
        "C1": {
            "decision_frequency": "PER_ROUND",
            "values": (12, 12)
        },  # (T=S) => PER_ROUNDS_STANDARD_BOUND (IDENTICAL) [CONTROL]

        # "C2": {
        #     "decision_frequency": "PER_ROUND",
        #     "values": (21, 21)
        # },  # (T>S) => PER_ROUNDS_WITHIN_STANDARD (IDENTICAL)
        # "C3": {
        #     "decision_frequency": "PER_ROUND",
        #     "values": (8, 8)
        # },  # (T<S) => PER_ROUNDS_STRICTLY_BELLOW (IDENTICAL)

        # "C4": {
        #     "decision_frequency": "PER_ROUND",
        #     "values": (18, 24)
        # },  # (T<S) => PER_ROUNDS_STRICTLY_BELLOW (NON- IDENTICAL)
        # "C5": {
        #     "decision_frequency": "PER_ROUND",
        #     "values": (12, 40)
        # },  # (T<S) => PER_ROUNDS_STRICTLY_BELLOW (NON- IDENTICAL)
        # "C6": {
        #     "decision_frequency": "PER_ROUND",
        #     "values": (8, 32)
        # },  # (T<S) => PER_ROUNDS_STRICTLY_BELLOW (NON- IDENTICAL)

        # "C7": {
        #     "decision_frequency": "ENFORCED",
        #     "values": (18, 24)
        # },  # (T<S) => PER_ROUNDS_STRICTLY_BELLOW (NON- IDENTICAL)
        # "C8": {
        #     "decision_frequency": "ENFORCED",
        #     "values": (12, 40)
        # },  # (T<S) => PER_ROUNDS_STRICTLY_BELLOW (NON- IDENTICAL)
        # "C9": {
        #     "decision_frequency": "ENFORCED",
        #     "values": (8, 32)
        # },  # (T<S) => PER_ROUNDS_STRICTLY_BELLOW (NON- IDENTICAL)
    }


class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    # Assign Treatments from the Previous app to the players
    if subsession.round_number > 1:
        subsession.group_like_round(1)

    for group in subsession.get_groups():
        for player in group.get_players():
            player.treatment = player.participant.treatment


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
        return C.TREATMENTS[player.treatment]["decision_frequency"] == "PER_ROUND"


class TransferEngagementResultsWaitPage(WaitPage):
    @staticmethod
    def is_displayed(player):
        return C.TREATMENTS[player.treatment]["decision_frequency"] == "PER_ROUND"

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_transfer_engagement_message()


class TransferEngagementResult(Page):
    @staticmethod
    def is_displayed(player):
        return C.TREATMENTS[player.treatment]["decision_frequency"] == "PER_ROUND"

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


# TODO ADD group matching waiting page as 1st

page_sequence = [TransferEngagement, TransferEngagementResultsWaitPage, TransferEngagementResult]
# ProcurementPhase, ResultsWaitPage, Results]
