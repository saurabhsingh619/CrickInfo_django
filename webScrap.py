import requests
from bs4 import BeautifulSoup
import sqlite3
import sys



conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

def getTeamList():
    page = requests.get("https://www.cricbuzz.com/")
    soup = BeautifulSoup(page.content, 'lxml')
    teamsList = []
    titlesList = []
    idList = []
    teams = soup.find('div', id = 'teamDropDown')
    teams = teams.nav.div.div
    teams = teams.find_all('a')
    print(teams)
    c.execute("CREATE TABLE IF NOT EXISTS crickinfo_teams (id integer UNIQUE PRIMARY KEY,name varchar UNIQUE,title varchar UNIQUE);")
    for i in range(12):
        team = teams[i].text
        teamsList.append(team)
        title = teams[i]['title']
        titlesList.append(title)
        ID = teams[i]['href'].split('/')[3]
        idList.append(ID)
    for i in range(12):
        try:
            c.execute("INSERT INTO crickinfo_teams (id , name, title) VALUES(?, ?, ?)", (idList[i], teamsList[i], titlesList[i]))
        except:
            print("Teams are already in table")
            return False

def getIplSchedules():
    c.execute("CREATE TABLE IF NOT EXISTS crickinfo_iplschedules (id integer primary key autoincrement, matchTitle varchar, matchVenue varchar, matchDate varchar);")
    page = requests.get("https://www.cricbuzz.com/cricket-series/3130/indian-premier-league-2020/matches")
    soup = BeautifulSoup(page.content, 'lxml')
    matchDetail = soup.find_all('div', class_='cb-series-matches')
    matchLinkList = []
    for i in range(len(matchDetail)):
        matchLink = "https://www.cricbuzz.com/"+str(matchDetail[i].a['href'])
        matchLinkList.append(matchLink)
    for i in range(len(matchLinkList)):
        page2 = requests.get(matchLinkList[i])
        soup2 = BeautifulSoup(page2.content, 'lxml')
        matchDetail = soup2.find('div', id = 'matchCenter')
        matchDetail = matchDetail.find('div', class_='cb-nav-main cb-col-100 cb-col cb-bg-white')
        matchTitle = matchDetail.h1.text.split("-")[0]
        matchDetail = matchDetail.find('div', class_='cb-nav-subhdr cb-font-12')
        matchSeries = matchDetail.a.span.text
        matchVenue = matchDetail.find('a', {"itemprop":"location"})['title']
        matchDate = matchDetail.find('span',{"itemprop":"startDate"}).text
        c.execute("INSERT INTO crickinfo_iplschedules (matchTitle, matchVenue, matchDate) VALUES(?,?,?)",(matchTitle, matchVenue, matchDate))

def getTeamSchedules(teamId):
    try:
        entryCount = c.execute("SELECT COUNT(*) FROM crickinfo_iplschedules")
    except:
        entryCount = 0
    if entryCount != 0:
        print("IPL schedules are already in table")
        return False
    c.execute("CREATE TABLE IF NOT EXISTS crickinfo_schedules (id integer primary key autoincrement, teamId integer,matchTitle varchar, matchVenue varchar, matchDate varchar);")
    teamName = c.execute("SELECT name FROM crickinfo_teams where id='"+str(teamId)+"'").fetchone()[0]
    teamName = teamName.lower()
    linkStr = "https://www.cricbuzz.com/cricket-team/"+str(teamName)+"/"+str(teamId)+"/schedule"
    page = requests.get(linkStr)
    soup = BeautifulSoup(page.content, 'lxml')
    matchDetail = soup.find_all('div', class_='cb-series-matches')
    matchLinkList = []
    for i in range(len(matchDetail)):
        matchLink = "https://www.cricbuzz.com/"+str(matchDetail[i].a['href'])
        matchLinkList.append(matchLink)
    for i in range(len(matchLinkList)):
        page2 = requests.get(matchLinkList[i])
        soup2 = BeautifulSoup(page2.content, 'lxml')
        matchDetail = soup2.find('div', id = 'matchCenter')
        matchDetail = matchDetail.find('div', class_='cb-nav-main cb-col-100 cb-col cb-bg-white')
        matchTitle = matchDetail.h1.text.split("-")[0]
        # print("\ntitle\n\n",matchTitle)
        # print("\n\nmatch\n\n\n",matchDetail.div)
        matchDetail = matchDetail.find('div', class_='cb-nav-subhdr cb-font-12')
        matchSeries = matchDetail.a.span.text
        matchVenue = matchDetail.find('a', {"itemprop":"location"})['title']
        matchDate = matchDetail.find('span',{"itemprop":"startDate"}).text
        c.execute("INSERT INTO crickinfo_schedules (teamId, matchTitle, matchVenue, matchDate) VALUES(?,?,?,?)",(teamId, matchTitle, matchVenue, matchDate))


