# Data Structures

# Ben Mooon
# David Johnston
#  -- Semester 1, 2021

#   Functions
outputdebug = True

def debug(msg):
    if outputdebug:
        print (msg)
        
def menu():
    print("1. Insert a new integer key into the AVL tree")
    print("2. Delete an integer key from the AVL tree")
    print("3. Print the in-order traversal sequence of the AVL tree")
    print("4. Print all leaf nodes of the AVL tree, and all non-leaf nodes (seperately)")
    print("5. Display the AVL tree")
    print("6. Return to Main Menu.\n")

#   Classes
class Node():
    def __init__(self, key):
        self.key = key
        self.left = None 
        self.right = None 

class AVLTree():
    def __init__(self, *args):
        self.node = None 
        self.height = -1  
        self.balance = 0; 
        
        if len(args) == 1: 
            for i in args[0]: 
                self.insert(i)

    def clear(self):
        self.node = None
        self.height = -1
        self.balance = 0
        
    def height(self):
        if self.node: 
            return self.node.height 
        else: 
            return 0
    
    def printLeaf(self, r):
        if r.node != None:
            self.printLeaf(r.node.left)
            if r.node.left.node == None and r.node.right.node == None:
                print(r.node.key, end = " ")
            self.printLeaf(r.node.right)

    def printNonLeaf(self, r):
        if r.node != None:
            self.printNonLeaf(r.node.left)
            if r.node.left.node != None or r.node.right.node != None:
                print(r.node.key, end = " ")
            self.printNonLeaf(r.node.right)
    
    def insert(self, key):
        tree = self.node
        newnode = Node(key)
        if tree == None:
            self.node = newnode 
            self.node.left = AVLTree() 
            self.node.right = AVLTree()
            debug("Inserted key <" + str(key) + ">")
        
        elif key < tree.key: 
            self.node.left.insert(key)
            
        elif key > tree.key: 
            self.node.right.insert(key)
        
        else: 
            debug("Key <" + str(key) + "> is already in tree.")
            
        self.rebalance()


    def delete(self, n):
        #   first iteration starts at root
        currentNode = self.node
        #   if the current node is not empty
        if currentNode != None:
            #   go down left children until node <n> found.
            if n < self.node.key:
                self.node.left.delete(n)
            #   go down right children until node <n> found.
            elif n > self.node.key:  
                self.node.right.delete(n)

            #   Node found! Let's delete it.
            elif self.node.key == n:
                #   if node has no children
                if self.node.left.node == None and self.node.right.node == None:
                    #   delete node
                    debug("deleting node")
                    self.node = None

                #   if node has right child (destroys current node)
                elif self.node.left.node == None:
                    debug("copy right node, deleted <n>")
                    self.node = self.node.right.node
                #   if node has left child (destroys current node)
                elif self.node.right.node == None:
                    debug("copy left node, deleted <n>")
                    self.node = self.node.left.node
                
                #   if node has left and right child, find successor
                else:  
                    nextNode = self.logicalSuccessor(self.node) 
                    if nextNode != None:
                        #   copy successor to node to delete
                        self.node.key = nextNode.key 
                        #   recursive, delete copied node
                        self.node.right.delete(nextNode.key)
                #   nodes have been deleted/copied, need rebalance
                self.rebalance()
            self.rebalance()
            
        else:
            print("ERROR: Node <",n,"> is not in the tree.",sep="")
        
    def rebalance(self): #  key inserted. Let's check if we're balanced
        self.updateHeights(False)
        self.updateBalances(False)
        while self.balance < -1 or self.balance > 1: 
            if self.balance > 1:
                if self.node.left.balance < 0:  
                    self.node.left.leftRotate() # we're in case II
                    self.updateHeights()
                    self.updateBalances()
                self.rightRotate()
                self.updateHeights()
                self.updateBalances()
                
            if self.balance < -1:
                if self.node.right.balance > 0:  
                    self.node.right.rightRotate() # we're in case III
                    self.updateHeights()
                    self.updateBalances()
                self.leftRotate()
                self.updateHeights()
                self.updateBalances()
            
    def rightRotate(self):
        # Rotate right pivoting on self
        debug ('Rotating ' + str(self.node.key) + ' right')
        A = self.node
        B = self.node.left.node
        T = B.right.node
        
        self.node =     B
        B.right.node =  A
        A.left.node =   T

    def leftRotate(self):
        # Rotate left pivoting on self
        debug ('Rotating ' + str(self.node.key) + ' left') 
        A = self.node 
        B = self.node.right.node 
        T = B.left.node 
        
        self.node =     B 
        B.left.node =   A 
        A.right.node =  T 
        
    def updateHeights(self, recurse=True):
        if not self.node == None: 
            if recurse: 
                if self.node.left != None: 
                    self.node.left.updateHeights()
                if self.node.right != None:
                    self.node.right.updateHeights()
            
            self.height = max(self.node.left.height,
                              self.node.right.height) + 1 
        else: 
            self.height = -1 
            
    def updateBalances(self, recurse=True):
        if not self.node == None: 
            if recurse: 
                if self.node.left != None: 
                    self.node.left.updateBalances()
                if self.node.right != None:
                    self.node.right.updateBalances()

            self.balance = self.node.left.height - self.node.right.height 
        else: 
            self.balance = 0 

    def logicalPredecessor(self, node):
        node = node.left.node 
        if node != None: 
            while node.right != None:
                debug("Logical Predecessor: traversing <" + str(node.key) + ">")
                if node.right.node == None: 
                    return node 
                else: 
                    node = node.right.node  
        return node 
    
    def logicalSuccessor(self, node):
        node = node.right.node  
        if node != None: # just a sanity check  
            while node.left != None:
                debug("Logical Successor: traversing <" + str(node.key) + ">")
                if node.left.node == None: 
                    return node 
                else: 
                    node = node.left.node  
        return node 

    def checkBalance(self):
        if self == None or self.node == None: 
            return True
        self.updateHeights()
        self.updateBalances()
        return ((abs(self.balance) < 2) and self.node.left.checkBalance() and self.node.right.checkBalance())  
        
    def inorder(self):
        if self.node == None:
            return [] 
        numbers = [] 
        l = self.node.left.inorder()
        for i in l: 
            numbers.append(i)
            
        numbers.append(self.node.key)
        l = self.node.right.inorder()
        for i in l: 
            numbers.append(i) 
        return numbers 
    
    def printTree(self):               ##  https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
        def display(root):             ##  AUTHOR: Original: J.V.     Edit: BcK
            #   No child.
            if root.node.right.node is None and root.node.left.node is None:
                line = (str(root.node.key) + ' [' + str(root.height) + ':' + str(root.balance) + ']' )
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle

            #   Only left child.
            if root.node.right.node is None:
                lines, n, p, x = display(root.node.left)
                nodeOutput = (str(root.node.key) + ' [' + str(root.height) + ':' + str(root.balance) + ']' )
                keyLength = len(nodeOutput)
                first_line = (x + 1) * ' ' + (n - x - 1) * '_' + nodeOutput
                second_line = x * ' ' + '/' + (n - x - 1 + keyLength) * ' '
                shifted_lines = [line + keyLength * ' ' for line in lines]
                return [first_line, second_line] + shifted_lines, n + keyLength, p + 2, n + keyLength // 2

            #   Only right child.
            if root.node.left.node is None:
                lines, n, p, x = display(root.node.right)
                nodeOutput = (str(root.node.key) + ' [' + str(root.height) + ':' + str(root.balance) + ']' )
                keyLength = len(nodeOutput)
                first_line = nodeOutput + x * '_' + (n - x) * ' '
                second_line = (keyLength + x) * ' ' + '\\' + (n - x - 1) * ' '
                shifted_lines = [keyLength * ' ' + line for line in lines]
                return [first_line, second_line] + shifted_lines, n + keyLength, p + 2, keyLength // 2

            #   Two children.
            left, n, p, x = display(root.node.left)
            right, m, q, y = display(root.node.right)
            nodeOutput = (str(root.node.key) + ' [' + str(root.height) + ':' + str(root.balance) + ']' )
            keyLength = len(nodeOutput)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + nodeOutput + y * '_' + (m - y) * ' '
            second_line = x * ' ' + '/' + (n - x - 1 + keyLength + y) * ' ' + '\\' + (m - y - 1) * ' '
            if p < q:
                left += [n * ' '] * (q - p)
            elif q < p:
                right += [m * ' '] * (p - q)
            zipped_lines = zip(left, right)
            lines = [first_line, second_line] + [a + keyLength * ' ' + b for a, b in zipped_lines]
            return lines, n + m + keyLength, max(p, q) + 2, n + keyLength // 2

        lines = []
        if self.node != None:
            lines, *_ = display(self)
            print("\t\t== AVL Tree ==     Key:  Node [Height : Balance]")
            print()
        if lines == []:
            print("No tree found, please rebuild a new Tree.\n")
            return -1
        for line in lines:
            print(line)
        print()
