from os import remove
import telebot
import json
import gtts
from textblob import TextBlob
admins =["1961668796" , "989490846" , "7616867" ,"880941250"]
all_data = { 
    "user_id":[], 
    "joined_channel":[],
    "groupe_or_channel_of_users": {},
}

def get_ids(type_of_id):
    users_id = []
    file = open("data.json",'r')
    data =json.loads( file.read())
    file.close()
    for i in data["{}".format(type_of_id)]:
        users_id.append(i)
    return users_id
    
def check_user(user_id,state ):
    file = open("data.json",'r')
    data =json.loads( file.read())
    file.close()
    data["user_id"][str(user_id)] = state
    file = open("data.json",'w')
    data = json.dumps(data)
    file.write(data)
    file.close()
    return state

def add_chat_id(chat_id):
    file = open("data.json",'r')
    data =json.loads( file.read())
    file.close()
    if str(chat_id) not in data["groupe_or_channel_of_users"]:
        data["groupe_or_channel_of_users"].append(str(chat_id))
        file = open("data.json",'w')
        data = json.dumps(data)
        file.write(data)
        file.close()
     
# def add_groupe_or_channel(user_id,group_or_channel_id):
#     file = open("data.json",'r')
#     data =json.loads( file.read())
#     file.close()@text_to_speech_en_bot
#     if str(user_id) in data["groupe_or_channel_of_users"]:
#         data["groupe_or_channel_of_users"][str(user_id)].append(str(group_or_channel_id))
#     else:
#         data["groupe_or_channel_of_users"][str(user_id)]=lis[str(group_or_channel_id)]

    #Englishvibesnow
channel_to_sub = "@Englishvibesnow"
bot = telebot.TeleBot('5081120757:AAHnN8FKIi0MoyEDB_LVP0xurTuwIERbUwk')
hello_message = """
مرحبا بك في بوت إنجلش ڤايبز الناطق بالإنجليزية!

- دوّن الكلمة الإنجليزية في الخاص مباشرةً واستمع لنطقها السليم،
- في المجموعات لابد من استخدام الأمر
/say 
متبوعًا بالكلمة الإنجليزية المراد التعرف على نطقها؛ مثال: 

/say Hello


"""
just_english = """
ادخل كلمة أو نصًا باللغة الإنجليزية فقط!
"""

channel_link = """ 
مرحبًا! 
 لتتمكن من استخدام بوت إنجلش ڤايبز الناطق بالإنجليزية؛ يتعين عليك الاشتراك في القناة: 

{}

ثم أرسل مجددًا:  start/

""".format(channel_to_sub)
just_admins = """
هذه الأوامر فقط لمالكي البوت

"""


#handle if there a post in a channel or not for converting the text to speech
@bot.channel_post_handler(content_types=['text'])
def channel(message):
    if "/say" in message.text:
        txt_2_speech = message.text.replace("/say","")
        language = TextBlob(txt_2_speech)
        language = str(language.detect_language())
        if language =="en":
            tts = gtts.gTTS(txt_2_speech,lang='en')
            if len(txt_2_speech.strip().split(' ')) > 1:
                file_name = "Sentence"
            else:
                file_name = txt_2_speech
            tts.save("{}.mp3".format(file_name))
            audio_file = open("{}.mp3".format(file_name),'rb')
            bot.send_voice(message.chat.id ,audio_file,reply_to_message_id=message.message_id)
            audio_file.close()
            remove("{}.mp3".format(file_name))
        else:
            bot.send_message(message.chat.id, just_english ,reply_to_message_id=message.message_id)

# the first command
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == "private" :
        state = bot.get_chat_member(channel_to_sub ,message.from_user.id).status
        state =  state!="left"
        result =check_user(message.from_user.id , state)
        if not result : 
            bot.send_message(message.chat.id, channel_link) 
        else : 
            bot.send_message(message.chat.id , hello_message)