def getAllTeamSchedules():
    try:
        entryCount = c.execute("SELECT COUNT(*) FROM crickinfo_schedules")
    except:
        entryCount = 0
    if entryCount != 0:
        print("Schedules are already in table")
        return False
    allTeamIds = c.execute("select id from crickinfo_teams").fetchall()
    for i in range(len(allTeamIds)):
        teamId = str(allTeamIds[i])[1:-2]
        getTeamSchedules(int(teamId))


def refreshDatabase():
    try:
        c.execute("DROP TABLE if exists crickinfo_schedules;")
        c.execute("DROP TABLE if exists crickinfo_teams;")
        c.execute("DROP TABLE if exists crickinfo_iplschedules;")
        c.execute("DROP TABLE if exists crickinfo_odiBatRank;")
        c.execute("DROP TABLE if exists crickinfo_odiBowlRank;")
        c.execute("DROP TABLE if exists crickinfo_odiallRank;")
        c.execute("DROP TABLE if exists crickinfo_teamOdiRank;")
        c.execute("DROP TABLE if exists crickinfo_teamTestRank;")
        c.execute("DROP TABLE if exists crickinfo_teamTtwentyRank;")
        c.execute("DROP TABLE if exists crickinfo_testBatRank;")
        c.execute("DROP TABLE if exists crickinfo_testBowlRank;")
        c.execute("DROP TABLE if exists crickinfo_testallRank;")
        c.execute("DROP TABLE if exists crickinfo_ttwentyBatRank;")
        c.execute("DROP TABLE if exists crickinfo_ttwentyBowlRank;")
        c.execute("DROP TABLE if exists crickinfo_ttwentyallRank;")
    except:
        print("Database refresh error!\nAlready refreshed")
    getTeamList()
    getAllTeamSchedules()
    getIplSchedules()
    getOdiBattingRanking()
    getTestBattingRanking()
    getTtwentyBattingRanking()
    getOdiBowlingRanking()
    getTestBowlingRanking()
    getTtwentyBowlingRanking()
    getOdiAllRanking()
    getTestAllRanking()
    getTtwentyAllRanking()
    getTeamsOdiRanking()
    getTeamsTestRanking()
    getTeamsTtwentyRanking()


def getOdiBattingRanking():
    c.execute("CREATE TABLE IF NOT EXISTS crickinfo_odiBatRank (id integer primary key autoincrement,rank integer unique, player varchar, playerCountry varchar, playerRatings varchar);")
    page = requests.get("https://www.cricbuzz.com/cricket-stats/icc-rankings/men/batting")
    soup = BeautifulSoup(page.content, 'lxml')
    rankDetail = soup.find('div',{"ng-show":"'batsmen-odis' == act_rank_format"})
    rankDetail = rankDetail.find_all('div', class_='cb-col cb-col-100 cb-font-14 cb-lst-itm text-center')
    for i in range(len(rankDetail)):
        rank = rankDetail[i].div.text
        player = rankDetail[i].find('a', class_='text-hvr-underline text-bold cb-font-16').text
        playerCountry = rankDetail[i].find('div', class_='cb-font-12 text-gray').text
        playerRatings = rankDetail[i].find('div', class_='cb-col cb-col-17 cb-rank-tbl pull-right').text
        c.execute("INSERT INTO crickinfo_odiBatRank (rank, player, playerCountry, playerRatings) VALUES(?,?,?,?)",(rank, player, playerCountry, playerRatings))

def getTestBattingRanking():
    c.execute("CREATE TABLE IF NOT EXISTS crickinfo_testBatRank (id integer primary key autoincrement,rank integer unique, player varchar, playerCountry varchar, playerRatings varchar);") 
    page = requests.get("https://www.cricbuzz.com/cricket-stats/icc-rankings/men/batting")
    soup = BeautifulSoup(page.content, 'lxml')
    rankDetail = soup.find('div',{"ng-show":"'batsmen-tests' == act_rank_format"})
    rankDetail = rankDetail.find_all('div', class_='cb-col cb-col-100 cb-font-14 cb-lst-itm text-center')
    for i in range(len(rankDetail)):
        rank = rankDetail[i].div.text
        player = rankDetail[i].find('a', class_='text-hvr-underline text-bold cb-font-16').text
        playerCountry = rankDetail[i].find('div', class_='cb-font-12 text-gray').text
        playerRatings = rankDetail[i].find('div', class_='cb-col cb-col-17 cb-rank-tbl pull-right').text
        c.execute("INSERT INTO crickinfo_testBatRank (rank, player, playerCountry, playerRatings) VALUES(?,?,?,?)",(rank, player, playerCountry, playerRatings))

