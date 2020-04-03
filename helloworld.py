import requests
import json
import os
import shutil

host = 'https://wa.boteater.us/api'

to = '6287859909669-1576979420@g.us'

myId = '6287859909669@c.us'

headers = {
    'apikey': 'YOUR APIKEY',
    'userid': 'YOUR USER ID',
    'username': 'YOUR USERNAME'
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

try:
    print('Scan this QR : ', qr['result']['qr-callback'])
except:
    print('Trying to login')

callback = requests.get(qr['result']['callback'], headers=headers)

print(callback.text)

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
                            
                        if message['subtype'] == 'invite' or message['subtype'] == 'add':
                            if myId in message['recipients']:
                                sendMention(to, 'Hello @{} Thanks for invited me'.format(message['author'].replace('@c.us','')), [message['author']])
                            else:
                                for recipient in message['recipients']:
                                    sendMention(to, 'Halo @{} Selamat datang di {}'.format(recipient.replace('@c.us',''),message['chat']['contact']['name']), [recipient])

                        if message['type'] == 'chat':
                            text = message['content']
                            txt  = text.lower()
                            cmd  = text.lower()
                            to   = chat_id
                            sender = sender_id
                            msg_id = message['id']

                            if txt == 'tag':
                              if sender == myId:
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
                            elif txt.startswith("topik_alquran: "):
                                sep = text.split(" ")
                                textnya = text.replace(sep[0] + " ","")
                                result = requests.get("https://api.haipbis.xyz/searchqurdis?q={}".format(textnya))
                                data = result.json()
                                ret_ = "╭──[ TOPIK AL-QUR'AN & HADITS ]"
                                ret_ += "\n├⌬ Ayat Qur'an : "+str(data[0]['quran/hadis'])
                                ret_ += "\n├⌬ Sumber : "+str(data[0]['link'])
                                ret_ += "\n├⌬ Isi Al-Qur'an: "
                                ret_ += "\n├⌬     Bahasa Arab : "+str(data[0]['teks']['arab'])
                                ret_ += "\n├⌬     Bahasa Latin : "+str(data[0]['teks']['latin'])
                                ret_ += "\n╰───────[ Bismillah ]"
                                sendMessage(to, str(ret_))
                            elif txt.startswith("musik:"):
                                proses = text.split(" ")
                                urutan = text.replace(proses[0] + " ","")
                                r = requests.get("https://api.fckveza.com/mp3={}".format(urutan))
                                data = r.text
                                data = json.loads(data)
                                ret_ = "╭──[ Musik MP3 ]"
                                ret_ += "\n├⋄ Title : {}".format(str(data["judul"]))
                                ret_ += "\n├⋄ Album : {}".format(str(data["album"]))
                                ret_ += "\n├⋄ Penyanyi : {}".format(str(data["penyanyi"]))
                                ret_ += "\n╰──[ Finish ]"
                                sendMediaWithURL(to, str(data["linkImg"]), 'pict.jpg', caption=ret_)
                                sendMediaWithURL(to, str(data["linkMp3"]), 'music.mp3')                                
                            elif txt == 'corona':
                                r=requests.get("https://api.kawalcorona.com/indonesia")
                                data=r.text
                                data=json.loads(data)
                                ret_ = "「 COVID-19」"
                                ret_ += "\nCountry : *{}*".format(str(data[0]["name"]))
                                ret_ += "\nVictims : *{}*".format(str(data[0]["positif"]))
                                ret_ += "\nRecover : *{}*".format(str(data[0]["sembuh"]))
                                ret_ += "\nDeath : *{}*".format(str(data[0]["meninggal"]))
                                sendMessage(to, ret_)
                            elif txt.startswith('corona '):
                                textt = text.replace(text.split(' ')[0] + ' ', '')
                                r=requests.get("https://api.kawalcorona.com/indonesia/provinsi").json()
                                for atr in r:
                                    data = atr['attributes']
                                    if data['Provinsi'].lower() == textt:
                                        res = '「 COVID-19」'
                                        res += '\nProvinsi   : *{}*'.format(data['Provinsi'])
                                        res += '\nVictims    : *{}*'.format(data['Kasus_Posi'])
                                        res += '\nRecover    : *{}*'.format(data['Kasus_Semb'])
                                        res += '\nKasus_Meni : *{}*'.format(data['Kasus_Meni'])
                                        sendMessage(to, res)
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
