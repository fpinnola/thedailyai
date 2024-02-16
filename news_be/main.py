import os
import uuid
import random

from dotenv import load_dotenv
from openai import OpenAI
from eventregistry import *
from user_model import UserModel
from gtts import gTTS
import boto3
from datetime import datetime, timedelta, date
from pymongo import MongoClient
from sources_model import SourcesModel
from article_model import ArticleModel

from utils import is_within_n_hours
from sources import mediastacksource


# Load environment variables from .env
load_dotenv()


# Load env variables
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_ACCESS_KEY_SECRET = os.getenv('AWS_ACCESS_KEY_SECRET')
AWS_REGION = os.getenv('AWS_REGION')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

er = EventRegistry(apiKey = NEWS_API_KEY, allowUseOfArchive=False)
client = OpenAI()
db_client = MongoClient(f"mongodb+srv://fpinnola:{MONGO_PASSWORD}@cluster0.9bnvnxh.mongodb.net/?retryWrites=true&w=majority", 27017)
users = UserModel(db_client)
articles = ArticleModel(db_client)
scrape_sources = SourcesModel(db_client)

THEMES =["business", "technology", "politics", "biotech"]
STYLES = ["newscaseter", "humorous", "serious"]

SAMPLE_DATA = [
    { 'title': 'Flying Cars to Become Mainstream by 2025', 'url': 'https://example.com/flying-cars-2025', 'summary': 'Industry experts predict flying cars will dominate city skies in the next year.' },
    { 'title': 'Scientists Discover Water on the Sun', 'url': 'https://example.com/water-on-sun', 'summary': 'A groundbreaking discovery reveals large bodies of water on the sun’s surface.' },
    { 'title': 'World’s First Time Machine Built in Secret', 'url': 'https://example.com/first-time-machine', 'summary': 'Sources claim a fully functional time machine has been created in a private lab.' },
    { 'title': 'Dinosaurs Found Alive in Remote Jungle', 'url': 'https://example.com/dinosaurs-alive', 'summary': 'Explorers uncover a hidden ecosystem where dinosaurs continue to thrive.' },
    { 'title': 'Global Internet to Shut Down for Maintenance', 'url': 'https://example.com/global-internet-shutdown', 'summary': 'Authorities announce a scheduled global internet shutdown for system upgrades.' }
]

from sources.hackernews import get_best_articles
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self,o)

def parse_json(data):
    return JSONEncoder().encode(data)


def is_within_n_days(input_date, n_days):
    """
    Check if the given date is within n_days from today.

    :param input_date: The date to check, as a datetime.date object or a string in the format 'YYYY-MM-DD'.
    :param n_days: Number of days to check within, as an integer.
    :return: True if the date is within n_days from today, False otherwise.
    """
    # Ensure input_date is a datetime.date object
    if isinstance(input_date, str):
        input_date = datetime.strptime(input_date, "%Y-%m-%d").date()

    # Get today's date
    today = date.today()

    # Calculate the difference in days
    day_difference = abs((input_date - today).days)

    # Check if the difference is within n_days
    return day_difference <= n_days


def update_news_articles():
    # TODO: add lock so multiple simultaneous runs not possible
    
    
    # Hackernews
    last_scrape = scrape_sources.time_since_scrape("hackernews")
    if not last_scrape or not is_within_n_hours(last_scrape, 8):

        # Need to update articles with latest from hackernews
        new_articles = get_best_articles(max_articles=15, within_days=5)
        print(f"got {len(new_articles)} new articles from hackernews")
        
        # Store new articles in db
        for article in new_articles:
            article['body'] = article['raw_text']
            summarize_article(article)
            article_id = str(uuid.uuid4())
            if not 'externalId' in article:
                article['externalId'] = None
            if (not 'summary' in article) or (not 'category' in article):
                print(f"Issue getting summary or cateogry for article {article['title']}")
                continue
            articles.save_article(article_id, article['title'], article['raw_text'], article['summary'], article['url'], article['category'], article['date'], article['externalId'])

        # Update scrape sources to prevent future scrapes
        scrape_sources.update_since_scrape("hackernews", datetime.now())

    # Mediastack
    last_scrape = scrape_sources.time_since_scrape("mediastack")
    if not last_scrape or not is_within_n_hours(last_scrape, 24):
        new_articles = mediastacksource.get_new_articles()
        print(f"got {len(new_articles)} new aritcles from mediastack")
        for article in new_articles:
            article['body'] = article['raw_text']
            summarize_article(article)
            article_id = str(uuid.uuid4())
            if not 'externalId' in article:
                article['externalId'] = None
            if (not 'summary' in article) or (not 'category' in article):
                print(f"Issue getting summary or cateogry for article {article['title']}")
                continue
            articles.save_article(article_id, article['title'], article['raw_text'], article['summary'], article['url'], article['category'], article['date'], article['externalId'])

        # Update scrape sources to prevent future scrapes
        scrape_sources.update_since_scrape("mediastack", datetime.now())

def get_articles_from_hackernews(categories, n=10):
    print(f"Requesting {n} articles from hackernews")
    if not n or n <=0:
        # Requesting 0 articles
        return []
    
    # Query Articles DB for relevant articles
    twenty_four_hours_ago = datetime.now() - timedelta(days=5)
    response = articles.get_articles_since(twenty_four_hours_ago)

    N = min(n, len(response))
    # Randomly select N elements from the list
    selected_elements = random.sample(response, N)
    print(N)
    return selected_elements

def create_user(username, password):
    return users.create_user(username, password)
    
