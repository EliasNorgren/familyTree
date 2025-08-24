from graphviz import Digraph
import json

class Person:
    def __init__(self, ahnentafel, name, info=""):
        self.ahnentafel = ahnentafel  # ahnentafel number
        self.name = name              # person’s name
        self.info = info              # extra text (birthdate, notes, etc.)
        self.father_ahnentafel = -1
        self.mother_ahnentafel = -1
        self.father : Person = None   # left child (2*n)
        self.mother : Person = None   # right child (2*n+1)

    def __repr__(self):
        return f"{self.ahnentafel}: {self.name} ({self.info}) - Father: {self.father_ahnentafel}, Mother: {self.mother_ahnentafel}\n"

def draw_tree(node):
    dot = Digraph()
    dot.attr(rankdir="BT")
    def add_node(n):
        if n is None:
            return
        dot.node(str(n.ahnentafel), f"[{n.ahnentafel}] {n.name}\n{n.info}")
        if n.father:
            dot.edge(str(n.ahnentafel), str(n.father.ahnentafel), color="blue")
            add_node(n.father)
        if n.mother:
            dot.edge(str(n.ahnentafel), str(n.mother.ahnentafel), color="pink")
            add_node(n.mother)
    
    add_node(node)
    return dot

def create_person_tree(data):
    people = {int(entry["number"]): Person(int(entry["number"]), entry["name"], entry["suffix"]) for entry in data}
    for number, person in people.items():
        father_number = number * 2
        mother_number = number * 2 + 1
        person.father_ahnentafel = father_number
        person.mother_ahnentafel = mother_number
        person.father = people.get(father_number)
        person.mother = people.get(mother_number)
    return people.get(1)  # Return the root person (ahnentafel number 1)
# Example usage:# 
# root = Person(1, "Root Person", "b. 1900")
# root.father = Person(2, "Father", "b. 1870")
# root.mother = Person(3, "Mother", "b. 1875")
# root.father.father = Person(4, "Paternal Grandfather", "b. 1840")
# root.father.mother = Person(5, "Paternal Grandmother", "b. 1845")
# root.mother.father = Person(6, "Maternal asd Grandfather", "b. 1850")

input_file = "merged_output/merged.json"

with open(f"{input_file}", "r", encoding="utf-8") as f:
    data = json.load(f)

root = create_person_tree(data)

def has_duplicate_ancestors(root):
    visited = set()
    def traverse(person):
        if person is None:
            return False
        if person.ahnentafel in visited:
            return True  # Found duplicate ancestor
        visited.add(person.ahnentafel)
        return traverse(person.father) or traverse(person.mother)
    return traverse(root)

# Usage:
if has_duplicate_ancestors(root):
    print("Warning: Duplicate ancestors detected (possible incestuous relation or pedigree collapse).")
else:
    print("No duplicate ancestors detected.")

# tree = draw_tree(root)
# tree.render(f'renders/{input_file}', format='png', cleanup=True)
# tree.render(f'renders/{input_file}', format='pdf', cleanup=True)
# tree.render(f'renders/{input_file}', format='svg', cleanup=True)
# tree.render(f'renders/{input_file}', format='gv', cleanup=True)

