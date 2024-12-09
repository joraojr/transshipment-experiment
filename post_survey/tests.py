import random
from otree.api import Currency as c, currency_range, expect, Bot
from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Welcome
        yield Q1, {
            'RT_QA1': random.randint(0, 10),
            'T_QA1': random.randint(0, 10),
            'A_QA1': random.randint(0, 10),
            'NR_QA1': random.randint(0, 10),
        }

        yield Q2, {
            'PR_QA1': random.choice([5, 10, 15, 20, 25, 30]),
        }

        yield Demographics, {
            'age': random.randint(14, 100),
            'gender': random.choice(["Male", "Female", "Other", "Prefer not to say"]),
            'subject': random.choice(["Economics/Business", "Law", "Humanities", "Science/Engineering", "None", "Other"]),
            'religion': random.choice(["Strongly Disagree", "Disagree", "Neither Agree nor Disagree", "Agree", "Strongly Agree"])
        }