def getTtwentyBattingRanking():
    c.execute("CREATE TABLE IF NOT EXISTS crickinfo_ttwentyBatRank (id integer primary key autoincrement,rank integer unique, player varchar, playerCountry varchar, playerRatings varchar);") 
    page = requests.get("https://www.cricbuzz.com/cricket-stats/icc-rankings/men/batting")
    soup = BeautifulSoup(page.content, 'lxml')
    rankDetail = soup.find('div',{"ng-show":"'batsmen-t20s' == act_rank_format"})
    rankDetail = rankDetail.find_all('div', class_='cb-col cb-col-100 cb-font-14 cb-lst-itm text-center')
    for i in range(len(rankDetail)):
        rank = rankDetail[i].div.text
        player = rankDetail[i].find('a', class_='text-hvr-underline text-bold cb-font-16').text
        playerCountry = rankDetail[i].find('div', class_='cb-font-12 text-gray').text
        playerRatings = rankDetail[i].find('div', class_='cb-col cb-col-17 cb-rank-tbl pull-right').text
        c.execute("INSERT INTO crickinfo_ttwentyBatRank (rank, player, playerCountry, playerRatings) VALUES(?,?,?,?)",(rank, player, playerCountry, playerRatings))

def getOdiBowlingRanking():
    c.execute("CREATE TABLE IF NOT EXISTS crickinfo_odiBowlRank (id integer primary key autoincrement,rank integer unique, player varchar, playerCountry varchar, playerRatings varchar);")
    page = requests.get("https://www.cricbuzz.com/cricket-stats/icc-rankings/men/bowling")
    soup = BeautifulSoup(page.content, 'lxml')
    rankDetail = soup.find('div',{"ng-show":"'bowlers-odis' == act_rank_format"})
    rankDetail = rankDetail.find_all('div', class_='cb-col cb-col-100 cb-font-14 cb-lst-itm text-center')
    for i in range(len(rankDetail)):
        rank = rankDetail[i].div.text
        player = rankDetail[i].find('a', class_='text-hvr-underline text-bold cb-font-16').text
        playerCountry = rankDetail[i].find('div', class_='cb-font-12 text-gray').text
        playerRatings = rankDetail[i].find('div', class_='cb-col cb-col-17 cb-rank-tbl pull-right').text
        c.execute("INSERT INTO crickinfo_odiBowlRank (rank, player, playerCountry, playerRatings) VALUES(?,?,?,?)",(rank, player, playerCountry, playerRatings))

def getTestBowlingRanking():
    c.execute("CREATE TABLE IF NOT EXISTS crickinfo_testBowlRank (id integer primary key autoincrement,rank integer unique, player varchar, playerCountry varchar, playerRatings varchar);")
    page = requests.get("https://www.cricbuzz.com/cricket-stats/icc-rankings/men/bowling")
    soup = BeautifulSoup(page.content, 'lxml')
    rankDetail = soup.find('div',{"ng-show":"'bowlers-tests' == act_rank_format"})
    rankDetail = rankDetail.find_all('div', class_='cb-col cb-col-100 cb-font-14 cb-lst-itm text-center')
    for i in range(len(rankDetail)):
        rank = rankDetail[i].div.text
        player = rankDetail[i].find('a', class_='text-hvr-underline text-bold cb-font-16').text
        playerCountry = rankDetail[i].find('div', class_='cb-font-12 text-gray').text
        playerRatings = rankDetail[i].find('div', class_='cb-col cb-col-17 cb-rank-tbl pull-right').text
        c.execute("INSERT INTO crickinfo_testBowlRank (rank, player, playerCountry, playerRatings) VALUES(?,?,?,?)",(rank, player, playerCountry, playerRatings))

