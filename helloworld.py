import requests
import json
import os
import shutil

host = 'https://wa.boteater.us/api'
#host = 'http://161.117.248.234:1234/api'
#host = 'http://127.0.0.1:5000/api'

to = '6287859909669-1576979420@g.us'

myId = '6287859909669@c.us'

headers = {
    'apikey': 'WApikey-Kbl9bHg9fKfNtSBA5502hcmNI',
    'userid': 'WAclient-aB9zKuZoXYVv5VS',
    'username': 'Ryns'
}

settings = {
    'autoRead': False
}

def downloadFileWithURL(url, filename):
    files = open(filename, 'wb')
    resp  = requests.get(url, stream=True)
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, files)
    return filename

def getClient():
    url = host + '/client'
    a = requests.get(url, headers=headers)
    return a

def getQr():
    url = host + '/login'
    a = requests.get(url, headers=headers)
    return a.json()

def sendMessage(to, text):
    url = host + '/sendMessage'
    data = {
        'chat_id': to,
        'message': text
    }
    req = requests.post(url, data=data, headers=headers)
    return req.text

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

def sendMediaWithURL(to, url, filename, caption=''):
    path = downloadFileWithURL(url, filename)
    r = sendMedia(to, path, caption)
    os.remove(path)
    return r

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

def getBatteryLevel():
    url = host + '/getBatteryLevel'
    req = requests.get(url, headers=headers)
    return req.json()

def getGroupParticipantsIds(to):
    url = host + '/getGroupParticipantsIds'
    data = {
        'group_id': to
    }
    req = requests.post(url, data=data, headers=headers)
    return req.json()

def mentionAll(message):
    to = message['chatId']
    if message['chat']['isGroup']:
        result = '╭───「 Mention Members 」\n'
        no = 0
        members = getGroupParticipantsIds(message['chatId'])['result']
        if myId in members:
            members.remove(myId)
        for member in members:
            no += 1
            result += '│ %i. @%s\n' % (no, member.replace('@c.us',''))
        result += '╰───「 Hello World 」\n'
        sendMention(to, result, members)
    else:
        sendMessage(to, 'Group only!')

print(getClient().text)

qr = getQr()

if 'url' in str(qr['result']):
    print('Please scan this QR\n\nQR: ' + str(qr['result']['url']))

callback = requests.get(qr['result']['callback'], headers=headers)

def check_m(include_me=True, include_notifications=True):
    
    if 'LoggedIn' in str(callback.text):
        while True:
            data = {
                'include_me': include_me,
                'include_notifications': include_notifications
            }
            req = requests.post(host + '/unread', data=data, headers=headers)
            if req.json()['result'] == []:
                pass
            else:
                try:
                    print(req.json()['error'])
                except:
                    pass
                for contact in req.json()['result']:
                    for message in contact['messages']:
                        try:
                            cont = str(message['content'][0:25])
                        except:
                            cont = 'None'
                        print('new message - {} from {} message {}...'.format(str(message['type']), str(message['sender']['formattedName']), cont))
                        try:
                            sender_id = message['sender']['id']
                        except:
                            sender_id = "None"
                        try:
                            chat_id = message['chatId']
                        except:
                            chat_id = sender_id

                        if settings['autoRead']:
                            sendSeen(to)

                        if message['type'] == 'chat':
                            text = message['content']
                            txt  = text.lower()
                            cmd  = text.lower()
                            to   = chat_id
                            sender = sender_id
                            msg_id = message['id']

                            if txt == 'tag':
                                mentionAll(message)
                            elif txt == 'status':
                                sendReply(msg_id, 'Alive Gan')
                            elif txt == 'battery':
                                battery = getBatteryLevel()
                                sendMessage(to, battery['result'])
                            elif txt == 'me':
                                nomer = sender.replace('@c.us','')
                                sendMention(to, '@' + nomer, [sender])
                            elif txt == 'author pict':
                                sendMediaWithURL(to, 'https://i.ibb.co/dBsw1Xf/photo-2019-10-28-18-07-44.jpg', 'pict.jpg')
                            elif txt == 'autoread on':
                                if settings['autoRead']:
                                    sendMessage(to, 'auto read telah di aktifkan')
                                else:
                                    settings['autoRead'] = True
                                    sendMessage(to, 'Berhasil mengaktifkan autoread')
                            elif txt == 'autoread off':
                                if not settings['autoRead']:
                                    sendMessage(to, 'auto read telah nonaktif')
                                else:
                                    settings['autoRead'] = False
                                    sendMessage(to, 'Berhasil menonaktifkan autoread')
    else:
        print(qr)


check_m()
