import os, sys, time

dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
marketcap = dirname + "/marketcap_data"
subreddit = dirname + "/subred_data"

def refactor_commas():
	# Refactor marketcap_data
	
	for filename in os.listdir(marketcap):
		filepath = os.path.join(marketcap, filename) 
		s = ""
		with open(filepath) as file:
			for line in file:
				if line.strip() == "":
					continue
				print("LINE: {}".format(line))
				date, btc_value, usd_value = line.strip().split(" , ")
				s += "{},{},{},{}\n".format(date, time.strftime("%H:%M:%S"), btc_value, usd_value)
		
		open(filepath, 'w').write(s)
	

	# Refactor subred_data
	for filename in os.listdir(subreddit):
		filepath = os.path.join(subreddit, filename)
		s = ""
		with open(filepath, encoding="utf8", errors='ignore') as file:
			for line in file:
				if line.strip() == "":
					continue
				try:
					print(line)
					date, t1, t2, followers = line.strip().split(",")
					s += "{},{},{}\n".format(date, time.strftime("%H:%M:%S"), followers)
				except Exception as e:
					print(e)

		open(filepath, 'w').write(s)

def refactor_dates():

	for filename in os.listdir(marketcap):
		filepath = os.path.join(marketcap, filename) 
		s = ""
		with open(filepath) as file:
			for line in file:
				if line.strip() == "":
					continue
				info = line.strip().split(",")
				month, day, year = info[0].split("/")
				rest = ""
				for i in range(1, len(info)):
					rest += ",{}".format(info[i])
				s += "{}/{}/{}{}\n".format(year, month, day, rest)
		
		#print(s)
		open(filepath, 'w').write(s)

	for filename in os.listdir(subreddit):
		filepath = os.path.join(subreddit, filename) 
		s = ""
		with open(filepath) as file:
			for line in file:
				if line.strip() == "":
					continue
				info = line.strip().split(",")
				month, day, year = info[0].split("/")
				rest = ""
				for i in range(1, len(info)):
					rest += ",{}".format(info[i])
				s += "{}/{}/{}{}\n".format(year, month, day, rest)
		
		#print(s)
		open(filepath, 'w').write(s)

def fix_double_commas():
	for filename in os.listdir(marketcap):
		filepath = os.path.join(marketcap, filename) 
		s = ""
		with open(filepath) as file:
			for line in file:
				s += line.replace(",,",",")
		#print(s)
		open(filepath, 'w').write(s)

	for filename in os.listdir(subreddit):
		filepath = os.path.join(subreddit, filename) 
		s = ""
		with open(filepath) as file:
			for line in file:
				s += line.replace(",,",",")
		
		#print(s)
		open(filepath, 'w').write(s)


def main():
	refactor_commas()
	refactor_dates()
	#fix_double_commas()

if __name__ == '__main__':
	main()