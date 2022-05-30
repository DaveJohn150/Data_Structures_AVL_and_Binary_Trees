# Data Structures

# Ben Mooon
# David Johnston
#  -- Semester 1, 2021

#   Functions
def menu():
    print()
    print("1. Print the pre-order, in-order, and post-order of the BST, in sequence")
    print("2. Print all leaf nodes in BST, then all non-leaf nodes (seperately)")
    print("3. Print the total number of nodes of a subtree")
    print("4. Print the depth of a subtree rooted at a particular node")
    print("5. Insert a new integer key into the BST")
    print("6. Delete an integer key from the BST")
    print("7. Print BST tree")
    print("8. Return to Main Menu.")
    print()

def printTree(root, element="element", left="left", right="right"):                                 ##  https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
    def display(root, element=element, left=left, right=right):                                     ##  AUTHOR: Original: J.V.     Edit: BcK
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if getattr(root, right) is None and getattr(root, left) is None:
            line = '%s' % getattr(root, element)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if getattr(root, right) is None:
            lines, n, p, x = display(getattr(root, left))
            s = '%s' % getattr(root, element)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if getattr(root, left) is None:
            lines, n, p, x = display(getattr(root, right))
            s = '%s' % getattr(root, element)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = display(getattr(root, left))
        right, m, q, y = display(getattr(root, right))
        s = '%s' % getattr(root, element)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2
    
    lines = []
    if root != None:
        lines, *_ = display(root, element, left, right)
    print("\t== Binary Tree ==")
    print()
    if lines == []:
        print("\t  No tree found")
    for line in lines:
        print("\t", line)
    print()

#   Classes
class TreeNode():
    def __init__(self, e):
      self.element = e
      self.left = None # Point to the left node, default None
      self.right = None # Point to the right node, default None

class BinaryTree:
    def __init__(self):
        self.root = None
        self.size = 0
        self.subSize = 0

    def insert(self, e):
        if self.root == None:
            self.root = self.createNewNode(e) # Create a new root
        else:
            #   Locate the parent node
            parent = None
            current = self.root
            while current != None:
                if e < current.element:
                    parent = current
                    current = current.left
                elif e > current.element:
                    parent = current
                    current = current.right
                else:
                    print("ERROR: Node <",e,"> already exists in the BST!")
                    return False #  Duplicate node not inserted

            #   Create the new node and attach it to the parent node
            if e < parent.element:
                parent.left = self.createNewNode(e)
            else:
                parent.right = self.createNewNode(e)

        self.size += 1
        return True 


    def delete(self, elem):
        parent = None
        current = self.root
        while current != None and current.element != elem:
            parent = current
            if elem < current.element:
                current = current.left
            else:
                current = current.right
                
        #   If node not found
        if current == None:
            return "ERROR: Node <"+str(elem)+"> not found!"
        #   Node has no children
        if current.left == None and current.right == None:
            if current != self.root:
                if parent.left == current:
                    parent.left = None
                else:
                    parent.right = None
            else:
                self.root = None
        #   node has two children
        elif current.left != None and current.right != None:
            nextNode = current.right
            while nextNode.left != None:
                nextNode = nextNode.left
            nextVal = nextNode.element
            self.delete(nextVal)
            current.element = nextVal
        #   node has one child
        else:
            if current.left != None:
                child = current.left
            else:
                child = current.right
            if current != self.root:
                if current == parent.left:
                    parent.left = child
                else:
                    parent.right = child
            else:
                self.root = child
        self.size -= 1
        return "SUCCESS: Node: "+str(elem)+" deleted."    

    # Returns element if in the tree
    def searchNode(self, e):
        current = self.root # Start from the root

        while current != None:
            if e < current.element:
                current = current.left
            elif e > current.element:
                current = current.right
            else: # element matches current.element
                return current # Element is found
        return None
        
    def isEmpty(self):
        return self.size == 0

    def clear(self):
        self.root = None
        self.size = 0
        
    def createNewNode(self, e):
        return TreeNode(e)

    def getSize(self):
        return self.size

    def getRoot(self):
        return self.root


    #   In order
    def inorder(self, r):
        if r != None:
            self.inorder(r.left)
            print(r.element, end = " ")
            self.inorder(r.right)

    def inorderLeafOnly(self, r):
        if r != None:
            self.inorderLeafOnly(r.left)
            if r.left == None and r.right == None:
                print(r.element, end = " ")
            self.inorderLeafOnly(r.right)

    def inorderNonLeaf(self, r):
        if r != None:
            self.inorderNonLeaf(r.left)
            if r.left != None or r.right != None:
                print(r.element, end = " ")
            self.inorderNonLeaf(r.right)


    #   Post order
    def postorder(self, root):
        if root != None:
            self.postorder(root.left)
            self.postorder(root.right)
            print(root.element, end = " ")

    def postorderSearchDepth(self, root, depth = 0):
        depth += 1
        if root != None:
            l = self.postorderSearchDepth(root.left, depth)
            r = self.postorderSearchDepth(root.right, depth)
            if l != None and r != None:
                if l >= r:
                    if l > depth:
                        depth = l
                else:
                    if r > depth:
                        depth = r
                        
            elif l != None:
                if l > depth:
                    depth = l
                    
            elif r != None:
                if r > depth:
                    depth = r 
            return depth

    #   Pre order
    def preorder(self, root):
        if root != None:
            print(root.element, end = " ")
            self.subSize += 1
            self.preorder(root.left)
            self.preorder(root.right)

    def subtreePreorder(self, elem):
        self.subSize = 0
        subNode = self.searchNode(elem)
        if subNode != None:
            self.preorder(subNode)
            return self.subSize
        else:
            print("ERROR: Node <"+str(elem)+"> not found!")


