from datetime import datetime

def is_same_day_as_today(date_to_check):
    # Get today's date
    today = datetime.now().date()

    # Compare only the date part of the datetime object
    return date_to_check.date() == today

class UserModel:
    def __init__(self, client) -> None:
        self.client = client
        self.db = self.client.news_db
        self.users = self.db.user_collection
        

    def get_user(self, userId):
        user = self.users.find_one({'userId': userId})
        if not user:
            print(f"User {userId} not found")
            return None
        return user

    def save_user_preferences(self, userId, preferences):
        new_user = self.users.update_one({
            'userId': userId
        }, {
            '$set': { 'preferences': preferences }
        }, upsert=True)

        return new_user

    def update_user_articles(self, userId, articles):
        new_user = self.users.update_one({
            'userId': userId
        }, {
            '$set': { 
                'articles': articles,
                'articlesDate': datetime.now()
             }
        })
        return new_user

    def get_user_articles(self, userId):
        user = self.get_user(userId)

        # User does not exist
        if not user:
            return None
        
        # No articles stored
        if not 'articles' in user or not 'articlesDate' in user:
            return []
        
        # Articles don't match current day
        if not is_same_day_as_today(user['articlesDate']):
            return []
        
        return user['articles']
        
    def save_daily_script(self, userId, script):
        new_user = self.users.update_one({
            'userId': userId
        }, {
            '$set': { 
                'dailyScript': script,
                'scriptDate': datetime.now()
             }
        })
        return new_user
    
    def get_daily_script(self, userId):
        user = self.get_user(userId)


        # User does not exist
        if not user:
            return None
        
        # No articles stored
        if not 'dailyScript' in user or not 'scriptDate' in user:
            return ''
        
        # Articles don't match current day
        if not is_same_day_as_today(user['scriptDate']):
            return ''
        
        return user['dailyScript']
    
    def set_daily_audio(self, userId, audio_url):
        new_user = self.users.update_one({
            'userId': userId
        }, {
            '$set': { 
                'dailyAudioURL': audio_url,
                'dailyAudioDate': datetime.now()
             }
        })
        return new_user
    
    def get_daily_audio(self, userId):
        user = self.get_user(userId)


        # User does not exist
        if not user:
            return None
        
        # No articles stored
        if not 'dailyAudioURL' in user or not 'dailyAudioDate' in user:
            return ''
        
        # Articles don't match current day
        if not is_same_day_as_today(user['dailyAudioDate']):
            return ''
        
        return user['dailyAudioURL']


if __name__ == '__main__':
    users = UserModel()

    print(users.get_user('abc123'))

    preferences = {
        'categories': ['biotech', 'tech']
    }

    users.save_user_preferences('abc123', preferences)

    print(users.get_user('abc123'))

    articles = ['abc123', 'article2!']
    users.update_user_articles('abc123', articles)

    print(users.get_user_articles('abc123'))
