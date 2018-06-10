from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
import logging
import requests
import tables
from bs4 import BeautifulSoup
import csv
def start(bot, update):
	msg='This Telegram Bot is for finding PNR Status.'+'\n'+'Enter your 10 Digit PNR Number.'
	bot.send_message(chat_id=update.message.chat_id, text=msg)
def echo(bot, update):
	pnr=update.message.text
	url="https://www.railyatri.in/pnr-status/"+pnr
	if len(pnr)!=10:
		bot.send_message(chat_id=update.message.chat_id,text="Retry with a valid PNR Number")
	else:	
		r=requests.get(url)
		soup = BeautifulSoup(r.content, 'html5lib')
		table=soup.find('div', attrs = {'class':'pnr-search-result-info'})
		if not table:
			bot.send_message(chat_id=update.message.chat_id,text="Retry with a valid PNR Number")
		else:
			train_booking='Booking Status:'
			train_name='Train Name:'
			train_from='From:'
			train_to='To:'
			train_date='Journey Date:'
			train_class='Class:'
			train_status='Current Status:'
			t=1
			for row in table.findAll('p',attrs={'class':'pnr-bold-txt'}):
				name=row.text
				if t==1:
					train_name=train_name+name
				elif t==2:
					train_from=train_from+name
				elif t==3:
					train_to=train_to+name
				elif t==4:
					train_date=train_date+name
				elif t==5:
					train_class=train_class+name
				t=t+1
			t=1	
			table=soup.find('div', attrs = {'id':'status'})	
			for row in table.findAll('p',attrs={'class':'pnr-bold-txt'}):
				if t==2:
					train_status=train_status+row.text
				elif t==1:
					train_booking=train_booking+row.text	
				t=t+1	
			pnr_info=train_booking+'\n'+train_status+'\n'+train_name+'\n'+train_from+'\n'+train_to+'\n'+train_date+'\n'+train_class
			bot.send_message(chat_id=update.message.chat_id,text=pnr_info)
			bot.send_message(chat_id=update.message.chat_id,text="Enter your PNR Number")	
updater=Updater(token='452137950:AAERj2f0RXcyWbbxde3Eg7vSEPYeo6wH5uk')
dispatcher=updater.dispatcher
logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',level=logging.INFO)		
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)