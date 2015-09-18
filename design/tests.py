from django.test import TestCase
from design.recommend import getMarkovRecommend, get_chain, predict
from design.file import createFolder,geneFileName,getSequenceResultImage
from design.models import parts,project,chain,tracks 
from design.project import getUserProject,formatProjectList,getChainList,getChain
from accounts.models import User 
from design.views import isLoggedIn,createProject,createNewDevice,saveChain,getChainLength,getTracks
from django.test.utils import setup_test_environment
from django.test import Client
from django.core.urlresolvers import reverse
from json import *
from importlib import import_module
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session 
import time
import datetime
import os.path

BASE = os.path.dirname(os.path.abspath(__file__))

class RecommendTestCase(TestCase):
    def setUp(self):
        self.partId = 1
    def test_MarkovRecommend(self):
        self.result = getMarkovRecommend(self.partId)
        self.isGet = self.result['isSuccessful']
        self.assertEqual(self.isGet, False)

class MarkovTestCase(TestCase):
    def test_get_chain(self):
        process = [{'f': [1, None]},
                   {'a': [0.5, 'f'], 'k': [0.5, 'f']},
                   {'j': [0.5, 'k'], 'g': [0.5, 'a']}]
        ans = ['f', 'k', 'j']
        res = get_chain('j', 2, process)
        self.assertEqual(ans, res, None)

    def test_predict(self):
        A = {'a': {'g': 1.0, 'j': 1.0},
             'g': {'f': 1.0},
             'f': {'a': 0.5, 'k': 0.5},
             'k': {'j': 0.5},
             'j': {'f': 1.0},
             'r': {'u': 1.0},
             'u': {'v': 1.0}}
        ss = ('f', 'b')
        anss = ([['a', 'j'], ['a', 'g']], None)
        for s, ans in zip(ss, anss):
            res = predict(2, 2, s, A)
            self.assertEqual(res, ans, None)

class createFolderTestCase(TestCase):
    def setUp(self):
        self.year     = str(time.localtime().tm_year)
        self.month    = str(time.localtime().tm_mon)
        self.day      = str(time.localtime().tm_mday)
        self.predict_result = BASE + '/../downloads/'
        self.predict_result += self.year + '/'
        self.predict_result += self.month + '/'
        self.predict_result += self.day + '/'

    # correct input, but the folder has existed
    def test_repeat_folder(self):
        self.contentType = "image"
        self.result = True
        if os.path.exists(BASE + self.contentType + '/'):
            pass
        else:
            createFolder(self.contentType)
        try:
            createFolder(self.contentType)
        except Exception, e:
            self.result = False
        finally:
            self.assertEqual(self.result,True,"can create same folder twice")
        
    # correct input, and the folder is new
    def test_new_folder(self):
        self.contentType = "image"
        self.result = True
        if not os.path.exists(BASE + self.contentType + '/'):
            try:
                createFolder(self.contentType)
            except Exception, e:
                self.result = False
            finally:
                self.assertEqual(self.result,True,"create new folder correctly")
        else:
            print "the folder has created!!!"

class geneFileNameTestCase(TestCase):
    def setUp(self):
        self.now = datetime.datetime.now()
        self.timeString = str(self.now.year)+'-'+str(self.now.month)+'-'+str(self.now.day)+'-'+str(self.now.hour)+'-'+str(self.now.minute)+'-'+str(self.now.second)

    #file name is correct and surfix is correct
    # for example:predict string is 2015-8-4-11-3-30-test.txt
    def test_normal(self):
        self.fileName = "test"
        self.surfix = "txt"
        self.timeString = self.timeString + '-' + self.fileName
        self.timeString = self.timeString + '.' + self.surfix
        self.assertEqual(geneFileName(self.fileName,self.surfix),self.timeString)


