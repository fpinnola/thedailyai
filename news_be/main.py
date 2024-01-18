import os

from dotenv import load_dotenv
from openai import OpenAI
from eventregistry import *


# Load environment variables from .env
load_dotenv()

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
er = EventRegistry(apiKey = NEWS_API_KEY, allowUseOfArchive=False)
client = OpenAI()

THEMES =["business", "technology", "politics", "biotech"]
STYLES = ["newscaseter", "humorous", "serious"]

SAMPLE_DATA = [
    { 'title': 'Flying Cars to Become Mainstream by 2025', 'url': 'https://example.com/flying-cars-2025', 'summary': 'Industry experts predict flying cars will dominate city skies in the next year.' },
    { 'title': 'Scientists Discover Water on the Sun', 'url': 'https://example.com/water-on-sun', 'summary': 'A groundbreaking discovery reveals large bodies of water on the sun’s surface.' },
    { 'title': 'World’s First Time Machine Built in Secret', 'url': 'https://example.com/first-time-machine', 'summary': 'Sources claim a fully functional time machine has been created in a private lab.' },
    { 'title': 'Dinosaurs Found Alive in Remote Jungle', 'url': 'https://example.com/dinosaurs-alive', 'summary': 'Explorers uncover a hidden ecosystem where dinosaurs continue to thrive.' },
    { 'title': 'Global Internet to Shut Down for Maintenance', 'url': 'https://example.com/global-internet-shutdown', 'summary': 'Authorities announce a scheduled global internet shutdown for system upgrades.' }
]

def get_articles_from_api(categories, n=10):

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
    
    print(f"articles: {articles}")

    return articles


'''
    Returns n latest articles given a theme
    Params:
        theme: string, must be in THEMES
        n: max articles to return (default 5)
'''
def get_latest_articles(theme, n=1):
    if not theme in THEMES:
        raise Exception(f"{theme} not a valid theme")
    

    # Pull articles from news api
    q = QueryArticlesIter(
        categoryUri = er.getCategoryUri(f"{theme}"),
        lang='eng'
    )
    articles = []
    for art in q.execQuery(er, sortBy = "date", maxItems=n):
        articles.append({
            'uri': art['uri'],
            'title': art['title'],
            'body': art['body']
        })

    # Use GPT to summarize article's body
    for i in range(len(articles)):
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Summarize the following article in the style of a news broadcast. Retain important facts and key ideas presented. Only provide your summary and no extra message."},
                {"role": "user", "content": f"{raw_data[i]['body']}"}
            ]
        )
        articles[i]['summary'] = completion.choices[0].message.content

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
            {"role": "system", "content": f"You are a news script writer. You will take in a list of summarized news articles and their titles, and produce a script for the day in the style of {style}"},
            {"role": "user", "content": f"Create a news script from the following articles: {bulk}"}
        ]
    )



def get_news_from_params(params, n=10):

    print(f"params: {params['categories']}")
    print(f"userId: {params['userId']}")

    articles = []

    # TODO: check DB for articles
    

    # Query API for missing articles
    n = n - len(articles)
    articles.extend(get_articles_from_api(params['categories'], n))
    # Generate summaries for articles


    # TODO: Store articles in DB


    return articles




if __name__ == "__main__":
    articles = get_latest_articles("technology")
    script = generate_script(articles)
    print(script)

