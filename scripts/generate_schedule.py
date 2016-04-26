# From: http://espn.go.com/nfl/schedule

from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request

season = 2016
week_list = range(0,18)

def get_games_from_one_week(season, week):
    url = "http://espn.go.com/nfl/schedule/_/year/{0}/week/{1}".format(season, week)
    print("url: {0}".format(url))
    with urllib.request.urlopen(url) as response:
        html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    for table in soup.findAll("table", class_="schedule"):
        for row in table.find_all('tr', {"class": "odd"}, {"class": "even"}):
            # Each row is one game
            game_time_data = row.find('td', { "data-behavior":"date_time" } )
            if game_time_data == None:
                # bye teams
                continue
            game_time = game_time_data['data-date']
            #  2016-12-16T01:25Z
            game_datetime = datetime.strptime(game_time, "%Y-%m-%dT%H:%MZ")
            teams = []
            for team_link in row.find_all('a', class_="team-name"):
                for team_parent in team_link.find_all('span'):
                    team_name = team_parent.contents[0]
                    teams.append(team_name)
            print("{0} at {1}, gametime: {2}".format(teams[0], teams[1], game_datetime.__str__()))

def main():
    for week in week_list:
        print("Fetching week {0}".format(week))
        get_games_from_one_week(season, week)

if __name__ == "__main__":
    main()

def update():
    url = "http://espn.go.com/nfl/schedulegrid"
    with urllib.request.urlopen(url) as response:
        html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    failure = 0
    successful_updates = 0
    
    # For each division:
    for table in soup.findAll("table", { "class" : "schedule" }):
        for row in table.find_all('tr'):
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
