import os
import uuid
import random
import logging

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from eventregistry import *
from user_model import UserModel
from gtts import gTTS
import boto3
from datetime import datetime, timedelta, date
from pymongo import MongoClient
from sources_model import SourcesModel
from article_model import ArticleModel
import numpy as np

from utils import is_within_n_hours
from sources import mediastacksource

# Load environment variables from .env



# Load env variables
# NEWS_API_KEY = os.getenv('NEWS_API_KEY')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_ACCESS_KEY_SECRET = os.getenv('AWS_ACCESS_KEY_SECRET')
AWS_REGION = os.getenv('AWS_REGION')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

# er = EventRegistry(apiKey = NEWS_API_KEY, allowUseOfArchive=False)
client = OpenAI()
db_client = MongoClient(f"mongodb+srv://fpinnola:{MONGO_PASSWORD}@cluster0.9bnvnxh.mongodb.net/?retryWrites=true&w=majority", 27017)
users = UserModel(db_client)
articlesModel = ArticleModel(db_client)
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
    logging.info("Updating hackernews news articles")
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
            articlesModel.save_article(article_id, article['title'], article['raw_text'], article['summary'], article['url'], article['category'], article['date'], article['externalId'])

        # Update scrape sources to prevent future scrapes
        scrape_sources.update_since_scrape("hackernews", datetime.now())


    # Mediastack
    logging.info("Updating mediastack articles")
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
            articlesModel.save_article(article_id, article['title'], article['raw_text'], article['summary'], article['url'], article['category'], article['date'], article['externalId'])

        # Update scrape sources to prevent future scrapes
        scrape_sources.update_since_scrape("mediastack", datetime.now())

def get_new_articles_fromdb(categories=[], n=10):
    print(f"Requesting {n} articles, with categories {categories}")
    if not n or n <=0:
        # Requesting 0 articles
        return []
    
    # Query Articles DB for relevant articles
    twenty_four_hours_ago = datetime.now() - timedelta(days=5)
    response = []
    if (len(categories) > 0):
        response = articlesModel.get_articles_category_since(categories, twenty_four_hours_ago)
    else:
        response = articlesModel.get_articles_since(twenty_four_hours_ago)

    return response

def create_user(username, password):
    return users.create_user(username, password)
    
def validate_user(username, password):
    return users.validate_user(username, password)

def update_user_prefs(userId, prefs):
    return users.save_user_preferences(userId, prefs)

def add_user_engagement(userId, articleId, action):
    return users.add_engagement(userId, articleId, action)


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
                    {"role": "system", "content": f"Rewrite the following article. Retain important facts and key ideas presented. Only provide your summary and no extra message. Keep your summary concise, less than 200 words. Output your resposnse as a json object with two properties, 'summary' which is the rewrite, and 'category' which is  one of the following 'technology', 'business', 'politics', 'legal', 'general' or 'other'."},
                    {"role": "user", "content": f"{article['body']}"}
                ],
                max_tokens=300,
                response_format={ "type": "json_object" }
            )
        
        response = completion.choices[0].message.content
        print(response)
        obj = json.loads(response)

        article['summary'] = obj['summary']
        if ('category' not in article):
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

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    similarity = dot_product / (norm_vec1 * norm_vec2)
    return similarity


def action_weight(action):
    if action == "goto-source":
        return 0.3
    if action == "thumbs-up":
        return 0.5
    if action == "thumbs-down":
        return -0.5
    

def generate_article_score(user_engagements, article):
    num_engagements = len(user_engagements)
    if 'embedding' not in article:
        article['user_score'] = 0.5
        return
    
    total_score = 0.0
    
    for e_a in user_engagements:
        # print(f"e: {e_a}")
        # e_a = articles.get_article(e['articleId'])
        if 'embedding' not in e_a or e_a['embedding'] is None:
            continue
        weighted_score = 0
        if 'embedding' not in e_a:
            print(f"No embedding found for article: {e['articleId']}")
        e_a_emb = np.array(e_a['embedding'])
        similarity = cosine_similarity(np.array(article['embedding']), e_a_emb)
        for action in e_a['actions']:
            weighted_score += similarity * action_weight(action)
        total_score += weighted_score
    
    article['user_score'] = total_score / num_engagements


    
def populate_embedding_in_engagement(user_engagement):
    e_a = articlesModel.get_article(user_engagement['articleId'])
    if e_a is None:
        return
    user_engagement['embedding'] = e_a['embedding']

def get_top_n_articles(articles, n):
    """
    Returns the top N articles by 'user_score'.
    
    Parameters:
    - articles: A list of dictionaries, where each dictionary represents an article
      and has at least a 'user_score' key.
    - n: The number of top articles to return.
    
    Returns:
    - A list of the top N articles sorted by 'user_score' in descending order.
    """
    # Sort the articles by 'user_score' in descending order
    sorted_articles = sorted(articles, key=lambda x: x['user_score'], reverse=True)
    
    # Return the top N articles, or all articles if there are less than N
    return sorted_articles[:n]

def get_news_from_params(params, n=10):

    categories = []
    userId = params['userId']
    user = users.get_user(userId)
    engagements = []
    if 'engagements' in user and len(user['engagements']) > 2:
        engagements = user['engagements']

    if not user:
        print(f"User not found {userId}")
        return []
    
    if 'categories' in user['preferences']:
        categories = user['preferences']['categories']


    if not categories or not userId:
        print("Error getting params from get news request")
        return []

    print(f"categories: {categories}")
    print(f"userId: {params['userId']}")

    user_new_articles = []

    user_artices = users.get_user_articles(userId)
    if user_artices is None:
        # User doesn't exist, create
        # users.save_user_preferences(userId, {})
        user_artices = []

    user_new_articles.extend(user_artices)

    n = n - len(user_new_articles) # How many articles needed

    if n > 0:
        # Get new candidate articles from db
        new_article_candidates = get_new_articles_fromdb(categories, 100)

        # Add vector embeddings to user engagements (SPEEDUP attempt)
        for e in engagements:
            populate_embedding_in_engagement(e)

        # Generate scores for each article
        for a in new_article_candidates:
            generate_article_score(engagements, a)

        top_articles = get_top_n_articles(new_article_candidates, n)

        for a in top_articles:
            # Generate summary
            if 'summary' not in a:
                summarize_article(a)
                articlesModel.save_article(a['articleId'], a['title'], a['body'], a['summary'], a['url'], a['category'], a['articleDate'], a['externalId'])
        
        temp_articles = []
        for article in top_articles:
            if not is_article_in_list(article, user_new_articles):
                temp_articles.append(article)

        user_new_articles.extend(temp_articles)


    if (n > 0):
        users.update_user_articles(userId, user_new_articles)

    print(f"articles {str(user_new_articles)[:500] + '...' if len(str(user_new_articles)) > 500 else str(user_new_articles)}")

    return parse_json(user_new_articles)

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
    get_news_from_params({'userId': 'fpinnola@stevens.edu'})