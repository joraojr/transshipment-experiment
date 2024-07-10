from otree.api import *

import settings
import time

doc = """
Introduction to the Transshipment Game
"""


class C(BaseConstants):
    NAME_IN_URL = 'introduction'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    MAIN_GAME_NUM_ROUNDS = settings.GAME_CONFIG_DEFAULTS["num_rounds"]
    TREATMENTS = settings.GAME_CONFIG_DEFAULTS["treatments"]


class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    # Assign Treatments to the players
    import itertools
    treatments = itertools.cycle(C.TREATMENTS.keys())

    if subsession.round_number == 1:
        players = subsession.get_players()
        treatment = next(treatments)
        transfer_price = itertools.cycle(C.TREATMENTS[treatment]["transfer_price"])

        for i, player in enumerate(players):
            player.treatment = player.participant.treatment = treatment
            player.transfer_price = player.participant.transfer_price = next(transfer_price)
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


class Instructions1(Page):
    pass


class Instructions2(Page):
    def vars_for_template(player: Player):
        return {
            'decision_frequency': C.TREATMENTS[player.treatment]["decision_frequency"],
            'p1_transfer_price': player.transfer_price,
            'p2_transfer_price': player.get_matched_player().transfer_price

        }


class Instructions3(Page):
    def vars_for_template(player: Player):
        return {
            'decision_frequency': C.TREATMENTS[player.treatment]["decision_frequency"]
        }


class Comprehension1(Page):
    def before_next_page(player, timeout_happened):
        epoch_time = int(time.time())
        to_export = ["initialize", epoch_time]
        player.participant.comprehension_activity = [to_export]


class Comprehension2(Page):
    def vars_for_template(player: Player):
        return {
            'decision_frequency': C.TREATMENTS[player.treatment]["decision_frequency"],
        }

    @staticmethod
    def live_method(player, data):
        epoch_time = int(time.time())
        to_export = [data["question_id"], data["selected_option"], epoch_time]
        player.participant.comprehension_activity.append(to_export)

    def before_next_page(player, timeout_happened):
        epoch_time = int(time.time())
        to_export = ["end", epoch_time]
        player.participant.comprehension_activity.append(to_export)


page_sequence = [Welcome, Introduction, Instructions1, Instructions2, Instructions3, Comprehension1, Comprehension2]
