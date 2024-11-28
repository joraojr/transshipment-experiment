from otree.api import *

import settings
import time

doc = """
Welcome to the Experiment  
"""


class C(BaseConstants):
    NAME_IN_URL = 'welcome'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    MAIN_GAME_NUM_ROUNDS = settings.GAME_CONFIG_DEFAULTS["num_rounds"]
    TREATMENTS = settings.GAME_CONFIG_DEFAULTS["treatments"]
    DEMANDS = settings.GAME_CONFIG_DEFAULTS["demands"]


class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    # Assign Treatments to the players
    import itertools
    treatments = itertools.cycle(C.TREATMENTS.keys())
    demands = itertools.cycle(C.DEMANDS.values())

    if subsession.round_number == 1:
        players = subsession.get_players()
        treatment = next(treatments)
        transfer_price = itertools.cycle(C.TREATMENTS[treatment]["transfer_price"])

        for i, player in enumerate(players):
            demand = next(demands)
            player.treatment = player.participant.treatment = treatment
            player.transfer_price = player.participant.transfer_price = next(transfer_price)
            player.participant.demand_history = demand
            # player.role = "A"

            # Ensure that each 2 player get the same treatment
            if i % 2 == 1:
                treatment = next(treatments)
                transfer_price = itertools.cycle(C.TREATMENTS[treatment]["transfer_price"])


    else:
        subsession.group_like_round(1)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField()
    transfer_price = models.IntegerField()

    def get_matched_player(self):
        # Retrieve all players in the same group
        all_players = self.group.get_players()
        # Filter out the current player
        other_players = [p for p in all_players if p.id_in_group != self.id_in_group]

        # get the other player in the group (only 2 players in a group)
        return other_players[0]


# PAGES
class Welcome(Page):
    pass


class Introduction(Page):
    def vars_for_template(self):
        return {
            'MAIN_GAME_NUM_ROUNDS': C.MAIN_GAME_NUM_ROUNDS,
            'show_up_fee': self.session.config['participation_fee'],
            'conversion_rate': 1 / self.session.config['real_world_currency_per_point'],  # 1EUR * conversion_rate
            'draw_earnings_num_rounds': self.session.config['draw_earnings_num_rounds']
        }




page_sequence = [Welcome, Introduction]
