from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from main import get_news_from_params, get_user_podcast, update_news_articles
import os

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'NONE')
jwt = JWTManager(app)
CORS(app)


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # Add your user authentication logic here
    # TODO: check db for user/pass
    if username != 'dev' or password != 'test':  # Dummy check, replace with real validation
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


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

@app.route('/news/refresh', methods=['GET'])
def handle_update_news():
    from threading import Thread
    thread = Thread(target = update_news_articles)

    thread.start()
    return "Began"

if __name__ == '__main__':
    DEV = False
    port = int(os.getenv('PORT', '5000'))
    if DEV:
        app.run(debug=True)
    else:
        app.run(debug=True, host='0.0.0.0', port=port)