from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request

from footballseason.models import Game, Team, Pick, Record

#Call from CLI via: $ python manage.py shell < scripts/update_records.py

def get_last_game_for_team(team):
    games = Game.objects.filter(Q(game_time__lte=timezone.now()) & Q(Q(home_team=team) | Q(away_team=team))).order_by('-game_time')
    if (len(games) == 0):
        print("Error: unable to find last game for team {0}".format(team))
        return None
    last_game = games[0]
    return last_game

def update_records(team):
    try:
        last_game = get_last_game_for_team(team)
        last_game_week = last_game.week
    except:
        # Error
        print("Error: Unable to find game to update records. Team: {0}".format(team))
        return 0
    
    winning_picks = last_game.pick_set.filter(team_to_win=team)
    for pick in winning_picks:
        try:
            record = Record.objects.get(user_name=pick.user_name, season=2015, week=last_game_week)
        except:
            record = Record(user_name=pick.user_name, season=2015, week=last_game_week, wins=0);
        record.wins += 1
        record.save()

def update():
    url = "http://www.usatoday.com/sports/nfl/standings/"
    with urllib.request.urlopen(url) as response:
        html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    failure = 0
    successful_updates = 0
    
    # For each division:
    for node in soup.find_all('table'):
        for row in node.find_all('tr'):
            teamname = row.find('th').text.strip()
            cols = row.find_all('td')
            if (len(cols) < 3):
                continue
            wins = int(cols[0].text)
            loses = int(cols[1].text)
            ties = int(cols[2].text)
            try:
                team = Team.objects.get(team_name=teamname)
                # An existing team was found, update standings
                if (team.wins != wins or team.loses != loses or team.ties != ties):
                    successful_updates += 1
                 
                if (team.wins < wins):
                    # This team won, update records. Assuming we update at least once a week
                    update_records(team)
                team.wins=wins
                team.loses=loses
                team.ties=ties
                team.save()
            except ObjectDoesNotExist:
                # Could not find team, this shouldn't happen
                errormsg = "Could not find team {0}, could not update standings".format(teamname)
                print(errormsg)
                failure=1
    
    if (failure == 0):
        if (successful_updates > 0):
            infomsg = "Successfully updated standings for {0} teams".format(successful_updates)
        else:
            infomsg = "No updates available"
        print(infomsg)

def main():
    #Since we're charged by the second, we want to only call update when
    # we expect there to be changes. During games, after games, etc
    today = datetime.today().weekday()
    hour = datetime.today().hour
    #if today is Wednesday or Saturday (the two days of the week that
    #there are no games and no games the previous day) then skip the update
    if (today == 2 or today == 5):
        print("Skipping update, today is Wednesday or Saturday")
        return
    #We'll give the website until 8am to update on Tuesday and Friday
    if ((today == 1 or today == 4) and hour > 8):
        print("Skipping update, it is after 8 on Tue or Fri")
        return
    #Mondays we won't check between 8am and 8pm
    if (today == 0 and hour > 8 and hour < 20):
        print("Skipping update, it is between 8 and 8 on Monday")
        return
    #Thursdays we won't check before 8pm
    if (today == 3 and hour < 20):
        print("Skipping update, it is before 8 on Thursday")
        return
    # Otherwise we'll update
    update()

main()
