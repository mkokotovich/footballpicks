# Generated by Django 2.2.5 on 2021-11-04 17:04

from django.db import migrations



def nothing_to_undo(apps, schema_editor):
    # It would be impossible to know which null fields were filled in
    # so we just won't do anything
    pass


_initial_logo_map = {
    "Arizona Cardinals": "Arizona_Cardinals_logo.svg",
    "Atlanta Falcons": "Atlanta_Falcons_logo.svg",
    "Baltimore Ravens": "Baltimore_Ravens_logo.svg",
    "Buffalo Bills": "Buffalo_Bills_logo.svg",
    "Carolina Panthers": "Carolina_Panthers_logo.svg",
    "Los Angeles Chargers": "Chargers_logo.svg",
    "Chicago Bears": "Chicago_Bears_logo.svg",
    "Cincinnati Bengals": "Cincinnati_Bengals_logo.svg",
    "Cleveland Browns": "Cleveland_Browns_logo.svg",
    "Dallas Cowboys": "Dallas_Cowboys.svg",
    "Denver Broncos": "Denver_Broncos_logo.svg",
    "Detroit Lions": "Detroit_Lions_logo.svg",
    "Green Bay Packers": "Green_Bay_Packers_logo.svg",
    "Houston Texans": "Houston_Texans_logo.svg",
    "Indianapolis Colts": "Indianapolis_Colts_logo.svg",
    "Kansas City Chiefs": "Kansas_City_Chiefs_logo.svg",
    "Las Vegas Raiders": "Las_Vegas_Raiders_logo.svg",
    "Miami Dolphins": "Miami_Dolphins_logo.svg",
    "New England Patriots": "New_England_Patriots_logo.svg",
    "New Orleans Saints": "New_Orleans_Saints_logo.svg",
    "New York Giants": "New_York_Giants_logo.svg",
    "New York Jets": "New_York_Jets_logo.svg",
    "Philadelphia Eagles": "Philadelphia_Eagles_logo.svg",
    "Pittsburgh Steelers": "Pittsburgh_Steelers_logo.svg",
    "Los Angeles Rams": "Rams_logo.svg",
    "San Francisco 49ers": "San_Francisco_49ers_logo.svg",
    "Seattle Seahawks": "Seattle_Seahawks_logo.svg",
    "Tampa Bay Buccaneers": "Tampa_Bay_Buccaneers_logo.svg",
    "Tennessee Titans": "Tennessee_Titans_logo.svg",
    "Washington Football Team": "Washington_football_team_wlogo.svg",
    "Jacksonville Jaguars": "jacksonville-jaguars-logo.svg",
    "Minnesota Vikings": "minnesota-vikings-logo.svg",
}

def fill_logos_for_all_teams(apps, schema_editor):
    Team = apps.get_model("footballseason", "Team")
    for team in Team.objects.all():
        logo = _initial_logo_map.get(team.team_name)
        team.logo_name = logo
        team.save()


class Migration(migrations.Migration):

    dependencies = [
        ('footballseason', '0010_team_logo_name'),
    ]

    operations = [
        migrations.RunPython(fill_logos_for_all_teams, reverse_code=nothing_to_undo),
    ]