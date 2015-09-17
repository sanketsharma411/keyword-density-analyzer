from flask_app import app
from flask import request,render_template,jsonify
from modules.webpage import *
import modules.nlp 
import json
from modules.word_density_analyze import  *


@app.route('/w/')
def webpage_analyze_index():
    return render_template('index.html')
    
    
    
@app.route('/w/submit/')
def submit_form():
    
    url = request.args['url']
    
    w = Webpage(url)
    
    w.load()
    print 'Computing'
    results = '<br>'.join(word_density_analyze(url))
    print 'Done Computing'
    
    return results
    
