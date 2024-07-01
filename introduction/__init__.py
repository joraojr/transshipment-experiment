from otree.api import *

import settings

doc = """
Introduction to the Transshipment Game
"""


class C(BaseConstants):
    NAME_IN_URL = 'introduction'
    PLAYERS_PER_GROUP = None
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
        for i, player in enumerate(players):
            player.treatment = player.participant.treatment = treatment

            # Ensure that each 2 player get the same treatment
            if i % 2 == 1:
                treatment = next(treatments)

    else:
        subsession.group_like_round(1)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField()


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
            'decision_frequency': C.TREATMENTS[player.treatment]["decision_frequency"]
        }


class Instructions3(Page):
    def vars_for_template(player: Player):
        return {
            'decision_frequency': C.TREATMENTS[player.treatment]["decision_frequency"]
        }


class Comprehension1(Page):
    pass


class Comprehension2(Page):
    pass


page_sequence = [Welcome, Introduction, Instructions1, Instructions2, Instructions3, Comprehension1, Comprehension2]
