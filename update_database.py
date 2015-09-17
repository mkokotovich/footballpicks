import psycopg2
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse

class Team:
    def __init__(self, name="", wins=0, loses=0, ties=0):
        self.name=name
        self.wins=wins
        self.loses=loses
        self.ties=ties

teams = []

def retreive_standings():
    url = "http://www.usatoday.com/sports/nfl/standings/"
    with urllib.request.urlopen(url) as response:
        html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    # For each division:
    for node in soup.find_all('table'):
        for row in node.find_all('tr'):
            team_name = row.find('th').text.strip()
            cols = row.find_all('td')
            if (len(cols) < 3):
                continue
            wins = int(cols[0].text)
            loses = int(cols[1].text)
            ties = int(cols[2].text)
            teams.append(Team(team_name, wins, loses, ties))

def print_teams():
    for team in teams:
        print("{0} ({1}-{2}-{3})".format(team.name, team.wins, team.loses, team.ties))
        

def update_database():
    DATABASE_URL="postgres://jjzwrulyelxmem:dSFKNdrKhxBupS3eJZPkQuKgJ4@ec2-54-204-20-164.compute-1.amazonaws.com:5432/d8cq541fs49168"

    url = urlparse(DATABASE_URL)

    try:
        conn = psycopg2.connect( database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
        #conn = psycopg2.connect(database="fbpicks", user="postgresusr", password="postgrespwd", host="localhost", port="5432")
    except:
        print("I am unable to connect to database")

    cur = conn.cursor()

    for team in teams:
        query = """UPDATE footballseason_team SET wins = {0}, loses = {1}, ties = {2} WHERE team_name='{3}'""".format(team.wins, team.loses, team.ties, team.name)
        cur.execute(query)
    conn.commit()
    print("Total number of rows updated: {0}".format(cur.rowcount))

def main():
    retreive_standings()
    print_teams()
    update_database()
    print("Success!")
    

if __name__ == "__main__":
    main()
