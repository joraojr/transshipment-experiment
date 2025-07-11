from email.policy import default

from otree.api import *

import settings
import random

doc = """
Core Transshipment Game for 2 players with different treatments and transfer prices.

This game needs the channel_matching as previous app to work
"""


class C(BaseConstants):
    NAME_IN_URL = 'transshipment_game'
    PLAYERS_PER_GROUP = None  # This game needs the channel_matching as previous app to work
    NUM_ROUNDS = settings.GAME_CONFIG_DEFAULTS["num_rounds"]
    TREATMENTS = settings.GAME_CONFIG_DEFAULTS["treatments"]


########### SUBSESSIONS HERE ############################################
class Subsession(BaseSubsession):
    pass


#############################################################

################# GROUP #######################################

class Group(BaseGroup):
    transfer_engagement = models.BooleanField(default=False)
    transfer_engagement_message_text = models.StringField(default="")

    def all_transfer_engagement_yes(self):
        # Check if all players in the group have answered 'yes' to transfer_engagement
        return all(player.transfer_engagement for player in self.get_players())

    def set_transfer_engagement_message(self):
        if self.all_transfer_engagement_yes():
            self.transfer_engagement = True
            self.transfer_engagement_message_text = (
                "You and the other retailer decided to engage in a transfer. "
                "If there is excess demand or excess inventory, <b>a transfer will take place automatically. </b>"
            )
        else:
            self.transfer_engagement = False
            self.transfer_engagement_message_text = (
                "You or the other retailer decided not to engage in a transfer. "
                "If there is excess demand or excess inventory, <b>there will be no transfer. </b>"
            )


##################################################################

###################### PLAYER ####################################

class Player(BasePlayer):
    is_dropout = models.BooleanField(default=0)
    is_timeout_engagement = models.BooleanField(default=0)
    treatment = models.StringField()
    transfer_cost = models.IntegerField()
    transfer_price = models.IntegerField()
    transfer_engagement = models.BooleanField(
        label="Do you want to engage in a transfer with the other retailer, in case you face excess demand or excess inventory?",
        blank=False
    )
    inventory_order = models.IntegerField(
        # label="Your task is to make an inventory order decision this round.",
        blank=False,
        min=0,
        max=200,
    )
    demand = models.IntegerField()
    earnings = models.IntegerField()
    excess_demand = models.BooleanField()
    excess_inventory = models.BooleanField()
    extra = models.IntegerField()
    send_units = models.IntegerField(default=0, min=0)
    received_units = models.IntegerField(default=0, min=0)

    result_message_text = models.StringField()

    # TODO Change it to be get other demand info
    # Create transfer cost and price for each player
    def get_matched_player(self):
        # Retrieve all players in the same group
        all_players = self.group.get_players()
        # Filter out the current player
        other_players = [p for p in all_players if p.id_in_group != self.id_in_group]
        # get the other player in the group (only 2 players in a group)
        return other_players[0]


#############################################################

