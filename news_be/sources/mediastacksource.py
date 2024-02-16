import requests
import os
from datetime import datetime, timedelta

def fetch_news(access_key, keywords=None, countries=None, categories=None, limit=100, offset=0, within_days=1):
    base_url = "http://api.mediastack.com/v1/news"


    start_date = datetime.now() - timedelta(days=within_days)
    start_date_str = start_date.strftime('%Y-%m-%d')
    today_str = datetime.now().strftime('%Y-%m-%d')

    params = {
        "access_key": access_key,
        "limit": limit,
        "date": f"{start_date_str},{today_str}"
    }
    
    # Conditionally add parameters if they are not None
    if keywords is not None:
        params["keywords"] = keywords
    if countries is not None:
        params["countries"] = countries
    if categories is not None:
        params["categories"] = categories
    if offset != 0:
        params["offset"] = offset

    print(f"params: {params}")
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises a HTTPError for bad responses
        return response.json()  # Returns the JSON response if successful
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    access_key = os.getenv('MEDIASTACK_API_KEY', '')  # Replace YOUR_ACCESS_KEY with your actual access key

    # You can now call the function with or without the optional parameters
    # news_data = fetch_news(access_key, keywords="tennis", countries="us,gb,de")
    news_data = fetch_news(access_key, categories="technology", countries="us")
    print(news_data)

    # Example calling the function without keywords and countries
    # news_data_no_params = fetch_news(access_key)
    # print(news_data_no_params)
