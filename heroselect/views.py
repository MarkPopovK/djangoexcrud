from django.shortcuts import render, get_object_or_404
from django.views.generic import View, FormView
from django.utils.datastructures import MultiValueDictKeyError
from django.http import Http404
from django.urls import reverse_lazy
from .forms import HeroForm
from .models import Hero
from .prediction_api import predict
from .leaguedota_api import fetch_live_games

if_true = lambda thing: thing if bool(thing) else None


class Heroview(View):

    def get(self, request):
        games = fetch_live_games(spectators=10, max_amount=4)
        forms = [HeroForm(if_true(request.GET), prefix=f'r{n}') for n in range(1, 6)] + \
                [HeroForm(if_true(request.GET), prefix=f'd{n}') for n in range(1, 6)]
        data = {}

        for game in games:
            if game['heroes_picked'] == 10:
                getgameurl = '?' + '&'.join(
                    [f'r{n}-hero={hero}' for n, hero in enumerate(game['r_picks'], 1)] + \
                    [f'd{n}-hero={hero}' for n, hero in enumerate(game['d_picks'], 1)])
                game['gameurl'] = reverse_lazy('heroselect') + getgameurl

        if request.GET:
            try:
                radiant_team = [int(request.GET[f'r{n}-hero']) for n in range(1, 6)]
                dire_team = [int(request.GET[f'd{n}-hero']) for n in range(1, 6)]
                together = radiant_team + dire_team
                if len(set(together)) < 10:
                    for each in together:
                        hero = get_object_or_404(Hero, pk=each)
                        if together.count(each) > 1:
                            raise Http404("Need 10 UNIQUE heroes, repeated: " + hero.name)

            except MultiValueDictKeyError as e:
                raise Http404("Need all 10 heroes")
            except ValueError as e:
                raise Http404("Hero IDs have to be numbers")

            else:
                p = predict(radiant=radiant_team, dire=dire_team)
                data['prediction'] = p
                print(p)
                # do stuff on valid forms entry
                pass
        data['forms'] = forms
        data['games'] = games

        return render(request, 'heroselect/home.html', context=data)

# <QueryDict: {'r1-hero': ['4'], 'r2-hero': ['8'], 'r3-hero': ['4'], 'r4-hero': ['13'],
# 'r5-hero': ['2'], 'd1-hero': ['1'], 'd2-hero': ['4'], 'd3-hero': ['7'], 'd4-hero': ['111'], 'd5-hero': ['119']}>
