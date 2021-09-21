# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from crickinfo.models import Teams ,Schedules, IplSchedules, OdiBatRank, TestBatRank, TtwentyBatRank




def index(request):
    scheduleObj = IplSchedules.objects.all()
    lenSchedules = len(scheduleObj)
    matchTitleList = []
    matchVenueList = []
    matchDateList = []
    for i in range(lenSchedules):
        matchTitleList.append(scheduleObj[i].matchTitle)
        matchVenueList.append(scheduleObj[i].matchVenue)
        matchDateList.append(scheduleObj[i].matchDate)
    context = {
        'matchTitleList':matchTitleList,
        'matchVenueList':matchVenueList,
        'matchDateList':matchDateList
    }
    return render(request, 'cricketPage.html',context)

def getRanks(request):
    batOdiRankObj = OdiBatRank.objects.all()
    rankBatOdiList = []
    playerBatOdiList = []
    countryBatOdiList = []
    ratingsBatOdiList = []
    batTestRankObj = TestBatRank.objects.all()
    rankBatTestList = []
    playerBatTestList = []
    countryBatTestList = []
    ratingsBatTestList = []
    batTtwentyRankObj = TtwentyBatRank.objects.all()
    rankBatTtwentyList = []
    playerBatTtwentyList = []
    countryBatTtwentyList = []
    ratingsBatTtwentyList = []
    for i in range(len(batOdiRankObj)):
        rankBatOdiList.append(batOdiRankObj[i].rank)
        playerBatOdiList.append(batOdiRankObj[i].player)
        countryBatOdiList.append(batOdiRankObj[i].playerCountry)
        ratingsBatOdiList.append(batOdiRankObj[i].playerRatings)
    for i in range(len(batTestRankObj)):
        rankBatTestList.append(batTestRankObj[i].rank)
        playerBatTestList.append(batTestRankObj[i].player)
        countryBatTestList.append(batTestRankObj[i].playerCountry)
        ratingsBatTestList.append(batTestRankObj[i].playerRatings)
    for i in range(len(batTtwentyRankObj)):
        rankBatTtwentyList.append(batTtwentyRankObj[i].rank)
        playerBatTtwentyList.append(batTtwentyRankObj[i].player)
        countryBatTtwentyList.append(batTtwentyRankObj[i].playerCountry)
        ratingsBatTtwentyList.append(batTtwentyRankObj[i].playerRatings)
    context = {
        'rankBatOdiList':rankBatOdiList,
        'playerBatOdiList':playerBatOdiList,
        'countryBatOdiList':countryBatOdiList,
        'ratingsBatOdiList':ratingsBatOdiList,
        'rankBatTestList':rankBatTestList,
        'playerBatTestList':playerBatTestList,
        'countryBatTestList':countryBatTestList,
        'ratingsBatTestList':ratingsBatTestList,
        'rankBatTtwentyList':rankBatTtwentyList,
        'playerBatTtwentyList':playerBatTtwentyList,
        'countryBatTtwentyList':countryBatTtwentyList,
        'ratingsBatTtwentyList':rankBatTtwentyList
    }
    return render(request, 'rankingsPage.html',context)

def team(request):
    path = request.path
    Id = int(path.split('/')[-2])
    teamObj = Teams.objects.get(id = Id)
    scheduleObj = Schedules.objects.filter(teamId = Id)
    lenSchedules = len(scheduleObj)
    matchTitleList = []
    matchVenueList = []
    matchDateList = []
    for i in range(lenSchedules):
        matchTitleList.append(scheduleObj[i].matchTitle)
        matchVenueList.append(scheduleObj[i].matchVenue)
        matchDateList.append(scheduleObj[i].matchDate)
    context = {
        'teamTitle':teamObj.title,
        'matchTitleList':matchTitleList,
        'matchVenueList':matchVenueList,
        'matchDateList':matchDateList
    }

    return render(request, 'teamPage.html', context)
