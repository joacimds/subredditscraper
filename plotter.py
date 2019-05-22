import bot
import matplotlib.pyplot as plt
import datetime
import numpy as np
def two_scales(ax1, time, data1, data2, c1, c2):
    """

    Parameters
    ----------
    ax : axis
        Axis to put two scales on

    time : array-like
        x-axis values for both datasets

    data1: array-like
        Data for left hand scale

    data2 : array-like
        Data for right hand scale

    c1 : color
        Color for line 1

    c2 : color
        Color for line 2

    Returns
    -------
    ax : axis
        Original axis
    ax2 : axis
        New twin axis
    """
    ax2 = ax1.twinx()

    ax1.plot(time, data1, color=c1)
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('exp')

    ax2.plot(time, data2, color=c2)
    ax2.set_ylabel('sin')
    return ax1, ax2

# Change color of each axis
def color_y_axis(ax, color):
    """Color your axes."""
    for t in ax.get_yticklabels():
        t.set_color(color)
    return None

def test():
	list1 = [100, 200, 300, 400]
	list2 = [120, 140, 130, 150]

	cointainer = bot.Currency_cointainer()
	cointainer.read_data_list()
	coin = cointainer.get_coin_by_ticker("NEO")


	sr = coin.get_subreddit_list()
	lists = sr.items()

	x,y = zip(*lists)
	x = [datetime.datetime.strptime(i, '%m/%d/%y') for i in x]
	#print(x)
	mc_list = coin.get_marketcap_list()
	mc_lists = mc_list.items()
	x2, y2 = zip(*mc_lists)
	
	btc_p = []
	usd_p = []
	#print("{}\n____________---——__-\n{}".format(mc_lists, mc_list))	
	#print(y2)
	for item in y2:
		splitted = item.split(' , ')
		btc_p.append(float(splitted[0]))
		usd_p.append(float(splitted[1]))

	#x,y = zip(*sorted(coin.get_marketcap_list().items())) 
	#print(y2)
	#fig, ax = plt.subplots()
	
	plt.plot(np.array(x), np.array(y))

	#fig, ax = plt.subplots()
	#ax1, ax2 = two_scales(ax, list1, list1, list2, 'r', 'b')
	#plt.ylabel("testing")
	plt.show()




test()