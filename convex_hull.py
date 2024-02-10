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
		self.view.addLines(line,color)
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



	def mergeHulls(self, leftHull, rightHull):
		print("left hull points: ", leftHull)
		print("\nright hull points: ", rightHull)
		copyCurrentPointsRight = rightHull.copy()
		#sort by slope
		def SortbySlopeClockWise(point): # in constant time sorts the points by slope in clock wise 
				if (point.x() == copyCurrentPointsRight[len(rightHull)-1].x()):
					slope = float('-inf')
				else: 
					slope = (point.y() - copyCurrentPointsRight[len(rightHull)-1].y()) / (point.x() - 
										    copyCurrentPointsRight[len(rightHull)-1].x())
				return slope
		rightHull.sort(key=SortbySlope)
		copyCurrentPointsLeft = leftHull.copy()
		def sortBySlopeCounterClockWise(point): # Also just constant time
				if (point.x() == copyCurrentPointsLeft[0].x()):
					slope = float('inf')
				else: 
					slope = (point.y() - copyCurrentPointsLeft[0].y()) / (point.x() - copyCurrentPointsLeft[0].x())
				return -1*slope
			
		leftHull.sort(key=sortBySlopeCounterClockWise)
		
		# Find the rightmost point of the left hull and the leftmost point of the right hull
		rightMostLeftHullPoint = max(leftHull, key=lambda point: point.x()) #done in O(N) time
		leftMostRightHullPoint = min(rightHull, key=lambda point: point.x())
		print("Right most point of the left hull: ", rightMostLeftHullPoint)
		print("\nLeft Most point of the Right hull: ", leftMostRightHullPoint)
		# Find the upper tangent
		
		# Find the lower tangent
		
		# Merge the left and right hulls
		
		
	def divideAndConquer(self, sortedPoints):
		if(len(sortedPoints) < 4):
			print("SortedPoints: ", sortedPoints)
			#self.createHull(sortedPoints)
			return sortedPoints
		midPoint = len(sortedPoints) // 2 #split here 
		leftHalf = self.divideAndConquer(sortedPoints[:midPoint])
		rightHalf = self.divideAndConquer(sortedPoints[midPoint:])
		self.mergeHulls(leftHalf, rightHalf)
		
	def createHull(self, points):
		print("points size: ", len(points))
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
			self.showHull(polygon,RED)
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
	
		
	