####### PAGES ###############################################
class Welcome(Page):
    timeout_seconds = 30

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    def vars_for_template(self):
        return {
            'MAIN_GAME_NUM_ROUNDS': C.NUM_ROUNDS,
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.inventory_order_history = []
        player.participant.earnings_list = []

        for i in range(1, C.NUM_ROUNDS + 1):
            p = player.in_round(i)
            p.treatment = player.participant.treatment
            p.transfer_cost = player.participant.transfer_cost
            p.transfer_price = player.participant.transfer_price
            p.demand = player.participant.demand_history[i - 1]
            if C.TREATMENTS[player.treatment]["decision_frequency"] == "ENFORCED":
                p.transfer_engagement = True
                p.group.transfer_engagement = True


class Instructions(Page):
    timeout_seconds = 120

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    def vars_for_template(self):
        return {
            'MAIN_GAME_NUM_ROUNDS': C.NUM_ROUNDS,
            'decision_frequency': C.TREATMENTS[self.treatment]["decision_frequency"],
            'draw_earnings_num_rounds': self.session.config['draw_earnings_num_rounds'],
            'p1_transfer_cost': self.transfer_cost,
            'p2_transfer_cost': self.transfer_price,
            'conversion_rate': round(1 / self.session.config['real_world_currency_per_point']),  # 1EUR * conversion_rate

        }


class TransferEngagement(Page):
    form_model = 'player'
    form_fields = ['transfer_engagement']

    @staticmethod
    def get_timeout_seconds(player):
        if player.round_number == 1:
            return 15
        elif 2 <= player.round_number <= 5:
            return 10
        elif 6 <= player.round_number <= 15:
            return 10

    @staticmethod
    def is_displayed(player):
        return C.TREATMENTS[player.treatment]["decision_frequency"] == "PER_ROUND"

    @staticmethod
    def vars_for_template(self):
        return {
            'CURRENT_ROUND': self.round_number,
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.is_timeout_engagement = True


class TransferEngagementResultsWaitPage(WaitPage):
    body_text = "Waiting for the other participant. Please refresh this page at last every 30 second otherwise you might skip one or several rounds."

    @staticmethod
    def is_displayed(player):
        return C.TREATMENTS[player.treatment]["decision_frequency"] == "PER_ROUND"

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_transfer_engagement_message()


class TransferEngagementResult(Page):
    @staticmethod
    def get_timeout_seconds(player):
        if player.round_number == 1:
            return 15
        elif 2 <= player.round_number <= 5:
            return 10
        elif 6 <= player.round_number <= 15:
            return 10

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


class InventoryOrder(Page):
    form_model = 'player'
    form_fields = ['inventory_order']

    @staticmethod
    def get_timeout_seconds(player):
        if player.round_number == 1:
            return 30
        elif 2 <= player.round_number <= 5:
            return 20
        elif 6 <= player.round_number <= 15:
            return 15

    @staticmethod
    def vars_for_template(player: Player):
        return {
            # 'player_inventory_order_history': player.participant.inventory_order_history,
            # 'player_demand_history': player.participant.demand_history,
            'player_earnings_list': player.participant.earnings_list,
            'CURRENT_ROUND': player.round_number,
            'decision_frequency': C.TREATMENTS[player.treatment]["decision_frequency"],
            'p1_transfer_cost': player.transfer_cost,
            'p2_transfer_cost': player.transfer_price

        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.is_dropout = True
        player.participant.inventory_order_history.append(player.inventory_order)
        # player.participant.demand_history.append(player.demand)


class ResultsWaitPage(WaitPage):
    body_text = "Waiting for the other participant. Please refresh this page at last every 30 second otherwise you might skip one or several rounds."

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
            p2 = p1.get_matched_player()

            ##### STANDARD ################################################################################################
            p1.result_message_text = """
                        <b> Your Order and Demand </b> <br>
                        You ordered {} units. <br>
                        Current demand is {} units. <br>
                        """.format(p1.inventory_order, p1.demand)

            if p1.extra == 0:
                p1.result_message_text += "You have met your demand. <br>"
            ################################################################################################################

            else:
                if p1.excess_demand:
                    p1.result_message_text += "Your excess demand is {} units ({} - {}). <br>".format(p1.demand - p1.inventory_order, p1.demand,
                                                                                                      p1.inventory_order)
                elif p1.excess_inventory:
                    p1.result_message_text += "Your excess inventory is {} units ({} - {}). <br>".format(p1.inventory_order - p1.demand,
                                                                                                         p1.inventory_order, p1.demand)

                if C.TREATMENTS[p1.treatment]["decision_frequency"] == "PER_ROUND":
                    p1.result_message_text += """   
                        <br> <b> Transfer Decision </b> <br>
                    """
                if p1.group.transfer_engagement:
                    if C.TREATMENTS[p1.treatment]["decision_frequency"] == "PER_ROUND":
                        p1.result_message_text += "You and the other retailer decided to engage in a transfer this round. <br>"

                    p1.result_message_text += """   
                        <br> <b> Transfer Result </b> <br>
                    """
                    if p1.excess_demand and p2.excess_inventory:
                        p1.received_units = p2.send_units = transfer_units = min(abs(p1.extra), p2.extra)
                        p1.result_message_text += (
                            "The other retailer has excess inventory of {} units.<br>"
                            "The other retailer transfers {} units to you from their excess inventory to meet your current demand.  <br>").format(
                            p2.extra, transfer_units)
                    elif p1.excess_inventory and p2.excess_demand:
                        p2.received_units = p1.send_units = transfer_units = min(p1.extra, abs(p2.extra))
                        p1.result_message_text += (
                            "The other retailer has excess demand of {} units. <br> "
                            "You transfer to the other retailer {} units from your excess inventory to meet their current demand.  <br>").format(
                            abs(p2.extra), transfer_units)

                    elif p1.excess_inventory and p2.excess_inventory:
                        p1.result_message_text += ("The other retailer has excess inventory.<br>"
                                                   "You both have excess inventory. No units are transferred. <br>")
                    elif p1.excess_demand and p2.excess_demand:
                        p1.result_message_text += ("The other retailer has excess demand.<br>"
                                                   "You both have excess demand. No units are transferred. <br>")
                    elif (p1.excess_inventory or p1.excess_demand) and p2.extra == 0:
                        p1.result_message_text += ("The other retailer met their demand.<br>"
                                                   "No units are transferred. <br>")

                else:
                    if C.TREATMENTS[p1.treatment]["decision_frequency"] == "PER_ROUND":
                        p1.result_message_text += ("You or the other retailer decided not to engage in a transfer this round. <br>"
                                                   "No units are transferred this round. <br>")


class Results(Page):

    @staticmethod
    def get_timeout_seconds(player):
        if player.round_number == 1:
            return 40
        elif 2 <= player.round_number <= 5:
            return 30
        elif 6 <= player.round_number <= 15:
            return 20

    @staticmethod
    def vars_for_template(player: Player):
        # Revenue for this round

        retail_units = player.demand if player.inventory_order - player.demand >= 0 else player.inventory_order
        total_retail_units = retail_units + player.received_units
        total_retail_unit_price = total_retail_units * 40

        total_transfer_units = player.send_units * player.get_matched_player().transfer_cost

        total_savage_units = max(0, player.inventory_order - player.demand - player.send_units)
        total_savage_unit_price = total_savage_units * 10

        total_price = total_retail_unit_price + total_transfer_units + total_savage_unit_price

        # Costs for this round

        procurement_cost = player.inventory_order * 20
        transfer_cost = player.received_units * player.transfer_cost

        total_cost = procurement_cost + transfer_cost

        # Payoff for this round

        player.earnings = earnings = total_price - total_cost

        result_message_text = player.result_message_text + "<br> <b> Earnings </b> <br> You earned {} ECU this round".format(earnings)

        return {
            'result_message_text': result_message_text,
            'CURRENT_ROUND': player.round_number,
            'retail_price': [total_retail_units, total_retail_unit_price],
            'transfer_cost': [player.received_units, transfer_cost],
            'salvage_price': [total_savage_units, total_savage_unit_price],
            'total_price': total_price,
            'procurement_cost': [player.inventory_order, procurement_cost],
            'transfer_price': [player.send_units, total_transfer_units],
            'total_cost': total_cost,
            'earnings': earnings,
            'decision_frequency': C.TREATMENTS[player.treatment]["decision_frequency"],
            'p1_transfer_cost': player.transfer_cost,
            'p2_transfer_cost': player.transfer_price

        }

    def before_next_page(player, timeout_happened):
        player.participant.earnings_list.append(player.earnings)


class RandomDraw(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Randomly draw rounds for the player payout
        drawn_indices = player.participant.draw_earnings_indexes = random.sample(
            range(C.NUM_ROUNDS),
            player.session.config['draw_earnings_num_rounds']
        )

        earnings_list = player.participant.earnings_list
        drawn_earnings = [earnings_list[i] for i in drawn_indices]
        player.participant.drawn_earnings = drawn_earnings
        player.participant.avg_earnings = avg_earnings = sum(drawn_earnings) / len(drawn_earnings)

        # Ensure the no negative payoff (At least the fixed participation fee must be paid)
        player.participant.payoff = cu(max(avg_earnings, 0))

    def vars_for_template(player: Player):
        return dict(
            DRAW_EARNINGS_NUM_ROUNDS=player.session.config['draw_earnings_num_rounds'],
            conversion_rate=round(1 / player.session.config['real_world_currency_per_point']),  # 1EUR * conversion_rate
            show_up_fee=player.session.config['participation_fee'],

        )


class RandomDrawResult(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            avg_earnings=player.participant.avg_earnings,
            payoff=player.participant.payoff_in_real_world_currency(),
            total_payoff=player.participant.payoff_plus_participation_fee(),
            drawn_earnings=player.participant.drawn_earnings,
            drawn_rouds=[x + 1 for x in player.participant.draw_earnings_indexes],
            conversion_rate=round(1 / player.session.config['real_world_currency_per_point']),  # 1EUR * conversion_rate
            show_up_fee=player.session.config['participation_fee'],

        )


#############################################################

##ORDER#######################################################

page_sequence = [Welcome, Instructions,
                 TransferEngagement, TransferEngagementResultsWaitPage, TransferEngagementResult,
                 InventoryOrder, ResultsWaitPage, Results,
                 RandomDraw, RandomDrawResult]
