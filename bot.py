from systemmanager import SystemManager
import sys, os, logging


def main():
	datalist = "datalist_updated.csv"
	manager = SystemManager(datalist)
	
	manager.update()
	manager.store()
	#manager.prettyprint()


if __name__ == '__main__':
	dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
	logging.basicConfig(filename="{}/logging.log".format(dirname), level=logging.ERROR)
	try:
		main()
	except Exception as e:
		logging.error("Main not functioning: {}".format(e))

#date = SystemManager("datalist.txt")
#date.new("Subreddit", "bitcoin")
#date.new("Marketcap", "BTC")
#date.new("Marketcap", "AEON")

#assert str(date.get("Subreddit", "bitcoin")) == "Subreddit-bitcoin"
#assert str(date.get("Marketcap", "BTC")) == "Marketcap-BTC"

#date.prettyprint()
#print(datetime.strptime("09/27/17", "%m/%d/%y"))
#date.store()
#date.update()
#date.store()
#print(SubredditContainer.folder_path())
#print(MarketcapContainer.folder_path())
