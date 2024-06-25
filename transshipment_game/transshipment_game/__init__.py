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
    import random
    # Assign Treatments from the Previous app to the players
    for player in subsession.get_players():
        player.treatment = player.participant.treatment
        player.participant.inventory_order_history = [-1]
        # player.demand = int(np.clip(np.random.normal(100, 30), 0, 200))
        # player.demand = random.randint(0, 200)
        player.demand = max(0, min(round(random.normalvariate(100, 15)), 200))  # mean 100 and std 15

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
    inventory_order = models.IntegerField(
        label="Your task is to make an inventory order decision this round.",
        blank=False,
        min=0,
        max=230,
    )
    demand = models.IntegerField()
    excess_demand = models.BooleanField()
    excess_inventory = models.BooleanField()
    extra = models.IntegerField()
    send_units = models.IntegerField(default=0, min=0)
    received_units = models.IntegerField(default=0, min=0)

    result_message_text = models.StringField()

    def get_other_players(self):
        # Retrieve all players in the same group
        all_players = self.group.get_players()
        # Filter out the current player
        other_players = [p for p in all_players if p.id_in_group != self.id_in_group]
        return other_players


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
        return player.session.config['treatments'][player.treatment]["decision_frequency"] == "PER_ROUND"

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_transfer_engagement_message()


class TransferEngagementResult(Page):
    @staticmethod
    def is_displayed(player):
        return player.session.config['treatments'][player.treatment]["decision_frequency"] == "PER_ROUND"

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return {
            'engagement_message': group.transfer_engagement_message_text,
            'CURRENT_ROUND': player.round_number,
        }


class ProcurementPhase(Page):
    form_model = 'player'
    form_fields = ['inventory_order']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'player_inventory_order_history': player.participant.inventory_order_history,
            'CURRENT_ROUND': player.round_number,
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.inventory_order_history.append(player.inventory_order)


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):

        for p in group.get_players():
            if p.inventory_order > p.demand:
                p.excess_inventory = True
                p.excess_demand = False
            elif p.inventory_order < p.demand:
                p.excess_inventory = False
                p.excess_demand = True
            else:  # demand == inventory_order
                p.excess_inventory = False
                p.excess_demand = False

            p.extra = p.inventory_order - p.demand

        for p1 in group.get_players():
            p2 = p1.get_other_players()[0] # get the other player in the group (only 2 players in a group)

            ##### STANDARD ################################################################################################
            p1.result_message_text = """
                        You ordered {} units. <br>
                        The current demand is {} units. <br>
            """.format(p1.inventory_order, p1.demand)

            if p1.extra == 0:
                p1.result_message_text += "You have met your demand."
            ################################################################################################################

            else:
                if p1.excess_demand:
                    p1.result_message_text += "You have an excess demand of {} units. <br>".format(p1.demand - p1.inventory_order)
                elif p1.excess_inventory:
                    p1.result_message_text += "You have an excess inventory of {} units. <br>".format(p1.inventory_order - p1.demand)

                if p1.group.transfer_engagement:
                    p1.result_message_text += "You and the other retailer decided to engage in a transfer this round. <br>"
                    if p1.excess_demand and p2.excess_inventory:
                        p1.received_units = p2.send_units = transfer_units = min(abs(p1.extra), p2.extra)
                        p1.result_message_text += (
                            "The other retailer has an excess inventory.<br>"
                            "The other retailer transfer to you {} units from their excess inventory to meet your current demand.").format(
                            transfer_units)
                    elif p1.excess_inventory and p2.excess_demand:
                        p2.received_units = p1.send_units = transfer_units = min(p1.extra, abs(p2.extra))
                        p1.result_message_text += (
                            "The other retailer has an excess demand. <br> "
                            "You transfer to the other retailer {} units from your excess inventory to meet their current demand.").format(
                            transfer_units)
                    elif p1.excess_inventory and p2.excess_inventory:
                        p1.result_message_text += "The other retailer has an excess inventory therefore no units are transferred. <br>"
                    elif p1.excess_demand and p2.excess_demand:
                        p1.result_message_text += "The other retailer has an excess demand therefore no units are transferred. <br>"

                else:
                    p1.result_message_text += "You or the other retailer decided not to engage in a transfer this round. No units are transferred this round."


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'result_message_text': player.result_message_text,
            'CURRENT_ROUND': player.round_number,
        }


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

page_sequence = [TransferEngagement, TransferEngagementResultsWaitPage, TransferEngagementResult,
                 ProcurementPhase, ResultsWaitPage, Results]
# RandomDraw,RandomDrawResult]
