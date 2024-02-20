import logging
import sys

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from flask_cors import CORS
from main import get_news_from_params, get_user_podcast, update_news_articles
from aggregation_engine import init_pipeline
from main import create_user, validate_user, update_user_prefs, add_user_engagement
import os
from datetime import timedelta

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'NONE')

jwt = JWTManager(app)
CORS(app)


@app.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    # TODO: Invalidate old refresh token

    # TODO: issue and store new refresh token
    new_token = create_access_token(identity=current_user, expires_delta=timedelta(hours=24))
    return jsonify({'access_token': new_token})


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password').encode('utf-8')
    # Add your user authentication logic here
    # TODO: check db for user/pass
    res = validate_user(username, password)
    print(f"res {res}")
    if 'error' in res:
        return jsonify(res), 401

    access_token = create_access_token(identity=username, expires_delta=timedelta(hours=24))

    # TODO: store refresh token
    refresh_token = create_refresh_token(identity=username)
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token})

@app.route('/signup', methods=['POST'])
def signup():
    # Get data from request
    data = request.json
    username = data.get('username')
    password = data.get('password')  # Ensure to hash passwords before storing them in production applications

    res = create_user(username, password)
    
    if 'error' in res:
        return jsonify(res), 401


    return jsonify(res), 201

@app.route('/user/prefs', methods=['POST'])
@jwt_required()
def handle_update_user_prefs():

    data = request.json
    prefs = data.get('preferences')

    current_user = get_jwt_identity()
    print(f"current_user: {current_user}")

    res = update_user_prefs(current_user, prefs)

    if 'error' in res:
        return jsonify(res), 401

    return jsonify(res), 200

@app.route('/user/action', methods=['POST'])
@jwt_required()
def handle_user_engagement():
    data = request.json
    action = data.get('action')
    articleId = data.get('articleId')
    current_user = get_jwt_identity()

    res = add_user_engagement(current_user, articleId, action)
    if 'error' in res:
        return jsonify(res), 401
    
    return jsonify(res), 200

@app.route('/getNews', methods=['POST'])
@jwt_required()
def handle_get_news():

    current_user = get_jwt_identity()
    print(f"current_user {current_user}")

    # Get request body
    data = request.json    
    data['userId'] = current_user

    articles = get_news_from_params(data)

    return articles

@app.route('/getAudio', methods=['POST'])
@jwt_required()
def handle_get_audio():

    data = request.json

    audio_url = get_user_podcast(data)

    response_obj = {
        'audio_url': audio_url
    }

    return jsonify(response_obj)

from threading import Thread
@app.route('/news/refresh', methods=['GET'])
def handle_update_news():
    logging.info("Starting refresh of news")
    def update_with_context():
        with app.app_context():
            init_pipeline()
    thread = Thread(target = update_with_context)
    thread.start()
    return "Began"

if __name__ == '__main__':
    DEV = False
    port = int(os.getenv('PORT', '5000'))
    if DEV:
        app.run(debug=True)
    else:
        app.run(debug=True, host='0.0.0.0', port=port)