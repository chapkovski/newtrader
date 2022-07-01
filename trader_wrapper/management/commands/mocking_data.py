from django.core.management.base import BaseCommand
import logging
from trader_wrapper.models import Event, Constants, AttrDict, UpdSession
from trader_wrapper.utils import creating_events
from dateparser import parse
from dateutil.relativedelta import relativedelta
import random
from otree.session import create_session
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('treatment', help='specific treatment name', type=str)
        parser.add_argument('num_participants', help='How many users to create', type=int)

    def handle(self,  treatment, num_participants, *args, **options):
        logger.info(f'Gonna generate a mocked data for trading platform')
        s = create_session(
            session_config_name=treatment,
            num_participants=num_participants,
        )
        creating_events(s)
        u = UpdSession(code=s.code)
        print(u.export_data())

