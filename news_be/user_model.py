from datetime import datetime

import bcrypt

from utils import is_within_n_hours

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
    
    def user_to_json(self, user):
        return {
            "userId": user["userId"],
            "preferences": user.get('preferences', {})
        }
    
    def create_user(self, username, password):
         # Check if the user already exists
        if self.users.find_one({"userId": username}):
            return {"error": "Username already exists"}
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert new user into the database
        result = self.users.insert_one({
            "userId": username,
            "password": hashed  # In a real application, make sure to hash this before storing
        })

        # Retrieve the new user to return as JSON
        new_user = self.users.find_one({"_id": result.inserted_id})

        return self.user_to_json(new_user)

    def validate_user(self, username, password):
        # Find the user in the database by username
        user = self.users.find_one({"userId": username})

        if not user:
            # User not found
            return {"error": "Invalid username or password"}

        # Check if the password is correct
        hashed = user['password']
        if bcrypt.checkpw(password, hashed):
            # Password is correct
            return {"message": "User validated successfully"}
        else:
            # Password is incorrect
            return {"error": "Invalid username or password"}

    def save_user_preferences(self, userId, preferences):

        print(f"updating {userId} with {preferences}")
        user = self.get_user(userId)

        if not user:
            return {"error": "user not found"}

        new_user = self.users.update_one({
            'userId': userId
        }, {
            '$set': { 'preferences': preferences }
        }, upsert=False)

        return self.user_to_json(self.get_user(userId))


    def update_user_articles(self, userId, articles):
        print(f"upatading user {userId} with {len(articles)} articles")
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
        if not is_within_n_hours(user['articlesDate'], 8):
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
    
    def add_engagement(self, userId, articleId, action):
        
        try:
            user = self.users.find_one({'userId': userId})
            if user:
                engagement_found = False
                if 'engagements' in user:
                    for engagement in user['engagements']:
                        if engagement['articleId'] == articleId:
                            # Engagement found, add action if not already present
                            self.users.update_one(
                                {'userId': userId, 'engagements.articleId': articleId},
                                {'$push': {'engagements.$.actions': action}}
                            )
                            engagement_found = True
                            break
                    
                if not engagement_found:
                    # Add new engagement
                    new_engagement = {'articleId': articleId, 'actions': [action]}
                    self.users.update_one(
                        {'userId': userId},
                        {'$push': {'engagements': new_engagement}},
                        upsert=True  # This creates the document if it doesn't exist
                    )
                return {"message": "success"}
            else:
                print(f"User with id {userId} not found.")
                return {"error": "User not found"}

        except Exception as e:
            return {"error": f"Error: {e}"}

