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
- a bunch of euclidian distances
let the game begin!

RULES:
- Each person is symbolically represented by a node in the graph. 
- The goal is the simulate friendships forming between different people. 
- If two people have enough in common,they will form a friendship and their nodes will be linked on the graph. 
- If they're too different, they won't become friends.
"""

class Gender(Enum):
    MALE = 1
    FEMALE = 2

movies_category = ["action", "drama, arthouse", "sci-fi", "comedy"]
movies = {
    # action, drama, arthouse, sci-fi, comedy, 
    "Fast_and_furious": [1, 0, 0, 1, 0],
    "The_devil_wears_prada": [0, 1, 0, 0, 1],
    "The_Lord_Of_The_Rings": [1, 1, 0, 1, 1],
    "Star_Wars": [1, 1, 0, 1, 1],
    "2001_A_Space_Odyssey": [0, 0, 1, 1, 0],
    "Andrei_Rublev": [0, 0, 1, 0, 0],
    "A_bout_de_souffle": [0, 0, 1, 0, 0],
    "Rabbi_Jacob": [1, 0, 0, 0, 1]
}

hobbies_categories = ["Sport", "Artistic", "Nerd", "Manual"]
hobbies = {
    # Sport, Art, Nerd, Manual
    "Running": [1, 0, 0, 0],
    "Football": [1, 0, 0, 0],
    "Painting": [0, 1, 0, 1],
    "Singing": [0.5, 1, 0, 0],
    "Coding": [0, 0.5, 1, 0],
    "Math": [0, 0, 1, 0],
    "Cooking": [0, 0.5, 0, 1],
    "History": [0, 0, 1, 0],
    "Writing": [0, 1, 1, 0]
}

""" fake data """
people = [
  {"name": "Stephane", "Age": 56, "Hobbies": hobbies["History"], "Gender": Gender["MALE"], "Favourite_movie": movies["Star_Wars"]},
  {"name": "Jagger", "Age": 25, "Hobbies": hobbies["Football"], "Gender": Gender["MALE"], "Favourite_movie": movies["Andrei_Rublev"]},
  {"name": "Sophie", "Age": 55, "Hobbies": hobbies["Running"], "Gender": Gender["FEMALE"], "Favourite_movie": movies["The_devil_wears_prada"]},
  {"name": "Auriane", "Age": 26, "Hobbies": hobbies["Coding"], "Gender": Gender["FEMALE"], "Favourite_movie": movies["A_bout_de_souffle"]},
  {"name": "Manon", "Age": 26, "Hobbies": hobbies["Writing"], "Gender": Gender["FEMALE"], "Favourite_movie": movies["A_bout_de_souffle"]},
  {"name": "Cyan", "Age": 24, "Hobbies": hobbies["Math"], "Gender": Gender["MALE"], "Favourite_movie": movies["The_Lord_Of_The_Rings"]},
  {"name": "René", "Age": 88, "Hobbies": hobbies["Football"], "Gender": Gender["MALE"], "Favourite_movie": movies["Rabbi_Jacob"]}
]

""" Influence variables kit """
FRIEND_THRESHOLD = 0.85
CLOSURE_BOOST = 0.10 
FRIENDS_INFLUENCE = 0.10
WEIGHT_AGE = 0.4
WEIGHT_GENDER = 0.1
WEIGHT_HOBBIES = 0.2
WEIGHT_MOVIES = 0.3

"""
RULE N°1. HOMOPHILIA / SIMILARITY 
If two people share similar traits, they're more likely to form a connection. Which is equivalent to say, two nodes in the graph are more likely to be linked. 
"""

#calculate distance between vectors
def movie_similarity(movie1, movie2): # movie 1 and movie 2 are represented by vector. 
    similarity = 0
    distance = 0
    for i in range(len(movie1)):
        distance += (movie1[i] - movie2[i]) ** 2
    distance = sqrt(distance)
    similarity = 1 - (distance / sqrt(len(movie1)))
    return similarity

def hobbie_similarity(hobbie1, hobbie2):
    similarity = 0
    distance = 0
    for i in range(len(hobbie1)):
        distance += pow(hobbie1[i] - hobbie2[i], 2) # euclidian distance
    distance = sqrt(distance)
    similarity = 1 - (distance / sqrt(len(hobbie1)))
    return similarity

def is_similar(node1, node2):
    dist = sqrt(WEIGHT_AGE * pow(node1["Age"] - node2["Age"], 2) + WEIGHT_GENDER * pow(node1["Gender"].value - node2["Gender"].value, 2) ) / sqrt( WEIGHT_AGE + WEIGHT_GENDER + WEIGHT_HOBBIES)
    similarity_score = 1 - dist / 100
    movie_score = movie_similarity(node1["Favourite_movie"], node2["Favourite_movie"]) # we add the movie score to the total score
    hobbie_score = hobbie_similarity(node1["Hobbies"], node2["Hobbies"]) # we add the hobbie score to the total score 
    similarity_score += WEIGHT_MOVIES * movie_score / 10
    similarity_score += WEIGHT_HOBBIES * hobbie_score / 10
    return similarity_score



""" RULE N°2. TRIADIC CLOSURE / FERMETURE TRIADIQUE+ :
People with common friends are more likely to become friends than complete strangers with no common acquaintances. 
It's about the distance between two people. 
To take this reality into account, we recalculate probabilities for nodes with small distances to each other. To do so, we use the CLOSURE_BOOST variable. """
def triadic_closure(graph_nodes, people):
  for friend_a in graph_nodes:
    for friend_b in graph_nodes[friend_a]:
        for friend_c in graph_nodes[friend_b]:
            if friend_c != friend_a and friend_c not in graph_nodes[friend_a]: # a -- b -- c
              for person in people:
                  if person["name"] == friend_a:
                      p1 = person
                  if p["name"] == friend_c:
                      p2 = person
              P = is_similar(p1, p2) + CLOSURE_BOOST
              if P > FRIEND_THRESHOLD:
                graph_nodes[friend_a].append(friend_c)
                graph_nodes[friend_c].append(friend_a)
    return graph_nodes




""" RULE N°3: EXPONENTIAL POPULARITY
The more someone has friends, the more they'll make new ones. We could modelize this the following way: the more friends someone has, the highest the probability 
to meet that person. """
def popularity(graph_nodes, people):
    for i in range(len(people)):
        for j in range(i + 1, len(people)):
            p1, p2 = people[i], people[j]
            p1_num_friends = len(graph_nodes[people[i]["name"]])
            p2_num_friends = len(graph_nodes[people[j]["name"]])

            # If either is socially active, increase the connection probability
            if p1_num_friends > 5 or p2_num_friends > 5:
                P = is_similar(p1, p2) + FRIENDS_INFLUENCE
                if P > FRIEND_THRESHOLD:
                    if p2["name"] not in graph_nodes[p1["name"]]:
                        graph_nodes[p1["name"]].append(p2["name"])
                        graph_nodes[p2["name"]].append(p1["name"])
    return graph_nodes


""" now, let's build the friendship graph. we'll call each of our rules and try to see how they influence the friend-making process. """
def build_connection_graph(people):
    #intialize an empty graph 
    graph_nodes = {}
    for person in people: 
        graph_nodes[person['name']] = []
    i = 1

# apply the tree socializing rules  
    """ step 1: similarity """
    for i in range(len(people)):
        for j in range(i + 1, len(people)):
            p1, p2 = people[i], people[j]
            P = is_similar(p1, p2)
            if P > FRIEND_THRESHOLD:
                graph_nodes[p1["name"]].append(p2["name"])
                graph_nodes[p2["name"]].append(p1["name"])
    
    """ step 2: triadic closure """
    graph_nodes = triadic_closure(graph_nodes, people)

    """ step 3 : popularity. """
    graph_nodes = popularity(graph_nodes, people)
    
    return graph_nodes


""" (print result graph) """
print("People before connecting:\n")
for p in people: 
    print(f"Name: {p["name"]} Age: {p["Age"]} Hobbies:{p["Hobbies"]} Gender: {p["Gender"]} Favourite Movie: {p["Favourite_movie"]}")

connection_graph = build_connection_graph(people)
print(connection_graph)
