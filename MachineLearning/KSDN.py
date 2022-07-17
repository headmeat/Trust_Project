# Import required modules
import networkx as nx, os
import matplotlib.pyplot as plt

def indegree2019(h, node):
    neigh = list(h.predecessors(node))
    c = 0
    
    for n in neigh:
        if(years[n]<=2019): c+=1
        
    return c

def indegree2020(h, node):
    neigh = list(h.predecessors(node))
    c = 0
    
    for n in neigh:
        if(years[n]>=2020): c+=1
        
    return c

# Check if there is any node left with degree d
def check2020(h, d):
	f = 0 # there is no node of deg <= d
	for i in h.nodes():
		if (indegree2020(h, i) <= d):
			f = 1
			break
	return f

# Find list of nodes with particular degree
def find_nodes2020(h, it):
	set1 = []
	for i in h.nodes():
		if (indegree2020(h, i) <= it):
			set1.append(i)
	return set1

def check2019(h, d):
	f = 0 # there is no node of deg <= d
	for i in h.nodes():
		if (indegree2019(h, i) <= d):
			f = 1
			break
	return f

# Find list of nodes with particular degree
def find_nodes2019(h, it):
	set1 = []
	for i in h.nodes():
		if (indegree2019(h, i) <= it):
			set1.append(i)
	return set1

lines = []
edges = []
years = dict()

with open('C:/Users/PC/Desktop/years_with_ids4.txt', encoding="UTF-8") as f:
    line = f.read().splitlines()
    
    for i in range(len(line)):
        tmp = line[i].split(" ")
        years[tmp[0]] = int(tmp[1])

with open('C:/Users/PC/Desktop/export.csv', encoding="UTF-8") as f:
    lines = f.read().splitlines()
    
    for i in range(1, len(lines)):
        tmp = lines[i].split(",")
        edges.append((tmp[1], tmp[0]))

k_years = dict()

for i in range(2006, 2022):
    k_years[i] = []
    
for user in years.keys():
    if years[user]>=2006: k_years[years[user]].append(user)

# Create graph object and add nodes
g = nx.DiGraph()
g.add_edges_from(edges)
pickle = dict()
mx = 0

for i in list(g.nodes()):
    pickle[i] = indegree2020(g, i)
    mx = max(mx, pickle[i])

for key in list(pickle.keys()):
    pickle[key] /= mx

print(pickle['1369385775566098432'])
print(mx)

# Copy the graph
h = g.copy()
h2 = g.copy()

it = 1
"""
# Bucket being filled currently
tmp = []
# list of lists of buckets
buckets = []

while (1):
    #if it%30 == 0: print("K-SHELL:",it)
    
    flag = check2020(h, it)
    
    if (flag == 0):
        it += 1
        buckets.append(tmp)
        tmp = []
    if (flag == 1):
        node_set = find_nodes2020(h, it)
        for each in node_set:
            h.remove_node(each)
            tmp.append(each)
    if (h.number_of_nodes() == 0):
        buckets.append(tmp)
        break

shells = dict()
avg = 0
total = 0
for i in range(len(buckets)):
    if len(buckets[i])==0: continue

    avg += i*len(buckets)
    total += len(buckets)
    shells[i] = buckets[i]
print("LO1")
#print(shells) 
print("AVG:",avg/total)
print("MAX:",max(list(shells.keys())))
"""
tmp2 = []
buckets2 = []

it = 1

while (1):
    if it % 5 == 0:
        print("K-SHELL:",it)
        print(h2.number_of_nodes())
        print(h2.number_of_edges())
        
    flag = check2019(h2, it)
    if (flag == 0):
        it += 1
        buckets2.append(tmp2)
        tmp2 = []
    if (flag == 1):
        node_set = find_nodes2019(h2, it)
        for each in node_set:
            h2.remove_node(each)
            tmp2.append(each)
    if (h2.number_of_nodes() == 0):
        buckets2.append(tmp2)
        break

shells = dict()
avg = 0
total = 0

k_users = dict()

for i in range(len(buckets2)):
    if len(buckets2[i])==0: continue

    for user in buckets2[i]:
        k_users[user] = i

    avg += i*len(buckets2)
    total += len(buckets2)
    shells[i] = buckets2[i]

print(k_users)

print("LO2")
#print(shells) 
print("AVG:",avg/total)
m = max(list(shells.keys()))
print("MAX:",m)

for i in range(len(buckets2)):
    if len(buckets2[i])==0: continue
    for user in buckets2[i]:
        k_users[user] = k_users[user]/m

shells = dict()

"""
for i in range(len(buckets)):
    if len(buckets[i])==0: continue
        
    for user in buckets[i]:
        shells[user] = indegree2020(g, user)
        #if user == '44196397': print(shells[user])
"""

alpha = 0.2

for i in range(len(buckets2)):
    if len(buckets2[i])==0: continue
        
    for user in buckets2[i]:
        shells[user] = alpha*k_users[user] + (1-alpha)*pickle[user]
        #if user == '44196397': print(shells[user])
        
shells = dict(sorted(shells.items(), key=lambda item: item[1], reverse=True))
print("LO3")
print(shells)
print()
print(list(shells.keys())[:25])
