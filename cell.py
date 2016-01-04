class Cell(object):

	"""Represents a Cell Object"""

	def __init__(self, curr_x, curr_y):
		self.x = curr_x
		self.y = curr_y
		self.wall = False
		self.reward = -0.04
		self.utility = 0.0

		# Left, Up, Right, Down
		self.qValues = [0.0, 0.0, 0.0, 0.0]
		self.qCount = [0, 0, 0, 0]

	def setReward(self, rewardStatus):
		self.reward = rewardStatus

	def setWall(self):
		self.wall = True

	def setUtility(self, curr_utility):
		self.utility = curr_utility

	#def appendUtilSeq(self, value):
	#	self.utilitySequence.append(value)

if __name__ == '__main__':
	main()