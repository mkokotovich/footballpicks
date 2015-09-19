import datetime
import csv
import calendar
import psycopg2
from urllib.parse import urlparse

filename="nfl-2015-schedule.csv"

teams = [
    "Steelers",
    "Patriots",
    "Packers",
    "Bears",
    "Chiefs",
    "Texans",
    "Browns",
    "Jets",
    "Colts",
    "Bills",
    "Dolphins",
    "Redskins",
    "Panthers",
    "Jaguars",
    "Seahawks",
    "Rams",
    "Saints",
    "Cardinals",
    "Lions",
    "Chargers",
    "Titans",
    "Buccaneers",
    "Bengals",
    "Raiders",
    "Ravens",
    "Broncos",
    "Giants",
    "Cowboys",
    "Eagles",
    "Falcons",
    "Vikings",
    "49ers"
];


class Game:
    def __init__(self, week, awayteam, hometeam, gametime):
        self.week = week
        self.awayteam = awayteam
        self.hometeam = hometeam
        self.gametime = gametime

    def __str__(self):
        return "wk %d: %s at %s, %s" % (self.week, self.awayteam, self.hometeam, self.gametime.strftime("%b %d, %I:%M %p"))

games = []
team_id_dict = {}

def read_game_info():
    f = open(filename,'rt')
    reader = csv.reader(f)

    #Skip first line
    next(reader)

    for row in reader:
        week = int(row[2].split()[1])
        awayteam = row[0]
        hometeam = row[1].split('@')[1]
        month_str = row[4].split()[0]
        month = list(calendar.month_abbr).index(month_str[:3])
        day = int(row[4].split()[1][:2])
        if (month == 1):
            year = 2016
        else:
            year = 2015
        hour=int(row[5].split(':')[0])-1
        if (row[5].split()[1] == "PM"):
            hour += 12
        minute=int(row[5].split(':')[1].split()[0])
        gametime = datetime.datetime(year, month, day, hour, minute)

        games.append(Game(week, awayteam, hometeam, gametime))

# Run heroku config -s to get production DATABASE_URL
DATABASE_URL=""
#DATABASE_URL="postgres://postgresusr:postgrespwd@localhost:5432/fbpicks"

def build_team_ids():
    url = urlparse(DATABASE_URL)

    try:
        conn = psycopg2.connect( database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
        #conn = psycopg2.connect(database="fbpicks", user="postgresusr", password="postgrespwd", host="localhost", port="5432")
    except:
        print("I am unable to connect to database")

    cur = conn.cursor()

    for team in teams:
        query = """SELECT id FROM footballseason_team WHERE team_name LIKE '%{0}' ;""".format(team)
        cur.execute(query)
        rows = cur.fetchall()
        team_id_dict[team] = rows[0][0]

def update_database():
    url = urlparse(DATABASE_URL)

    try:
        conn = psycopg2.connect( database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
        #conn = psycopg2.connect(database="fbpicks", user="postgresusr", password="postgrespwd", host="localhost", port="5432")
    except:
        print("I am unable to connect to database")

    cur = conn.cursor()

    for game in games:
        #skip the first two weeks
        if (game.week < 3):
            continue

        query = """INSERT INTO footballseason_game (week, home_team_id, away_team_id, game_time) VALUES ('{0}', '{1}', '{2}', '{3}');""".format(game.week, team_id_dict[game.hometeam], team_id_dict[game.awayteam], game.gametime)
        print(query)
        cur.execute(query)

    conn.commit()
    print("Total number of rows updated: {0}".format(cur.rowcount))

def main():
    read_game_info()
    build_team_ids()
    update_database()
    print("Success!")

if __name__ == "__main__":
    main()