# handle the command /read in a groupe and private
@bot.message_handler(commands=['say'])
def read_text(message):
    try:
        if message.chat.type !="private":
            state = bot.get_chat_member(channel_to_sub ,message.from_user.id).status
            state =  state!="left"
            state =True
            if state :
                file_name = ""
                txt_2_speech = message.text.replace("/say","")
                print(len(txt_2_speech))
                language = TextBlob(txt_2_speech)
                language = str(language.detect_language())
                if language =="en":
                    tts = gtts.gTTS(txt_2_speech,lang='en')
                    if len(txt_2_speech.strip().split(' ')) > 1:
                        file_name = "Sentence"
                    else:
                        file_name = txt_2_speech
                    tts.save("{}.mp3".format(file_name))
                    audio_file = open("{}.mp3".format(file_name),'rb')
                    bot.send_voice(message.chat.id ,audio_file,reply_to_message_id=message.message_id)
                    audio_file.close()
                    remove("{}.mp3".format(file_name))
                else:
                    bot.send_message(message.chat.id, just_english ,reply_to_message_id=message.message_id)
            else : 
                bot.send_message(message.chat.id , channel_link)
        else:
            bot.send_message(message.chat.id , "قم بإرسال الرسالة بدون /say ")
    except:
        pass

# handle if a bot was adden to a groupe or channel
@bot.my_chat_member_handler(func=lambda message  :message )
def ss(message):
    try:
        # print(message.chat.id)
        # print(message.from_user.id)
        s=bot.get_chat_member(channel_to_sub ,message.from_user.id).status
        if s =="left":
            bot.send_message(message.chat.id ,channel_link )
            bot.leave_chat(message.chat.id)
        else:
            if  not message.new_chat_member.status =="left" and not message.new_chat_member.status =="kicked":
                add_chat_id(message.chat.id)
            print(s , message.chat.id)
            bot.send_message(message.chat.id ,text = hello_message)

    except: 
        pass

# @bot.message_handler(commands=['help'])
# def help(message):
#     if str(message.from_user.id) in admins:
#         bot 

@bot.message_handler(commands=['send_pri'])
def send_private(message):
    if str(message.from_user.id) in admins:
        text = message.text.replace("/send_pri","")
        users_id = get_ids("user_id")
        for id in users_id:
            try: 
                bot.send_message(id , text);
            except:
                pass
    else : 
        bot.send_message(message.chat.id , just_admins ,reply_to_message_id=message.message_id)
#send message to groups and channels 
@bot.message_handler(commands=['send_n_pri'])
def send_not_private(message):

    if str(message.from_user.id) in admins:
        text = message.text.replace("/send_n_pri","")
        groups_and_channel_id = get_ids("groupe_or_channel_of_users")
    
        for id in groups_and_channel_id:
            try: 
                bot.send_message(id , text);
            except:
                pass
    else : 
        bot.send_message(message.chat.id ,just_admins ,reply_to_message_id=message.message_id)
#send message to groups , channels and praivet users         
@bot.message_handler(commands=['send_all'])
def send_not_private(message):
    if str(message.from_user.id) in admins:
        text = message.text.replace("/send_all","")
        groups_and_channel_id = get_ids("groupe_or_channel_of_users")
        users_id = get_ids("user_id")
        for id in groups_and_channel_id:
            try: 
                bot.send_message(id , text);
            except:
                pass
        for id in users_id:
                try: 
                    bot.send_message(id , text);
                except:
                    pass
    else : 
        bot.send_message(message.chat.id ,just_admins ,reply_to_message_id=message.message_id)

    
@bot.message_handler(content_types=['text'])
def reply_message(message):
    
    try:
        if message.chat.type =='private'  :
            state = bot.get_chat_member(channel_to_sub ,message.from_user.id).status
            print(state)
            state =  state!="left"
            
            if str(message.from_user.id) in admins or state:
                file_name=""
                txt_2_speech = message.text 
                try:
                    print(len(message.text))
                    language = TextBlob("{}.".format(txt_2_speech))
                    language = str(language.detect_language())
                except:
                    bot.send_message(message.chat.id , "يجب ان يكون طول الكلمة اكبر من 3 احرف")
                print(language)
                if language =="en":
                    tts = gtts.gTTS(txt_2_speech,lang='en')
                    if len(txt_2_speech.strip().split(' ')) > 1:
                        file_name = "Sentence"
                    else:
                        file_name = txt_2_speech
                    tts.save("{}.mp3".format(file_name))
                    audio_file = open("{}.mp3".format(file_name),'rb')
                    bot.send_voice(message.chat.id ,audio_file,reply_to_message_id=message.message_id)
                    audio_file.close()
                    remove("{}.mp3".format(file_name))
                else:
                    bot.send_message(message.chat.id ,  just_english ,reply_to_message_id=message.message_id )
            else:
                bot.send_message(message.chat.id, text = channel_link)
        
    except:
        pass
#Sentence

#send message to private users


print("working bot2 ...")

bot.polling(True)

