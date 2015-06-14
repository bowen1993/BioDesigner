import os
import django
import sys
import urllib2
import xml.etree.ElementTree as ET

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import parts, features, part_twins, part_features

baseXmlUrl = 'http://parts.igem.org/cgi/xml/part.cgi?part='

def extractAndSave(partObj, xmlStr):
    try:
        doc = ET.fromstring(xmlStr)
    except:
        print 'part %s error, passed' % partObj.part_name
    try:
        part_url = doc.find('part_list/part/part_url').text
    except:
        return
    featuresInfo = doc.findall('part_list/part/features/feature')
    twins = doc.findall('part_list/part/twins/twin')
    if featuresInfo:
        for f in featuresInfo:
            fId = int(f.find('id').text)
            #print fId
            featureObj = features.objects.get_or_create(feature_id=fId)
            if featureObj[1]:
                title = f.find('title')
                #print title.text
                ftype = f.find('type')
                #print ftype.text
                direction = f.find('direction')
                #print direction.text
                startpos = f.find('startpos')
                #print startpos.text
                endpos = f.find('endpos')
                #print endpos.text
                featureObj[0].title = title.text
                featureObj[0].feature_type = ftype.text
                featureObj[0].direction = direction.text
                featureObj[0].startpos = int(startpos.text)
                featureObj[0].endpos = int(endpos.text)
                try:
                    featureObj[0].save()
                except:
                    pass
                newPF = part_features(part=partObj, feature=featureObj[0])
                newPF.save()
    if twins:
        for twin in twins:
            partB = parts.objects.filter(part_name=twin.text)
            if len(partB) == 0:
                continue
            else:
                partB = partB[0]
            newPP = part_twins(part_1=partObj, part_2=partB)
            try:
                newPP.save()
            except:
                pass
    partObj.part_url = part_url
    partObj.save()


    

def mainFunc():
    #get all parts
    step = 50
    head = 29800
    tail = head + step
    total = parts.objects.count() - head
    while total > 0:
        partlist = parts.objects.all()[head:tail]
        print 'first %d' % tail
        for partObj in partlist:
            print 'processing part %s' % partObj.part_name
            tmp = part_features.objects.filter(part=partObj)
            if len(tmp) != 0:
                print 'passing'
                continue
            print 'getting xml data'
            req = urllib2.Request(baseXmlUrl+partObj.part_name)
            response = urllib2.urlopen(req)
            xmlStr = response.read()
            print 'extracting data'
            extractAndSave(partObj,xmlStr)
        head += step
        tail += step
        total -= step

if __name__ == '__main__':
    django.setup()
    mainFunc()