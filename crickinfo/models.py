# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Teams(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 100)
    title = models.CharField(max_length = 200)
    
class Schedules(models.Model):
    id = models.IntegerField(primary_key=True)
    teamId = models.IntegerField()
    matchTitle = models.CharField(max_length =100)
    matchVenue = models.CharField(max_length = 100)
    matchDate = models.CharField(max_length =100)

class IplSchedules(models.Model):
    id = models.IntegerField(primary_key=True)
    matchTitle = models.CharField(max_length = 100)
    matchVenue = models.CharField(max_length = 100)
    matchDate = models.CharField(max_length = 100)

class OdiBatRank(models.Model):
    id = models.IntegerField(primary_key=True)
    rank = models.IntegerField()
    player = models.CharField(max_length = 100)
    playerCountry = models.CharField(max_length = 100)
    playerRatings = models.CharField(max_length = 100)

class TestBatRank(models.Model):
    id = models.IntegerField(primary_key=True)
    rank = models.IntegerField()
    player = models.CharField(max_length = 100)
    playerCountry = models.CharField(max_length = 100)
    playerRatings = models.CharField(max_length = 100)

class TtwentyBatRank(models.Model):
    id = models.IntegerField(primary_key=True)
    rank = models.IntegerField()
    player = models.CharField(max_length = 100)
    playerCountry = models.CharField(max_length = 100)
    playerRatings = models.CharField(max_length = 100)