#                                                                                                                               #
#####################################################-- END BinaryTree Class --##################################################
#                                                                                                                               #
#   Main Program
tree = BinaryTree()
while True:
    while True:
        print("1. Pre-load a sequence of integers to build a BST")
        print("2. Manually enter integer values/keys, one-by-one, to build a BST")
        print("3. Quit Program")
        x = input(" >> ")
        if x == "1":
            numbers = [55, 81, 65, 20, 35, 79, 23, 14, 21, 103, 92, 45, 85, 51, 47, 48, 50, 46]
            break
        elif x == "2":
            numbers = []
            count = 0
            while count < 5:
                try:
                    treeSize = int(input("Please enter the size of the tree\n >> "))
                    if treeSize < 0:
                        raise ValueError
                    break
                except ValueError:
                    print("ERROR: Invalid Input")
                    count += 1
                    treeSize = 0
            count = 0
            while len(numbers) < treeSize and count < 5:
                try:
                    addNumber = int(input("Please enter a number\n >> "))
                    numbers.append(addNumber)
                except ValueError:
                    print("ERROR: Invalid Input")
                    count += 1
            break
        elif x == "3":
            break
        else:
            print("ERROR: Invalid Input")

    if x == "3":
        break
    
    for i in numbers:
        tree.insert(i)

    menu()
    printTree(tree.getRoot())
    count = 0
    while count < 5:
        y = input("Select menu item ('m' to see menu):\n >> ").lower()

        #   Selection 1
        if y == "1":
            print("Tree Traversals ")
            print("Pre-order Traversal:")
            tree.preorder(tree.getRoot())
            print()
            print("In-order Traversal:")
            tree.inorder(tree.getRoot())
            print()
            print("Post-order Traversal:")
            tree.postorder(tree.getRoot())
            print()

        #   Selection 2
        elif y == "2":
            print("Leaf Only (inorder): ")
            tree.inorderLeafOnly(tree.getRoot())
            print()
            print("Non-leaf Only (inorder): ")
            tree.inorderNonLeaf(tree.getRoot())
            print()

        #   Selection 3
        elif y == "3":
            print("Preorder: ")
            tree.preorder(tree.getRoot())
            print()
            while True:
                while True:
                    try:
                        n = int(input("Input the node to calculate subtree size\n >> "))
                        print("Preorder of subtree:",n)
                        m = tree.subtreePreorder(n)
                        break
                    except ValueError:
                        print("ERROR: Invalid input.")
                if m != None:
                    print("\nThe total nodes of Sub-tree: <",n,"> is: ",m, sep="")
                    printTree(tree.searchNode(n))
                    break
                else:
                    continue

        #   Selection 4
        elif y == "4":
            print("Preorder: ")
            tree.postorder(tree.getRoot())
            print()
            while True:
                while True:
                    try:
                        n = int(input("Please select a node to find the depth of that sub-tree\n >> "))
                        m = tree.searchNode(n)
                        break
                    except ValueError:
                        print("ERROR: Invalid input.")
                if m != None:
                    print("Sub-tree ",n," has a depth of: ", tree.postorderSearchDepth(m) - 1, sep="")
                    printTree(tree.searchNode(n))
                    break
                else:
                    print ("ERROR: <",n,"> not found in Binary tree", sep="")
                
        #   Selection 5
        elif y == "5":
            while True:
                try:
                    n = int(input("Enter a number to insert into a tree\n >> "))
                    if tree.insert(n) == True:
                        print("Success: Node ",n," has been inserted.",sep="")
                        break
                except ValueError:
                    print("ERROR: Invalid input.")
                break

        #   Selection 6
        elif y == "6":
            print("Preorder: ")
            tree.preorder(tree.getRoot())
            print()
            while True:
                try:
                    i = int(input("Enter a number to delete from the tree\n >> "))
                    print(tree.delete(i))
                    break
                except ValueError:
                    print("ERROR: Invalid input.")

        #   Selection 7
        elif y == "7":
            printTree(tree.getRoot())
            
        #   Selection 8
        elif y == "8":
            tree.clear()
            break
        elif y == "m":
            menu()
            
        else:
            print("Invalid Input")
            count += 1
