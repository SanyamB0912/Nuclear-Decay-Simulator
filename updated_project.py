import periodictable
import sys
import time
import graphviz

# Increase recursion limit
sys.setrecursionlimit(10000)

# Define maximum recursion depth
MAX_RECURSION_DEPTH = 1000

# Basic node structure of a graph
class GraphNode:
    def __init__(self, element, atomic_number, mass_number):
        self.value = [element, atomic_number, mass_number]
        self.decay_products = []

# Declaration of a graph class
class NuclearGraph:
    def __init__(self):
        self.root = None
        self.max_depth = 0  # Initialize maximum recursion depth
        self.byproducts = set()

    def find_element(self, atomic_number, mass_number):
        element = periodictable.elements[atomic_number]
        for i in element:
            if str(i)[:3] == str(mass_number):
                return i
        return None

    def alpha_decay(self, atomic_number, mass_number):
        return atomic_number - 2, mass_number - 4

    def beta_minus_decay(self, atomic_number, mass_number):
        return atomic_number + 1, mass_number

    def beta_plus_decay(self, atomic_number, mass_number):
        return atomic_number - 1, mass_number

    def build_decay_tree(self, element, atomic_number, mass_number, depth=0):
        new_node = GraphNode(element, atomic_number, mass_number)
        depth += 1

        # Update maximum recursion depth
        self.max_depth = max(self.max_depth, depth)

        # Perform alpha decay
        alpha_atomic_number, alpha_mass_number = self.alpha_decay(atomic_number, mass_number)
        alpha_element = self.find_element(alpha_atomic_number, alpha_mass_number)
        if alpha_element:
            alpha_node = self.build_node("Alpha Decay", alpha_element, alpha_atomic_number, alpha_mass_number, depth)
            if alpha_node:
                if alpha_element not in self.byproducts:
                    new_node.decay_products.append(alpha_node)
                    self.byproducts.add(alpha_element)
                    self.build_decay_tree(alpha_element, alpha_atomic_number, alpha_mass_number, depth)

        # Perform beta-minus decay
        beta_minus_atomic_number, beta_minus_mass_number = self.beta_minus_decay(atomic_number, mass_number)
        beta_minus_element = self.find_element(beta_minus_atomic_number, beta_minus_mass_number)
        if beta_minus_element:
            beta_minus_node = self.build_node("Beta-Minus Decay", beta_minus_element, beta_minus_atomic_number,
                                              beta_minus_mass_number, depth)
            if beta_minus_node:
                if beta_minus_element not in self.byproducts:
                    new_node.decay_products.append(beta_minus_node)
                    self.byproducts.add(beta_minus_element)
                    self.build_decay_tree(beta_minus_element, beta_minus_atomic_number, beta_minus_mass_number, depth)

        # Perform beta-plus decay
        beta_plus_atomic_number, beta_plus_mass_number = self.beta_plus_decay(atomic_number, mass_number)
        beta_plus_element = self.find_element(beta_plus_atomic_number, beta_plus_mass_number)
        if beta_plus_element:
            beta_plus_node = self.build_node("Beta-Plus Decay", beta_plus_element, beta_plus_atomic_number,
                                             beta_plus_mass_number, depth)
            if beta_plus_node:
                if beta_plus_element not in self.byproducts:
                    new_node.decay_products.append(beta_plus_node)
                    self.byproducts.add(beta_plus_element)
                    self.build_decay_tree(beta_plus_element, beta_plus_atomic_number, beta_plus_mass_number, depth)

        return new_node

    def build_node(self, decay_type, element, atomic_number, mass_number, depth):
        return GraphNode(decay_type + " " + element.symbol, atomic_number, mass_number)

    def get_max_recursion_depth(self):
        return self.max_depth

    def create_dot_graph(self, root):
        dot = graphviz.Digraph()
        
        def add_edges_to_graph(node):
            if node is None:
                return
            dot.node(str(node.value), label=str(node.value))
            for product in node.decay_products:
                dot.edge(str(node.value), str(product.value))
                add_edges_to_graph(product)

        add_edges_to_graph(root)
        return dot


# Main
graph = NuclearGraph()

# Start the timer
start_time = time.time()

# Build the decay tree representing the decay process
root = graph.build_decay_tree('U', 92, 238)  # Uranium-238 decay

# End the timer
end_time = time.time()

# Calculate the time taken
time_taken = (end_time - start_time) * 1000  # Convert to milliseconds

# Get the maximum recursion depth
max_depth = graph.get_max_recursion_depth()

# Display the maximum recursion depth and time taken
print("Maximum Recursion Depth:", max_depth)
print("Time taken to build the graph:", time_taken, "milliseconds")

# Create Graphviz graph
dot = graph.create_dot_graph(root)

# Save the graph as a PDF file
dot.render("decay_process_graph", format="pdf", cleanup=True)

print("Graph visualization saved as 'decay_process_graph.pdf'")
