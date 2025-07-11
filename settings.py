from os import environ

SESSION_CONFIGS = [

    dict(
        name='Transshipment_Game',
        app_sequence=['welcome', 'pre_survey', 'game_instructions', 'channel_matching', 'transshipment_game', 'post_survey'],
        num_demo_participants=6,
    ),
    # dict(
    #     name='Channel_testing',
    #     app_sequence=['game_instructions', 'channel_matching', 'transshipment_game'],
    #     num_demo_participants=6,
    # ),
    # dict(
    #     name='Payout_measuring',
    #     app_sequence=['game_instructions', 'transshipment_game'],
    #     num_demo_participants=1 * 2,
    # ),
    # dict(
    #     name='post_survey',
    #     app_sequence=['post_survey'],
    #     num_demo_participants=1 * 2,
    # ),
    #
    # dict(
    #     name='pre_survey',
    #     app_sequence=['pre_survey'],
    #     num_demo_participants=2 * 2,
    # ),
]

ROOMS = [
    {
        'name': 'waiting_room_1',
        'display_name': 'Waiting Room 1 - With Labels',
        'participant_label_file': '_rooms/exp_labels.txt',  # You can specify a file with participant labels if needed
        'use_secure_urls': True,  # Use secure URLs for participant login
    },
    {
        'name': 'waiting_room_2',
        'display_name': 'Waiting Room 2- Not Labels',
        # 'participant_label_file': '_rooms/exp_labels.txt',  # You can specify a file with participant labels if needed
        # 'use_secure_urls': True,  # Use secure URLs for participant login
    },
]

GAME_CONFIG_DEFAULTS = dict(
    num_rounds=15,
    demands={
        "A": [170, 96, 189, 3, 180, 16, 113, 87, 54, 151, 5, 58, 155, 114, 146],
        "B": [153, 135, 32, 147, 130, 169, 32, 64, 54, 98, 149, 11, 157, 173, 49]

    },
    treatments={
        #     "C4_PER_ROUND": {
        #         "decision_frequency": "PER_ROUND",
        #         "roles": "non-identical",
        #         "transfer_cost": [18, 24]  # demands [A,B]
        #     },
        #
        #     "C4_ENFORCED": {
        #         "decision_frequency": "ENFORCED",
        #         "roles": "non-identical",
        #         "transfer_cost": [18, 24]  # demands [A,B]
        #     },
        #
        #     "C5_PER_ROUND": {
        #         "decision_frequency": "PER_ROUND",
        #         "roles": "non-identical",
        #         "transfer_cost": [10, 40]
        #     },
        #
        #     "C5_ENFORCED": {
        #         "decision_frequency": "ENFORCED",
        #         "roles": "non-identical",
        #         "transfer_cost": [10, 40]
        #     },

        "C2_PER_ROUND": {
            "decision_frequency": "PER_ROUND",
            "roles": "identical",
            "transfer_cost": [18]
        },
        "C2_ENFORCED": {
            "decision_frequency": "ENFORCED",
            "roles": "identical",
            "transfer_cost": [18]
        },

        # "C6_PER_ROUND": {
        #     "decision_frequency": "PER_ROUND",
        #     "roles": "non-identical",
        #     "transfer_cost": [8, 24]
        # },
        #
        # "C6_ENFORCED": {
        #     "decision_frequency": "ENFORCED",
        #     "roles": "non-identical",
        #     "transfer_cost": [8, 24]
        # },
    }
)

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1 / 1000,  # 0.05% => 200 ECU = 1 EUR, 0.10% => 100 ECU = 1 EUR, 0.003 => 333.33 ECU = 1 EUR
    participation_fee=5,  # ==> 8.5 EUR (range 6-9 GBP)
    draw_earnings_num_rounds=4,
    draw_dictator_endowments=500,
    draw_earnings_dictator=5,
    doc="",
)

# TODO add conversion_rate round to 0 decimal places here

PARTICIPANT_FIELDS = [
    "treatment", "transfer_cost", "transfer_price", "inventory_order_history", "demand_history",
    "comprehension_activity",
    "channel_done", "channel_matching",
    "selected_for_earning_dictator", "earning_dictator",
    "earnings_list", "draw_earnings_indexes", "drawn_earnings", "avg_earnings",
    "earning_risk", "selected_risk",
    "finished"
]
SESSION_FIELDS = ["prolific_completion_url"]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'ECU'

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6733260475510'

BROWSER_COMMAND = "brave-browser"

# treatments = {
#     # (T=S) => PER_ROUNDS_STANDARD_BOUND (IDENTICAL) [CONTROL]
#     "C1_PER_ROUND": {
#         "decision_frequency": "PER_ROUND",
#         "roles": "identical",
#         "transfer_cost": [12]
#     },
#
#     # "C1_ENFORCED": {
#     #     "decision_frequency": "ENFORCED",
#     #     "roles": "identical",
#     #     "transfer_cost": [12]
#     # },
#     ##################################################
#
#     # (T>S) => PER_ROUNDS_WITHIN_STANDARD (IDENTICAL)
#     "C2_PER_ROUND": {
#         "decision_frequency": "PER_ROUND",
#         "roles": "identical",
#         "transfer_cost": [18]
#     },
#     # "C2_ENFORCED": {
#     #     "decision_frequency": "ENFORCED",
#     #     "roles": "identical",
#     #     "transfer_cost": [18]
#     # },
#     ##################################################
#
#     # (T<S) => PER_ROUNDS_STRICTLY_BELLOW (IDENTICAL)
#
#     "C3_PER_ROUND": {
#         "decision_frequency": "PER_ROUND",
#         "roles": "identical",
#         "transfer_cost": [8]
#     },
#
#     # "C3_ENFORCED": {
#     #     "decision_frequency": "ENFORCED",
#     #     "roles": "identical",
#     #     "transfer_cost": [8]
#     # },
#
#     ##################################################
#
#     # (T<S) => PER_ROUNDS_STRICTLY_BELLOW (NON- IDENTICAL)
#     "C4_PER_ROUND": {
#         "decision_frequency": "PER_ROUND",
#         "roles": "non-identical",
#         "transfer_cost": [18, 24]
#     },
#
#     # "C4_ENFORCED": {
#     #     "decision_frequency": "ENFORCED",
#     #     "roles": "non-identical",
#     #     "transfer_cost": [18, 24]
#     # },
#     ##################################################
#
#     # (T<S) => PER_ROUNDS_STRICTLY_BELLOW (NON- IDENTICAL)
#     "C5_PER_ROUND": {
#         "decision_frequency": "PER_ROUND",
#         "roles": "non-identical",
#         "transfer_cost": [10, 40]
#     },
#
#     # "C5_ENFORCED": {
#     #     "decision_frequency": "ENFORCED",
#     #     "roles": "non-identical",
#     #     "transfer_cost": [10, 40]
#     # },
#
#     ##################################################
#
#     # (T<S) => PER_ROUNDS_STRICTLY_BELLOW (NON- IDENTICAL)
#
#     "C6_PER_ROUND": {
#         "decision_frequency": "PER_ROUND",
#         "roles": "non-identical",
#         "transfer_cost": [8, 24]
#     },
#
#     # "C6_ENFORCED": {
#     #     "decision_frequency": "ENFORCED",
#     #     "roles": "non-identical",
#     #     "transfer_cost": [8, 24]
#     # },
#     ##################################################
#
# }
