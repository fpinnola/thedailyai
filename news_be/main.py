import os

from dotenv import load_dotenv
from openai import OpenAI
from eventregistry import *
from user_model import UserModel
import concurrent.futures
from gtts import gTTS
import os


# Load environment variables from .env
load_dotenv()

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
er = EventRegistry(apiKey = NEWS_API_KEY, allowUseOfArchive=False)
client = OpenAI()
users = UserModel()

THEMES =["business", "technology", "politics", "biotech"]
STYLES = ["newscaseter", "humorous", "serious"]

SAMPLE_DATA = [
    { 'title': 'Flying Cars to Become Mainstream by 2025', 'url': 'https://example.com/flying-cars-2025', 'summary': 'Industry experts predict flying cars will dominate city skies in the next year.' },
    { 'title': 'Scientists Discover Water on the Sun', 'url': 'https://example.com/water-on-sun', 'summary': 'A groundbreaking discovery reveals large bodies of water on the sun’s surface.' },
    { 'title': 'World’s First Time Machine Built in Secret', 'url': 'https://example.com/first-time-machine', 'summary': 'Sources claim a fully functional time machine has been created in a private lab.' },
    { 'title': 'Dinosaurs Found Alive in Remote Jungle', 'url': 'https://example.com/dinosaurs-alive', 'summary': 'Explorers uncover a hidden ecosystem where dinosaurs continue to thrive.' },
    { 'title': 'Global Internet to Shut Down for Maintenance', 'url': 'https://example.com/global-internet-shutdown', 'summary': 'Authorities announce a scheduled global internet shutdown for system upgrades.' }
]


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
        
        print(f"getting summary for article: {article['uri']}")

        completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Summarize the following article in the style of a news broadcast. Retain important facts and key ideas presented. Only provide your summary and no extra message."},
                    {"role": "user", "content": f"{article['body']}"}
                ],
                max_tokens=150
            )
        
        article['summary'] = completion.choices[0].message.content
    except Exception as e:
        print("Error in summarizing article:", str(e))


def generate_pod_audio(script):
    tts = gTTS(script)
    local_file = f"./tmp/test_audio.mp3"
    tts.save(local_file)
    return


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
    if not user_artices:
        # User doesn't exist, create
        users.save_user_preferences(userId, {})
        user_artices = []

    articles.extend(user_artices)

    # Query API for missing articles
    n = n - len(articles)
    articles.extend(get_articles_from_api(categories, n))

    # Generate summaries for articles
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(summarize_article, article) for article in articles]
        concurrent.futures.wait(futures)


    # TODO: Store articles in DB
    users.update_user_articles(userId, articles)

    return articles



if __name__ == "__main__":
    articles = users.get_user_articles('frank123')
    script = generate_script(articles)
    users.save_daily_script('frank123', script)
    # print(f"script: {script}")
    generate_pod_audio(script)
    # print(script)

