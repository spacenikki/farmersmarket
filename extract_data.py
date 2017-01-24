from collections import Counter
import csv
import re
import matplotlib.pyplot as plt  # import module and RENAME it as 'plt'
import numpy as np
from pylab import *
import six 
from matplotlib import colors
from random import randrange

MY_FILE = "./farmers-markets.csv"


def main():
	# have market county starting with a p 
	dict1 = parse('farmers-markets.csv')

	#  filter out County starts with a 'P'
	new_data = []
	for i in range(len(dict1)):
		if not re.search(r'^P',dict1[i]['County']): # if County name does not starts with a 'p', add to new_data
			new_data.append(dict1[i])

	question1(new_data)
	question2()
	question3(new_data)
	visualize_type_bar(new_data)
	visualize_type_round(new_data)


# question 1 - Veg and meat
def question1(new_data):
	no_market_1 = 0
	for collection in new_data:

		if collection['Vegetables'] == 'Y' and collection['Meat'] == 'N':
			no_market_1 += 1

	print "There are %r of markets which sell vegetables but not meat" %(no_market_1)

def question2():
	market_location_data = parse(MY_FILE)
	
	# check how many kind location and types
	location_counter = Counter(item['Location'] for item in market_location_data)
	print location_counter


def question3(new_data):
	no_market_3 = 0 
	for collection in new_data:
		# print type(collection['Longitude'])   # string
		if collection.has_key('Latitude') and collection.has_key('Longitude'):
			# first stripe all the space then compare that to ""
			Latitude = collection['Latitude'].strip(" ")
			Longitude = collection['Longitude'].strip(" ")
			# only look at those who are not empty
			if Latitude != "" and Longitude != "":
				# convert str to int
				Longitude = float(collection['Longitude'])
				Latitude = float(collection['Latitude'])
				# print type(Latitude)
				if Longitude < -73.9501 and Longitude > -122.333392 and Latitude > 40.7737 and Latitude < 47.608858:
					no_market_3 += 1
	
	print "There are %i US farmers markets are within this shaded rectangle " %(no_market_3)


def random_color_generator():
	colors_ = list(six.iteritems(colors.cnames))
	# all colors under matplotlib
	rand_color = colors_[randrange(len(colors_))][1]
	return rand_color

def visualize_type_bar(new_data):
	# return all states and its occurence 
	state_counter = Counter(item["State"] for item in new_data) 
	# if user choose how many farmers markets sells honey, then change item['honey'] 0> will retxurn Counter(['Y',60],['N',100]) -> then present this on graph

	labels = tuple(state_counter.keys())

	# set where label hit the x-axis (numpy's method np)
	xlocations = np.array(range(len(labels)))+2  # 1.5 is how far should the very first bar away from y-axis
	print "xlocations is" ,xlocations  # xlocations is where they plot the y marks
	width = 0.5  # bar's width

	# assign data to a bar plot, .bar, change color to red
	plt.bar(xlocations*1.2,state_counter.values(), width=width, align="center", color= random_color_generator(), linewidth=0.5)  #width here = bar's width, not the space between each bar...
	ylabel("No. of Farmer Markets in the States")
	xlabel("States")


	# Assign labels and tick location to x-axis
	plt.xticks(xlocations*1.2 + width/2, labels, fontsize=10, rotation=90, color=random_color_generator()) #width here = how far is state's names away from the y-axis

	# Give some more toom so the labels aren't cut off in the graph
	plt.subplots_adjust(bottom=0.4)

	# make the overall graph/figure larger
	plt.rcParams['figure.figsize'] = 16, 12
	plt.title("Farmers Market in each States. (Except those starts with 'P'", color= "salmon", fontsize = 16)

	# save the plot
	plt.savefig("./images/Type_wider5.png")

	# show bar chart in python interpreter
	plt.show()

	# close figure
	plt.clf()


def visualize_type_round(new_data):

	state_counter = Counter(item["State"] for item in new_data) 

	x_labels = tuple(state_counter.keys())
	y_labels = tuple(state_counter.values())

	# replace x location
	plt.xticks(range(len(state_counter)),x_labels,rotation="vertical")
	
	# 'r' - color, 'o' round shape
	plt.plot(y_labels,'ro')
	
	ylabel("No. of Farmer Markets in the States")
	xlabel("States")

	# plt.xticks(range(len(y)),labels,rotation="vertical")
	plt.margins(0.2)
	plt.subplots_adjust(bottom=0.15)

	# save the plot
	plt.savefig("./images/Type_round.png")
	
	plt.show()
	plt.clf()


def parse(raw_file):
	# parse a raw CSV file to a JSON-line object
	f = open(raw_file)
	# f = open('farmers-markets.csv')
	csv_data = csv.reader(f)

	# build data structure to return parsed_data
	parsed_data = []
	fields = csv_data.next()  # only to extract header from the CSV file 

	# take care of the body
	for value in csv_data:
		parsed_data.append(dict(zip(fields,value)))
	# print parsed_data
	# print len(parsed_data)
	f.close()

	return parsed_data


if __name__ == "__main__":
	main()

