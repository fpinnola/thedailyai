from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

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

'''
    Returns n latest articles given a theme
    Params:
        theme: string, must be in THEMES
        n: max articles to return (default 5)
'''
def get_latest_articles(theme, n=5):
    if not theme in THEMES:
        raise Exception(f"{theme} not a valid theme")
    
    # TODO: pull articles from web => Summarize

    return SAMPLE_DATA

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

    print(completion)





if __name__ == "__main__":
    articles = get_latest_articles("technology")
    generate_script(articles)

