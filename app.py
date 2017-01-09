import os
import sys
import json
import latest_news
import requests
from flask import Flask, request

import apiai
app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events
    add_get_started_button()
    add_persistent_menu()
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    req=requests.get("http://awaaziitkgp.org/test/chatbot/index.php",params={"action":"view","sender_id":messaging_event["sender"]["id"]})
                    if(req.text!='false'):
                    	postback(sender_id,req.text,message_text)

                    else:
                    	message=apiai_call(message_text)

                    	send_message(sender_id, message)


                if messaging_event.get('postback'):
                        payload_text = messaging_event["postback"][
                            "payload"]  # the payload's text
                        if payload_text == 'PLACEMENT':
                            user_details = get_user(
                                messaging_event["sender"]["id"])
                            try:
                                msg = "Hello {} , Please enter company name".format(user_details['first_name'])
                            except KeyError:
                                msg = "Please enter company name"
         
                            send_message(messaging_event["sender"]["id"],msg)
                            requests.get("http://awaaziitkgp.org/test/chatbot/index.php",params={"action":"add","sender_id":messaging_event["sender"]["id"],"flag":"placement"})
                            
                            # ---------**************************__-------------
                            log("Changing value of flag")
                        elif payload_text == 'GET_STARTED_PAYLOAD':
                            user_details = get_user(
                                messaging_event["sender"]["id"])
                            try:
                                msg = "Welcome from Awaaz, What do you want to know {} ?".format(user_details['first_name'])
                            except KeyError:
                                msg = "Welcome from Awaaz, What do you want to know ?"
                            send_message(messaging_event["sender"]["id"], msg)
                        elif payload_text == "PAYLOAD_RECRUIT":
                            user_details = get_user(
                                messaging_event["sender"]["id"])
                            try:
                                msg = "Please follow our facebook page."
                            except KeyError:
                                msg = "Error occurred."
                            send_message(messaging_event["sender"]["id"], msg)
                        elif payload_text == "LATEST_NEWS":
                            user_details = get_user(
                                messaging_event["sender"]["id"])
                            
                            

                            try:
                                msg = "Latest news are here."

                                bubble_list = latest_news.main()

                                sending_generic_template(
                                    messaging_event["sender"]["id"], bubble_list)



                            except KeyError:
                                msg = "Something went wrong."
                            send_message(messaging_event["sender"]["id"], msg)
                                
                           





                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def add_get_started_button():
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps(
        {
            "setting_type": "call_to_actions",
            "thread_state": "new_thread",
            "call_to_actions": [
                {
                    "payload": "GET_STARTED_PAYLOAD"
                }
            ]
        }
    )
    r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings",
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        error_msg = "Got following error while adding get started button:\nStatus Code : {}\nText : {}".format(
            r.status_code, r.text)
        
        log(r.status_code)
        log(r.text)


def add_persistent_menu():
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
                      "setting_type": "call_to_actions",
                      "thread_state": "existing_thread",
                      "call_to_actions": [
                          {
                              "type": "postback",
                              "title": "Latest News",
                              "payload": "LATEST_NEWS"
                          },
                          {
                              "type": "postback",
                              "title": "Recruitment",
                              "payload": "PAYLOAD_RECRUIT"
                          },
                          {
                              "type": "postback",
                              "title": "Placement data",
                              "payload": "PLACEMENT"
                          },
                          {
                              "type": "web_url",
                              "title": "View Website",
                              "url": "http://awaaziitkgp.org/"
                          }
                      ]
                      })
    r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings",
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        error_msg = "Got following error while adding persistent menu:\nStatus Code : {}\nText : {}".format(
            r.status_code, r.text)
        
        log(r.status_code)
        log(r.text)



def sending_generic_template(recipient_id, result_list):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps(
        {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": result_list
                    }
                }
            }
        })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        error_msg = "Got following error while sending generic template:\nStatus Code : {}\nText : {}".format(
            r.status_code, r.text)
        slack_notification(error_msg)
        log("in sending_generic_template : {}".format(r.status_code))
        log(r.text)



def postback(sender_id,flag,msg):
	if(flag=='placement'):
		req=requests.get("http://awaaziitkgp.org/test/chatbot/placement.php",params={"company":msg})
		send_message(sender_id,req.text)















def get_user(sender_id):
    '''
    The user_details dictionary will have following keys
    first_name : First name of user
    last_name : Last name of user
    profile_pic : Profile picture of user
    locale : Locale of the user on Facebook
    '''
    base_url = "https://graph.facebook.com/v2.6/{}?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token={}".format(
        sender_id, os.environ["PAGE_ACCESS_TOKEN"])
    user_details = requests.get(base_url).json()
    return user_details


def apiai_call(message):
    ai = apiai.ApiAI(os.environ["APIAI_CLIENT_ACCESS_TOKEN"])
    request = ai.text_request()
    request.query = message
    response = request.getresponse()
    response_json = json.loads(response.read().decode('utf-8'))
    return response_json['result']['fulfillment']['speech']






















def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
