from flask import g,render_template
from gammabin import app, conf
from gammabin.models import Paste


@app.before_request
def before_request():
    g.appname = conf.config['APPNAME']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api')
def api_view():
    return render_template('api.html')

@app.route('/paste/<uri>')
def paste_view(uri):
	paste = Paste.query.filter_by(uri=uri).first()
	return render_template('paste.html', paste=paste)