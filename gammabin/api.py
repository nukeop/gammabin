import datetime

from flask import g, jsonify, make_response, request, url_for
from flask.views import MethodView

from gammabin import app, db
from gammabin.models import Paste
from gammabin.generate import generate_url


def make_error(message, http_status):
    return make_response(jsonify({'error': message, 'status': http_status}), http_status)


@app.errorhandler(404)
def not_found(error=None):
    return make_error('The requested resource has not been found', 404)


@app.errorhandler(400)
def not_found(error=None):
    return make_error('There was an error in client\'s request', 400)


class PastesAPI(MethodView):
    def get_paste(self, uri):
        paste = Paste.query.filter_by(uri=uri).first()
        result = paste.as_dict()
        result['url'] = url_for('pastes_GET', uri=result['uri'], _external=True)

        return jsonify({
            'paste': result
        })


    def create_paste(self, form):
        keys = list(form.keys())
        if not 'content' in keys:
            return make_error('Not all required parameters were supplied', 400)

        title, content = 'Untitled', None
        content = form['content']

        if 'title' in keys:
            title = form['title']

        uri = generate_url()

        paste = Paste(title, content, None, uri, request.remote_addr, datetime.datetime.now(), 'public')

        db.session.add(paste)
        db.session.commit()

        return make_response(jsonify({
            'status': 'created',
            'uri': uri
        }), 201)


    def get(self, url):
        if url is None:
            return jsonify({
                    'huj': 'dupa'
                })
        else:
            return self.get_paste(url)

    def post(self):
        return self.create_paste(request.form)


pastes_view_get = PastesAPI.as_view('pastes_GET')
app.add_url_rule('/api/v1/pastes/', defaults={'url': None}, view_func=pastes_view_get, methods=['GET'])
app.add_url_rule('/api/v1/pastes/<url>', view_func=pastes_view_get, methods=['GET'])

pastes_view_post = PastesAPI.as_view('pastes_POST')
app.add_url_rule('/api/v1/pastes/', view_func=pastes_view_post, methods=['POST'])