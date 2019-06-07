from systemmanager import SystemManager
import sys

# container-type name

def main():
	datalist = "datalist.txt"
	if len(sys.argv) != 3:
		print("USAGE: plot.py [container-type] [name]")
		exit()
	

	manager = SystemManager(datalist)
	
	print(manager.container_keys())
	
	container_type = sys.argv[1]
	name = sys.argv[2]
	container = manager.get(container_type, name)
	container.plot("testplot")
	

	#print(container)



if __name__ == '__main__':
	main()