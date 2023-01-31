from os import environ
import os
import pandas as pd
EXTENSION_APPS=['trader_wrapper']
import yaml
with open(r'./data/params.yaml') as file:
    blocks = yaml.load(file, Loader=yaml.FullLoader)

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
        num_demo_participants=2,
        app_sequence=['post_experimental'],

    ),
    dict(
        name='full',
        display_name="FULL STUDY",
        num_demo_participants=len(blocks),
        app_sequence=default_app_seq,
    ),
    dict(
        name='trader',
        display_name="trader only",
        num_demo_participants=len(blocks),
        app_sequence=[ 'trader_wrapper',],
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
    prediction_at=30,
    trading_at=4,
    tick_frequency=5,
    awards_at='10,25,35,45,60'
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
