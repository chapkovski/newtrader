from os import environ
import os
import pandas as pd
EXTENSION_APPS=['trader_wrapper']

# def get_game_params(url):
#     df = pd.read_csv(url)
#     game_params = {i.get('parameter'): i.get('value') for i in df.to_dict('records')}
#     return game_params
#
# def get_round_params(url):
#     df = pd.read_csv(url)
#
#     game_params = {i.get('round_number'): { 'crash_probability':i.get('crash_probability'), 'training': i.get('training')==1, 'tick_frequency':i.get('tick_frequency')} for i in df.to_dict('records')}
#     return game_params
#
# DEFAULT_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8DDDK8eY0eWTwnz8iJSLFheO9_Ah5e16H48cwSJw4vRLWa5bbDaxm91LCF75_Lt7IPi4KmLqftcS2/pub?gid=0&single=true&output=csv"
# DEFAULT_ROUND_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8DDDK8eY0eWTwnz8iJSLFheO9_Ah5e16H48cwSJw4vRLWa5bbDaxm91LCF75_Lt7IPi4KmLqftcS2/pub?gid=607283197&single=true&output=csv"
# URL_TO_READ = environ.get('URL_TO_READ', DEFAULT_URL)
# ROUND_URL_TO_READ = environ.get('ROUND_URL_TO_READ', DEFAULT_ROUND_URL)
# GAME_PARAMS = get_game_params(URL_TO_READ)
# ROUND_GAME_PARAMS = get_round_params(ROUND_URL_TO_READ)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TIME_ZONE = 'UTC'
default_app_seq = [
    'pretrade',
    'trader_wrapper',
    'post_experimental'

]
SESSION_CONFIGS = [

    dict(
        name='traderonlhy',
        display_name="trader ONLY - within-subject",
        num_demo_participants=2,
        app_sequence=['trader_wrapper'],
        gamified=True,
    ),

    dict(
        name='post',
        display_name="post-experimental (quiz, SES)",
        num_demo_participants=2,
        app_sequence=['post_experimental'],

    ),
    dict(
        name='full_baseline',
        display_name="FULL STUDY - within-subject",
        num_demo_participants=2,
        app_sequence=default_app_seq,
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0,
    participation_fee=0.00, doc="",
    for_prolific=False,
    prolific_redirect_url='http://www.lenta.ru',
    prediction_at=10,
    trading_at=6,
    tick_frequency=6,
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
