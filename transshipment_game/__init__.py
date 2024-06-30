from otree.api import *

doc = """
Core Transshipment Game
"""


class C(BaseConstants):
    import random

    NAME_IN_URL = 'transshipment_game'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 20  # TODO to make it dynamic


class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    import random

    # Assign Treatments from the Previous app to the players
    for player in subsession.get_players():
        player.treatment = player.participant.treatment
        player.participant.inventory_order_history = []
        player.participant.earnings_list = []
        player.participant.demand_history = []
        player.demand = random.randint(0, 200)
        # player.demand = max(0, min(round(random.normalvariate(100, 15)), 200))  # mean 100 and std 15

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
                "You and the other retailer decided to engage in a transfer. "
                "If there is excess demand or excess inventory, <b>a transfer will take place automatically. </b>"
            )
        else:
            self.transfer_engagement = False
            self.transfer_engagement_message_text = (
                "You or the other retailer decided not to engage in a transfer. "
                "If there is excess demand or excess inventory, <b>there will be no transfer. </b>"
            )


class Player(BasePlayer):
    treatment = models.StringField()
    transfer_engagement = models.BooleanField(
        label="Decide whether you want to engage in a transfer with the other retailer, in case you face excess demand or excess inventory.",
        blank=False
    )
    inventory_order = models.IntegerField(
        # label="Your task is to make an inventory order decision this round.",
        blank=False,
        min=0,
        max=200,
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


class InventoryOrder(Page):
    form_model = 'player'
    form_fields = ['inventory_order']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'player_inventory_order_history': player.participant.inventory_order_history,
            'player_demand_history': player.participant.demand_history,
            'CURRENT_ROUND': player.round_number,
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.inventory_order_history.append(player.inventory_order)
        player.participant.demand_history.append(player.demand)


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
            p2 = p1.get_other_players()[0]  # get the other player in the group (only 2 players in a group)

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
                    p1.result_message_text += "Your excess excess inventory is {} units ({} - {}). <br>".format(p1.inventory_order - p1.demand,
                                                                                                                p1.inventory_order, p1.demand)

                p1.result_message_text += """   
                    <br> <b> Transfer Decision </b> <br>
                """

                if p1.group.transfer_engagement:
                    p1.result_message_text += "You and the other retailer decided to engage in a transfer this round. <br>"
                    p1.result_message_text += """   
                        <br> <b> Transfer Result </b> <br>
                    """
                    if p1.excess_demand and p2.excess_inventory:
                        p1.received_units = p2.send_units = transfer_units = min(abs(p1.extra), p2.extra)
                        p1.result_message_text += (
                            "The other retailer has excess inventory of {} units.<br>"
                            "The other retailer transfer to you {} units from their excess inventory to meet your current demand.  <br>").format(
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
                    p1.result_message_text += ("You or the other retailer decided not to engage in a transfer this round. <br>"
                                               "No units are transferred this round. <br>")


class Results(Page):

    @staticmethod
    def vars_for_template(player: Player):
        # Revenue for this round

        retail_units = player.demand if player.inventory_order - player.demand >= 0 else player.inventory_order
        total_retail_units = retail_units + player.received_units
        total_retail_unit_price = total_retail_units * 40

        total_transfer_units = player.send_units * 12

        total_savage_units = max(0, player.inventory_order - player.demand - player.send_units)
        total_savage_unit_price = total_savage_units * 10

        total_price = total_retail_unit_price + total_transfer_units + total_savage_unit_price

        # Costs for this round

        procurement_cost = player.inventory_order * 20
        transfer_cost = player.received_units * 12

        total_cost = procurement_cost + transfer_cost

        # Payoff for this round

        earnings = total_price - total_cost

        result_message_text = player.result_message_text + "<br> <b> Earnings </b> <br> You earned {} ECU this round".format(earnings)

        player.participant.earnings_list.append(earnings)

        return {
            'result_message_text': result_message_text,
            'CURRENT_ROUND': player.round_number,
            'retail_price': [total_retail_units, total_retail_unit_price],
            'transfer_price': [player.send_units, total_transfer_units],
            'salvage_price': [total_savage_units, total_savage_unit_price],
            'total_price': total_price,
            'procurement_cost': [player.inventory_order, procurement_cost],
            'transfer_cost': [player.received_units, transfer_cost],
            'total_cost': total_cost,
            'earnings': earnings

        }


class RandomDraw(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Randomly draw rounds for the player payout
        import random

        drawn_indices = player.participant.draw_earnings_indexes = random.sample(
            range(C.NUM_ROUNDS),
            player.session.config['draw_earnings_num_rounds']
        )

        earnings_list = player.participant.earnings_list
        drawn_earnings = [earnings_list[i] for i in drawn_indices]
        player.participant.drawn_earnings = drawn_earnings
        player.participant.avg_earnings = avg_earnings = sum(drawn_earnings) / len(drawn_earnings)

        # Ensure the no negative payoff (At least the show-up fee must be paid)
        player.participant.payoff = round(max(avg_earnings, 0))

    def vars_for_template(player: Player):
        return dict(
            DRAW_EARNINGS_NUM_ROUNDS=player.session.config['draw_earnings_num_rounds'],
            conversion_rate=1 / player.session.config['real_world_currency_per_point'],  # 1EUR * conversion_rate
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
            conversion_rate=1 / player.session.config['real_world_currency_per_point'],  # 1EUR * conversion_rate
        )


# TODO ADD group matching waiting page as 1st

page_sequence = [TransferEngagement, TransferEngagementResultsWaitPage, TransferEngagementResult,
                 InventoryOrder, ResultsWaitPage, Results,
                 RandomDraw, RandomDrawResult]