class getUserProjectTestCase(TestCase):
    def setUp(self):
        #initial information into temperory database
        self.user = User()
        self.user.username = "Bob"
        self.user.password = "123"
        self.user.email = "asfja"
        self.user.is_confirmed = True
        self.user.save()
        self.emptyProjectUser = User()
        self.emptyProjectUser.username = "empty"
        self.emptyProjectUser.password = "123"
        self.emptyProjectUser.email = "1312"
        self.emptyProjectUser.is_confirmed = False
        self.emptyProjectUser.save()

        self.project1 = project()
        self.project1.project_name = "project1"
        self.project1.creator = self.user
        self.project1.save()
        self.project2 = project()
        self.project2.project_name = "project2"
        self.project2.creator = self.user
        self.project2.save()

    def test_normal(self):
        self.assertTrue(getUserProject(self.user)['isSuccessful'])
    def test_empty_project(self):
        self.assertEqual(getUserProject(self.emptyProjectUser)['projects'],[])

class formatProjectListTestCase(TestCase):
    def setUp(self):
        #initial information into temperory database
        self.user = User()
        self.user.username = "Bob"
        self.user.password = "123"
        self.user.email = "asfja"
        self.user.is_confirmed = True
        self.user.save()

        self.project1 = project()
        self.project1.project_name = "project1"
        self.project1.creator = self.user
        self.project1.save()
        self.project2 = project()
        self.project2.project_name = "project2"
        self.project2.creator = self.user
        self.project2.save()

    def test_list_exist(self):
        self.projectList = project.objects.filter(creator=self.user, is_deleted=False)
        # construct the predict result
        #print formatProjectList(self.projectList)
        self.predictResult = list()
        self.p1 = {
            'id':1L,
            'name':unicode(self.project1.project_name,"utf-8"),
            'creator':unicode(self.user.username,"utf-8"),
            'function':None,
            'track':None,
        }
        self.p2 = {
            'id':2L,
            'name':unicode(self.project2.project_name, "utf-8"),
            'creator':unicode(self.user.username,"utf-8"),
            'function':None,
            'track':None,
        }
        self.predictResult.append(self.p1)
        self.predictResult.append(self.p2)
        self.assertEqual(cmp(formatProjectList(self.projectList),self.predictResult), 1)
        

    def test_null_list(self):
        self.assertEqual(cmp(formatProjectList([]),[]),0)

class getChainListTestCase(TestCase):
    def setUp(self):
        #initial information into temperory database
        self.user = User()
        self.user.username = "Bob"
        self.user.password = "123"
        self.user.email = "email"
        self.user.is_confirmed = True
        self.user.save()

        self.project = project()
        self.project.project_name = "project"
        self.project.creator = self.user
        self.project.save()
        
        self.chain1 = chain()
        self.chain1.name = "chain1"
        self.chain1.project = self.project
        self.chain1.save()
        self.chain2 = chain()
        self.chain2.name = "chain2"
        self.chain2.project = self.project
        self.chain2.save()

    def test_id_exist(self):
        self.predictResult = [{
        'id':1,
        'name':'chain1',
        },{
        'id':2,
        'name':'chain2',
        }]
        self.realResult = getChainList(self.project.pk)
        self.assertEqual(cmp(self.realResult,self.predictResult),1)

    def test_id_not_exist(self):
        self.predictResult = []
        self.realResult = getChainList(5)
        self.assertEqual(cmp(self.realResult,self.predictResult),0)
    def test_id_null(self):
        self.predictResult = []
        self.realResult = getChainList(None)
        self.assertEqual(cmp(self.realResult,self.predictResult),0)

