from otree.api import *

import settings
import time

doc = """
Instructions to the Transshipment Game
"""


class C(BaseConstants):
    NAME_IN_URL = 'instructions'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    MAIN_GAME_NUM_ROUNDS = settings.GAME_CONFIG_DEFAULTS["num_rounds"]
    TREATMENTS = settings.GAME_CONFIG_DEFAULTS["treatments"]
    DEMANDS = settings.GAME_CONFIG_DEFAULTS["demands"]


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField()
    transfer_cost = models.IntegerField()

    def get_matched_player(self):
        # Retrieve all players in the same group
        all_players = self.group.get_players()
        # Filter out the current player
        other_players = [p for p in all_players if p.id_in_group != self.id_in_group]

        # get the other player in the group (only 2 players in a group)
        return other_players[0]


# PAGES

class Welcome(Page):
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
    pass


class Instructions3(Page):
    def vars_for_template(player: Player):
        return {
            'draw_earnings_num_rounds': player.session.config['draw_earnings_num_rounds'],
            'conversion_rate': 1 / player.session.config['real_world_currency_per_point'],  # 1EUR * conversion_rate

        }


class Comprehension1(Page):
    def before_next_page(player, timeout_happened):
        epoch_time = int(time.time())
        to_export = ["initialize", epoch_time]
        player.participant.comprehension_activity = [to_export]


class Comprehension2(Page):
    @staticmethod
    def live_method(player, data):
        epoch_time = int(time.time())
        to_export = [data["question_id"], data["selected_option"], epoch_time]
        player.participant.comprehension_activity.append(to_export)

    def before_next_page(player, timeout_happened):
        epoch_time = int(time.time())
        to_export = ["end", epoch_time]
        player.participant.comprehension_activity.append(to_export)


page_sequence = [Welcome, Instructions1, Instructions2, Instructions3, Comprehension1, Comprehension2]
