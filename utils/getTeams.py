import os
import django
import sys
import xml.sax
import datetime
from BeautifulSoup import BeautifulSoup
import urllib2

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import teams, functions, tracks

regionList2014 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Latin America', 'table_Teams_from_North America']
regionList2013 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Latin America', 'table_Teams_from_North America']
regionList2012 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Latin America', 'table_Teams_from_Americas East', 'table_Teams_from_Americas West']
regionList2011 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Americas']
regionList2010 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Canada', 'table_Teams_from_Latin America', 'table_Teams_from_US']
regionList2007 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Canada', 'table_Teams_from_Latin America', 'table_Teams_from_US', 'table_Teams_from_Other']
regionList2006 = ['table_Teams_from_Other']


def getTeamDict(baseURL):
    print 'get html doc'
    result = dict()
    req = urllib2.Request(baseURL)
    response = urllib2.urlopen(req)
    htmlStr = response.read()
    print 'geting wiki url'
    teamDict = analyseHTMLPage(htmlStr)
    for key in teamDict:
        print 'writing team: ' + key
        #if os.path.exists('./team/' + key + '.txt'):
        #    print 'passing: ' + key
        #    continue
        teamId = int(teamDict[key]['id'])
        print teamId
        try:
            newTeam = teams.objects.get(team_id = teamId)
            newTeam.year = '2004'
            try:
                newTeam.save()
            except:
                print 'save year error for team %s' % key
            print 'passing'
            continue
        except:
            pass
            track = getTeamAbstruct(teamDict[key]['url'])
            print 'saving'
            if 'not been assigned' in track:
                track = 'none'
            else:
                track = track[19:-4]
            newTrack = tracks.objects.get_or_create(track=track)
            if newTrack[1]:
                newTrack[0].save()
            newTeam = teams(team_id=teamId, track=newTrack[0], name=key, year='2004')
            newTeam.save()
    return result

def analyseHTMLPage(htmlStr):
    resultDict = dict()
    soup = BeautifulSoup(htmlStr)
    for regionStr in regionList2006:
        regionTable = soup.find(id=regionStr)
        aTag = regionTable.findAll('a')
        for a in aTag:
            idIndex = a['href'].find('=')
            resultDict[a.string] = {
                'url': a['href'],
                'id' : a['href'][idIndex+1:]
            }
    return resultDict

def getTeamAbstruct(wikiURL):
    req = urllib2.Request(wikiURL)
    idIndex = wikiURL.find('=')
    cookieStr = 'team_ID=' + wikiURL[idIndex+1:]
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Cookie', cookieStr)
    print cookieStr
    response = urllib2.urlopen(req)
    htmlStr = response.read()
    soup = BeautifulSoup(htmlStr)
    #get track
    #print soup
    trackTable = soup.find(id='table_tracks')
    abstractTr = str(trackTable.find('tr').td.contents)

    return abstractTr

if __name__ == '__main__':
    django.setup()
    getTeamDict('http://igem.org/Team_List?year=2004')