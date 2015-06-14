import os
import django
import sys
import xml.sax
import datetime
import re
import chardet
from chardet.universaldetector import UniversalDetector

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import parts

filename = 'newnew.xml'

class partsHandler(xml.sax.ContentHandler):
    def __init__(self):
        #attribute for analyse
        self.currentTag = ""
        self.currentAttribute = ""
        #choose the table
        self.isPart = 0
        #create the part object
        self.partTable = parts()
        #part table element
        self.part_id = ""
        self.ok = ""
        self.part_name = ""
        self.short_desc = ""
        self.description = ""
        self.part_type = ""
        self.author = ""
        self.status = ""
        self.dominant = ""
        self.discontinued = ""
        self.part_status = ""
        self.sample_status = ""
        self.p_status_cache = ""
        self.s_status_cache = ""
        self.creation_date = ""
        self.m_datetime = ""
        self.in_stock = ""
        self.results = ""
        self.favorite = ""
        self.specified_u_list = ""
        self.deep_u_list = ""
        self.deep_count = ""
        self.ps_string = ""
        self.scars = ""
        self.barcode = ""
        self.notes = ""
        self.source = ""
        self.nickname = ""
        self.premium = ""
        self.categories = ""
        self.sequence = ""
        self.seq_edit_cache = ""
        self.sequence_length = ""

    def startElement(self,tag,attributes):
        self.currentTag = tag
        if tag == "field" or tag == "table_data":
            self.currentAttribute = attributes.get("name")
        if tag == "table_data" and self.currentAttribute == "parts":
            self.isPart = 1
        if tag == "table_data" and self.currentAttribute == "parts_seq_features":
            self.isPart = 0

    def endElement(self,tag):
        if self.isPart == 1:
            if tag == "row":
                self.partTable.save()
                print "stored"
                self.partTable = parts()
            elif self.currentTag == "field" and self.currentAttribute == "part_id":
                self.partTable.part_id = int(self.part_id)
                print "part_id"+self.part_id
            elif self.currentTag == "field" and self.currentAttribute == "ok":
                if self.ok == "0":
                    self.partTable.ok = False
                elif self.ok == "1":
                    self.partTable.ok = True
                #print "self.ok" + self.ok
            elif self.currentTag == "field" and self.currentAttribute == "part_name":
                self.partTable.part_name = self.part_name
                print "self.part_name" + self.part_name
            elif self.currentTag == "field" and self.currentAttribute == "short_desc":
                self.partTable.short_desc = self.short_desc
                #print "self.short_desc" + self.short_desc
            elif self.currentTag == "field" and self.currentAttribute == "description":
                self.partTable.description = self.description
            elif self.currentTag == "field" and self.currentAttribute == "part_type":
                self.partTable.part_type = self.part_type
                #print "self.part_type" + self.part_type
            elif self.currentTag == "field" and self.currentAttribute == "author":
                self.partTable.author = self.author
                #print "self.author" + self.author
            elif self.currentTag == "field" and self.currentAttribute == "status":
                self.partTable.status = self.status
                #print "self.status" + self.status
            elif self.currentTag == "field" and self.currentAttribute == "dominant":
                if self.dominant == "0":
                    self.partTable.dominant = False
                elif self.dominant == "1":
                    self.partTable.dominant = True
                #print "self.dominant" + self.dominant
            elif self.currentTag == "field" and self.currentAttribute == "discontinued":
                if self.discontinued != "":
                    self.partTable.discontinued = int(self.discontinued)
                #print "self.discontinued" + self.discontinued
            elif self.currentTag == "field" and self.currentAttribute == "part_status":
                self.partTable.part_status = self.part_status
                #print "self.part_status" + self.part_status
            elif self.currentTag == "field" and self.currentAttribute == "sample_status":
                self.partTable.sample_status = self.sample_status
                #print "self.sample_status" + self.sample_status
            elif self.currentTag == "field" and self.currentAttribute == "p_status_cache":
                self.partTable.p_status_cache = self.p_status_cache
                #print "self.p_status_cache" + self.p_status_cache
            elif self.currentTag == "field" and self.currentAttribute == "s_status_cache":
                self.partTable.s_status_cache = self.s_status_cache
                #print "self.s_status_cache" + self.s_status_cache
            elif self.currentTag == "field" and self.currentAttribute == "creation_date":
                pass
                #if self.creation_date != "":
                #    print "origin date: " + self.creation_date
                #    str_split = self.creation_date.split('-')
                #    print str_split
                #    temp_date = datetime.date(int(str_split[0]),int(str_split[1]),int(str_split[2]))
                #    self.partTable.creation_date = temp_date
                #print "self.creation_date" + self.creation_date
            elif self.currentTag == "field" and self.currentAttribute == "m_datetime":
                pass
                #print "origin data: %s" % self.m_datetime
                #str_split = re.split('[- :]',self.m_datetime)
                #if str_split != [u'\t\t']:
                #    year = int(str_split[0])
                #    month = int(str_split[1])
                #    day = int(str_split[2])
                #    hour = int(str_split[3])
                #    minute = int(str_split[4])
                #    second = int(str_split[5])
                #    temp_date = datetime.datetime(year,month,day,hour,minute,second)
                    #print temp_date
                #    self.partTable.m_datetime = temp_date
                #print "self.m_datetime" + self.m_datetime

            elif self.currentTag == "field" and self.currentAttribute == "in_stock":
                if self.in_stock == "0":
                    self.partTable.in_stock = False
                elif self.in_stock == "1":
                    self.partTable.in_stock = True
                #print "self.in_stock" + self.in_stock
            elif self.currentTag == "field" and self.currentAttribute == "results":
                self.partTable.results = self.results
                #print "self.results" + self.results
            elif self.currentTag == "field" and self.currentAttribute == "favorite":
                if self.favorite != "":
                    self.partTable.favorite = int(self.favorite)
                #print "self.favorite" + self.favorite
            elif self.currentTag == "field" and self.currentAttribute == "specified_u_list":
                self.partTable.specified_u_list = self.specified_u_list
                #print "self.specified_u_list" + self.specified_u_list
            elif self.currentTag == "field" and self.currentAttribute == "deep_u_list":
                self.partTable.deep_u_list = self.deep_u_list
                #print "self.deep_u_list" + self.deep_u_list
            elif self.currentTag == "field" and self.currentAttribute == "deep_count":
                if self.deep_count != "":
                    self.partTable.deep_count = int(self.deep_count)
                #print "self.deep_count" + self.deep_count
            elif self.currentTag == "field" and self.currentAttribute == "ps_string":
                self.partTable.ps_string = self.ps_string
                #print "self.ps_string" + self.ps_string
            elif self.currentTag == "field" and self.currentAttribute == "scars":
                self.partTable.scars = self.scars
                #print "scars" + self.scars
            elif self.currentTag == "field" and self.currentAttribute == "barcode":
                self.partTable.barcode = self.barcode
                #print "barcode" + self.barcode
            elif self.currentTag == "field" and self.currentAttribute == "notes":
                self.partTable.notes = self.notes
                #print "notes" + self.notes
            elif self.currentTag == "field" and self.currentAttribute == "source":
                self.partTable.source = self.source
                #print "source" + self.source
            elif self.currentTag == "field" and self.currentAttribute == "nickname":
                self.partTable.nickname = self.nickname
                #print "nickname" + self.nickname
            elif self.currentTag == "field" and self.currentAttribute == "premium":
                self.partTable.premium = int(self.premium)
                #print "premium" + self.premium
            elif self.currentTag == "field" and self.currentAttribute == "categories":
                self.partTable.categories = self.categories
                #print "categories" + self.categories
            elif self.currentTag == "field" and self.currentAttribute == "sequence":
                self.partTable.sequence = self.sequence
                #print "sequence"
            elif self.currentTag == "field" and self.currentAttribute == "sequence_length":
                if self.sequence_length != "":
                    self.partTable.sequence_length = int(self.sequence_length)
                #print "sequence_length" + self.sequence_length

            #print self.currentTag
            #print "the read tag is: " + tag 
            self.currentTag = ""
    def characters(self,content):
        #choose the first table
        if self.isPart == 1:
            if self.currentTag == "field" and self.currentAttribute == "part_id":
                self.part_id = content
            elif self.currentTag == "field" and self.currentAttribute == "ok":
                self.ok = content
            elif self.currentTag == "field" and self.currentAttribute == "part_name":
                self.part_name = content 
            elif self.currentTag == "field" and self.currentAttribute == "short_desc":
                self.short_desc = content
            elif self.currentTag == "field" and self.currentAttribute == "description":
                self.description = content
            elif self.currentTag == "field" and self.currentAttribute == "part_type":
                self.part_type = content
            elif self.currentTag == "field" and self.currentAttribute == "author":
                self.author = content
            elif self.currentTag == "field" and self.currentAttribute == "status":
                self.status = content
            elif self.currentTag == "field" and self.currentAttribute == "dominant":
                self.dominant = content
            elif self.currentTag == "field" and self.currentAttribute == "discontinued":
                self.discontinued = content
            elif self.currentTag == "field" and self.currentAttribute == "part_status":
                self.part_status = content
            elif self.currentTag == "field" and self.currentAttribute == "sample_status":
                self.sample_status = content
            elif self.currentTag == "field" and self.currentAttribute == "p_status_cache":
                self.p_status_cache = content
            elif self.currentTag == "field" and self.currentAttribute == "s_status_cache":
                self.s_status_cache = content
            elif self.currentTag == "field" and self.currentAttribute == "creation_date":
                if len(content) != 10:
                    self.creation_date += content
                else:
                    self.creation_date = content
            elif self.currentTag == "field" and self.currentAttribute == "m_datetime":
                if len(content) != 19:
                    self.m_datetime += content
                else:
                    self.m_datetime = content
            elif self.currentTag == "field" and self.currentAttribute == "in_stock":
                self.in_stock = content
            elif self.currentTag == "field" and self.currentAttribute == "results":
                self.results = content
            elif self.currentTag == "field" and self.currentAttribute == "favorite":
                self.favorite = content
            elif self.currentTag == "field" and self.currentAttribute == "specified_u_list":
                self.specified_u_list = content
            elif self.currentTag == "field" and self.currentAttribute == "deep_u_list":
                self.deep_u_list = content
            elif self.currentTag == "field" and self.currentAttribute == "deep_count":
                self.deep_count = content
            elif self.currentTag == "field" and self.currentAttribute == "ps_string":
                self.ps_string = content
            elif self.currentTag == "field" and self.currentAttribute == "scars":
                self.scars = content
            elif self.currentTag == "field" and self.currentAttribute == "barcode":
                self.barcode = content
            elif self.currentTag == "field" and self.currentAttribute == "notes":
                self.notes = content
            elif self.currentTag == "field" and self.currentAttribute == "source":
                self.source = content
            elif self.currentTag == "field" and self.currentAttribute == "nickname":
                self.nickname = content
            elif self.currentTag == "field" and self.currentAttribute == "premium":
                self.premium = content
            elif self.currentTag == "field" and self.currentAttribute == "categories":
                self.categories = content
            elif self.currentTag == "field" and self.currentAttribute == "sequence":
                self.sequence = content
            elif self.currentTag == "field" and self.currentAttribute == "sequence_length":
                self.sequence_length = content

def mainFunc():
    #analyse code here
    
    #create XML reader
    parser = xml.sax.make_parser()
    #turn off namespaces
    parser.setFeature(xml.sax.handler.feature_namespaces,0)
    #rewrite ContextHander
    handler = partsHandler()
    parser.setContentHandler(handler)
    parser.parse(filename)

if __name__ == '__main__':
    django.setup()
    mainFunc()