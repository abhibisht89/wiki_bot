from wit import Wit 
import wikipedia as wk

access_token = "" #paste here your wit.ai app Server Access Token

client = Wit(access_token = access_token)

def wit_response(message_text):
	resp = client.message(message_text)
	print("response is:"+str(resp))
	if not resp['entities']:
		return "Please ask something like:\nTell me something about "+message_text+"\nWho is "+message_text+"\nWhat is "+message_text
	else:	
		print("next response is:"+str(resp['entities']['wikipedia_search_query'][0]['value']))
		return (resp['entities']['wikipedia_search_query'][0]['value'])


def get_wiki_content(categories):

	try:
		title=wk.search(categories)[0]
		page=wk.page(title)
		content=wk.summary(categories).splitlines()
		print(content)
		return content

	except Exception as ex:	
		print ("util class exp"+str(ex))
		return "I have more that one reuslt for your search query,Please be specific."