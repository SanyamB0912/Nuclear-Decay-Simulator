import periodictable
import sys
import time
from graphviz import Digraph
from fpdf import FPDF

# Increase recursion limit
sys.setrecursionlimit(10000)

import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz-11.0.0-win64/bin'


class Element:
    """
    Custom defined singly linked list that is used to store each property/feature of an element in each node.
    Node structure is as below
    """
    class Node():                                     #Node definition for Element class
        def __init__(self, prop, value):
            self.prop = prop
            self.value = value
            self.next = None
    
    def __init__(self, element, atomic_no, mass_no):       #initialization populates the entire list. Binding energy is calculated by pre-defined function
        self.symbol = self.head = self.Node("Symbol", element)
        self.atomic_number = self.head.next = self.Node("Atomic Number", atomic_no)
        self.mass_number = self.head.next.next = self.Node("Mass Number", mass_no)
        self.binding_energy = self.head.next.next.next = self.tail = self.Node("Binding Energy", self.calculate_binding_energy(element, atomic_no, mass_no))
        self.size = 4

    def __getitem__(self, key):
        """
        This is a magic method in python. We can compare it to operator overloading in the sense that this function allows us to
        use the [] operators and helps us index the linked list.

        Time complexity to get the item of an index: O(n) since the implementation traverses the list in a for loop until the node
        of that index is reached.
        """
        if not str(key).isnumeric():                           #validating the index to see if it is an integer
            print("Error: Not a number")
            return
        if 0 > key or key >= self.size:                        #validating to check if the index is within bounds NOTE negative index support not added
            print("Error: Index out of bounds")
            return

        node = self.head                                       #traversing the list until the required node is reached
        for _ in range(key):                                   # O(n) where n is the list size
            node = node.next
        return node.value
        
    def __setitem__(self, key, value):
        """
        This method also overrides [] operator and allows modifying a node/ object accessed at given index
        Time Complexity: O(n) for similar reasons as __getitem__
        """
        if not str(key).isnumeric():
            raise TypeError("Index must be an integer")
            return
        if  0 > key or key >= self.size:
            raise ValueError("Index out of bounds")
            return

        node = self.head
        for _ in range(key):
            node = node.next
        node.value = value

    def __str__(self) -> str: 
        """
        Also a magic method, this returns the string format of the list whenever needed. Eg. 
        Sodium = Element("Na", 11, 23)
        print(Sodium)

        Sample O/P
        [Na, 11, 23, 7.87]
        """
        return "[" + str(self.head.value) + ", " + str(self.head.next.value) + ", " + str(self.head.next.next.value) +", " + str(self.head.next.next.next.value) + "]"
    
    def calculate_binding_energy(self, atom, atomic_number, mass_number):
        """
        Function to calculate the binding energy based on the mass no and atomic no
        Time Complexity:O(no of isotopes)=can be approximated to O(1) since most elements have very few isotopes. + any overhead due to periodictable library
        """
        element = getattr(periodictable, atom)
        protons = atomic_number
        neutrons = mass_number - atomic_number
        mass = 0
        
        total_mass_atom = (protons * 1.007276) + (neutrons * 1.008665)
        for isotopes in element:
            if str(isotopes)[:3:] == str(mass_number):
                mass = isotopes.mass
        mass_defect = total_mass_atom - mass
        bepn = mass_defect * (931.5) / mass_number
        return bepn