class getChainTestCase(TestCase):
    def setUp(self):
        #initial information into temperory database
        self.user = User()
        self.user.username = "Bob"
        self.user.password = "123"
        self.user.email = "email"
        self.user.is_confirmed = True
        self.user.save()

        self.project = project()
        self.project.project_name = "project"
        self.project.creator = self.user
        self.project.save()
        
        self.chain1 = chain()
        self.chain1.name = "chain1"
        self.chain1.id = 1
        self.chain1.sequence = "1_2_3"
        self.chain1.project = self.project
        self.chain1.save()
        self.chain2 = chain()
        self.chain2.id = 2
        self.chain2.name = "chain2"
        self.chain2.sequence = ""
        self.chain2.project = self.project
        self.chain2.save()

        self.partObj1 = parts()
        self.partObj1.part_id = 1
        self.partObj1.part_name = "part1"
        self.partObj1.part_type = "type1"
        self.partObj1.save()
        self.partObj2 = parts()
        self.partObj2.part_id = 2
        self.partObj2.part_name = "part2"
        self.partObj2.part_type = "type2"
        self.partObj2.save()
        self.partObj3 = parts()
        self.partObj3.part_id = 3
        self.partObj3.part_name = "part3"
        self.partObj3.part_type = "type3"
        self.partObj3.save()

    # chain id exist, chain contains several parts
    def test_normal_chain(self):
        self.predictResult = [{
        'part_id' : unicode('1',"utf-8"),
        'part_name' : unicode('part1',"utf-8"),
        'part_type' : unicode('type1',"utf-8")
        },{
        'part_id' : unicode('2',"utf-8"),
        'part_name' : unicode('part2',"utf-8"),
        'part_type' : unicode('type2',"utf-8")
        },{
        'part_id' : unicode('3',"utf-8"),
        'part_name' : unicode('part3',"utf-8"),
        'part_type' : unicode('type3',"utf-8")
        }]
        self.realResult = getChain(1)
        print self.realResult
        self.cmpResult = cmp(self.predictResult,self.realResult[1])
        self.assertTrue(self.cmpResult==0 and self.realResult[0])

    # chain id exist, chain's sequence is empty
    def test_empty_chain(self):
        self.predictResult = []
        self.realResult = getChain(2)
        self.cmpResult = cmp(self.predictResult,self.realResult[1])
        self.assertTrue(self.cmpResult==0 and self.realResult[0])
    # chain id doesn't exist
    def test_chainId_not_exist(self):
        self.predictResult = None
        self.realResult = getChain(3)
        self.cmpResult = cmp(self.predictResult,self.realResult[1])
        self.assertTrue((self.cmpResult==0)and(self.realResult[0] == False))

class createProjectTestCase(TestCase):
    def setUp(self):
        #initail information into temperory database
        self.user = User()
        self.user.username = "Bob"
        self.user.password = "123"
        self.user.email = "email"
        self.user.is_confirmed = True
        self.user.save()

        self.track = tracks()
        self.track.id = 1
        self.track.track = "track1"
        self.track.save()

        self.client = Client()
    def test_no_login_create(self):
        self.response = self.client.post('/home/newProject',{'track':self.track.id})
        #response.content is The body of the response, as a string. 
        #This is the final page content as rendered by the view,
        # or any error message.
        # self.response.content is a string ,need to 
        self.result = JSONDecoder().decode(self.response.content)
        self.assertEqual(self.result['isSuccessful'],False)

    def test_create_afterLogin(self):
        #modify the value in session
        self.engine = import_module(settings.SESSION_ENGINE)
        self.session = self.engine.SessionStore()
        self.session['username'] = 'Bob'
        self.session['isLoggedIn'] = True
        self.session.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = self.session.session_key
        #get the real response
        self.createResponse = self.client.post('/home/newProject',{'track':self.track.id,'name':'project1'})
        # convert the result string to dict object
        self.realResult = JSONDecoder().decode(self.createResponse.content)
        self.predictResult = {
        'isSuccessful':True,
        'project_name':'project1',
        'id':1,
        'track':'track1',
        'creator':'Bob'
        }
        self.assertEqual(cmp(self.realResult,self.predictResult),1)

class createNewDeviceTestCase(TestCase):
    def setUp(self):
        #initail information into temperory database
        self.user = User()
        self.user.username = "Bob"
        self.user.password = "123"
        self.user.email = "email"
        self.user.is_confirmed = True
        self.user.save()

        self.project = project()
        self.project.id = 1
        self.project.project_name = "project"
        self.project.creator = self.user
        self.project.save()
        
        self.client = Client()

    def test_no_login_createDevice(self):
        self.response = self.client.post('/home/newDevice',{'name':'newChain','id':1})
        #response.content is The body of the response, as a string. 
        #This is the final page content as rendered by the view,
        # or any error message.
        # self.response.content is a string ,need to 
        self.result = JSONDecoder().decode(self.response.content)
        self.assertEqual(self.result['isSuccessful'],False)

    def test_createDevice_afterLogin(self):
        #modify the value in session
        self.engine = import_module(settings.SESSION_ENGINE)
        self.session = self.engine.SessionStore()
        self.session['username'] = 'Bob'
        self.session['isLoggedIn'] = True
        self.session.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = self.session.session_key
        #get the real response
        self.createResponse = self.client.post('/home/newDevice',{'name':'newChain','id':1})
        # convert the result string to dict object
        self.realResult = JSONDecoder().decode(self.createResponse.content)
        self.predictResult = {
        unicode('isSuccessful',"utf-8"):True,
        unicode('name',"utf-8"):unicode('newChain',"utf-8"),
        unicode('id',"utf-8"):unicode('1',"utf-8")
        }
        self.assertEqual(cmp(self.realResult,self.predictResult),0)

