from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



import time
DEBUGGER = False

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
PAUSE = 0.25

#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

# Class constructor
	def __init__( self):
		super().__init__()
		self.pause = False

# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line, color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseHull(self,polygon):
		self.view.clearLines(polygon)

	def showText(self,text):
		self.view.displayStatusText(text)
	def sortClockWiseFromLeftmost(self, points, leftmost):
				print("in sort clockwise\n")
				def calculate_slope(point):
					if point.x() == leftmost.x():
						return float('-inf')
					return (point.y() - leftmost.y()) / (point.x() - leftmost.x())
				return sorted(points, key=calculate_slope)
	def sortCounterClockWiseFromRightmost(self, points, rightmost):
			def calculate_slope(point):
				if point.x() == rightmost.x():
					return float('inf')
				return (point.y() - rightmost.y()) / (point.x() - rightmost.x())
			return sorted(points, key=calculate_slope, reverse=True)

	def mergeHulls(self, leftHull, rightHull):
		print("left hull points: ", leftHull)
		print("\nright hull points: ", rightHull)
		# Find the rightmost point of the left hull and the leftmost point of the right hull
		rightMostLeftHullPoint = max(leftHull, key=lambda point: point.x()) #done in O(N) time
		leftMostRightHullPoint = min(rightHull, key=lambda point: point.x())
		print("Right most point of the left hull: ", rightMostLeftHullPoint)
		print("\nLeft Most point of the Right hull: ", leftMostRightHullPoint)
		#sorting points by slope 
		
		slopeOrderedRightHull = self.sortClockWiseFromLeftmost(points=rightHull, leftmost=leftMostRightHullPoint)
		print("\nRight hull sorted by slope based on leftMost Point: ", slopeOrderedRightHull)

		slopeOrderedLeftHull = self.sortCounterClockWiseFromRightmost(points=leftHull, rightmost=rightMostLeftHullPoint)
		print("\nLeft hull sorted by slope based on rightMost Point: ", slopeOrderedLeftHull)

		# Find the upper tangent
		left_index = 0
		right_index = 0
		maxLeftIndex = 0
		maxRightIndex = 0
		newMaxFound = True
		lowestSlope = None
		
		while newMaxFound == True:
			newMaxFound = False # set false as no new max has been found
			# Calculate slopes of current points
			print("left index: ", slopeOrderedLeftHull[left_index], "\nright index: ", slopeOrderedRightHull[right_index])
			newSlope = self.findSlope(slopeOrderedLeftHull[left_index], slopeOrderedRightHull[right_index]) # find a new slope
			print("newSlope: ", newSlope, "\nmaxSlope before check: ", lowestSlope)
			if lowestSlope == None: # if max slope not set then new slope is max slope 
				lowestSlope = newSlope
				newMaxFound = True
				maxLeftIndex = left_index
			elif newSlope < lowestSlope:
				lowestSlope = newSlope
				newMaxFound = True
				maxLeftIndex = left_index
			
			# Move pointers
			# Increment left pointer if left slope is smaller
			left_index = (left_index - 1) % len(slopeOrderedLeftHull)
		maxSlope = None
		newMaxFound = True
		while newMaxFound == True:
			newMaxFound = False # set false as no new max has been found
			# Calculate slopes of current points
			print("left index: ", slopeOrderedLeftHull[maxLeftIndex], "\nright index: ", slopeOrderedRightHull[right_index])
			newSlope = self.findSlope(slopeOrderedLeftHull[maxLeftIndex], slopeOrderedRightHull[right_index]) # find a new slope
			print("newSlope: ", newSlope, "\nmaxSlope before check: ", maxSlope)
			if maxSlope == None: # if max slope not set then new slope is max slope 
				maxSlope = newSlope
				newMaxFound = True
				maxRightIndex = right_index
			elif newSlope > maxSlope:
				maxSlope = newSlope
				newMaxFound = True
				maxRightIndex = right_index
			# Move pointers
			# Increment left pointer if left slope is smaller
			right_index = (right_index - 1) % len(slopeOrderedRightHull)
		
		polygon = []
		line = QLineF(slopeOrderedLeftHull[maxLeftIndex], slopeOrderedRightHull[maxRightIndex])
		polygon.append(line)
		self.showHull(polygon,RED)
				
		# Find the lower tangent
		print("in lower tangent")
		#reset variables 
		left_index = 0
		right_index = 0
		maxLeftIndex = 0
		maxRightIndex = 0
		newMaxFound = True
		lowestSlope = None
		
		while newMaxFound == True:
			newMaxFound = False # set false as no new max has been found
			# Calculate slopes of current points
			print("left index: ", slopeOrderedLeftHull[left_index], "\nright index: ", slopeOrderedRightHull[right_index])
			newSlope = self.findSlope(slopeOrderedLeftHull[left_index], slopeOrderedRightHull[right_index]) # find a new slope
			print("newSlope: ", newSlope, "\nmaxSlope before check: ", lowestSlope)
			if lowestSlope == None: # if max slope not set then new slope is max slope 
				lowestSlope = newSlope
				newMaxFound = True
				maxRightIndex = right_index
			elif newSlope < lowestSlope:
				lowestSlope = newSlope
				newMaxFound = True
				maxRightIndex = right_index
			# Move pointers
			# Increment left pointer if left slope is smaller
			right_index = (right_index - 1) % len(slopeOrderedRightHull)

		maxSlope = None
		newMaxFound = True
		while newMaxFound == True:
			newMaxFound = False # set false as no new max has been found
			# Calculate slopes of current points
			print("left index: ", slopeOrderedLeftHull[left_index], "\nright index: ", slopeOrderedRightHull[maxRightIndex])
			newSlope = self.findSlope(slopeOrderedLeftHull[left_index], slopeOrderedRightHull[maxRightIndex]) # find a new slope
			print("newSlope: ", newSlope, "\nmaxSlope before check: ", maxSlope)
			if maxSlope == None: # if max slope not set then new slope is max slope 
				maxSlope = newSlope
				newMaxFound = True
				maxLeftIndex = left_index
			elif newSlope > maxSlope:
				maxSlope = newSlope
				newMaxFound = True
				maxLeftIndex = left_index
			
			# Move pointers
			# Increment left pointer if left slope is smaller
			left_index = (left_index - 1) % len(slopeOrderedLeftHull)
		polygon = []
		line = QLineF(slopeOrderedLeftHull[maxLeftIndex], slopeOrderedRightHull[maxRightIndex])
		polygon.append(line)
		self.showHull(polygon,GREEN)
		# Merge the left and right hulls
		return 
	def findSlope(self, point1, point2):
		slope = (point1.y() - point2.y()) / (point1.x() - point2.x())
		return slope
	def divideAndConquer(self, sortedPoints):
		if(len(sortedPoints) < 4):
			#print("SortedPoints: ", sortedPoints)
			self.createHull(sortedPoints)
			return sortedPoints
		midPoint = len(sortedPoints) // 2 #split here 
		leftHalf = self.divideAndConquer(sortedPoints[:midPoint])
		rightHalf = self.divideAndConquer(sortedPoints[midPoint:])
		return self.mergeHulls(leftHalf, rightHalf)
		
	def createHull(self, points):
		if len(points) == 1:#should not happen throw error
			raise ValueError("Error: only one point is passed in ")
		if len(points) > 1:
			polygon = []
			for i in range(len(points)):
				if(i == len(points) - 1):
					line = QLineF(points[i],points[(0)])
				else:
					line = QLineF(points[i],points[(i+1)])
				polygon.append(line)
			self.showHull(polygon,BLUE)
# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		# TODO: SORT THE POINTS BY INCREASING X-VALUE 
		#sort using sorted with key 
		sortedPoints = sorted(points, key=lambda point: point.x())	
		t2 = time.time()
		if DEBUGGER == True: #check if sorted properly 
			print(sortedPoints)
			polygon = [QLineF(sortedPoints[i],sortedPoints[(i+1)]) for i in range(9)]
			self.showHull(polygon,RED)	
			print("time: ", t1)
		#divide the sortedpoints divide and conquere
		dividedPoints = self.divideAndConquer(sortedPoints)
		print("divided Points: ", dividedPoints)
		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		#polygon = [QLineF(points[i],points[(i+1)%3]) for i in range(3)]
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		#self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
	
		
	
