from os import environ

SESSION_CONFIGS = [
    dict(
        name='Transshipment_Game',
        app_sequence=['introduction', 'transshipment_game', 'post_survey'],
        num_demo_participants=20,
    ),
    dict(
        name='Testing',
        app_sequence=['introduction', 'transshipment_game'],
        num_demo_participants=4,
    ),
]

ROOMS = [
    {
        'name': 'waiting_room',
        'display_name': 'Waiting Room',
        'participant_label_file': '_rooms/exp_labels.txt',  # You can specify a file with participant labels if needed
        'use_secure_urls': True,  # Use secure URLs for participant login
    },
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    treatments={
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
    },
    doc="",
)

PARTICIPANT_FIELDS = ["treatment"]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6733260475510'
