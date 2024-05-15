import periodictable

class Element:
    class Node():
        def __init__(self, prop, value):
            self.prop = prop
            self.value = value
            self.next = None
    
    def __init__(self, element, atomic_no, mass_no):
        self.head = self.Node("Symbol", element )
        self.head.next = self.Node("Atomic Number", atomic_no)
        self.head.next.next = self.Node("Mass Number", mass_no)
        self.head.next.next.next= self.tail = self.Node("Binding Energy", self.calculate_binding_energy(element, atomic_no, mass_no))

        self.size = 4

    def __getitem__(self, key):
        if not str(key).isnumeric():
            print("Error: Not a number")
            return
        
        # Check for out-of-bounds access
        if key >= self.size:
            print("Error: Index out of bounds")
            return

        node = self.head
        for _ in range(key):
            node = node.next
        return node.value
        
    def __setitem__(self, key, value):
        if not str(key).isnumeric():
            print("Error: Not a number")
            return
        
        # Similar check for out-of-bounds access
        if key >= self.size:
            print("Error: Index out of bounds")
            return

        node = self.head
        for _ in range(key):
            node = node.next
        node.value = value

    def __str__(self) -> str:
        return str([self.head.value, self.head.next.value, self.head.next.next.value])
    
    def calculate_binding_energy(self,atom, atomic_number, mass_number):
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
        return bepn
    
#doubly linked implementation for storing details of each element in each node (final fission path)
class ElementList:
    class Node():
        def __init__(self, element, atomic_no=0, mass_no=0, binding_energy=0):
            self.element = element
            self.atmoic_no = atomic_no
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
        #check if index is a number
        if not str(key).isnumeric():
            raise TypeError("Index must be an  integer")
            return

        # Check for out-of-bounds access
        if key >= self.size or key<(-self.size):
            raise ValueError("Index out of bounds")
            return

        node = self.head
        for _ in range(key):
            node = node.next
        return node
        
    def __setitem__(self, key, value):
        if not str(key).isnumeric():
            print("Error: Not a number")
            return

        # Check for out-of-bounds access
        if key >= self.size:
            print("Error: Index out of bounds")
            return

        node = self.head
        for _ in range(key):
            node = node.next
        node.element = value

    def addnode(self, element, atomic_no, mass_no):
        # Try to find element using both atomic and mass number
        element = None
        if atomic_no > 0:
            try:
                element = periodictable.elements[atomic_no]  # Access element by atomic number
            except KeyError:
                pass
    
        if element:
            # Element found, get binding energy using the library
            binding_energy = self.calculate_binding_energy(element.symbol, atomic_no, mass_no)  # Assuming binding energy in eV
            if self.head == None:
                self.head = self.tail = self.Node(element.symbol, atomic_no, mass_no, binding_energy)
            else:
                self.tail.next = self.Node(element.symbol, atomic_no, mass_no, binding_energy)
                self.tail = self.tail.next
            self.size += 1
        else:
            print("Error: Element not found in periodic table")
    
    
    def delnode(self, element):
        if self.head == None:
            print("Error: List is empty")
        else:
            node = self.head
            for _ in range(self.size):
                if node.element == element:
                    if self.head.element == element:
                        self.head = self.head.next
                        self.head.next.prev = None
                    elif self.tail.element == element:
                        self.tail = self.tail.prev
                        self.tail.next = None
                    else:
                        node.prev.next = node.next
                        node.next.prev = node.prev
    
    def calculate_binding_energy(atom, atomic_number, mass_number):
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
        
        #931.5 MeV is the energy for 1 amu
        be = mass_defect * (931.5) 
        return be