def validate_user(username, password):
    return users.validate_user(username, password)

def update_user_prefs(userId, prefs):
    return users.save_user_preferences(userId, prefs)

'''
    Returns n latest articles given categories
    Params:
        categories: list of strings
        n: max articles to return (default 5)
'''
def get_articles_from_api(categories, n=10):
    print(f"Requesting {n} articles from external API")
    if not n:
        # Requesting 0 articles
        return []

    ri = ReturnInfo(ArticleInfoFlags(categories=True))

    q = QueryArticlesIter(
        categoryUri= QueryItems.OR([f"{er.getCategoryUri(cat)}" for cat in categories]),
        lang='eng',
        startSourceRankPercentile=0,
        endSourceRankPercentile=10,
        dataType="news"
    )

    articles = []
    for art in q.execQuery(er, sortBy = "date", maxItems=n, returnInfo=ri):
        articles.append({
            'title': art['title'],
            'body': art['body'],
            'uri': art['uri'],
            'meta': {k: v for k, v in art.items() if k not in ['body', 'title', 'url']}
        })
    
    return articles

    
'''
    Returns a finalized script for a news broadcast given a set of articles
    Params:
        articles: list of articles objects that have 'title' and 'summary' fields
        style: string, should be in the STYLES list
'''
def generate_script(articles, style="newscaster"):
    if not len(articles):
        raise Exception("No articles passed")
    
    bulk = ''
    for a in articles:
        bulk += a['title'] + ': ' + a['summary'] + '\n'
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a news script writer. You will take in a list of summarized news articles and their titles, and produce a script for the day in the style of {style}. Do not include any text,except what should be spoken. Do not leave openings for reporters names. It should read as a story. No introduction or closing, only the content. "},
            {"role": "user", "content": f"Create a news script from the following articles: {bulk}"}
        ]
    )

    return completion.choices[0].message.content

def summarize_article(article):
    try :
        if 'summary' in article:
            return
        
        # print(f"getting summary for article: {article['uri']}")

        completion = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=[
                    {"role": "system", "content": f"Summarize the following article in the style of a news broadcast. Retain important facts and key ideas presented. Only provide your summary and no extra message. Keep your summary concise, less than 200 words. Output your resposnse as a json object with two properties, 'summary' which is the summary, and 'category' which is  one of the following 'technology', 'software', 'biotech', 'politics', or 'other'."},
                    {"role": "user", "content": f"{article['body']}"}
                ],
                max_tokens=300,
                response_format={ "type": "json_object" }
            )
        
        response = completion.choices[0].message.content
        print(response)
        obj = json.loads(response)

        article['summary'] = obj['summary']
        article['category'] = obj['category']
    except Exception as e:
        print("Error in summarizing article:", str(e))


def generate_pod_audio(userId, script):
    tts = gTTS(script)
    unique_file_name = f"{userId}pod-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
    local_file = f"./tmp/{unique_file_name}.mp3"
    tts.save(local_file)

    audio_url = save_file_to_s3(unique_file_name)
    
    return audio_url

def save_file_to_s3(file_name):
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_ACCESS_KEY_SECRET,
        region_name=AWS_REGION
    )
    s3 = session.resource('s3')

    s3_object_key = f"{file_name}.mp3"
    s3.Bucket(AWS_BUCKET_NAME).upload_file(f"./tmp/{file_name}.mp3", s3_object_key)

    s3_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_object_key}"

    return s3_url


def is_article_in_list(article, articles):
    for a in articles:
        if a['externalId'] == article['externalId']:
            return True
    return False

def get_news_from_params(params, n=10):

    categories = params['categories']
    userId = params['userId']

    if not categories or not userId:
        print("Error getting params from get news request")
        return []

    print(f"params: {params['categories']}")
    print(f"userId: {params['userId']}")

    articles = []

    user_artices = users.get_user_articles(userId)
    if user_artices is None:
        # User doesn't exist, create
        users.save_user_preferences(userId, {})
        user_artices = []

    articles.extend(user_artices)

    # Query API for missing articles
    n = n - len(articles)
    new_articles = get_articles_from_hackernews(categories, n)

    temp_articles = []
    for article in new_articles:
        if not is_article_in_list(article, articles):
            temp_articles.append(article)

    articles.extend(temp_articles)


    # TODO: Store articles in DB
    if (n > 0):
        users.update_user_articles(userId, articles)

    print(f"articles {str(articles)[:500] + '...' if len(str(articles)) > 500 else str(articles)}")

    return parse_json(articles)

def get_user_podcast(params):

    userId = params['userId']
    style = params['style']

    script = users.get_daily_script(userId)

    if script is None:
        # User does not exist
        raise Exception('User does not exist')

    if not len(script):
        articles = users.get_user_articles(userId)
        print(articles)
        script = generate_script(articles, style)
        users.save_daily_script(userId, script)

    audio_url = users.get_daily_audio(userId)

    if not len(audio_url):
        audio_url = generate_pod_audio(userId, script)
        users.set_daily_audio(userId, audio_url)

    return audio_url





if __name__ == "__main__":
    res = get_articles_from_hackernews([])
    # print(res)

    # article_body = "TOKYO -- Japan will establish a new visa status that will make it easier for IT engineers and other workers for overseas companies to reside in the country, the Immigration Services Agency said Friday. The planned status will allow highly skilled workers to work in Japan on a teleworking basis for up to six months while enjoying sightseeing trips, the agency said."
    # article = {
    #     'body': article_body
    # }
    # summary = summarize_article(article)
    # print(article)
 
    pass
