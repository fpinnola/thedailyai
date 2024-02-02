
class SourcesModel:
    def __init__(self, client) -> None:
        self.client = client
        self.db = self.client.news_db
        self.scrape_sources = self.db.scrape_sources
    

    def time_since_scrape(self, sourceId):
        source = self.scrape_sources.find_one({'sourceId': sourceId})
        if not source:
            print(f"Source {sourceId} not found")
            return None
        return source['lastScrape']
    
    def update_since_scrape(self, sourceId, scrape_time):
        new_source = self.scrape_sources.update_one({
            'sourceId': sourceId
        }, {
            '$set': { 'lastScrape': scrape_time }
        }, upsert=True)
        return new_source