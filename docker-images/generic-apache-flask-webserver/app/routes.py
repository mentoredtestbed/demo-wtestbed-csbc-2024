# coding=utf-8

from flask import render_template, flash, redirect, session, url_for, request, g, Markup
from app import app
from lorem.text import TextLorem

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/random_text/<min_words>/<max_words>')
def random_text(min_words, max_words):
    lorem = TextLorem(wsep=' ', srange=(int(min_words),int(max_words)))
    return render_template('random_text.html', random_text=lorem.sentence())