class saveChainTestCase(TestCase):
    def setUp(self):
        #initial information into temperory database
        self.user = User()
        self.user.username = "Bob"
        self.user.password = "123"
        self.user.email = "email"
        self.user.is_confirmed = True
        self.user.save()

        self.project = project()
        self.project.project_name = "project"
        self.project.creator = self.user
        self.project.save()
        
        self.chain1 = chain()
        self.chain1.name = "chain1"
        self.chain1.id = 1
        self.chain1.sequence = "1_2_3"
        self.chain1.project = self.project
        self.chain1.save()

        self.client = Client()

    def test_chainId_not_exist(self):
        self.saveResponse = self.client.post('/home/updateChain',{'chain':'1_2','id':3})
        self.realResult = JSONDecoder().decode(self.saveResponse.content)
        self.assertEqual(self.realResult['isSuccessful'],False)
    def test_chainId_exist(self):
        self.saveResponse = self.client.post('/home/updateChain',{'chain':'1_2','id':1})
        self.realResult = JSONDecoder().decode(self.saveResponse.content)
        self.assertEqual(self.realResult['isSuccessful'],True)

class getTracksTestCase(TestCase):
    def setUp(self):
        self.client = Client()
    def test_noTracks_in_database(self):
        self.trackResponse = self.client.post('/home/tracks')
        self.realResult = JSONDecoder().decode(self.trackResponse.content)
        self.assertTrue(self.realResult['isSuccessful']==True and self.realResult['tracks'] == [])
    def test_hasTracks_in_database(self):
        #write track infromation into database
        self.track1 = tracks()
        self.track1.id = 1
        self.track1.track = "track1"
        self.track1.save()
        self.track2 = tracks()
        self.track2.id = 2
        self.track2.track = "track2"
        self.track2.save()

        self.trackResponse = self.client.post('/home/tracks')
        self.realResult = JSONDecoder().decode(self.trackResponse.content)
        self.predictResult = [{
        'id':1,
        'track':'track1'
        },{
        'id':2,
        'track':'track2'
        }]
        self.assertEqual(cmp(self.realResult['tracks'],self.predictResult),0)

class getChainLengthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        #initial information into temperory database
        self.user = User()
        self.user.username = "Bob"
        self.user.password = "123"
        self.user.email = "email"
        self.user.is_confirmed = True
        self.user.save()

        self.project = project()
        self.project.project_name = "project"
        self.project.creator = self.user
        self.project.save()
        
        self.chain1 = chain()
        self.chain1.name = "chain1"
        self.chain1.id = 1
        self.chain1.sequence = "1_2_3_4_5"
        self.chain1.project = self.project
        self.chain1.save()
        self.chain2 = chain()
        self.chain2.name = "chain2"
        self.chain2.id = 2
        self.chain2.sequence = ""
        self.chain2.project = self.project
        self.chain2.save()
        self.chain3 = chain()
        self.chain3.name = "chain3"
        self.chain3.id = 3
        self.chain3.sequence = "1"
        self.chain3.project = self.project
        self.chain3.save()
        self.chain4 = chain()
        self.chain4.name = "chain4"
        self.chain4.id = 4
        self.chain4.sequence = "1__5"
        self.chain4.project = self.project
        self.chain4.save()

    def test_normalLen_chain(self):
        self.lenResponse = self.client.get('/home/getChainLength',{'id':1})
        self.realResult = JSONDecoder().decode(self.lenResponse.content)
        self.assertEqual(self.realResult['length'],5)
    def test_oneLen_chain(self):
        self.lenResponse = self.client.get('/home/getChainLength',{'id':3})
        self.realResult = JSONDecoder().decode(self.lenResponse.content)
        self.assertEqual(self.realResult['length'],1)


