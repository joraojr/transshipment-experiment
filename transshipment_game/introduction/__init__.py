from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
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
    # Assign Treatments to the players
    import itertools
    treatments = itertools.cycle(C.TREATMENTS.keys())

    if subsession.round_number == 1:
        players = subsession.get_players()
        for player in players:
            player.treatment = player.participant.treatment = next(treatments)

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
    pass


class Instructions1(Page):
    pass


class Instructions2(Page):
    pass


class Instructions3(Page):
    pass


class Comprehension(Page):
    pass


page_sequence = [Welcome, Introduction, Instructions1, Instructions2, Instructions3, Comprehension]
