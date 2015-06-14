import os
import django
import sys
import urllib2
import xml.etree.ElementTree as ET

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import parts

baseXmlUrl = 'http://parts.igem.org/cgi/xml/part.cgi?part='

def anaFASTA():
    #get the part from allparts.txt and save to DB
    part_file = open('All_Parts.txt', 'r')
    totalCount = 0;
    for line in part_file.readlines():
        if line.startswith('>'):
            info_list = line[1:].split(' ')
            partObj = parts.objects.get_or_create(part_id=info_list[2])
            if partObj[1]:
                print 'adding part: %s' % info_list[0]
                partObj[0].part_name = info_list[0]
                partObj[0].part_type = info_list[3]
                getPartInfoDetail(partObj[0])
                totalCount += 1
            else:
                print 'passing part %s' % info_list[0]
    print 'total count : %d' % totalCount

def getPartInfoDetail(partObj):
    req = urllib2.Request(baseXmlUrl+partObj.part_name)
    response = urllib2.urlopen(req)
    xmlStr = response.read()
    # analyse the xmlStr and save info to DB
    part_info = extractInfoFromXML(xmlStr)
    partObj.short_desc = part_info['short_desc']
    partObj.author = part_info['part_author']
    partObj.sequence = part_info['sequence']
    partObj.deep_u_list = part_info['sub_part']
    partObj.deep_count = part_info['count']
    partObj.part_url = part_info['url']
    partObj.save()
    print 'part %s saved' % partObj.part_name

def extractInfoFromXML(xmlStr):
    doc = ET.fromstring(xmlStr)
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
        'short_desc' : short_desc,
        'part_author' : part_author,
        'sequence' : sequence,
        'sub_part' : sub_part_str,
        'url' : part_url,
        'count' : str(list_count)
    }
    return result

def mainFunc():
    anaFASTA();

if __name__ == '__main__':
    django.setup()
    mainFunc()
    