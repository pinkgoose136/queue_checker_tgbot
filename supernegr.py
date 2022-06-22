import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import csv
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

URL = 'https://registration.mfa.gov.ua/qmaticwebbooking/#/'

api_key = '5552748824:AAGPQdrxaeSzL7jpqL3nsviPlMFoBLowFbY'
user_id = 981556791

def start(bot, context):
	context.bot.send_message(chat_id=user_id, text="Подождите")
	try:
		seti = webdriver.ChromeOptions()
		
		prefs = {'dom.webdriver.enabled': False,
		'dom.volume_scale.enabled': False,
		'dom.volume_scale': '0.0',
		'dom.useragent.override': 'nie'}

		seti.add_argument("--disable-dev-shm-usage")
		seti.add_argument("--no-sandbox")
		seti.add_argument("--headless")
		seti.add_argument("--private")

		seti.add_argument("start-maximized")
		seti.add_argument("disable-infobars")
		seti.add_argument("--disable-extensions")
		seti.add_argument("--disable-gpu")

		seti.add_experimental_option("prefs", prefs)

		seti.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

		#binary = FirefoxBinary(os.environ.get("FIREFOX_BIN"))

		browser = webdriver.Chrome(
			executable_path=os.environ.get("CHROMEDRIVER_PATH"),
			chrome_options=seti
			)
		#browser.set_window_size(1000, 10000)
		browser.get(URL)
		time.sleep(5)
		table = browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/ul')

		s = browser.find_element(By.XPATH, '//*[@id="branchBroup1"]').click()
		b1 = browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/ul/li[1]/div[2]/div/div[2]/ul/li[1]/div[2]/div/div/div[1]/div/div/div/div').click()
		time.sleep(3)
		b2 = browser.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div/ul/li[2]/div[2]/div/div[2]/div/div/ul/div[1]/div/div/div[1]/div/li[6]/div[1]/div[1]/div/div/div').click()
		b3 = browser.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div/ul/li[3]/div[1]').click()
		time.sleep(3)
		def check():
			b4 = browser.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div/ul/li[3]/div[2]/div/div[2]/div[1]/div/div/div[2]/table')
			bb = b4.find_elements(By.TAG_NAME, "tr")
			for aa in bb:
				ab = aa.find_elements(By.TAG_NAME, "td")
				for aa in ab:
					try:
						o = aa.find_element(By.TAG_NAME, "button")
						to = o.get_attribute("class")
						if to == 'v-btn v-btn--flat v-btn--floating v-btn--disabled theme--light' or to == 'v-btn v-btn--active v-btn--floating v-btn--disabled theme--light':
							pass
						else:
							context.bot.send_message(chat_id=user_id, text=str("Найдено свободное место на: "+o.text))
							print(o.text)
					except:
						pass
			bebe = browser.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div/ul/li[3]/div[2]/div/div[2]/div[1]/div/div/div[1]/button[2]').click()
			time.sleep(3)
		for x in range(3):
			check()
		context.bot.send_message(chat_id=user_id, text="Ничего не обнаружено. Попробуйте позже")
		browser.close()
	except Exception as e:
		print(e)
		context.bot.send_message(chat_id=user_id, text="Произошла ошибка")		

def main():
    print('es')
    TOKEN = "5552748824:AAGPQdrxaeSzL7jpqL3nsviPlMFoBLowFbY"
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

main()