class ElementList:
    """
    Custom defined doubly linked list that is used to store each element in each node.
    Node structure is as below
    """
    class Node():
        """
        Each feature of the element is a separate data member.
        """
        def __init__(self, element, atomic_no=0, mass_no=0, binding_energy=0):
            self.element = element
            self.atomic_no = atomic_no
            self.mass_no = mass_no
            self.binding_energy = binding_energy
            self.prev = None
            self.key = None
            self.next = None

    def __init__(self):
        self.head = None 
        self.tail = None
        self.size = 0

    def __getitem__(self, key):
        """
        This is a magic method in python. We can compare it to operator overloading in the sense that this function allows us to
        use the [] operators and helps us index the linked list.

        Time complexity to get the item of an index: O(n) since the implementation traverses the list in a for loop until the node
        of that index is reached.
        """
        if not str(key).isnumeric():
            raise TypeError("Index must be an integer")
        if key >= self.size or key <0:
            raise ValueError("Index out of bounds")

        node = self.head
        for _ in range(key):
            node = node.next
        return node
        
    def __setitem__(self, key, value):
        """
        This method also overrides [] operator and allows modifying a node/ object accessed at given index
        Time Complexity: O(n) for similar reasons as __getitem__
        """
        if not str(key).isnumeric():
            raise TypeError("Index must be an integer")
            return
        if key >= self.size or key <0:
            raise ValueError("Index out of bounds")
            return

        node = self.head
        for _ in range(key):
            node = node.next
        node.element = value

    def addnode(self, element, atomic_no, mass_no):
        """
        Function to add nodes to the DLL. Gets the element, atomic no, mass no as the inputs.
        Time Complexity: O(1)
        """
        element_obj = None
        if atomic_no > 0:
            try:
                element_obj = periodictable.elements[atomic_no]
            except KeyError:
                pass

        if element_obj:
            binding_energy = self.calculate_binding_energy(element_obj.symbol, atomic_no, mass_no)
            new_node = self.Node(element_obj.symbol, atomic_no, mass_no, binding_energy)
            if self.head is None:
                self.head = self.tail = new_node
            else:
                self.tail.next = new_node
                new_node.prev = self.tail
                self.tail = new_node
            self.size += 1
        else:
            print("Error: Element not found in periodic table")
    

    def __str__(self) -> str:
        """
        Method to provide the string representation of the ElementList class"""
        l = []
        node = self.head
        for _ in range(self.size):
            l.append(str([node.element, node.atomic_no, node.mass_no]))
            node = node.next
        return str(l)
    
    def calculate_binding_energy(self, atom, atomic_number, mass_number):
        """
        Function to calculate the binding energy based on the mass no and atomic no
        Time Complexity:O(no of isotopes)=can be approximated to O(1) since most elements have very few isotopes. + any overhead due to periodictable library
        """
        element = getattr(periodictable, atom)
        protons = atomic_number
        neutrons = mass_number - atomic_number
        mass = 0
        
        total_mass_atom = (protons * 1.007276) + (neutrons * 1.008665)
        for isotopes in element:
            if str(isotopes)[:3] == str(mass_number):
                mass = isotopes.mass
        mass_defect = total_mass_atom - mass
        be = mass_defect * (931.5)
        return be

class TreeNode:
    def __init__(self, element, atomic_number, mass_number, node_id):  # node structure of the tree
        self.value = Element(element, atomic_number, mass_number)
        self.node_id = node_id
        self.left = None           # alpha decay
        self.right = None          # beta plus
        self.middle = None         # beta minus

