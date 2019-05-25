import os, sys
from datetime import datetime

class InfoContainer:

	def __init__(self, name, manager, id):
		self._name = name
		self.manager = manager
		self._id = id
		self._data_lists = {}
		self._file_init()

	def __str__(self):
		return "{}-{}".format(self._name, self._id)

	def _file_init(self):
		with open(os.path.join(self.folder_path(), self._id)) as file:
			for line in file:
				data = line.strip().split(",")
				i = 1
				while i < len(data):
					date = datetime.strptime("{} {}".format(data[0], data[i]), "%m/%d/%y %H:%M:%S")
					self._add_data_to_lists(i, date, data)					
					i += self._lines_per_update()

	def prettyprint(self):
		print(self._name)
		for key, value in self._data_lists.items():
			print(key)
			value.sort()
			
			year = -1
			month = -1
			day = -1
			for item in value:
				date = item[0]
				if date.year != year or date.month != month or date.day != day:
					year = date.year
					month = date.month
					day = date.day
					print("\t - {}-{}-{}".format(year, month, day))
				print("\t\t   {}:{}:{} - {}".format(date.hour, date.minute, date.second, item[1]))
			

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

class SubredditContainer(InfoContainer):

	def __init__(self, parent_container, name):
		self._followers = []
		super().__init__("Subreddit", parent_container, name)

		self._data_lists["followers"] = self._followers

	def _add_data_to_lists(self, i, date, data):
		info = (date, data[i+1])
		self._followers.append(info)

	def _lines_per_update(self):
		return 2

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

	def _add_data_to_lists(self, i, date, data):
			btc = (date, data[i+1])
			usd = (date, data[i+2])
			self._btc_value.append(btc)
			self._usd_value.append(usd)

	def _lines_per_update(self):
		return 3

	def folder_location(self):
		return "marketcap_data/"

	def folder_path(self):
		return os.path.join(self.directory_location(), self.folder_location())

class SystemManager:
	
	def ValiDate(date):
		try:
			datetime.strptime(date, '%m/%d/%y')
		except ValueError:
			raise ValueError("Incorrect data format, should be MM/DD/YY")


	def __init__(self, date):
		SystemManager.ValiDate(date)
		self._date = date
		self._info_containers = {}



	def __str__(self):
		s = str(self._date)
		for container in self._info_containers:
			s += " {}".format(container)

		return s

	def get_date(self):
		return self._date

	def _create_key(self, container_type, name):
		return "{}-{}".format(container_type, name)

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
		supported_types = {"Subreddit" : SubredditContainer, "Marketcap" : MarketcapContainer}
		
		key = self._create_key(container_type, name)
		if key in self._info_containers:
			return self._info_containers[key]
		
		elif container_type in supported_types:

			new_container = supported_types[container_type](self, name)
			self._info_containers[key] = new_container
			return new_container

		#else
		raise ValueError("Incorrect container_type, should be one of {}".format(supported_types.keys()))


	def get(self, container_type, name):
		key = self._create_key(container_type, name)
		if key in self._info_containers:
			return self._info_containers[key]

		return None

	def prettyprint(self):
		for container in self._info_containers.values():
			container.prettyprint()

date = SystemManager("09/27/17")
date.new("Subreddit", "bitcoin")
date.new("Marketcap", "BTC")

assert str(date.get("Subreddit", "bitcoin")) == "Subreddit-bitcoin"
assert str(date.get("Marketcap", "BTC")) == "Marketcap-BTC"

date.prettyprint()
print(datetime.strptime("09/27/17", "%m/%d/%y"))
#print(SubredditContainer.folder_path())
#print(MarketcapContainer.folder_path())
