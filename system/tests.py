import sys

from django.test import TestCase

from django.test.utils import setup_test_environment
from django.test import Client
from django.core.urlresolvers import reverse
from json import *
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session 
from importlib import import_module
from django.conf import settings
from system.gene import gene_graph
from models import compound,gene,reaction,reaction_compound,compound_gene,part_gene,organism,pathway,pathway_compound
from fasta_reader import read_fastas,parse_fasta_str,parse_fasta_str
from gene import search_compound,fuzzy_search_compound,format_fuzzy_result,get_gene_info,get_compound_info
from system.views import systemView,searchCompound,getCompound,getGene,getRelatedCompound
import time
import datetime
import os.path


BASE = os.path.dirname(os.path.abspath(__file__))

class read_fastas_testcase(TestCase):
    def setUp(self):
        self.fq = ['string1','string2']
    def test_normal(self):
        read_fastas(self.fq);

class parse_fasta_str_testcase(TestCase):
    def setUp(self):
        self.fasta_str = "string1\nstring2\nstring3\n"

    def test_normal(self):
        parse_fasta_str(self.fasta_str)
class parse_fasta_str_testcase(TestCase):
    def setUp(self):
        self.fasta_filename = "testfile1"
    def test_normal(self):
        parse_fasta_str(self.fasta_filename)

class search_compound_testcase(TestCase):
    def test_normal(self):
        pass
class fuzzy_search_compound_testcase(TestCase):
    def test_normal(self):
        pass
class testcase(TestCase):
    def setUp(self):
        self.gr = gene_graph('C00001', None)
        self.center_node = compound()
        self.center_node.compound_id = 'C00001'
        self.center_node.name = 'H2O'
        self.test_compound = compound()
        self.test_compound.compound_id = 'C00002'
        self.test_compound.name = 'ATP'
        self.gene_id_list = ['100008683']
    def test_normal(self):
        get_gene_info('C00001')
        get_compound_info('C00001')
        self.gr.get_compound_object('C00001')
        self.gr.retrive_gene_detain(1)
        self.gr.related_compound('C00001')
        self.gr.create_node('hello', 1)
        self.gr.create_n_link(self.center_node, self.test_compound)
        self.gr.get_or_create_gene('100008683')
        self.gr.save_relation_to_db(self.gene_id_list, self.test_compound)
        #self.gr.search_gene(self.test_compound)
        self.gr.cal_graph()
        self.gr.get_graph()
class testSystemView(TestCase):
    def setUp(self):
        pass
    def test_normal(self):
        pass