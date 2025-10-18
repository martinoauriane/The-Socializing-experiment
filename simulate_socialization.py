from enum import Enum
from math import *


"""
What you need for this experiment: 
- a graph
- nodes 
- links between those nodes
- probably a computer
- a terminal 
- python3 with a venv environment
- a set of willing people
- a set of friendless still-willing people
- some corriander 
- and.. a bunch of euclidian distances! 
let the game BEGIN!

RULES:
- Each person is symbolically represented by a node in the graph. 
- The goal here is the simulate how different people would socialize. By socialize we mean making a friend (yay!). 
If certain criterias are met, two people form a friendship and their nodes are now linked on the graph. 
On the contrary, if they don't meet the pre-defined friendship requirements, they won't pass the test and won't become friends (sad!).

REMINDER : Each person is symbolically represented by a node in the graph. 
"""

class Sport(Enum):
    FOOTBALL = 1
    DANCE = 2
    RUNNING = 3

class Gender(Enum):
    MALE = 1
    FEMALE = 2

""" using vectors to modelize movie tastes """
movies_features = {
    "FASTANDFURIOUS": {"action":1, "drama":0, "arthouse":0, "sci-fi":0},
    "THE_DEVIL_WEARS_PRADA": {"action":0, "drama":1, "arthouse":0, "sci-fi":0},
    "THE_LORDS_OF_THE_RINGS": {"action":1, "drama":1, "arthouse":0, "sci-fi":1},
    "STAR_WARS": {"action":1, "drama":1, "arthouse":0, "sci-fi":1},
    "2001": {"action":0, "drama":0, "arthouse":1, "sci-fi":1},
    "ANDREI_RUBLEV": {"action":0, "drama":1, "arthouse":1, "sci-fi":0},
    "A_BOUT_DE_SOUFFLE": {"action":0, "drama":1, "arthouse":1, "sci-fi":0},
}

""" fake data """
people = [
  {"name": "Anna", "Age": 40, "Hobbies": Sport["FOOTBALL"], "Gender": Gender["FEMALE"]},
  {"name": "Alfred", "Age": 88, "Hobbies": Sport["RUNNING"], "Gender": Gender["MALE"]},
  {"name": "Sara", "Age": 22, "Hobbies": Sport["DANCE"], "Gender": Gender["FEMALE"]},
  {"name": "Tom", "Age": 56, "Hobbies": Sport["RUNNING"], "Gender": Gender["MALE"]},
  {"name": "Elise", "Age": 30, "Hobbies": Sport["FOOTBALL"], "Gender": Gender["FEMALE"]},
]

""" Influence variables kit """
THRESHOLD = 0.69
CLOSURE_BOOST = 0.15 
FRIENDS_INFLUENCE = 0.20



""" UNIVERSAL LAWS OF MATING ON THIS EARTH.  """

"""
RULE N°1. SIMILARITY 
If two people share similar traits, they're more likely to form a connection. Which is equivalent to say, two nodes are more likely to be linked. 
"""


""" first to get the right movie score we define euclidian distance between two vectors. each vector represents a movie. """
max_dist = sqrt(len(next(iter(movies_features.values()))))  
""" if two movies share exactly the same caracteristics (vector1 == vector2), then the distance between them = 0. 
On the other hand, if the two films are totally opposed, then dist = max_dist """
def movie_similarity(f1, f2):
    vector1 = movies_features[f1.name]
    vector2 = movies_features[f2.name]
    distance = sqrt(sum((vector1[k] - vector2[k])**2 for k in vector1))
    similarity =  1 - distance / max_dist 
    """ similarity = 1 : the two movies are alike. 
     similarity = 0 : the two movies are different. """
    return similarity


def is_similar(node1, node2):
    weight_age = 5
    weight_gender = 3
    weight_hobbies = 1
    weight_movie = 2  

    dist = sqrt(weight_age * pow(node1["Age"] - node2["Age"], 2) + weight_gender * pow(node1["Gender"].value - node2["Gender"].value, 2) + weight_hobbies * pow(node1["Hobbies"].value - node2["Hobbies"].value)) / sqrt( weight_age * 6 + weight_gender + weight_hobbies)
    """ if the similarity score is superior to a particular defined threshold, then a connection will be formed"""

    similarity_score = 1 - dist / 100

    """ we add the movie score to the total score """
    movie_score = 0
    if "FavoriteMovie" in node1 and "FavoriteMovie" in node2:
        movie_score = movie_similarity(node1["FavoriteMovie"], node2["FavoriteMovie"])

    similarity_score = similarity_score + weight_movie * movie_score / 10
    return similarity_score



""" RULE N°2. TRIADIC CLOSURE :
People with common friends are more likely to become friends than complete strangers with no common acquaintances. To take this reality into account, 
we recalculate probabilities for nodes with small distances to each other. To do so, we use the CLOSURE_BOOST variable. """
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




""" RULE N°3: EXPONENTIAL POPULARITY
The more someone has friends, the more they'll make new ones. We could modelize this the following way: the more friends someone has, the highest the probability 
to meet that person. """
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





""" NOW, LET'S BUILD OUR GRAPH OF FRIENDSHIPS!
we'll call each of our rules and try to see how they influence the friend-making process. """
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

    """ step 3 : popularity. """
    graph_nodes = popularity(graph_nodes, people)
    
    return graph_nodes



""" and voilà! (print result graph) """
connection_graph = build_connection_graph(people)
print(connection_graph)
