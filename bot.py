from os.path import isfile
from datetime import datetime, timedelta
import requests, time, os, calendar
import logging

logging.basicConfig(filename="logging.log", level=logging.ERROR)


debug = 1



class Currency:

	def __init__(self, desc_name, coin_name = None, coin_short = None,
				subreddit = None, twitter = None):
		self._desc_name = desc_name 		# Description name
		self._coin_name = coin_name
		self._coin_short = coin_short
		self._subreddit = subreddit
		self._twitter = twitter

		self._subreddit_list = {}
		self._marketcap_list = {}
		self._btc_value = {}
		self._usd_value = {}

	def __str__(self):
		return self._desc_name

	def get_subreddit_list(self):
		return self._subreddit_list

	def get_marketcap_list(self):
		return self._marketcap_list

	def print_information(self):
		print(self._desc_name)

	def read_subreddit_list(self):

		self._subreddit_list = {}
		if isfile('subred_data/'+self._subreddit):
			with open('subred_data/'+self._subreddit, 'r') as file:
				for date_line in file:
						if date_line == '\n':
							continue
						splitlist = date_line.split(' , ')
						self._subreddit_list[splitlist[0]] = splitlist[1].replace('\n', '')
			logging.info("Read file: {}".format(self._subreddit_list))
		else:
			logging.error("No data for " + self._subreddit + ".")

	def read_marketcap_list(self):
		self._marketcap_list = {}
		if isfile('marketcap_data/'+self._coin_short):
			with open('marketcap_data/'+self._coin_short) as file:
				for date_line in file:
					if date_line == '\n':
						continue
					splitlist = date_line.split(' , ')

					self._marketcap_list[splitlist[0]] = splitlist[1] + ' , ' + splitlist[2].replace('\n', '')
					self._btc_value[splitlist[0]] = splitlist[1]
					self._usd_value[splitlist[0]] = splitlist[2].replace('\n', '')

		else:
			logging.debug(f"No marketcap data for {self._desc_name} - data: {self._coin_short}")

	def get_coin_short(self):
		if self._coin_short != 'None':
			return self._coin_short
		return None

	# 0 if today, -1 if yesterday etc.
	def get_date(self, date_num):
		return datetime.strftime(datetime.now() + timedelta(date_num), "%x")

	def calculate_increase(self, pre, post):
		return ((int(post) - int(pre)) / int(pre)) * 100
	
	def get_subr_increase_since(self, date):
		if self.get_date(0) in self._subreddit_list and self.get_date(date) in self._subreddit_list:
			return self.calculate_increase(self._subreddit_list[self.get_date(date)], self._subreddit_list[self.get_date(0)])
		return None


	def print_total_subr_increase(self):
		if self.get_date(-1) in self._subreddit_list:
			print("Increase since yesterday:\t {:.3f}%".format(self.get_subr_increase_since(-1)))
		if self.get_date(-2) in self._subreddit_list:
			print("Increase last 2 days: \t\t {:.3f}%".format(self.get_subr_increase_since(-2)))
		if self.get_date(-7) in self._subreddit_list:
			print("Increase this week:\t\t {:.3f}%".format(self.get_subr_increase_since(-7)))
		if self.get_date(-30) in self._subreddit_list:
			print("Increase this month:\t\t {:.3f}%".format(self.get_subr_increase_since(-30)))

	def update_subreddit(self):
		folder = 'subred_data/'
		if self._subreddit == None or self._subreddit == "None":
			logging.debug(f"Could not update subreddit for {self._desc_name}, subreddit information missing.")
			return

		if not isfile(folder+self._subreddit):
			open(folder+self._subreddit, 'w').close()

		request_string = 'http://www.reddit.com/r/' + self._subreddit +'/about/.json'
		response = requests.get(request_string, headers = {'User-agent': 'floffbot'})
		data = response.json()

		if not self.get_date(0) in self._subreddit_list:
			self._subreddit_list[self.get_date(0)] = str(data['data']['subscribers'])

		file_out = open(folder+self._subreddit, 'w')

		for key in self._subreddit_list:
			file_out.write(key + ' , ' + self._subreddit_list[key] + '\n')

	def update_coin_marketcap(self, data):
		if not self.get_date(0) in self._marketcap_list:
			self._marketcap_list[str(self.get_date(0))] = str(data['BTC']) + " , " + str(data['USD'])
			self._btc_value[str(self.get_date(0))] = str(data['BTC'])
			self._usd_value[str(self.get_date(0))] = str(data['USD'])

		folder = 'marketcap_data/'
		if not isfile(folder + self._coin_short):
			open(folder+self._coin_short, 'w').close()


		file_out = open(folder + self._coin_short, 'w')
		for key in self._marketcap_list:
			#print("Printing + " + str(self._marketcap_list[key]))
			file_out.write(key + ' , ' + str(self._marketcap_list[key]) + '\n')

