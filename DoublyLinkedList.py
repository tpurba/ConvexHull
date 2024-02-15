from Node import Node

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, point):
        new_node = Node(point)
        if not self.head:
            self.head = new_node
            self.head.prev = self.head  # Circular reference
            self.head.next = self.head  # Circular reference
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.prev = current
            new_node.next = self.head #each time a new node is added the new nodes next is set to the self.head or the start
            self.head.prev = new_node #each time a new node is added the first nodes previous is set to the new node

    def display_forward(self):
        current = self.head
        while current:
            print(current.point, end=" <-> ")
            current = current.next
            if current == self.head:
                break
        print("None")

    def display_backward(self):
        current = self.head
        while current.prev != self.head:
            current = current.prev
        while current:
            print(current.point, end=" <-> ")
            current = current.next
        print("None")