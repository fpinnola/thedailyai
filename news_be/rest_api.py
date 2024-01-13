from flask import Flask, request, jsonify
from main import get_news_from_params

app = Flask(__name__)

@app.route('/getNews', methods=['POST'])
def handle_get_news():

    # Get request body
    data = request.json    

    news = get_news_from_params(data)

    return jsonify(news)


if __name__ == '__main__':
    app.run(debug=True)