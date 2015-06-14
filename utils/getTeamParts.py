import os
import django
import csv
import sys
from BeautifulSoup import BeautifulSoup
import urllib2
import xml.etree.ElementTree as ET

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import teams, team_parts, parts

regionList2014 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Latin America', 'table_Teams_from_North America']
regionList2013 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Latin America', 'table_Teams_from_North America']
regionList2012 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Latin America', 'table_Teams_from_Americas East', 'table_Teams_from_Americas West']
regionList2011 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Americas']
regionList2010 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Canada', 'table_Teams_from_Latin America', 'table_Teams_from_US']
regionList2007 = ['table_Teams_from_Asia', 'table_Teams_from_Europe', 'table_Teams_from_Canada', 'table_Teams_from_Latin America', 'table_Teams_from_US', 'table_Teams_from_Other']
regionList2006 = ['table_Teams_from_Other']
filenamelist1 = ['2006tp.csv', '2007tp.csv', '2008tp.csv', '2009tp.csv', '2010tp.csv']
filenamelist = ['2014tp.csv']
baseXmlUrl = 'http://parts.igem.org/cgi/xml/part.cgi?part='


def getTeamDict(baseUrl):
    result = dict()
    req = urllib2.Request(baseUrl)
    response = urllib2.urlopen(req)
    htmlStr = response.read()
    teamDict = analyseHTMLPage(htmlStr)
    for teamname in teamDict:
        saveParts(teamDict[teamname]['url'], teamname)
        
def saveParts(wikiUrl, teamname):
    req = urllib2.Request(wikiUrl)
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    response = urllib2.urlopen(req)
    htmlStr = response.read()
    soup = BeautifulSoup(htmlStr)
    # get favorite parts
    try:
        partsTable1 = soup.find(id='Table_1')
        part_names = partsTable1.findAll('a')
        for part in part_names:
            print '%s,2006,%s' % (teamname, part.string)
    except:
        pass
    try:
        partTable2 = soup.find(id='Table_2')
        part_names = partTable2.findAll('a')
        for part in part_names:
            print '%s,2006,%s' % (teamname, part.string)
    except:
        pass


def analyseHTMLPage(htmlStr):
    resultDict = dict()
    soup = BeautifulSoup(htmlStr)
    for regionStr in regionList2006:
        regionTable = soup.find(id=regionStr)
        aTag = regionTable.findAll('a')
        for a in aTag:
            idIndex = a.string.find('=')
            resultDict[a.string] = {
                'id' : a['href'][idIndex+1:],
                'url' : a['href']
            }
    return resultDict

def getPartInfo(partName):
    req = urllib2.Request(baseXmlUrl+partName)
    response = urllib2.urlopen(req)
    xmlStr = response.read()
    # analyse the xmlStr and save info to DB
    print 'getting part %s' % partName
    try:
        part_info = extractInfoFromXML(xmlStr)
    except:
        return None
    partObj = parts(part_id=part_info['id'], part_name=partName)
    partObj.part_type = part_info['part_type']
    partObj.short_desc = part_info['short_desc']
    partObj.author = part_info['part_author']
    partObj.sequence = part_info['sequence']
    partObj.deep_u_list = part_info['sub_part']
    partObj.deep_count = part_info['count']
    partObj.part_url = part_info['url']
    try:
        partObj.save()
        print 'part %s saved' % partObj.part_name
    except:
        print 'part %s error' % partObj.part_name
    return partObj

def extractInfoFromXML(xmlStr):
    doc = ET.fromstring(xmlStr)
    part_id = doc.find('part_list/part/part_id').text
    part_type = doc.find('part_list/part/part_type').text
    short_desc = doc.find('part_list/part/part_short_desc').text
    part_author = doc.find('part_list/part/part_author').text
    sequence = doc.find('part_list/part/sequences/seq_data').text
    sub_parts = doc.findall('part_list/part/deep_subparts/subpart')
    part_url = doc.find('part_list/part/part_url').text
    sub_part_str = ''
    list_count = 0
    if sub_parts:
        for sub_part in sub_parts:
            id = sub_part.find('part_id').text
            sub_part_str += id + '_'
            list_count += 1
    result = {
        'id' : part_id,
        'part_type' : part_type,
        'short_desc' : short_desc,
        'part_author' : part_author,
        'sequence' : sequence,
        'sub_part' : sub_part_str,
        'url' : part_url,
        'count' : str(list_count)
    }
    return result

def getTeamPart(filename):
    csvReader = csv.reader(open(filename, 'r'))
    for row in csvReader:
        print 'processing team %s @ year %s' % (row[0], row[1])
        teamObj = teams.objects.get(name=row[0], year=row[1])
        partObj = parts.objects.filter(part_name=row[2])
        if len(partObj) == 0:
            partObj = getPartInfo(row[2])
            if not partObj:
                continue
            newTP = team_parts(team=teamObj, part=partObj)
            try:
                newTP.save()
            except:
                pass
        else:
            newTP = team_parts.objects.get_or_create(team=teamObj, part=partObj[0])
            if newTP[1]:
                newTP[0].save()
            else:
                print 'passing'


def mainFunc():
    for filename in filenamelist:
        print 'processing %s' % filename
        getTeamPart(filename)

if __name__ == '__main__':
    django.setup()
    mainFunc()