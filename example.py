import requests
import json

host = 'http://127.0.0.1:5000'

to = '6287859909669-1576979420@g.us' #groupid
#to = '6287859909669@c.us' #chatid

headers = {
	'auth-key': 'WApikey-Kbl9bHg9fKfNtSBA5502hcmNI',
	'client_id': 'WAclient-aB9zKuZoXYVv5VS',
	'username': 'Ryns'
}

def getQr():
	url = host + '/screen'
	a = requests.get(host + '/screen', headers=headers)
	result = host + '/' + a.json()['result']
	return result

def sendMessage(to, text):
	url = host + '/sendMessage'
	data = {
		'chat_id': to,
		'message': text
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()

def sendMention(to, text, userids=[]):
	url = host + '/sendMention'
	data = {
		'chat_id': to,
		'message': text,
		'user_ids': userids
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()

def sendMedia(to, path, caption=''):
	url = host + '/sendMedia'
	data = {
		'chat_id': to,
		'caption': caption
	}
	files ={'files': open(path,'rb')}
	req = requests.post(url, data=data, files=files, headers=headers)
	return req.json()

def setName(name):
	url = host + '/setMyName'
	data = {
		'name': name
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()

def setBio(bio):
	url = host + '/setMyStatus'
	data = {
		'status': bio
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()

def getBio(user_id):
	url = host + '/getBio'
	params = {
		'user_id': user_id
	}
	req = requests.get(url, params=params, headers=headers)
	return req.json()

def getContacts():
	url = host + '/getContacts'
	req = requests.get(url, headers=headers)
	return req.json()

def getMyContacts():
	url = host + '/getMyContacts'
	req = requests.get(url, headers=headers)
	return req.json()

def blockContact(user_id):
	url = host + '/blockContact'
	data = {
		'chat_id': user_id
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()

def unblockContact(user_id):
	url = host + '/unblockContact'
	data = {
		'chat_id': user_id
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()

def getChats():
	url = host + '/getChats'
	req = requests.get(url, headers=headers)
	return req.json()

def getChat(to):
	url = host + '/getChats/' + to
	req = requests.get(url, headers=headers)
	return req.json()

def sendSeen(to):
	url = host + '/sendSeen'
	data = {
		'chat_id': to
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()

def sendReply(message_id, text):
	url = host + '/sendReply'
	data = {
		'message_id': message_id,
		'message': text
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()

def downloadObjMessage(message_id):
	url = host + '/message/' + message_id + '/download'
	req = requests.get(url, headers=headers)
	return req.json()

def loadChat(to):
	url = host + '/chatLoadEarlier'
	data = {
		'chat_id': to
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()

def loadAllChat(to):
	url = host + '/chatLoadAllEarlier'
	data = {
		'chat_id': to
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()

def loadChatStatus(to):
	url = host + '/chatLoadStatus'
	data = {
		'chat_id': to
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()

def getBatteryLevel():
	url = host + '/getBatteryLevel'
	req = requests.get(url, headers=headers)
	return req.json()

def deleteChat(to):
	url = host + '/deleteChat'
	data = {
		'chat_id': to
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()

def unsendMessage(to):
	url = host + '/unsendMessage'
	data = {
		'chat_id': to
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()

def getGroupParticipantsIds(to):
	url = host + '/getGroupParticipantsIds'
	data = {
		'group_id': to
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()

def getGroupParticipants(to):
	url = host + '/getGroupParticipants'
	data = {
		'group_id': to
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()

def getGroupAdminsIds(to):
	url = host + '/getGroupAdminIds'
	data = {
		'group_id': to
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()

def getGroupAdmins(to):
	url = host + '/getGroupAdmins'
	data = {
		'group_id': to
	}
	req = requests.post(url, data=data, headers=headers)
	return req.json()
