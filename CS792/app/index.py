from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.babel import gettext
from datetime import datetime
from app import app, babel
from config import LANGUAGES

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())

@app.route('/',  methods=['GET', 'POST'])
def index():

  staticDir = '/static/'
  return render_template('index.html', static=staticDir)

@app.route('/search',  methods=['GET', 'POST'])
@app.route('/search/<int:page>', methods=['GET', 'POST'])
def search():
  rs = 'test'
  return render_template('index.html', result=rs)

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    #db.session.rollback()
    return render_template('500.html'), 500
