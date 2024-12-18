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


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Welcome(Page):
    pass


class Introduction(Page):
    def vars_for_template(self):
        return {
            'MAIN_GAME_NUM_ROUNDS': C.MAIN_GAME_NUM_ROUNDS,
            'show_up_fee': self.session.config['participation_fee'],
            'conversion_rate': round(1 / self.session.config['real_world_currency_per_point']),  # 1EUR * conversion_rate
            'draw_earnings_num_rounds': self.session.config['draw_earnings_num_rounds']
        }


page_sequence = [Welcome, Introduction]