class Currency_cointainer:

	def __init__(self):
		self._currency_list = []


	def in_currency_list(self, coin):
		for elem in self._currency_list:
			if elem._desc_name == coin._desc_name:
				return True
		return False

	def read_data_list(self):
		logging.debug("Enter: funct read_data_list") 
		with open("datalist.txt", 'r') as file:
			for line in file:
				line = line.replace("\n", "")
				if line == "" or line[0] == "#":
					logging.debug("Found an empty line or comment.")
					continue 

				coindata = line.split(" , ")
				coin = ""
				try:
					coin = Currency(coindata[0], coindata[1], coindata[2], coindata[3], coindata[4])
					coin.read_subreddit_list()
					coin.read_marketcap_list()
				except Exception as e:
					logging.error("Received error message: \n{}\nwhen in read_data_list".format(e))
				
				if not self.in_currency_list(coin):
					self._currency_list.append(coin)

		logging.debug("Exit: funct read_data_list") 
		#print(self._currency_list)
	

	def read_marketcap_list(self):
		logging.debug("Enter: funct read_marketcap_list") 
		
		for coin in self._currency_list:
			coin.read_marketcap_list()

		logging.debug("Exit: funct read_marketcap_list") 
	
	def read_currency_data(self, folder_name):
		print("Nothing here yet.")

	def get_coin_by_name(self, name):
		for currency in self._currency_list:
			if name == currency._desc_name:
				return currency
		return None

	def get_coin_by_ticker(self, ticker):
		for currency in self._currency_list:
			if currency.get_coin_short() != None and currency.get_coin_short().lower() == ticker.lower():
				return currency
		return None

	def test_coin(self, name):
		coin = self.get_coin_by_name(name)
		if coin != None:
			logging.info(coin.print_total_subr_increase())
		else:
			logging.info("Could not test coin with name {}.".format(name))

	def test_print_all(self):
		logging.debug("Enter: funct test_print_all") 
		for coin in self._currency_list:
			print("Subreddit increase for {}".format(coin._desc_name.upper()))
			try:
				print("Todays price (BTC, USD): {} ".format(coin._marketcap_list[coin.get_date(0)]))
			except KeyError as error:
				print("Key error for coin: {}".format(coin))
			coin.print_total_subr_increase()
			print("\n")

		logging.debug("Exit: funct test_print_all") 

	def update_subreddit_data(self):
		logging.debug("Enter: funct update_subreddit_data") 


		for coin in self._currency_list:
			coin.update_subreddit()

		logging.debug("Exit: funct update_subreddit_data") 

	def update_coin_marketcap(self):
		logging.debug("Enter: funct update_coin_marketcap") 
		#response = requests.get("https://www.cryptocompare.com/api/data/coinlist/")
		#data = response.json()
		#data = data['Data']
		ticker_list = []
		ticker_str = ''
		for currency in self._currency_list:
			ticker_name = currency.get_coin_short()
			if ticker_name != None:
				ticker_list.append(ticker_name)
				ticker_str += ',' + ticker_name
		ticker_str = ticker_str[1:]
		string = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms=BTC,USD'.format(ticker_str)		
		#print(ticker_str)
		response = requests.get(string)
		data = response.json()
		#print(data)

		for key in data:
			coin = self.get_coin_by_ticker(key)
			if coin == None:
				logging.error("Could not find data for {}.".format(key))
				continue

			coin.update_coin_marketcap(data[key])

		logging.debug("Exit: funct update_coin_marketcap") 


def main():
	print("\n\n")
	container = Currency_cointainer()
	
	while True:
		os.system('clear')
		update_time = 30
		try:
			container.read_data_list()
			container.read_marketcap_list()
			container.update_subreddit_data()
			container.update_coin_marketcap()
			#container.test_print_all()
		except requests.ConnectionError:
			logging.error("No connection. Trying again in {} minutes.".format(update_time))

		#print("{}\t{}".format(datetime.strftime(datetime.now(), '%x'), time.strftime("%H:%M:%S")))
		#print("Sleeping...")
		#time.sleep(60 * update_time)
		#print("Finished sleeping: \n")
		#print("{}\t{}".format(datetime.strftime(datetime.now(), '%x'), time.strftime("%H:%M:%S")))
		break
	#print("Epoch time: {}".format(calendar.timegm(time.gmtime())))
	logging.debug("Finished logging at: {} {}".format(datetime.strftime(datetime.now(), '%x'), time.strftime("%H:%M:%S")))

if __name__ == '__main__':
	main()

