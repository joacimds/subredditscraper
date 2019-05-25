import os, sys, requests
from datetime import datetime, timedelta

class InfoContainer:

	def __init__(self, container_type, manager, ticker_id):
		self._container_type = container_type
		self.manager = manager
		self._ticker_id = ticker_id
		self._data_lists = {}
		self._elements = 0
		self._file_init()
		for value in self._data_lists.values():
			value.sort()

	def __str__(self):
		return "{}-{}".format(self._container_type, self._ticker_id)

	def _file_init(self):
		# Make folder if it does not exists
		if not os.path.exists(self.folder_path()):
			os.makedirs(self.folder_path())

		# Make file if it does not exists
		if not os.path.isfile(self.file_path()):
			open(self.file_path(), 'w').close()

		# Read data in file
		with open(self.file_path()) as file:
			for line in file:
				data = line.strip().split(",")
				i = 1
				while i < len(data):
					try:
						date = datetime.strptime("{} {}".format(data[0], data[i]), "%y/%m/%d %H:%M:%S")
					except ValueError as ve:
						date = datetime.strptime("{} {}".format(data[0], data[i]), "%Y/%m/%d %H:%M:%S")
					self._add_data_to_lists(i, date, data)					
					i += self._lines_per_update()
					self._elements += 1

	def get_ticker_id(self):
		return self._ticker_id

	def get_container_type(self):
		return self._container_type

	def prettyprint(self):
		print("{} - {}".format(self._container_type, self._ticker_id))
		for key, value in self._data_lists.items():
			print(key)
			
			year = -1
			month = -1
			day = -1
			for item in value:
				date = item[0]
				if date.year != year or date.month != month or date.day != day:
					year = date.year
					month = date.month
					day = date.day
					print("\t * {}-{}-{}".format(year, month, day))
				print("\t\t   {}:{}:{} - {}".format(date.hour, date.minute, date.second, item[1]))
			
	def write_to_file(self):
		s = ""
		year = -1
		month = -1
		day = -1
		dates = next(iter(self._data_lists.values()))
		for i in range(0, self._elements):
			date = dates[i][0]
			if date.year != year or date.month != month or date.day != day:
				if year != -1:
					s += "\n"
				year = date.year
				month = date.month
				day = date.day
				s+= "{}/{}/{}".format(year, month, day)
			
			info = self._get_write_info(i)
			s += "," + info
			#print(info)
		open(self.file_path(), 'w').write(s)

	def update(self):
		date = datetime.now()
		data = self._get_update_data(date)
		if data == None:
			return
		assert self._lines_per_update() - 1 == len(data), "{} update expected {} data elements, but got {}.".format(self._ticker_id, self._lines_per_update() - 1, len(data))
		data = ["",""] + data
		self._add_data_to_lists(1, date, data)
		self._elements += 1
	'''
		returns: a list of information which is passed to _add_data_to_lists
	'''
	def _get_update_data(self, date):
		raise NotImplementedError
		
	def _get_write_info(self, i):
		raise NotImplementedError

	def _add_data_to_lists(self, i, date, data):
		raise NotImplementedError

	def _lines_per_update(self):
		raise NotImplementedError

	def directory_location(self):
		return os.path.dirname(os.path.abspath(sys.argv[0]))

	def folder_location(self):
		raise NotImplementedError

	def folder_path(self):
		return NotImplementedError

	def file_path(self):
		return os.path.join(self.folder_path(), self._ticker_id)

	def get_date(self, date_num):
		return datetime.strftime(datetime.now() + timedelta(date_num), "%x")

class SubredditContainer(InfoContainer):

	def __init__(self, parent_container, name):
		self._followers = []

		super().__init__("Subreddit", parent_container, name)

		self._data_lists["followers"] = self._followers
	
	def _get_update_data(self, date):
		request_string = 'http://www.reddit.com/r/' + self._ticker_id +'/about/.json'
		response = requests.get(request_string, headers = {'User-agent': 'floffbot'})
		data = response.json()
		return [data['data']['subscribers']]

	def _add_data_to_lists(self, i, date, data):
		info = (date, int(data[i+1]))
		self._followers.append(info)

	def _lines_per_update(self):
		return 2

	def _get_write_info(self, i):
		info = self._followers[i]
		date = info[0]
		return "{}:{}:{},{}".format(date.hour, date.minute, date.second, info[1])

	def folder_location(self):
		return "subred_data/"

	def folder_path(self):
		return os.path.join(self.directory_location(), self.folder_location())

class MarketcapContainer(InfoContainer):

	def __init__(self, parent_container, name):
		self._usd_value = []
		self._btc_value = []

		super().__init__("Marketcap", parent_container, name)

		self._data_lists["usd_value"] = self._usd_value
		self._data_lists["btc_value"] = self._btc_value

	def _get_update_data(self, date):
		data = self.manager.get_marketcap_data(self._ticker_id)
		if data == None:
			return data
		return [data['BTC'], data['USD']]

	def _add_data_to_lists(self, i, date, data):
			btc = (date, float(data[i+1]))
			usd = (date, float(data[i+2]))
			self._btc_value.append(btc)
			self._usd_value.append(usd)

	def _lines_per_update(self):
		return 3

	def _get_write_info(self, i):
		btc_info = self._btc_value[i]
		usd_info = self._usd_value[i]
		date = btc_info[0]
		return "{}:{}:{},{},{}".format(date.hour, date.minute, date.second, btc_info[1], usd_info[1])

	def folder_location(self):
		return "marketcap_data/"

	def folder_path(self):
		return os.path.join(self.directory_location(), self.folder_location())
