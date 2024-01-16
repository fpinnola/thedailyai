from flask import Flask, request, jsonify
from flask_cors import CORS
from main import get_news_from_params

app = Flask(__name__)
CORS(app)

@app.route('/getNews', methods=['POST'])
def handle_get_news():

    # Get request body
    data = request.json    

    news = get_news_from_params(data)

    return jsonify(news)


if __name__ == '__main__':
    app.run(debug=True)