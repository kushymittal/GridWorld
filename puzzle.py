from cell import *
from numpy import *
from random import randint
from sklearn.metrics import * 
from math import sqrt
import matplotlib.pyplot as plt

class Puzzle(object):

	"""Represents a Puzzle"""

	def __init__(self, endOnReward):

		self.maze = [ [ Cell(x, y) for y in range(6)] for x in range(6) ]
		self.endOnRewardState = endOnReward
		self.discountFactor = 0.99

	def printUtilities(self):
		for x in xrange(0,6):
			for y in xrange(0,6):
				print self.maze[x][y].utility, "\t",
			print "\n"
		
		
	# def copyUtilities(self):
	#     temp = [6][6]

	# 	for x in xrange(0,6):
	# 		for y in xrange(0,6):
	# 			temp[x][y] = self.maze[x][y].utility
				
	# 	return temp
	def copyUtilities(self):
		temp = zeros((6,6))

		for x in range(0,6):
			for y in range(0,6):
				temp[x][y] = self.maze[x][y].utility
		return temp

	def readInMaze(self):
		# File containing maze
		file = open("maze.txt", "r")

		x = 0

		# Set the wall status and the rewards here
		for line in file:

			# Remove the \n
			line = line.rstrip()

			elements = line.split("\t")
			y = 0

			for character in elements:
				if character == 'T':
					self.maze[x][y].setWall()
					self.maze[x][y].setReward(0.0)
				elif character == 'F':
					pass
				else:
					self.maze[x][y].setReward(float(character))

				y += 1

			x += 1

		file.close()

	def setUtilitiesMDP(self, iterations):

		for x in range(0,6):
			for y in range(0,6):
				if (abs(self.maze[x][y].reward) >= 1):
					self.maze[x][y].utility = self.maze[x][y].reward
		
		

		for n in range(iterations):

			#breakOut = False

			for x in (range(0,6)):

				for y in range(0,6):

					#print "x: ", x," y: ", y, " reward: ",self.maze[x][y].reward

					if self.maze[x][y].wall == True:
						continue

					# Reward States are terminal and we reached a reward state
					if (self.endOnRewardState == True) and (abs(self.maze[x][y].reward) >= 1):
						self.maze[x][y].utility = self.maze[x][y].reward
						#breakOut = True
						#break
						continue
						#raise Exception('Reached a Reward State')

					# Leftwards, Upwards, Rightwards, Downwards
					potentialValues = [0.0, 0.0, 0.0, 0.0]

					# Intended Direction is left
					if (y-1 < 0) or (self.maze[x][y-1].wall == True):
						potentialValues[0] += 0.8*self.maze[x][y].utility
					else:
						potentialValues[0] += 0.8 * self.maze[x][y-1].utility

					if (x-1 >= 0) and (self.maze[x-1][y].wall == False):
						potentialValues[0] += 0.1 * self.maze[x-1][y].utility
					else:
						potentialValues[0] += 0.1*self.maze[x][y].utility

					if (x+1 <= 5) and (self.maze[x+1][y].wall == False):
						potentialValues[0] += 0.1 * self.maze[x+1][y].utility
					else:
						potentialValues[0] += 0.1*self.maze[x][y].utility

					# Intended Direction is up
					if (x-1 < 0) or (self.maze[x-1][y].wall == True):
						potentialValues[1] += 0.8*self.maze[x][y].utility
					else:
						potentialValues[1] += 0.8 * self.maze[x-1][y].utility

					if (y-1 >= 0) and (self.maze[x][y-1].wall == False):
						potentialValues[1] += 0.1 * self.maze[x][y-1].utility
					else:
						potentialValues[1] += 0.1*self.maze[x][y].utility

					if (y+1 <= 5) and (self.maze[x][y+1].wall == False):
						potentialValues[1] += 0.1 * self.maze[x][y+1].utility
					else:
						potentialValues[1] += 0.1*self.maze[x][y].utility

					# Intended Direction is right
					if (y+1 > 5) or (self.maze[x][y+1].wall == True):
						potentialValues[2] += 0.8*self.maze[x][y].utility
					else:
						potentialValues[2] += 0.8 * self.maze[x][y+1].utility

					if (x-1 >= 0) and (self.maze[x-1][y].wall == False):
						potentialValues[2] += 0.1 * self.maze[x-1][y].utility
					else:
						potentialValues[2] += 0.1*self.maze[x][y].utility

					if (x+1 <= 5) and (self.maze[x+1][y].wall == False):
						potentialValues[2] += 0.1 * self.maze[x+1][y].utility
					else:
						potentialValues[2] += 0.1*self.maze[x][y].utility

					# Intended Direction is down
					if (x+1 > 5) or (self.maze[x+1][y].wall == True):
						potentialValues[3] += 0.8*self.maze[x][y].utility
					else:
						potentialValues[3] += 0.8 * self.maze[x+1][y].utility

					if (y-1 >= 0) and (self.maze[x][y-1].wall == False):
						potentialValues[3] += 0.1 * self.maze[x][y-1].utility
					else:
						potentialValues[3] += 0.1*self.maze[x][y].utility

					if (y+1 <= 5) and (self.maze[x][y+1].wall == False):
						potentialValues[3] += 0.1 * self.maze[x][y+1].utility
					else:
						potentialValues[3] += 0.1*self.maze[x][y].utility

					#print (potentialValues)
					self.maze[x][y].utility = self.maze[x][y].reward + self.discountFactor * max(potentialValues)
				#if (breakOut == True):
				#	break
				#else:
				#	continue
				#	breakOut = False
				#	break

	def computeAction(self, currX, currY):
		# Returns which action to take
		# 0 - Left 		1 - Up 		2 - Right 	3 - Down

		# max = -1000.0
		# index = 0

		# for u in xrange(0,4):
		# 	if(self.maze[currX][currY].qCount[u]%100>50):
		# 		if(self.maze[currX][currY].qValues[u] > max):
		# 			max = self.maze[currX][currY].qValues[u]
		# 			index = u
		# 	else:
		# 		max = 3* abs(self.maze[currX][currY].qValues[u])
		# 		index = u

		index = self.maze[currX][currY].qCount.index(min(self.maze[currX][currY].qCount))
		#x = randint(0, 3)
		#print x
		#return x
		return index


	def setUtilitiesTDQL(self):
		startX = 3
		startY = 1
		beta = 1.0

		# Set the utilities for reward states as their rewards
		for x in range(0,6):
			for y in range(0,6):
				if (abs(self.maze[x][y].reward) >= 1):
					self.maze[x][y].utility = self.maze[x][y].reward
					for dir in range(0,4):
						self.maze[x][y].qValues[dir] = self.maze[x][y].reward

		numTrials = 0

		while abs(beta) > .00001:
		#while numTrials < 5000:
			
			# Begin at the start state
			curr_x = startX
			curr_y = startY

			num_moves = 1

			while True:
				# Terminal State
				if (abs(self.maze[curr_x][curr_y].reward) >= 1):
					#beta = 1.0
					#print "Break: ", numTrials
					break

				alpha = float(60)/(59+num_moves)

				# Blackboxed action from this state
				curr_action = self.computeAction(curr_x, curr_y)
				
				next_X = curr_x
				next_Y = curr_y

				# Update the current co-ordinates based on curr_action
				if curr_action == 0:
					if curr_y-1 >= 0 and self.maze[curr_x][curr_y-1].wall != True:
						next_Y = curr_y - 1
					else:
						next_Y = curr_y
				elif curr_action == 1:
					if curr_x-1 >= 0 and self.maze[curr_x-1][curr_y].wall != True:
						next_X = curr_x - 1
					else:
						next_X = curr_x
				elif curr_action == 2:
					if curr_y+1 <= 5 and self.maze[curr_x][curr_y+1].wall != True:
						next_Y = curr_y + 1
					else:
						next_Y = curr_y
				else:
					if curr_x+1 <= 5 and self.maze[curr_x+1][curr_y].wall != True:
						next_X = curr_x +1
					else:
						next_X = curr_x

				# Perform TD update
				beta = float(alpha) * (self.maze[curr_x][curr_y].reward + ( self.discountFactor * max(self.maze[next_X][next_Y].qValues)) - self.maze[curr_x][curr_y].qValues[curr_action])
				self.maze[curr_x][curr_y].qValues[curr_action] += float(beta)

				#print "Q-Values: ", self.maze[curr_x][curr_y].qValues[curr_action]
				#print "Alpha: ", float(alpha)
				#print "Discount times", ( self.discountFactor * max(self.maze[next_X][next_Y].qValues))
				#print "Beta: ", beta

				# Update Variables
				self.maze[curr_x][curr_y].qCount[curr_action] += 1

				#print "X: ", curr_x, "Y: ", curr_y
				#for temp in range(4):
				#	print self.maze[curr_x][curr_y].qCount[temp] 

				curr_x = next_X
				curr_y = next_Y

				#print "num_moves ", num_moves
				num_moves += 1

			# Increment the number of times we've gone through the maze
			numTrials += 1

		#print "Num Trials", numTrials

		# Set the utilities for all states
		for x in range(0,6):
			for y in range(0,6):
				if (abs(self.maze[x][y].reward) < 1):
					self.maze[x][y].utility = max(self.maze[x][y].qValues)


def main():
	puzzle = Puzzle(True)	# Reward States are considered Terminal States
	puzzle.readInMaze()
	rmse = zeros((4000))
	utilitiesTDQ = zeros((4000))

	#puzzle.setUtilitiesMDP(400)
	#puzzle.printUtilities()
	#puzzle.setUtilitiesTDQL()
	#puzzle.printUtilities()
	
	#Utilities
	#for i in xrange(0,50):
	#	puzzle.setUtilitiesMDP(i)
		
	    
	
	#RMSE
	for i in xrange(0,4000):
		puzzle.setUtilitiesMDP(i)
		value = puzzle.copyUtilities()
		puzzle.setUtilitiesTDQL()
		tdq = puzzle.copyUtilities()
		rmse[i] = sqrt(sum(subtract(value,tdq)**2)/float(25))
	plt.plot(rmse)
	plt.show()
	plt.saveimg("figure1.png")
	

if __name__ == '__main__':
	main()