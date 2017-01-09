import requests
import json
import os
app_id=os.environ["APP_ID"]
app_secret=os.environ["APP_SECRET"]
url="https://graph.facebook.com/v2.6/146188872068143/posts/?fields=permalink_url,link,message,picture \
		&limit=5&access_token="+app_id+"|"+app_secret

def main():
	bubble_list = list()
	data=requests.get(url)
    	data1=json.loads(data.text)
    	for post in data1['data']:
        	

        	link=post['permalink_url'] if 'link' not in post.keys() else post['link']

        	subtitle='not found' if 'message' not in post.keys() else post['message']

        	image_url='http://awaaziitkgp.org/logo.png' if 'picture' not in post.keys() else post['picture']
        	bubble_list.append({"title": "Awaaz,IIT Kharagpur", "subtitle": subtitle, "image_url": image_url,"default_action": {"type": "web_url","url": link}})
	
	return bubble_list
