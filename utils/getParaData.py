import os
import django
import sys
import urllib2
import xml.etree.ElementTree as ET
import csv

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import parts, part_parameters

baseXmlUrl = 'http://parts.igem.org/cgi/xml/part.cgi?part='

def getParaDataForParts(part_list, csv_writer):
    for partObj in part_list:
        name = partObj.part_name
        print 'inforing for %s id: %d' % (name, partObj.part_id)
        paraInfos = getPartParaInfo(name)
        if len(paraInfos) == 0:
            continue
        try:
            csv_writer.writerows(paraInfos)
        except:
            pass

def getPartParaInfo(name):
    req = urllib2.Request(baseXmlUrl+name)
    response = urllib2.urlopen(req)
    xmlStr = response.read()
    return getInfosFromXML(xmlStr, name)

def getInfosFromXML(xmlStr, partName):
    try:
        doc = ET.fromstring(xmlStr)
    except:
        return []
    para_nodes = doc.findall('part_list/part/parameters/parameter')
    result_list = list()
    for para_node in para_nodes:
        try:
            name = para_node.find('name').text
            value = para_node.find('value').text
            para_info = [partName, name, value]
            result_list.append(para_info)
        except:
            pass
    return result_list


def mainFunc():
    startpos = 29623
    step = 1000
    endpos = startpos + step
    totalPartCount = parts.objects.count()
    remainCount = totalPartCount
    csv_writer = csv.writer(open('paraData6.csv', 'wb'), delimiter=',')
    print 'process started'
    while remainCount > 0:
        print 'processing %d to %d' % (startpos, endpos)
        part_list = parts.objects.all().order_by('part_id')[startpos:endpos]
        startpos += step
        endpos += step
        remainCount -= step
        getParaDataForParts(part_list, csv_writer)
    print 'process end'
    del csv_writer

if __name__ == '__main__':
    django.setup()
    mainFunc()
