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
""" influence of the triadic closure """
CLOSURE_BOOST = 0.15 
FRIENDS_INFLUENCE = 0.20

""" FIRST RULE: the more someone is like us (same gender, same age, etc), the likier we are to become friends with that person"""
def is_similar(node1, node2):
    weight_age = 5
    weight_gender = 3
    weight_hobbies = 1

    dist = sqrt(weight_age * pow(node1["Age"] - node2["Age"], 2) + weight_gender * pow(node1["Gender"].value - node2["Gender"].value, 2) + weight_hobbies * pow(node1["Hobbies"].value - node2["Hobbies"].value)) / sqrt( weight_age * 6 + weight_gender + weight_hobbies)
    """ if the similarity score is superior to a particular defined threshold, then a connection will be formed"""
    similarity_score = 1 - dist / 100
    return similarity_score



""" SECOND RULE :
using triadic to closure. People with common friends are more likely to become friends than complete strangers with no common
acquaintances. To take this reality into account, we recalculate probabilities for nodes with small distances to each other. To do so, 
we use the CLOSURE_BOOST variable. 
 """
def triadic_closure(graph_nodes, people):
  for a in graph_nodes:
    for b in graph_nodes[a]:
        for c in graph_nodes[b]:
            if c != a and c not in graph_nodes[a]:
              p1 = next(p for p in people if p["name"] == a)
              p2 = next(p for p in people if p["name"] == c)
              P = is_similar(p1, p2) + CLOSURE_BOOST
              if P > THRESHOLD:
                graph_nodes[a].append(c)
                graph_nodes[c].append(a)
    return graph_nodes




""" THIRD RULE:
    The more someone has friends, the more they'll make new ones. 
    We could modelize this the following way: the more friends someone has, the highest the probability to meet that person.
"""
def popularity(graph_nodes, people):
    for i in range(len(people)):
        for j in range(i + 1, len(people)):
            p1, p2 = people[i], people[j]
            p1_friends = len(graph_nodes[people[i]["name"]])
            p2_friends = len(graph_nodes[people[j]["name"]])

            # If either is socially active, increase the connection probability
            if p1_friends > 5 or p2_friends > 5:
                P = is_similar(p1, p2) + FRIENDS_INFLUENCE
                if P > THRESHOLD:
                    if p2["name"] not in graph_nodes[p1["name"]]:
                        graph_nodes[p1["name"]].append(p2["name"])
                        graph_nodes[p2["name"]].append(p1["name"])
    return graph_nodes


def build_connection_graph(people):
    graph_nodes = {person["name"]: [] for person in people}
    i = 1

    """ step 1: mere similarity """
    for i in range(len(people)):
        for j in range(i + 1, len(people)):
            p1, p2 = people[i], people[j]
            P = is_similar(p1, p2)
            if P > THRESHOLD:
                graph_nodes[p1["name"]].append(p2["name"])
                graph_nodes[p2["name"]].append(p1["name"])
    
    """ step 2: triadic closure """
    triadic_closure(graph_nodes, people)

    """ step 3 : popularity. number of friends """
    graph_nodes = popularity(graph_nodes, people)
    
    return graph_nodes

connection_graph = build_connection_graph(people)
print(connection_graph)
