from django.forms import Form, ModelChoiceField
from .models import Hero


class HeroForm(Form):

    hero = ModelChoiceField(queryset=Hero.objects)
