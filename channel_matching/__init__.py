import itertools
import random

from otree.api import *

import settings

doc = """
    Channel Matching with 6 players
"""


class C(BaseConstants):
    NAME_IN_URL = 'channel_matching'
    PLAYERS_PER_GROUP = CHANNEL_SIZE = 6
    NUM_ROUNDS = 1
    TREATMENTS = settings.GAME_CONFIG_DEFAULTS["treatments"]
    MAIN_GAME_NUM_ROUNDS = settings.GAME_CONFIG_DEFAULTS["num_rounds"]
    DEMANDS = settings.GAME_CONFIG_DEFAULTS["demands"]


class Subsession(BaseSubsession):
    num_groups_created = models.IntegerField(initial=0)

    def group_by_arrival_time_method(subsession, waiting_players):
        print('in group_by_arrival_time_method')
        if len(waiting_players) >= C.CHANNEL_SIZE:
            print('enough players to create a group')
            return waiting_players[:C.CHANNEL_SIZE]
        print('We have only {} players. Not enough players yet to create a group'.format(len(waiting_players)))


def creating_session(subsession):
    if subsession.round_number == 1:
        for player in subsession.get_players():
            player.participant.channel_matching = -1
            player.participant.channel_done = False


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES

class ResultsWaitPage(WaitPage):
    group_by_arrival_time = True

    def after_all_players_arrive(group: Group):
        # TODO to be changed to be dynamic
        next_app_subsessions = group.session.get_subsessions()[4:(C.MAIN_GAME_NUM_ROUNDS + 4)]

        subsession = group.subsession

        idx = subsession.num_groups_created % len(C.TREATMENTS.keys())
        treatment = list(C.TREATMENTS.keys())[idx]
        transfer_cost = itertools.cycle(C.TREATMENTS[treatment]["transfer_cost"])

        demands = itertools.cycle(C.DEMANDS.values())

        roles = {
            "A": [],
            "B": []
        }
        role = itertools.cycle(roles.keys())

        players_ids = []

        for p in group.get_players():
            # print("Players id:{} --- {} ".format(p.id_in_group, p.participant.id_in_session))
            p.participant.channel_matching = group.id_in_subsession
            p.participant.treatment = treatment
            p.participant.transfer_cost = next(transfer_cost)
            p.participant.transfer_price = next(transfer_cost)
            next(transfer_cost)
            p.participant.demand_history = next(demands)

            roles[next(role)].append(p.participant.id_in_session)
            players_ids.append(p.participant.id_in_session)
            p.participant.channel_done = True

        for sub in next_app_subsessions:
            players_matrix = sub.get_group_matrix()
            # print("Player matrix:{}".format(players_matrix))
            last_match = players_matrix[-1]
            # print("Last matrix:{}".format(last_match))
            for p_id in players_ids:
                last_match.remove(p_id)

            new_matrix = players_matrix[:-1]
            tmp_roles_b = roles["B"].copy()
            for element in roles["A"]:
                random_element = random.choice(tmp_roles_b)
                new_matrix.append([element, random_element])
                tmp_roles_b.remove(random_element)

            if len(last_match) > 0:
                new_matrix.append(last_match)
            # print("New matrix:{}".format(new_matrix))
            sub.set_group_matrix(new_matrix)
            # print(new_matrix)

        subsession.num_groups_created += 1


page_sequence = [ResultsWaitPage]
