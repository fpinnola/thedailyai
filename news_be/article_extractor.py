# import the necessary functions
from trafilatura import fetch_url, extract
import json

def get_article_info(articleURL):


    # grab a HTML file to extract data from
    downloaded = fetch_url(articleURL)

    # output main content and comments as plain text
    result = extract(downloaded)

    # change the output format to XML (allowing for preservation of document structure)
    result = extract(downloaded, output_format="json")

    if not result:
        return None

    return json.loads(result)


if __name__ == "__main__":
    ai = get_article_info("https://www.cnn.com/2024/01/22/business/ftc-turbotax-free-services/index.html")
    print(ai)
    print(type(ai))

