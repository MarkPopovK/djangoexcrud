import dota2api
from heroselect.credentials import d2apikey
from operator import itemgetter
import time

api = dota2api.Initialise(d2apikey)

_t = 0
last_games = []


def fetch_live_games(spectators=10, max_amount=6):
    global last_games, _t
    if (time.time() - _t) < 30:  # handmade cache, updates on request but not more often that once per 30 sec
        return last_games
    _t = time.time()
    print('fetching live games')

    try:
        live_games = api.get_live_league_games()['games']
    except Exception as e:
        print(e)
        return []

    if spectators:
        live_games = [game for game in live_games if game.get('spectators', 0) >= spectators]
    live_games = sorted(live_games, reverse=True, key=itemgetter('spectators'))
    games = []
    for game in live_games:
        if 'scoreboard' in game:
            sboard = game['scoreboard']
        else:
            continue

        duration = round(sboard['duration']/60)
        r_name = game['radiant_team']['team_name'] if 'radiant_team' in game else 'noname'
        d_name = game['dire_team']['team_name'] if 'dire_team' in game else 'noname'
        r_picks = [pick['hero_id'] for pick in sboard['radiant']['picks']] if 'picks' in sboard['radiant'] else []
        d_picks = [pick['hero_id'] for pick in sboard['dire']['picks']] if 'picks' in sboard['dire'] else []
        games.append({
            'r_name': r_name,
            'd_name': d_name,
            'r_picks': r_picks,
            'd_picks': d_picks,
            'duration': duration,
            'spectators': game.get('spectators', 0),
            'heroes_picked': len(r_picks + d_picks),
        })
    last_games = games[:max_amount]
    return games[:max_amount]


if __name__ == '__main__':
    g = fetch_ongoing_games()
    print(g)
