import random

from otree.api import Currency as c, currency_range, expect, Bot
from . import *


class PlayerBot(Bot):
    def play_round(self):
        # # Set participant fields
        # self.participant.vars['initial_endowment'] = 100
        # self.participant.vars['some_other_field'] = 'example_value'

        if self.round_number == 1:
            # Navigate through the Welcome page
            yield Welcome

        if C.TREATMENTS[self.participant.treatment]["decision_frequency"] == "PER_ROUND":
            # Simulate data submission on TransferEngagement page
            yield TransferEngagement, {'transfer_engagement': random.choice([True, False])}

            # Verify the results on TransferEngagementResult page
            yield TransferEngagementResult

        # Simulate data submission on InventoryOrder page
        yield InventoryOrder, {'inventory_order': random.randint(0, 200)}

        yield Results

        if self.round_number == C.NUM_ROUNDS:
            yield RandomDraw

            # yield RandomDrawResult
