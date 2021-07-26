import os
import telebot
import dotenv

dotenv.load_dotenv('.env')
tok = os.environ["API_KEY"]
bot = telebot.TeleBot(tok) #token

# telebot.apihelper.proxy = {'https': 'socks5h://<host>:<port>'}

# with open("file_name.mp4", mode='rb') as f:
#     	bot.send_video(chat_id, videonote)
# pp = telegram.utils.request.Request(proxy_url='PROTOCOL://IP:SOCKET') # use any free proxy ip:socket
# bot = telegram.Bot(token=tok, request=pp)
@bot.message_handler(commands=['greet'])
def start_command(message):
    bot.send_message(message.chat.id, "Hello!")
    with open("file_name.mp4", mode='rb') as f:
    	print(1)
    	bot.send_video(message.chat.id, f, caption=r"file_name.mp4")
    	print(2)
bot.polling(timeout=999,none_stop=True)

