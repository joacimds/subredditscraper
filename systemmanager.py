import os, sys, requests
from datetime import datetime, timedelta
from infocontainers import SubredditContainer, MarketcapContainer, SubredditSentimentAverageContainer, HypePredictor

class SystemManager:

	def ValiDate(date):
		try:
			datetime.strptime(date, '%m/%d/%y')
		except ValueError:
			raise ValueError("Incorrect data format, should be MM/DD/YY")

	def directory_location(self):
		return os.path.dirname(os.path.abspath(sys.argv[0]))

	def __init__(self, init_file=None):
		self._supported_types = {"Subreddit" : SubredditContainer, "Marketcap" : MarketcapContainer, "SubredditSentimentAverage" : SubredditSentimentAverageContainer, "HypePredictor" : HypePredictor}
		
		self._info_containers = {}
		self._marketcap_data = None
		if init_file:
			self._init_from_file(init_file)

	def _init_from_file(self, init_file):
		self.new('HypePredictor', 'CryptoCurrency')
		self.new('HypePredictor', 'CryptoMarkets')

		with open(os.path.join(self.directory_location(), init_file), 'r') as file:
			for line in file:
				data = line.split(",")
				if line.strip()[0] == '#':
					continue
		
				if len(data) < 5:
					continue

				description_name = data[0].strip()  # Plain description
				coin_name = data[1].strip()			# Its name?
				coin_code = data[2].strip()			# Marketcap code
				subreddit = data[3].strip()			# Its subreddit
				twitter = data[4].strip()			# Twitter account
				
				if subreddit != "None" and subreddit != "":
					self.new("Subreddit", subreddit)
					self.new("SubredditSentimentAverage", subreddit)
					pass

				if coin_code != "None" and coin_code != "":
					self.new("Marketcap", coin_code)
					pass

				if twitter != "None" and twitter != "":
					pass
				
				#print("{} - {} - {} - {} - {}".format(description_name, coin_name, coin_code, subreddit, twitter))

	def __str__(self):
		s = "SystemManager: \n"
		for container in self._info_containers:
			s += " {}".format(container)

		return s


	def _create_key(self, container_type, name):
		return "{}-{}".format(container_type, name)

	def supported_types(self):
		return list(self._supported_types.keys())

	def container_keys(self):
		return list(self._info_containers.keys())

	def add(self, container):
		raise AttributeError("Add operation in SystemManager is not supported - use new")

		if str(container) in self._info_containers:
			return False

		self._info_containers[str(container)] = container
		return True

	'''
	Creates a new container_type 
	'''
	def new(self, container_type, name):
		
		key = self._create_key(container_type, name)
		if key in self._info_containers:
			return self._info_containers[key]
		
		elif container_type in self._supported_types:

			new_container = self._supported_types[container_type](self, name)
			self._info_containers[key] = new_container
			return new_container

		#else
		raise ValueError("Incorrect container_type, should be one of {}".format(supported_types.keys()))


	def get(self, container_type, name):
		key = self._create_key(container_type, name)
		if key in self._info_containers:
			return self._info_containers[key]

		return None

	def prettPrint(self):
		for container in self._info_containers.values():
			container.prettyprint()

	def store(self):
		for container in self._info_containers.values():
			container.write_to_file()


	def update(self):
		self._marketcap_data = self._fetch_marketcap()
		assert self._marketcap_data != None, "Performed an update,  but could not fetch marketcap_data"
		for container in self._info_containers.values():
			container.update()

	# Quickfix to lessen the cryptocompare API calls
	def _fetch_marketcap(self):
		ticker_list = []
		marketcap_datas = []
		for container in self._info_containers.values():
			if container.get_container_type() == "Marketcap":
				ticker_list.append(container.get_ticker_id())
		
		i = 30

		while i < len(ticker_list):
			ticker_list_2 = ticker_list[i-30:i]
			ticker_str = ",".join(ticker_list_2)
			string = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms=BTC,USD'.format(ticker_str)		
			response = requests.get(string)
			data = response.json()
			marketcap_datas.append(data)

			i += 30
		
		return marketcap_datas

	def get_marketcap_data(self, ticker_id):
		assert self._marketcap_data != None
		for response in self._marketcap_data:
			if ticker_id in response:
				return response[ticker_id]

		print("Did not fint {}".format(ticker_id))
		return None