def getTtwentyBowlingRanking():
    c.execute("CREATE TABLE IF NOT EXISTS crickinfo_ttwentyBowlRank (id integer primary key autoincrement,rank integer unique, player varchar, playerCountry varchar, playerRatings varchar);")
    page = requests.get("https://www.cricbuzz.com/cricket-stats/icc-rankings/men/bowling")
    soup = BeautifulSoup(page.content, 'lxml')
    rankDetail = soup.find('div',{"ng-show":"'bowlers-t20s' == act_rank_format"})
    rankDetail = rankDetail.find_all('div', class_='cb-col cb-col-100 cb-font-14 cb-lst-itm text-center')
    for i in range(len(rankDetail)):
        rank = rankDetail[i].div.text
        player = rankDetail[i].find('a', class_='text-hvr-underline text-bold cb-font-16').text
        playerCountry = rankDetail[i].find('div', class_='cb-font-12 text-gray').text
        playerRatings = rankDetail[i].find('div', class_='cb-col cb-col-17 cb-rank-tbl pull-right').text
        c.execute("INSERT INTO crickinfo_ttwentyBowlRank (rank, player, playerCountry, playerRatings) VALUES(?,?,?,?)",(rank, player, playerCountry, playerRatings))

def getOdiAllRanking():
    c.execute("CREATE TABLE IF NOT EXISTS crickinfo_odiallRank (id integer primary key autoincrement,rank integer unique, player varchar, playerCountry varchar, playerRatings varchar);")
    page = requests.get("https://www.cricbuzz.com/cricket-stats/icc-rankings/men/all-rounder")
    soup = BeautifulSoup(page.content, 'lxml')
    rankDetail = soup.find('div',{"ng-show":"'allrounders-odis' == act_rank_format"})
    rankDetail = rankDetail.find_all('div', class_='cb-col cb-col-100 cb-font-14 cb-lst-itm text-center')
    for i in range(len(rankDetail)):
        rank = rankDetail[i].div.text
        player = rankDetail[i].find('a', class_='text-hvr-underline text-bold cb-font-16').text
        playerCountry = rankDetail[i].find('div', class_='cb-font-12 text-gray').text
        playerRatings = rankDetail[i].find('div', class_='cb-col cb-col-17 cb-rank-tbl pull-right').text
        c.execute("INSERT INTO crickinfo_odiallRank (rank, player, playerCountry, playerRatings) VALUES(?,?,?,?)",(rank, player, playerCountry, playerRatings))

def getTestAllRanking():
    c.execute("CREATE TABLE IF NOT EXISTS crickinfo_testallRank (id integer primary key autoincrement,rank integer unique, player varchar, playerCountry varchar, playerRatings varchar);")
    page = requests.get("https://www.cricbuzz.com/cricket-stats/icc-rankings/men/all-rounder")
    soup = BeautifulSoup(page.content, 'lxml')
    rankDetail = soup.find('div',{"ng-show":"'allrounders-tests' == act_rank_format"})
    rankDetail = rankDetail.find_all('div', class_='cb-col cb-col-100 cb-font-14 cb-lst-itm text-center')
    for i in range(len(rankDetail)):
        rank = rankDetail[i].div.text
        player = rankDetail[i].find('a', class_='text-hvr-underline text-bold cb-font-16').text
        playerCountry = rankDetail[i].find('div', class_='cb-font-12 text-gray').text
        playerRatings = rankDetail[i].find('div', class_='cb-col cb-col-17 cb-rank-tbl pull-right').text
        c.execute("INSERT INTO crickinfo_testallRank (rank, player, playerCountry, playerRatings) VALUES(?,?,?,?)",(rank, player, playerCountry, playerRatings))

def getTtwentyAllRanking():
    c.execute("CREATE TABLE IF NOT EXISTS crickinfo_ttwentyallRank (id integer primary key autoincrement,rank integer unique, player varchar, playerCountry varchar, playerRatings varchar);")
    page = requests.get("https://www.cricbuzz.com/cricket-stats/icc-rankings/men/all-rounder")
    soup = BeautifulSoup(page.content, 'lxml')
    rankDetail = soup.find('div',{"ng-show":"'allrounders-t20s' == act_rank_format"})
    rankDetail = rankDetail.find_all('div', class_='cb-col cb-col-100 cb-font-14 cb-lst-itm text-center')
    for i in range(len(rankDetail)):
        rank = rankDetail[i].div.text
        player = rankDetail[i].find('a', class_='text-hvr-underline text-bold cb-font-16').text
        playerCountry = rankDetail[i].find('div', class_='cb-font-12 text-gray').text
        playerRatings = rankDetail[i].find('div', class_='cb-col cb-col-17 cb-rank-tbl pull-right').text
        c.execute("INSERT INTO crickinfo_ttwentyallRank (rank, player, playerCountry, playerRatings) VALUES(?,?,?,?)",(rank, player, playerCountry, playerRatings))

