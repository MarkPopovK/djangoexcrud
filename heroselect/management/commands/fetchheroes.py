from django.core.management.base import BaseCommand, CommandError
from heroselect.models import Hero
import requests, json


class Command(BaseCommand):
    help = 'Fetches new heroes to the DB'

    def handle(self, *args, **options):
        heroes_json = json.loads(requests.get('https://api.opendota.com/api/heroes').text)
        for hero in heroes_json:
            h = Hero(id=hero['id'], name=hero['localized_name'])
            h.save()
        print(Hero.objects.all())