from os import environ
import os
import pandas as pd

EXTENSION_APPS = ['trader_wrapper']
import yaml

with open(r'./data/blocks.yaml') as file:
    blocks = yaml.load(file, Loader=yaml.FullLoader)
with open(r'./data/treatments.yaml') as file:
    treatments = yaml.load(file, Loader=yaml.FullLoader)
num_blocked_treatments = len(blocks) * len(treatments)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TIME_ZONE = 'UTC'
default_app_seq = [
    'pretrade',
    'trader_wrapper',
    'post_experimental'

]
SESSION_CONFIGS = [

    dict(
        name='post',
        display_name="post-experimental (quiz, SES)",
        num_demo_participants=num_blocked_treatments,
        app_sequence=['post_experimental'],

    ),
    dict(
        name='full',
        display_name="FULL STUDY",
        num_demo_participants=num_blocked_treatments,
        app_sequence=default_app_seq,
    ),
    dict(
        name='trader',
        display_name="trader only",
        num_demo_participants=num_blocked_treatments,
        app_sequence=['trader_wrapper', ],
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0,  # exchange rate between real world currency and points
    participation_fee=0.00, doc="",  # participation fee
    training_round_name='Training round',  # name of the training round
    for_prolific=False,  # is the experiment run on Prolific?
    prolific_redirect_url='https://prolific.com/',  # URL to redirect to after the experiment is completed
    prediction_at=30,  # tick number at which the prediction is made
    trading_at=4,  # tick number at which trading starts
    tick_frequency=5,  # number of seconds between ticks
    awards_at='10, 15, 20, 25, 30'  # tick numbers at which awards are given
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'y(8c37tkwqf#m$gg9=z*54k&jojh6ddhlj75j4klo6evkkfwb%'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = [
    'otree',

    'trader_wrapper',
    # 'pretrade',
    'django_countries'
]
COUNTRIES_FIRST = ['US', 'GB']
COUNTRIES_FIRST_BREAK = '-------'
COUNTRIES_FIRST_REPEAT = True

POINTS_DECIMAL_PLACES = 2
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 2
