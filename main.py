import periodictable
import sys
import time

# Increase recursion limit
sys.setrecursionlimit(10000)
   
# Basic node structure of a tree    
class TreeNode:
    def __init__(self, element, atomic_number, mass_number):
        self.value = [element, atomic_number, mass_number]
        self.left = None           # alpha decay
        self.right = None          # beta plus
        self.middle = None
        
# Declaration of a tree class       
class Tree:
    def __init__(self):
        self.root = None
        self.max_depth = 0  # Initialize maximum recursion depth
    
    def find_element(self, atomic_number, mass_number):
        element = periodictable.elements[atomic_number]
        for i in element:
            if str(i)[:3] == str(mass_number):
                return i.symbol
        return None
    
    def alpha_decay(self, atomic_number, mass_number):
        return atomic_number - 2, mass_number - 4
    
    def beta_minus(self, atomic_number, mass_number):
        return atomic_number + 1, mass_number
    
    def beta_plus(self, atomic_number, mass_number):
        return atomic_number - 1, mass_number
    
    def compare_calculate_mass_defect(self, atom1, atomic_number1, mass_number1, atom, atomic_number, mass_number):
         #calculations for child node
         element = getattr(periodictable, atom)
         protons = atomic_number
         neutrons = mass_number - atomic_number
         mass = 0
         
         total_mass_atom = (protons * 1.007276) + (neutrons * 1.008665)
         for isotopes in element:
             if str(isotopes)[:3:] == str(mass_number):
                 mass = isotopes.mass
         mass_defect = total_mass_atom - mass
         #bepn denotes binding energy per nucleon
         #931.5 MeV is the energy for 1 amu
         bepn = mass_defect * (931.5) / mass_number
         
         
         #calculations for parent node
         element = getattr(periodictable, atom1)
         protons = atomic_number1
         neutrons = mass_number1 - atomic_number1
         mass1 = 0
         total_mass_atom1 = (protons * 1.007276) + (neutrons * 1.008665)
         for isotopes in element:
             if str(isotopes)[:3:] == str(mass_number1):
                 mass1 = isotopes.mass
         mass_defect = total_mass_atom1 - mass1
         bepn1 = mass_defect * (931.5) / mass_number1
         
         
         if bepn1 < bepn:
             return 1
         else:
             return 0

        
    def build_tree(self, element, atomic_number, mass_number, depth=0):
        if atomic_number < 70 or mass_number <= 0 or atomic_number > 103:
            return None
        
        new_node = TreeNode(element, atomic_number, mass_number)
        print(new_node.value)
        depth += 1
        
        # Update maximum recursion depth
        self.max_depth = max(self.max_depth, depth)
        
        # Building left tree for alpha decay
        new_a_num, new_mass_num = self.alpha_decay(atomic_number, mass_number)
        
        l = self.find_element(new_a_num, new_mass_num)
        if l is not None:
            if self.compare_calculate_mass_defect(new_node.value[0], new_node.value[1], new_node.value[2], l, new_a_num, new_mass_num):
                new_node.left = self.build_tree(l, new_a_num, new_mass_num, depth)
          
        # Building right tree for beta plus decay
        new_a_num, new_mass_num = self.beta_plus(atomic_number, mass_number)
        l = self.find_element(new_a_num, new_mass_num)
        if l is not None:
            if self.compare_calculate_mass_defect(new_node.value[0], new_node.value[1], new_node.value[2], l, new_a_num, new_mass_num):
                new_node.right = self.build_tree(l, new_a_num, new_mass_num, depth)
                
        # Building middle tree for beta minus decay
        new_a_num, new_mass_num = self.beta_minus(atomic_number, mass_number)
        l = self.find_element(new_a_num, new_mass_num)
        if l is not None:
            if self.compare_calculate_mass_defect(new_node.value[0], new_node.value[1], new_node.value[2], l, new_a_num, new_mass_num):
                new_node.middle = self.build_tree(l, new_a_num, new_mass_num, depth)
        
        return new_node
    
    def print_tree(self, root, level=0, prefix="Root:"):
        if root is None:
            return
        print(" " * (level * 4) + prefix + f" {root.value}")
        if root.left is not None:
            self.print_tree(root.left, level + 1, "Left:")
        if root.right is not None:
            self.print_tree(root.right, level + 1, "Right:")
        if root.middle is not None:
            self.print_tree(root.middle, level + 1, "Middle:")
    
    def get_max_recursion_depth(self):
        return self.max_depth


# Main
tree = Tree()

# Start the timer
start_time = time.time()

# Build the tree
root = tree.build_tree('U', 92, 235)

# End the timer
end_time = time.time()

# Calculate the time taken
time_taken = (end_time - start_time) * 1000  # Convert to milliseconds

# Get the maximum recursion depth
max_depth = tree.get_max_recursion_depth()

# Display the maximum recursion depth and time taken
print("Maximum Recursion Depth:", max_depth)
print("Time taken to run the code:", time_taken, "milliseconds")
