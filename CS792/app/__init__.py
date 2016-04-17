from flask import Flask, jsonify
from flask.ext.restful import reqparse, abort, Api, Resource
from flask.json import JSONEncoder
from flask.ext.babel import Babel, lazy_gettext

import operator
import re
import os
import feedparser

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
babel = Babel(app)

from app import index
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS, SEARCH_ENGINES, RSS_RESOURCES
from app import querygenerator
from app import googleScraper

'''
APIs
'''
class CustomJSONEncoder(JSONEncoder):
    """This class adds support for lazy translation texts to Flask's
    JSON encoder. This is necessary when flashing translated texts."""
    def default(self, obj):
        from speaklater import is_lazy_string
        if is_lazy_string(obj):
            try:
                return unicode(obj)  # python 2
            except NameError:
                return str(obj)  # python 3
        return super(CustomJSONEncoder, self).default(obj)

app.json_encoder = CustomJSONEncoder

class Test(Resource):
    def get(selfself):
        return {'hello': 'Smart Medical Search Engine'}

class Search(Resource):
    def get(self, query, page_num=1):
        page_size = int(POSTS_PER_PAGE)
        max_records = int(MAX_SEARCH_RESULTS)
        if max_records <= 0:
            max_records = 50
        max_pages = int((max_records-1) / page_size) + 1

        # Background Searching Engines
        searchEngines = SEARCH_ENGINES
        if searchEngines.strip() == '':
            searchEngines = 'google'

        page_num = int(page_num)
        if page_num < 1:
            return {'error':'Invalid page_num'}

        '''
        Call Query Generator
        '''
        new_query = querygenerator.query(query)
        if not new_query:
            return {'error':'Invalid query'}

        '''
        Execute query
        1. Call Google Scraper
        2. (Phase II): Search our index (Cassandra or DynamoDB)
        '''
        results = googleScraper.query(new_query, 'basic', searchEngines, max_pages)

        '''
        Page Ranking
        '''
        #reranked = googleScraper.PageRanking(results)
        #count = reranked[0]
        #results = reranked[1]
        #ret = googleScraper.Convert2Dictionary(results)
        #print(ret)
        ret = googleScraper.PageRankingExpress(results)
        count = len(ret)
        page_count = int((count-1) / page_size) + 1
        page_next = page_num+1 if page_num < page_count else -1
        page_prev = page_num-1 if page_num > 1 else -1

        '''
        Return results in JSON
        '''
        list = {
            'result':ret,
            'page_num':page_num,
            'page_count':page_count,
            'page_size':page_size,
            'page_prev':page_prev,
            'page_next':page_next,
            'query':query
        }
        return jsonify(list)

class LoadRSS(Resource):
    def get(self, query, page_num=1):
        page_size = int(POSTS_PER_PAGE)
        max_records = int(MAX_SEARCH_RESULTS)
        if max_records <= 0:
            max_records = 50
        max_pages = int((max_records-1) / page_size) + 1

        # RSS Resources
        resourceRSS = RSS_RESOURCES['news']
        if query != 'news':
            # ToDo: better search the topic from list
            # ToDo: words translation, e.g. gallstone -> gallstones
            if query.find('woman') >= 0 or query.find('women') >= 0 or query.find('girl') >= 0:
                resourceRSS = RSS_RESOURCES['health'] + 'womens_health.xml'
            elif query.find('men') >= 0 or query.find('man') >= 0 or query.find('boy') >= 0:
                resourceRSS = RSS_RESOURCES['health'] + 'mens_health.xml'
            elif query.find('kid') >= 0 or query.find('child') >= 0:
                resourceRSS = RSS_RESOURCES['health'] + 'kids_health.xml'
            elif query.find('diet') >= 0 or query.find('weight') >= 0:
                resourceRSS = RSS_RESOURCES['health'] + 'diet_and_weight_management.xml'
            else:
                if query.find('gall') >= 0:
                    query = 'gallstones'
                elif query.find('allerg') >= 0:
                    query = 'allergy'
                elif query.find('alzheim') >= 0:
                    query = 'Alzheimers-Disease'
                elif query.find('arthri') >= 0:
                    query = 'arthritis'
                resourceRSS = RSS_RESOURCES['disease'] + query + '.aspx'

        page_num = int(page_num)
        if page_num < 1:
            return {'error':'Invalid page_num'}

        # Load RSS
        rssData = feedparser.parse(resourceRSS)
        count = len(rssData.entries)
        page_count = int((count-1) / page_size) + 1
        page_next = page_num+1 if page_num < page_count else -1
        page_prev = page_num-1 if page_num > 1 else -1
        if app.debug:
            print('DebugInfo - LoadRSS: ' + resourceRSS + ', items=%d' % count)

        '''
        Return results in JSON
        '''
        list = {
            'result':rssData,
            'page_num':page_num,
            'page_count':page_count,
            'page_size':page_size,
            'page_prev':page_prev,
            'page_next':page_next,
            'query':query
        }
        return jsonify(list)

class LoadLBS(Resource):
    def get(self, query):
        # Load POIs
        # ToDo: now only show dummy data. Later will query historical searching information from database
        poiData = [
            {'pos_x':43.1, 'pos_y':-80.6, 'user':'test1'},
            {'pos_x':43.2, 'pos_y':-80.2, 'user':'test2'},
            {'pos_x':43.8, 'pos_y':-80.1, 'user':'test3'},
            {'pos_x':43.7, 'pos_y':-80.9, 'user':'test4'},
        ]
        count = len(poiData)

        '''
        Return results in JSON
        '''
        list = {
            'query':query,
            'poi_count':count,
            'result':poiData
        }
        return jsonify(list)

##
## Actually setup the Api resource routing here
##
api.add_resource(Test, '/apis/test')
api.add_resource(Search, '/apis/search/<query>/<page_num>', endpoint = 'user')
api.add_resource(LoadRSS, '/apis/loadRSS/<query>/<page_num>', endpoint = 'rss')
api.add_resource(LoadLBS, '/apis/loadLBS/<query>', endpoint = 'lbs')
