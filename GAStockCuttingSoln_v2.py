'''
Missouri State University, Fall 2018
Ken Vollmar
Genetic algorithm for stock cutting
Assumptions:
-- Stock and pieces are rectangles with integer coordinates, and 
	edges are oriented strictly "north-south" and "east-west." This 
	simplifies determining whether two pieces intersect.
-- Assume that the "cut" has zero width, so that two edges may be
	coincident and still valid. Example:  y1 --- yA:::::yB --------y2
-- The size of the stock, and the size and position of all pieces, are
	specified by the upper-left and lower-right corner coordinates.


tkinter documentation:
http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html
https://www.c-sharpcorner.com/blogs/basics-for-displaying-image-in-tkinter-python
https://tkdocs.com/
'''


import time  # for pause during graphic display
import random
import sys
#import tkFont  # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/fonts.html
random.seed(0)  # Initialize internal state of the random number generator.

NUMBER_OF_PIECES = 6  # HARDCODED  
STOCK_WIDTH = 800 # HARDCODED  Width of stock
STOCK_HEIGHT = 400 # HARDCODED  Height of stock = 
NUMBER_OF_GENERATIONS = 1 # HARDCODED Number of generations of evolution
POPULATION_SIZE = 1  # HARDCODED Number of individuals in population

piece_colors = ["gold", "deepskyblue", "green3", "tan1", "orchid1", 
	"purple1", "red2", "palegreen", "goldenrod", "thistle2", "lightblue3",
	"thistle"]

''' 
Definition of a class Piece that has data members:
	xcoord	X coordinate of the upper left corner
	ycoord	Y coordinate of the upper left corner
	. . . (other values as desired)
	
Create an object of the class Piece using     Piece(x, y, ...)
Place an object of the class Piece into a list   myList.append(myPiece)
'''
##class Piece:
##        x1 = 0
##        y1 = 0
##        x2 = 0
##        y2 = 0
##        def __init__(self, x1coord, y1coord, x2coord, y2coord): # Add other values to this list
##                self.x1 = x1coord
##                self.y1 = y1coord
##                self.x2 = x2coord
##                self.y2 = y2coord

		
	# As you wish, define other function members of class Piece 
	# to return other individual values or a set of several 
	# values within a tuple or list.
	
	
'''
Create a Piece object in a dictionary data structure, using the parameters
for the piece position.
TBD -- this places the piece within the stock (as opposed to putting
at least the UL corner but not necessarily the LR corner in stock)
'''
# https://www.w3schools.com/python/python_dictionaries.asp
def makeRectObj(w, h, x1, y1, c):
	return { "width": w, "height": h, "color": c,
		"x1": x1, "y1": y1, 
		"x2": x1+w, "y2": y1+h, "fit":0}  # Return a dictionary object
	
def overlap(x1,y1,evalx1,evaly1,evalx2,evaly2):
	if(x1 < evalx2 and x1 > evalx1 and y1 < evaly2 and y1 > evaly1):
		return True
	else:
		return False
# Use tkinter to display stock and pieces
from tkinter import *      
root = Tk()      
canvas = Canvas(root, width = STOCK_WIDTH, height = STOCK_HEIGHT, bg='khaki')   
canvas.pack()   



# Read data from a file if a file is given on the command line.
# Open the file and read it into the list "content"
if (len(sys.argv) > 1): # A command-line argument exists; assume it is an input filename
	filename = sys.argv[1]
	'''
	# This section not genuinely indented, but necessary for comment
	else: # Prompt for input filename
		filename = input("\n\n\tPlease type an input data file name: ")
	'''
	try:
		with open(filename) as f:
			content = f.readlines()
	except FileNotFoundError:
		sys.exit('Could not find file ' + filename)

	# Data in file is expected to be, on separate lines as shown:
	# 	Width of stock
	#	Height of stock
	#	Number of pieces to be cut from stock
	#	Width Height   of piece 0
	#	Width Height   of piece 1
	#		. . .
	#	Width Height   of piece (N-1)
	#
	# Show the data of the input data file, one word at a time
	for i in range(0, len(content)):
		line = content[i].split()
		for j in range(0, len(line)):
			print(str(line[j]))
		#print()


