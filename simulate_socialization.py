from enum import Enum
from math import *

""" the goal here is the simulate how different people would create links between them. 
They are symbolically represented by nodes in a graph. 
Thanks to mathematical laws, we're going to arbitrary define some factors which will shape their socialization. 
"""

"""
1. SIMILARITY 
If two people share similar traits, they're more likely to form a connection. 
Which is equivalent to say, two nodes are more likely to be linked. 
"""


class Sport(Enum):
    FOOTBALL = 1
    DANCE = 2
    RUNNING = 3

class Gender(Enum):
    MALE = 1
    FEMALE = 2

""" The people array is a collection of objects with different attributes for each person.  """

people = [
  {"name": "Anna", "Age": 40, "Hobbies": Sport["FOOTBALL"], "Gender": Gender["FEMALE"]},
  {"name": "Alfred", "Age": 88, "Hobbies": Sport["RUNNING"], "Gender": Gender["MALE"]},
  {"name": "Sara", "Age": 22, "Hobbies": Sport["DANCE"], "Gender": Gender["FEMALE"]},
  {"name": "Tom", "Age": 56, "Hobbies": Sport["RUNNING"], "Gender": Gender["MALE"]},
  {"name": "Elise", "Age": 30, "Hobbies": Sport["FOOTBALL"], "Gender": Gender["FEMALE"]},
]

THRESHOLD = 0.69

def is_similar(node1, node2):
    weight_age = 5
    weight_gender = 3
    weight_hobbies = 1

    dist = sqrt(weight_age * pow(node1["Age"] - node2["Age"], 2) + weight_gender * pow(node1["Gender"].value - node2["Gender"].value, 2) + weight_hobbies * pow(node1["Hobbies"].value - node2["Hobbies"].value)) / sqrt( weight_age * 6 + weight_gender + weight_hobbies)
    P = 1 - dist / 100
    return P

""" if the similarity score is superior to a particular defined threshold, then a connection will be formed"""

def build_connection_graph(people):
    graph_nodes = {person["name"]: [] for person in people}
    i = 1

    for i in range(len(people)):
        for j in range(i + 1, len(people)):
            p1, p2 = people[i], people[j]
            P = is_similar(p1, p2)
            if P > THRESHOLD:
                graph_nodes[p1["name"]].append(p2["name"])
                graph_nodes[p2["name"]].append(p1["name"])
    return graph_nodes

connection_graph = build_connection_graph(people)
print(connection_graph)
