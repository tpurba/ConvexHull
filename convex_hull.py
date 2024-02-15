from which_pyqt import PYQT_VER
from DoublyLinkedList import DoublyLinkedList
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
		#print("In show hull")
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseHull(self,polygon):
		self.view.clearLines(polygon)

	def showText(self,text):
		self.view.displayStatusText(text)

	def findSlope(self, point1, point2):
		slope = (point1.y() - point2.y()) / (point1.x() - point2.x())
		return slope
	def convertHullToPolygon(self, hull):
		# print("In convert hull to polygon")
		# print("PRINTING THE HULL FORWARD")
		# hull.display_forward()
		current = hull.head
		polygon = []
		while current:
			polygon.append(QLineF(current.point, current.next.point))
			current = current.next
			if current == hull.head:
				break
			if current == None:
				break
			
			
		#print("polygon: ", polygon)
		self.showHull(polygon, RED)
	def findUpperTangent(self, leftHull, rightHull):
		#print("In find upper tangent")
		done = False
		leftChecking = True
		rightChecking = True
		currentLeft = leftHull.head
		currentRight = rightHull.head
		leftUpperTangent = leftHull.head
		rightUppertangent = rightHull.head
		#print("left Hull head: ", currentLeft.point, "\n right hull head: ", currentRight.point)
		maxSlope = self.findSlope(currentLeft.point,  currentRight.point)
		while done == False:
			while(leftChecking == True):
				currentLeft = currentLeft.prev # move the iterator counter clockwise 
				if(currentLeft.point == leftHull.head.point):#made a full circle
					leftChecking = False
					done = True # set to finish 
				tempSlope = self.findSlope(currentLeft.point, rightUppertangent.point)
				if(maxSlope > tempSlope): # means that the slope we found is more in line to be upper tangent 
					leftChecking = True
					maxSlope = tempSlope
					leftUpperTangent = currentLeft # set the current upper tangent point
					rightChecking = True
			while(rightChecking == True):
				currentRight = currentRight.next 
				if(currentRight.point == rightHull.head.point):
					rightChecking = False
					leftChecking = True # to check left again 
					done = False
				tempSlope = self.findSlope(leftUpperTangent.point, currentRight.point)
				if(tempSlope > maxSlope):
					rightChecking = True
					maxSlope = tempSlope
					rightUppertangent = currentRight
		return leftUpperTangent, rightUppertangent
	
	def findLowerTangent(self, leftHull, rightHull):
		#print("In find lower tangent")
		done = False
		leftChecking = True
		rightChecking = True
		currentLeft = leftHull.head
		currentRight = rightHull.head
		leftLowerTangent = leftHull.head
		rightLowerTangent = rightHull.head
		#print("left Hull head: ", currentLeft.point, "\n right hull head: ", currentRight.point)
		maxSlope = self.findSlope(currentLeft.point,  currentRight.point)
		while done == False:
			while(rightChecking == True):
				currentRight = currentRight.next 
				if(currentRight.point == rightHull.head.point):
					rightChecking = False
					done = True # set to finish 
				tempSlope = self.findSlope(leftLowerTangent.point, currentRight.point)
				if(tempSlope < maxSlope):
					rightChecking = True
					maxSlope = tempSlope
					rightLowerTangent = currentRight
					leftChecking = True
			while(leftChecking == True):
				currentLeft = currentLeft.prev # move the iterator counter clockwise 
				if(currentLeft.point == leftHull.head.point):#made a full circle
					leftChecking = False
					done = False
					rightChecking = True
				tempSlope = self.findSlope(currentLeft.point, rightLowerTangent.point)
				if(tempSlope > maxSlope): # means that the slope we found is more in line to be upper tangent 
					leftChecking = True
					maxSlope = tempSlope
					leftLowerTangent = currentLeft # set the current upper tangent point
		return leftLowerTangent, rightLowerTangent
	
	def mergeHulls(self, leftHull, rightHull):
		#print("In mergeHulls")
		leftUpperTangent, rightUpperTangent = self.findUpperTangent(leftHull, rightHull)
		leftLowerTangent, rightLowerTangent = self.findLowerTangent(leftHull, rightHull)
		#print("Finished finding tangents")
		leftUpperTangent.next = rightUpperTangent
		rightUpperTangent.prev = leftUpperTangent
		rightLowerTangent.next = leftLowerTangent
		leftLowerTangent.prev = rightLowerTangent
		#leftHull.display_forward()
		return leftHull
	
	def divideAndConquer(self, sortedPoints):
		if(len(sortedPoints) < 4):
			#print("SortedPoints: ", sortedPoints)
			hullLinkedList = self.createHull(sortedPoints)
			#hullLinkedList.display_forward()
			#hullLinkedList.display_backward()
			return hullLinkedList
		midPoint = len(sortedPoints) // 2 #split here 
		leftHalf = self.divideAndConquer(sortedPoints[:midPoint])
		rightHalf = self.divideAndConquer(sortedPoints[midPoint:])
		return self.mergeHulls(leftHalf, rightHalf)
		
	def createHull(self, points):
		hullLinkedList = DoublyLinkedList()
		if len(points) == 2:
			hullLinkedList.append(points[0])
			hullLinkedList.append(points[1])
			return hullLinkedList
		else:
			# if slope point 1 is less than point 2 swap so that the first one has highest slope 
			if(self.findSlope(points[0], points[1]) < self.findSlope(points[0], points[2])):
				points[1], points[2] = points[2], points[1]#swap points 1 and 2 
			hullLinkedList.append(points[0])
			hullLinkedList.append(points[1])
			hullLinkedList.append(points[2])
			return hullLinkedList
# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		# TODO: SORT THE POINTS BY INCREASING X-VALUE 
		#sort using sorted with key 
		sortedPoints = sorted(points, key=lambda point: point.x())# mention that this sort is nlogn
		t2 = time.time()
		if DEBUGGER == True: #check if sorted properly 
			print(sortedPoints)
			polygon = [QLineF(sortedPoints[i],sortedPoints[(i+1)]) for i in range(9)]
			self.showHull(polygon,RED)	
			print("time: ", t1)
		#divide the sortedpoints divide and conquere
		finishedHull = self.divideAndConquer(sortedPoints)
		self.convertHullToPolygon(finishedHull)
		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		#polygon = [QLineF(points[i],points[(i+1)%3]) for i in range(3)]
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		#self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t1))
	








	# if len(points) == 1:#should not happen throw error
	# 		raise ValueError("Error: only one point is passed in ")
	# 	if len(points) > 1:
	# 		polygon = []
	# 		for i in range(len(points)):
	# 			if(i == len(points) - 1):
	# 				line = QLineF(points[i],points[(0)])
	# 			else:
	# 				line = QLineF(points[i],points[(i+1)])
	# 			polygon.append(line)
	# 		self.showHull(polygon,BLUE)
		
	