#                                                                                                                               #
#####################################################-- END AVLTree Class --#####################################################
#                                                                                                                               #
#   Main Program
tree = AVLTree()
attempts = 0
while True:
    #   Menu 1: Build a tree
    choice = None
    attempts = 0
    while True:
        print("1. Pre-load a sequence of integers to build an AVL Tree")
        print("2. Manually enter integer values/keys, one-by-one, to build an AVL Tree")
        print("3. Quit Program")
        choice = input(" >> ")

        #   Selection 1: Use built-in integers
        if choice == "1":
            numbers = [55, 81, 65, 20, 35, 79, 23, 14, 21, 103, 92, 45, 85, 51, 47, 48, 50, 46]
            break

        #   Selection 2: Build from input integers
        if choice == "2":
            numbers = []
            attempts = 0
            while attempts < 5:
                try:
                    treeSize = int(input("Please enter the size of the tree\n >> "))
                    if treeSize < 0:
                        raise ValueError
                    break
                except ValueError:
                    attempts += 1
                    print("ERROR: Invalid Input")
                    
            while len(numbers) < treeSize and attempts < 5:
                try:
                    addNumber = int(input("Please enter a number\n >> "))
                    numbers.append(addNumber)
                except ValueError:
                    attempts += 1
                    print("ERROR: Invalid Input")
            break

        if choice == "3" or attempts == 5:
            break
    
        else:
            attempts += 1
            print("ERROR: Invalid Input")

    if choice == "3" or attempts == 5:
        print("Exiting Program")
        break
    
    for i in numbers:
        tree.insert(i)

    #   Menu 2: Edit the tree
    if tree.printTree() == -1:
        continue
    menu()
    while True:
        choice = input("Select menu item ('m' to see menu):\n >> ").lower()

        #   Selection 1: Insert a Node
        if choice == "1":
            if tree.printTree() == -1:
                break
            
            attempts = 0
            while attempts < 5:
                attempts += 1
                try:
                    n = int(input("Enter a number to insert into the tree\n >> "))
                    tree.insert(n)
                    break
                except ValueError:
                    print("ERROR: Invalid input.")
            if attempts == 5:
                print("Returning to Menu ...")

        #   Selection 2: Delete a Node
        elif choice == "2":
            if tree.printTree() == -1:
                break

            attempts = 0
            while attempts < 5:
                try:
                    n = int(input("Enter a Node from the above tree to delete\n >> "))
                    tree.delete(n)
                    break
                except ValueError:
                    attempts += 1
                    print("ERROR: Invalid input.")
            if attempts == 5:
                print("Returning to Menu ...")

        #   Selection 3: Print in-order Traversal
        elif choice == "3":
            if tree.printTree() == -1:
                break
            print("In-order Traversal:")
            print(tree.inorder())

        #   Selection 4: Print all leaf nodes of the AVL tree, and all non-leaf nodes (seperately)
        elif choice == "4":
            if tree.printTree() == -1:
                break
            print("Leaf Nodes: ")
            tree.printLeaf(tree)
            print()
            print("Non-Leaf Nodes: ")
            tree.printNonLeaf(tree)
            print()

        #   Selection 5: Display the AVL tree
        elif choice == "5":
            if tree.printTree() == -1:
                break

        #   Selection 6: Display Menu
        elif choice == "m":
            menu()

        #   Selection 6: Return to main menu
        elif choice == "6" or attempts == 5:
            print("Returning to Main Menu, AVLTree has been reset.")
            tree.clear()
            break

        else:
            attempts += 1
            print("Invalid Input")

if attempts == 5:
    print("Too many invalid attempts")
