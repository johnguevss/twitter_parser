import os

MY_S3_BUCKET='<write your bucket uri here>'
TWITTER_USER='<write twitter user here>'
EMAIL_RECIPIENT='jrguevarra.21@gmail.com'

access_key = os.environ.get("TWITTER_API_KEY") 
access_secret = os.environ.get("TWITTER_API_SECRET")
consumer_key = os.environ.get("TWITTER_ACCESS_TOKEN")
consumer_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")