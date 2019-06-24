from systemmanager import SystemManager
import sys

# container-type name
def usage():
	print("USAGE: plot.py [container-type] [name]")
	print("plot.py all")
	exit()

def main():
	datalist = "datalist_updated.csv"
	plot_all = False
	if len(sys.argv) == 2 and sys.argv[1] == 'all':
		plot_all = True
	elif len(sys.argv) != 3:
		usage()		
	
	manager = SystemManager(datalist)
	
	print(manager.container_keys())
	if plot_all:
		for key in manager.container_keys():
			print(key)
			container_type, name = key.split("-")
			container = manager.get(container_type, name)
			try:
				container.plot(container_type + "-" + name)
			except ValueError as ve:
				print(ve)
	else:
		container_type = sys.argv[1]
		name = sys.argv[2]
		container = manager.get(container_type, name)
		container.plot(container_type + "-" + name)
	

	#print(container)



if __name__ == '__main__':
	main()