def getTeamsOdiRanking():
    c.execute("CREATE TABLE IF NOT EXISTS crickinfo_teamOdiRank (id integer primary key autoincrement,rank integer unique, team varchar, rating varchar, points varchar);")
    page = requests.get("https://www.cricbuzz.com/cricket-stats/icc-rankings/men/teams")
    soup = BeautifulSoup(page.content, 'lxml')
    rankDetail = soup.find('div',{"ng-show":"'teams-odis' == act_rank_format"})
    rankDetail = rankDetail.find_all('div', class_='cb-col cb-col-100 cb-font-14 cb-brdr-thin-btm text-center')
    ratingPoints = rankDetail[0].find_all('div', class_='cb-col cb-col-14 cb-lst-itm-sm')
    rating = ratingPoints[0].text
    points = ratingPoints[1].text
    for i in range(len(rankDetail)):
        rank = rankDetail[i].div.text
        team = rankDetail[i].find('div', class_='cb-col cb-col-50 cb-lst-itm-sm text-left').text
        ratingPoints = rankDetail[i].find_all('div', class_='cb-col cb-col-14 cb-lst-itm-sm')
        rating = ratingPoints[0].text
        points = ratingPoints[1].text
        c.execute("INSERT INTO crickinfo_teamOdiRank (rank, team, rating, points) VALUES(?,?,?,?)",(rank, team, rating, points))

def getTeamsTestRanking():
    c.execute("CREATE TABLE IF NOT EXISTS crickinfo_teamTestRank (id integer primary key autoincrement,rank integer unique, team varchar, rating varchar, points varchar);")
    page = requests.get("https://www.cricbuzz.com/cricket-stats/icc-rankings/men/teams")
    soup = BeautifulSoup(page.content, 'lxml')
    rankDetail = soup.find('div',{"ng-show":"'teams-tests' == act_rank_format"})
    rankDetail = rankDetail.find_all('div', class_='cb-col cb-col-100 cb-font-14 cb-brdr-thin-btm text-center')
    ratingPoints = rankDetail[0].find_all('div', class_='cb-col cb-col-14 cb-lst-itm-sm')
    rating = ratingPoints[0].text
    points = ratingPoints[1].text
    for i in range(len(rankDetail)):
        rank = rankDetail[i].div.text
        team = rankDetail[i].find('div', class_='cb-col cb-col-50 cb-lst-itm-sm text-left').text
        ratingPoints = rankDetail[i].find_all('div', class_='cb-col cb-col-14 cb-lst-itm-sm')
        rating = ratingPoints[0].text
        points = ratingPoints[1].text
        c.execute("INSERT INTO crickinfo_teamTestRank (rank, team, rating, points) VALUES(?,?,?,?)",(rank, team, rating, points))

def getTeamsTtwentyRanking():
    c.execute("CREATE TABLE IF NOT EXISTS crickinfo_teamTtwentyRank (id integer primary key autoincrement,rank integer unique, team varchar, rating varchar, points varchar);")
    page = requests.get("https://www.cricbuzz.com/cricket-stats/icc-rankings/men/teams")
    soup = BeautifulSoup(page.content, 'lxml')
    rankDetail = soup.find('div',{"ng-show":"'teams-t20s' == act_rank_format"})
    rankDetail = rankDetail.find_all('div', class_='cb-col cb-col-100 cb-font-14 cb-brdr-thin-btm text-center')
    ratingPoints = rankDetail[0].find_all('div', class_='cb-col cb-col-14 cb-lst-itm-sm')
    rating = ratingPoints[0].text
    points = ratingPoints[1].text
    for i in range(len(rankDetail)):
        rank = rankDetail[i].div.text
        team = rankDetail[i].find('div', class_='cb-col cb-col-50 cb-lst-itm-sm text-left').text
        ratingPoints = rankDetail[i].find_all('div', class_='cb-col cb-col-14 cb-lst-itm-sm')
        rating = ratingPoints[0].text
        points = ratingPoints[1].text
        c.execute("INSERT INTO crickinfo_teamTtwentyRank (rank, team, rating, points) VALUES(?,?,?,?)",(rank, team, rating, points))

refreshDatabase()



conn.commit()
conn.close()

