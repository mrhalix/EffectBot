# -*- coding: utf-8 -*-

# 2017 Mrhalix
# all rights reserved

from PIL import Image
from PIL import ImageFilter

import telebot, urllib
from telebot import types

API_TOKEN = 'XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

#Just these filters works
filters = ['BLUR', 'CONTOUR', 'DETAIL', 'EDGE_ENHANCE', 'EDGE_ENHANCE_MORE', 'EMBOSS', 'FIND_EDGES', 'SMOOTH', 'SMOOTH_MORE', 'SHARPEN']
bot = telebot.TeleBot(API_TOKEN)

#Receiving callback querys
@bot.callback_query_handler(func=lambda call: True)
def callback_handle(call):
	matches = call.data.split(" ")
	uid = matches[0]
	filter = matches[1]
	bot.send_chat_action(call.from_user.id, "upload_photo")
	im0 = Image.open("temp/{}.jpg".format(call.from_user.id))
	
	if filter == "BLUR":
		im = im0.filter(ImageFilter.GaussianBlur(radius=5))
	elif filter == "CONTOUR":
		im = im0.filter(ImageFilter.CONTOUR)
	elif filter == "DETAIL":
		im = im0.filter(ImageFilter.DETAIL)
	elif filter == "EDGE_ENHANCE":
		im = im0.filter(ImageFilter.EDGE_ENHANCE)
	elif filter == "EDGE_ENHANCE_MORE":
		im = im0.filter(ImageFilter.EDGE_ENHANCE_MORE)
	elif filter == "EMBOSS":
		im = im0.filter(ImageFilter.EMBOSS)
	elif filter == "FIND_EDGES":
		im = im0.filter(ImageFilter.FIND_EDGES)
	elif filter == "SMOOTH":
		im = im0.filter(ImageFilter.SMOOTH)
	elif filter == "SMOOTH_MORE":
		im = im0.filter(ImageFilter.SMOOTH_MORE)
	elif filter == "SHARPEN":
		im = im0.filter(ImageFilter.SHARPEN)
	else:
		bot.reply_to(msg, "unknown filter 😨")
		
	im.save("temp/filtered/{}.jpg".format(call.from_user.id))
	bot.answer_callback_query(call.id, text="Success")
	bot.send_photo(call.message.chat.id, open("temp/filtered/{}.jpg".format(call.from_user.id)))
	
#handeling /start
@bot.message_handler(commands=['start'])
def send_welcome(msg):
	markup = types.InlineKeyboardMarkup()
	start_bt = types.InlineKeyboardButton('📞Contact📞', url="http://telegram.me/noobsag")
	markup.add(start_bt)
	bot.reply_to(msg, u"Welcome {} Just send your photo.".format(msg.from_user.first_name), reply_markup=markup)

#Processing photos
@bot.message_handler(content_types=['photo'])
def photo_received(msg):
	#Downloading photo
	FILEID = msg.photo[1].file_id
	file_info = bot.get_file(FILEID)
	urllib.urlretrieve('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path), "temp/{}.jpg".format(msg.from_user.id))
	
	#Sending Message
	markup = types.InlineKeyboardMarkup()
	for i in filters:
		bt = types.InlineKeyboardButton(i, callback_data="{} {}".format(msg.from_user.id, i))
		markup.add(bt)
	bot.reply_to(msg, "[Choose one and Enjoy](http://t.me/mrhalix)\nthis is beta and more colors soon,\nfriend if you want contact with me click [HERE](https://t.me/noobsag)", parse_mode="markDown", reply_markup=markup, disable_web_page_preview=True)

bot.polling()

# COPYRIGHT Mrhalix
