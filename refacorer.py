import os, sys, time

dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
marketcap = dirname + "/marketcap_data"
subreddit = dirname + "/subred_data"

def main():
	# Refactor marketcap_data
	
	for filename in os.listdir(marketcap):
		filepath = os.path.join(marketcap, filename) 
		s = ""
		with open(filepath) as file:
			for line in file:
				date, btc_value, usd_value = line.strip().split(" , ")
				s += "{},{},{},{}\n".format(date, time.strftime("%H:%M:%S"), btc_value, usd_value)
		
		open(filepath, 'w').write(s)
	

	# Refactor subred_data
	for filename in os.listdir(subreddit):
		filepath = os.path.join(subreddit, filename)
		s = ""
		with open(filepath, encoding="utf8", errors='ignore') as file:
			for line in file:
				try:
					print(line)
					date, t1, t2, followers = line.strip().split(",")
					s += "{},{},{}\n".format(date, time.strftime("%H:%M:%S"), followers)
				except Exception as e:
					print(e)

		open(filepath, 'w').write(s)

if __name__ == '__main__':
	main()