class Tree:
    def __init__(self):      # constructor of tree class
        self.root = None
        self.max_depth = 0
        self.e = ElementList()
        self.node_counter = 0
        self.optimal_path_nodes = []  # Store nodes in the optimal path
        self.optimal_path_edges = []  # Store edges in the optimal path

    def find_element(self, atomic_number, mass_number):   #finding element based on given atomic and mass number
    #time complexity O(n)    
        element = periodictable.elements[atomic_number]
        for i in element:                      # traversal to check through the isotopes
            if str(i)[:3] == str(mass_number):
                return i.symbol
        return None
    
    def alpha_decay(self, atomic_number, mass_number):   #function for alpha decay
        return atomic_number - 2, mass_number - 4
    
    def beta_minus(self, atomic_number, mass_number):   #function for beta minus decay
        return atomic_number + 1, mass_number
    
    def beta_plus(self, atomic_number, mass_number):    #function for beta plus decay
        return atomic_number - 1, mass_number
    
    def compare_calculate_mass_defect(self, atom1, atomic_number1, mass_number1, atom, atomic_number, mass_number):
         '''
         Function to compare the binding energy of 2 elements. Only if the binding energy of the product 
         element greater than the reactant element, the child is created
         
         Time Complexity: O(n)
         '''
        
         #calculations for child node
         element = getattr(periodictable, atom)    #getting the element from periodic table
         protons = atomic_number                   #number of protons
         neutrons = mass_number - atomic_number     #number of neutrons
         mass = 0
         
         total_mass_atom = (protons * 1.007276) + (neutrons * 1.008665)    #total mass of atoms 
         for isotopes in element:                                          #loop to extract mass of atom from periodic table
             if str(isotopes)[:3:] == str(mass_number):
                 mass = isotopes.mass
         mass_defect = total_mass_atom - mass                                 #mass defect of atom (theoretical mass of atom-actual mass of atom )
         #bepn denotes binding energy per nucleon
         #931.5 MeV is the energy for 1 amu
         bepn = mass_defect * (931.5) / mass_number                       #calculation for bindinf energy (e=mc**2)
         
         #calculations for parent node
         element = getattr(periodictable, atom1)    #getting the element from periodic table
         protons = atomic_number1                   #number of protons
         neutrons = mass_number1 - atomic_number1     #number of neutrons
         mass1 = 0
         total_mass_atom1 = (protons * 1.007276) + (neutrons * 1.008665)   #total mass of atoms 
         for isotopes in element:#loop to extract mass of atom from periodic table
             if str(isotopes)[:3:] == str(mass_number1):
                 mass1 = isotopes.mass
         mass_defect = total_mass_atom1 - mass1       #mass defect of atom (theoretical mass of atom-actual mass of atom )
         bepn1 = mass_defect * (931.5) / mass_number1  #calculation for bindinf energy (e=mc**2)
         
         
         if bepn1 < bepn:       # if the binding energy of product is higher, return 1
             return 1
         else:
             return 0
  
    def build_tree(self, element, atomic_number, mass_number, depth=0):   #function to build tree
        if atomic_number < 80 or mass_number <= 0 or atomic_number > 103:   # base condition to terminate
            return None
        
        self.node_counter += 1
        new_node = TreeNode(element, atomic_number, mass_number, self.node_counter)   #new node for given element
        
        depth += 1   #increment of depth
        self.max_depth = max(self.max_depth, depth)
        
        new_a_num, new_mass_num = self.alpha_decay(atomic_number, mass_number)    #new atom after alpha decay
        l = self.find_element(new_a_num, new_mass_num)   #finding atom symbol after decay
        if l is not None:  
            if self.compare_calculate_mass_defect(new_node.value[0], new_node.value[1], new_node.value[2], l, new_a_num, new_mass_num): #compare binding energy
                new_node.left = self.build_tree(l, new_a_num, new_mass_num, depth)   #if condition is satisfied, build left tree
        
        new_a_num, new_mass_num = self.beta_plus(atomic_number, mass_number) #new atom after beta plus decay
        l = self.find_element(new_a_num, new_mass_num) #finding atom symbol after decay
        if l is not None:
            if self.compare_calculate_mass_defect(new_node.value[0], new_node.value[1], new_node.value[2], l, new_a_num, new_mass_num):
                new_node.right = self.build_tree(l, new_a_num, new_mass_num, depth) #right child if condition satisfied
        
        new_a_num, new_mass_num = self.beta_minus(atomic_number, mass_number)  #new atom after beta minus decay
        l = self.find_element(new_a_num, new_mass_num)  #atom symbol
        if l is not None:
            if self.compare_calculate_mass_defect(new_node.value[0], new_node.value[1], new_node.value[2], l, new_a_num, new_mass_num):
                new_node.middle = self.build_tree(l, new_a_num, new_mass_num, depth)  #building the middle tree after beta minus decay
        
        return new_node
    
    def levelorder(self, root):
        '''
        Level order traversal through the tree to get nodes at each level
        The level order traversal is required to find the most optimal path to traverse through     
        Time complexity: O(n)
        '''
                
        l = []
        l.append(root)
        q = []

        while len(l) > 0:
            level_size = len(l)
            for i in range(level_size):
                node = l.pop(0)
                q.append(node.value)
                if node.left is not None:
                    l.append(node.left)
                if node.middle is not None:
                    l.append(node.middle)
                if node.right is not None:
                    l.append(node.right)
            q.append(None)
        return q
    
    def get_path(self, root):
        '''
        This function is concerned about the most optimal path that the parent element (root node) can take to reach one of 
        its leaf nodes.
        The data of the elements through which traversal will happen is stored in a linked list
        Time Complexicty: O(d) - depth of the tree, at any give point it will only travers one of the 3 child nodes. 
                                 So the worst case for this code is if the the node we need to reach is at the bottom
                                 hence O(d). Every other operation is O(1). due to the use of recursion it becomes O(d)
        '''
        if root:
            self.optimal_path_nodes.append(root)  # Add node to optimal path
            dif1 = dif2 = dif3 = 0
            if root.left is not None:
                dif1 = root.left.value.binding_energy.value - root.value.binding_energy.value 
            if root.middle is not None:
                dif2 = root.middle.value.binding_energy.value - root.value.binding_energy.value
            if root.right is not None:
                dif3 = root.right.value.binding_energy.value - root.value.binding_energy.value
            
            m = max(dif1, dif2, dif3)
            if m == dif1:
                self.optimal_path_edges.append((root, root.left, 'α'))
                root = root.left
            elif m == dif2:
                self.optimal_path_edges.append((root, root.middle, 'β-'))
                root = root.middle
            else:
                self.optimal_path_edges.append((root, root.right, 'β+'))
                root = root.right
            
            if root is not None:
                self.e.addnode(root.value.symbol.prop, root.value.atomic_number.value, root.value.mass_number.value)
                self.get_path(root)
        
    def get_max_recursion_depth(self):
        return self.max_depth

    def visualize_tree(self, root):
        dot = Digraph()

        def add_nodes_edges(node, parent_id=None, relation=None):
            if node is None:
                return
            node_id = f"{node.value.symbol.value}_{node.value.atomic_number.value}_{node.value.mass_number.value}_{node.node_id}"
            label = f"{node.value.symbol.value}\nZ={node.value.atomic_number.value}\nA={node.value.mass_number.value}\nBE={node.value.binding_energy.value:.2f} MeV"
            if node in self.optimal_path_nodes:
                dot.node(node_id, label, color='red', style='filled', fillcolor='yellow')
            else:
                dot.node(node_id, label)
            if parent_id is not None:
                if (parent_id, node, relation) in self.optimal_path_edges:
                    dot.edge(parent_id, node_id, label=relation, color='red', penwidth='2')
                else:
                    dot.edge(parent_id, node_id, label=relation)
            add_nodes_edges(node.left, node_id, 'α')
            add_nodes_edges(node.middle, node_id, 'β-')
            add_nodes_edges(node.right, node_id, 'β+')

        add_nodes_edges(root)
        return dot

    def generate_pdf(self, filepath="optimal_path.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        node = self.e.head
        while node is not None:
            line = f"Element: {node.element}, Atomic Number: {node.atomic_no}, Mass Number: {node.mass_no}, Binding Energy: {node.binding_energy:.2f} MeV"
            pdf.cell(200, 10, txt=line, ln=True, align='L')
            node = node.next
        
        pdf.output(filepath)

# Main
tree = Tree()

def check_element_exists(symbol, atomic_number, mass_number):
    '''
    Function to check if the element actually exists in periodic table
    If element symbolis correct, atomic number and mass number are also verified.
    Isotopes are also taken in consideration
    If all 3 user inputs are correct, the tree is built and operations are performed.
    Otherwise an error is raised
    
    Time Complexity: O(n)
    
    
    
    '''
    try:
        element = getattr(periodictable, symbol)
        if element.number == atomic_number:
            for i in element:
                if str(i)[:3] == str(mass_number):
                    return 1
            return 0
        else:
            return 0
    except AttributeError:
        return 0

symbol = input("Enter the symbol: ")
atomic_number = int(input("Enter the atomic number of the element: "))
mass_number = int(input("Enter the mass number of the element: "))

if check_element_exists(symbol, atomic_number, mass_number):
    tree.root = tree.build_tree(symbol, atomic_number, mass_number)

    l = (tree.levelorder(tree.root))    
    print("The tree looks like the following:")
    for i in l:
        if i is None:
            print()
        else:
            print(i, end=" ")
        
    print()
    print()

    tree.get_path(tree.root)
    print(tree.e)

    dot = tree.visualize_tree(tree.root)
    dot.render('nuclear_decay_tree', format='png', cleanup=True)  
    dot.view()  

    
    tree.generate_pdf()

else:
    print("Invalid input")