''' Initialize and display POPULATION_SIZE number of pieces.
TBD -- Initially, create all pieces of _size_ 200x200, 
at _positions_ TBD.  
TBD -- this places the piece within the stock (as opposed to putting
at least the UL corner but not necessarily the LR corner in stock)
'''
population = [0 for i in range(POPULATION_SIZE)]
for indiv_count in range(POPULATION_SIZE):
	individual = [0 for j in range(NUMBER_OF_PIECES)]
	for piece_count in range(NUMBER_OF_PIECES):
		w = 200  #  TBD HARDCODED
		h = 200  #  TBD HARDCODED
		c = piece_colors[piece_count]  # TBD -- need more colors when more pieces
		x1 = random.randint(0, STOCK_WIDTH - w)   # piece is within stock
		y1 = random.randint(0, STOCK_HEIGHT - h)    # piece is within stock
		
		# An individual is an array of dictionary objects
		individual[piece_count] = makeRectObj(w, h, x1, y1,c)
		#print(individual[piece_count])
		#print("	Piece ", piece_count, " x1 is ", (individual[piece_count]).get("x1"))

		
		
		# TBD  -- display the  first individual
		# in general, display the fittest individual of this generation
		if indiv_count == 0:
			canvas.create_rectangle(x1, y1, x1+w, y1+h, fill=c, outline='black')
			canvas.update()
			time.sleep(0.02) # HARDCODED

		print("individual  is ", individual)
		print()

	# The population is an array of individual objects
	population[indiv_count] = individual
	print("population[", indiv_count,"] is ", population[indiv_count])
	print()
	#print("Piece ", piece_count, " x1 is ", (population[piece_count]).get("x1")
	#print("Piece ", piece_count, " x1 is ", (population[piece_count])["x1"]
	#print("Piece ", piece_count, " x1 is ", (population[piece_count])["x1"]
	#print(population[piece_count])["x1"]
	
	
	
	#print()


'''
This is the main GA loop, performing the evolutionary sequence of
operations: Evaluation, Selection, Crossover, Mutation.
Remember:
	A POPULATION is a set of POPULATION_SIZE individuals.
	An INDIVIDUAL is a set of PIECE_COUNT pieces.
'''
for looper in range(NUMBER_OF_GENERATIONS):
	# EVALUATE ALL INDIVIDUALS
	for indv in population:
		for i in range(len(indv)):
			
			x1 = indv[i].get("x1")
			y1 = indv[i].get("y1")
			x2 = indv[i].get("x2")
			y2 = indv[i].get("y2")
			fit = indv[i].get("fit")
			for j in range(len(indv)-i):
				nextx1 = indv[j].get("x1")
				nexty1 = indv[j].get("y1")
				nextx2 = indv[j].get("x2")
				nexty2 = indv[j].get("y2")
				if (overlap(x1,y1,nextx1,nexty1,nextx2,nexty2) or overlap(x1,y2,nextx1,nexty1,nextx2,nexty2) or overlap(x2,y1,nextx1,nexty1,nextx2,nexty2) or overlap(x2,y2,nextx1,nexty1,nextx2,nexty2)):
					fit += 1
				
					
				print(fit)
					
			indv[i].update({"fit":fit})
			print(indv[i])		
			
			
		
	
	# SELECT INDIVIDUALS FOR REPRODUCTION IN THE NEXT GENERATION
	
	
	# CROSSOVER OPERATION FOR INDIVIDUALS
	for indv in population:
		fits = []
		for piece in indv:
			fits.append(piece.get("fit"))
		fits.sort()
		drop_indexes = []
		for i in range(NUMBER_OF_PIECES):
			if (indv[i].get("fit") == fits[NUMBER_OF_PIECES - 1] or indv[i].get("fit") == fits[NUMBER_OF_PIECES - 2 ]):
				  drop_indexes.append(i)  
		print(drop_indexes)		
		
	# MUTATION OPERATION FOR INDIVIDUALS
	# In general, select with some randomness "several" individuals upon which
	# to perform mutation of "some" (one or more) characteristics.
	# TBD This demo is hardcoded to change only the first characteristic of the first individual.
##	mutating_individual = population[0] # mutating_individual is a list of dictionary 
##	print()
##	print("mutating indiv is ", mutating_individual)
##	print()
##	mutating_characteristic = mutating_individual[0]
##	print(" mutating_characteristic is ", mutating_characteristic)
##	print()
##
##	prev_value = mutating_characteristic.get("x1") 
##	new_value = prev_value + 5  # Mutate by incrementing
##	mutating_characteristic["x1"] = new_value
##	prev_value = mutating_characteristic.get("x2") 
##	new_value = prev_value + 5  # Mutate by incrementing
##	mutating_characteristic["x2"] = new_value

	
	
	# Display all pieces in their new position.
	# In general, display the fittest individual of this generation.
	# In this demo, display only the first individual.
	# Clear the display by re-drawing the background with no elements  
	canvas.create_rectangle(0, 0, STOCK_WIDTH, STOCK_HEIGHT, fill='khaki') 
	display_individual = population[0] # display this individual, which is a list of dictionary 
	for piece_count in range(NUMBER_OF_PIECES):
		canvas.create_rectangle(display_individual[piece_count].get("x1"), 
			display_individual[piece_count].get("y1"),
			display_individual[piece_count].get("x2"),
			display_individual[piece_count].get("y2"),
			fill = display_individual[piece_count].get("color"),
			outline = "black")
		#tkFont.Font(family='Helvetica',size=36, weight='bold') # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/fonts.html
		canvas.create_text(display_individual[piece_count].get("x1") + 20, 
			display_individual[piece_count].get("y1") + 20,
			text=str(piece_count))
			
	canvas.update()
	time.sleep(1) # HARDCODED TIME -- pause briefly between generations




		

mainloop()   # Graphics loop -- This statement follows all other statements
