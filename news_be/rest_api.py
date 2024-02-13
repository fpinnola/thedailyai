from flask import Flask, request, jsonify
from flask_cors import CORS
from main import get_news_from_params, get_user_podcast, update_news_articles
import os

app = Flask(__name__)
CORS(app)

@app.route('/getNews', methods=['POST'])
def handle_get_news():

    # Get request body
    data = request.json    

    articles = get_news_from_params(data)

    return articles

@app.route('/getAudio', methods=['POST'])
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