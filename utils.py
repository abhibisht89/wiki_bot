from wit import Wit 
import wikipedia as wk

access_token = ""

client = Wit(access_token = access_token)


def wit_response(message_text):
	resp = client.message(message_text)
	#print("response is:"+str(resp))
	if not resp['entities']:
		return "Please ask something like:\nTell me something about "+message_text+"\nWho is "+message_text+"\nWhat is "+message_text
	else:	
		#print("next response is:"+str(resp['entities']['wikipedia_search_query'][0]['value']))
		return (resp['entities']['wikipedia_search_query'][0]['value'])


def get_wiki_content(categories):
	try:
		listoption=''
		title=wk.search(categories)[0]
		page=wk.page(title)
		urlinfo=page.url
		content=wk.summary(categories).splitlines()
		#print(content,urlinfo)
		return content ,urlinfo
	except:	
		topics = wk.search(categories)
		initial='Please be specific '+categories+" may refer to: "
		for i, topic in enumerate(topics):
			if i==0:
			   continue
			listoption=listoption+str(i)+' '+ topic+' '+'\n'
	return initial +'\n'+listoption,'Search from above recommendation.'
