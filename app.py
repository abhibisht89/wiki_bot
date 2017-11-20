import os, sys
from flask import Flask, request
from utils import wit_response,get_wiki_content
import json
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = ""


@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200   
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	#log(body)
	try:
		if data['object'] == 'page':
			for entry in data['entry']:
				for messaging_event in entry['messaging']:

					# IDs
					sender_id = messaging_event['sender']['id']
					recipient_id = messaging_event['recipient']['id']

					if messaging_event.get('message'):
						# Extracting text message
						if 'text' in messaging_event['message']:
							messaging_text = messaging_event['message']['text']
						else:
							messaging_text = 'no text'

						#print("messaging_text:"+messaging_text)
						greetlist=['hi','hii','hiii','hello','helloo','hey']
						if(messaging_text.lower() in greetlist):
							greetresp='Hi, I am a Wikibot. I can provide you information from Wikipedia. Please ask your question'
							response_content = {
											            "recipient": {
											                "id": sender_id
											            },
											            "message": {
											            "text": greetresp
											            
											            }
											        }
						else :
							#categories = wit_response("hello")
							categories = ""
							#print("categories is:"+categories)
							if categories.startswith('Please'):
								response_content = {
										            "recipient": {
										                "id": sender_id
										            },
										            "message": {
										            "text": categories
										            }
										        }
							else:
								elements,urlinfo= get_wiki_content(messaging_text)
								elements=''.join(str(e) for e in elements)
								#print(elements)
								ele=elements[300:400]
								lst=ele.find('.')
								lst=ele[:lst+1]
								response_content = {
											            "recipient": {
											                "id": sender_id
											            },
											            "message": {
											            "text": elements[:300]+lst +'\n'+'Read More: '+ urlinfo											            
											            }
											        }
						headers = {"Content-Type": "application/json"}
						url = "https://graph.facebook.com/v2.6/me/messages?access_token=%s" % PAGE_ACCESS_TOKEN
						r = requests.post(url, data=json.dumps(response_content), headers=headers)	


	except Exception as ex:
    		print ("main class exp "+str(ex))	

	return "ok", 200

def log(message):
	print(message)
	sys.stdout.flush()


if __name__ == "__main__":
	app.run(debug=True)
