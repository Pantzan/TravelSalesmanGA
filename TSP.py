import random
import operator

class Tsp:	
	def __init__(self):
		# initialize arguments
		self.population = 8

		self.parents = []
		self.children = []
		# create 2D list
		self.cities = [[]]
		self.cities = [[0 for i in range(self.population)] for i in range(self.population)]
		self.createCities()
		self.bests = []
	
	# fill the 2D list with the travel distances of this problem
	def createCities(self):
		self.cities[0][0] = 0
		self.cities[0][1] = 172
		self.cities[0][2] = 145
		self.cities[0][3] = 607
		self.cities[0][4] = 329
		self.cities[0][5] = 72
		self.cities[0][6] = 312
		self.cities[0][7] = 120

		self.cities[1][0] = 172
		self.cities[1][1] = 0
		self.cities[1][2] = 192
		self.cities[1][3] = 494
		self.cities[1][4] = 209
		self.cities[1][5] = 158
		self.cities[1][6] = 216
		self.cities[1][7] = 92

		self.cities[2][0] = 145
		self.cities[2][1] = 192
		self.cities[2][2] = 0
		self.cities[2][3] = 490
		self.cities[2][4] = 237
		self.cities[2][5] = 75
		self.cities[2][6] = 205
		self.cities[2][7] = 100

		self.cities[3][0] = 607
		self.cities[3][1] = 494
		self.cities[3][2] = 205
		self.cities[3][3] = 0
		self.cities[3][4] = 286
		self.cities[3][5] = 545
		self.cities[3][6] = 296
		self.cities[3][7] = 489

		self.cities[4][1] = 329
		self.cities[4][2] = 209
		self.cities[4][3] = 286	
		self.cities[4][4] = 0
		self.cities[4][5] = 421
		self.cities[4][6] = 49
		self.cities[4][7] = 208

		self.cities[5][0] = 72
		self.cities[5][1] = 158
		self.cities[5][2] = 75
		self.cities[5][3] = 545
		self.cities[5][4] = 421
		self.cities[5][5] = 0
		self.cities[5][6] = 249
		self.cities[5][7] = 75

		self.cities[6][0] = 312
		self.cities[6][1] = 216
		self.cities[6][2] = 205
		self.cities[6][3] = 296
		self.cities[6][4] = 49
		self.cities[6][5] = 249
		self.cities[6][6] = 0
		self.cities[6][7] = 194

		self.cities[7][0] = 120
		self.cities[7][1] = 92
		self.cities[7][2] = 100
		self.cities[7][3] = 489
		self.cities[7][4] = 208
		self.cities[7][0] = 120
		self.cities[7][5] = 75
		self.cities[7][6] = 194
		self.cities[7][7] = 0

	# make sure that the crossover list has not any dublicate values.
	def isUnique(self, childpos, temp):
		sample = [0,1,2,3,4,5,6,7]
		for	i in childpos:
			for index, k in enumerate(temp):
				# if a dublicate value from the first and second part of the list
				if i == k:
					del temp[index]
					for s in sample:
						t = childpos + temp
						# replace it with a value that does not already exists
						if s not in t:
							temp.insert(index,s)
							break
		return temp

	# do crossover between two parents 
	def crossover(self, v1, v2, ratio=3):
		rem_char = len(v1)-ratio
		clone1 = v1.copy()
		clone2 = v2.copy()

		#split the list in parts
		child1pos = clone1[:rem_char]
		child2pos = clone2[:rem_char]
		child1suf = clone1[-ratio:]
		child2suf = clone2[-ratio:]	
		# check for dublicates
		unique1 = self.isUnique(child1pos, child2suf)
		unique2 = self.isUnique(child2pos, child1suf)

		# create child
		child1 = child1pos + unique1
		child2 = child2pos + unique2

		# return children
		return child1, child2

	# calculate fitness for each route
	def fitness(self, child):
		sum = 0
		for i in range(0, len(child)-2):
			sum += self.cities[ child[i] ] [ child[i+1] ]
		return sum

	# sort children and keep the 4 best
	def selection(self, lists):
		bests = []
		self.bests = []
		for i in lists:
			# calculate fitness and append in tuple for reference
			cost = self.fitness(i)
			bests.append((cost, i))

		# sort the  tuple by fitness function
		bests.sort(key=operator.itemgetter(0))
		self.bests = bests
		# keep only4 best children
		bests = [x[1] for x in bests][:4]
		return bests

	# initialize the class program by creating parents
	def initialize(self):
		for i in range(1, self.population//2+1):
			vector = random.sample(range(8), 8)
			self.parents.append(vector)

	# evaluate the GA algorithm
	def evalutation(self):
		self.children = []
		length = len(self.parents)
		ratio = random.randint(1, length)

		# crossover parents and create 2Xparents list of children
		crossovered1 = self.crossover(self.parents[0], self.parents[1], ratio)
		crossovered2 = self.crossover(self.parents[1], self.parents[2], ratio)
		crossovered3 = self.crossover(self.parents[2], self.parents[3], ratio)
		crossovered4 = self.crossover(self.parents[3], self.parents[0], ratio)
		self.children.append(crossovered1[0])
		self.children.append(crossovered1[1])
		self.children.append(crossovered2[0])
		self.children.append(crossovered2[1])
		self.children.append(crossovered3[0])
		self.children.append(crossovered4[1])
		self.children.append(crossovered4[0])
		self.children.append(crossovered4[1])
		
		# mutate children by randomize them
		mutated = self.mutation(self.children)
		# get the sorted selection
		selection = self.selection(mutated)
		self.parents = selection

	# mutate children under a certain property
	def mutation(self, children):
		import random
		choices = []
		from copy import deepcopy
		# hardcopy the children list to avoid reference issues
		copies = deepcopy(children)
		# check that the above will happen three unique times
		while len(choices) < 3:
			# create a random index
			choice = random.randint(0, len(copies)-1)
			# calculate a random boundary for the randomizing mutation process
			boundary = random.randint(0, len(copies)-1)
			# check again for multiplied indexes
			if choice not in choices:
				# if the index is larger that the boundary do the mutation (randomizer)
				if choice >= boundary:
					chosen = copies[choice]
					# shuffle the array by changing the indexes of the values
					random.shuffle(copies[choice])
				choices.append(choice)	
		return copies

	# run the program
	def run(self, iter=5000):
		total = []
		self.initialize()
		for i in range(iter):
			self.evalutation()
			best = self.bests[0]
			total.append(best)
		# sort the best children list and print the best children as outcome of this program
			if best[0] == 388:
				print("388 found!")
				break
		total.sort(key=operator.itemgetter(0))		
		found = total[0]
		print("The sortest path under {} iterations is {} with cost {}" .format(iter,found[1],found[0]))
		from collections import Counter 


# t = Tsp()
# t.run()