# -*- coding: utf8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'uw-syde-course-cs792-2016-winter'

# pagination
POSTS_PER_PAGE = 8
MAX_SEARCH_RESULTS = 8

# Background Searching Engines
### Full list: 'google, bing, yahoo, yandex, baidu, duckduckgo'
SEARCH_ENGINES = 'google'

# available languages
LANGUAGES = {
    'en': 'English',
    'cn': '简体中文'
}

# Query Generator
QG_MAX_KEYWORDS = 10

# RSS Resources
RSS_RESOURCES = {
    'news': 'http://www.medpagetoday.com/rss/Headlines.xml',
    'disease': 'http://www.news-medical.net/tag/feed/',
    'health': 'http://www.medicinenet.com/rss/general/'
}

# For SSO
OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
