# Import required modules
import networkx as nx
import matplotlib.pyplot as plt
  
  
# Check if there is any node left with degree d
def check(h, d):
    f = 0  # there is no node of deg <= d
    for i in h.nodes():
        if (len(list(h.predecessors(i))) <= d):
            f = 1
            break
    return f
  
  
# Find list of nodes with particular degree
def find_nodes(h, it):
    set1 = []
    for i in h.nodes():
        if (len(list(h.predecessors(i))) <= it):
            set1.append(i)
    return set1

k_users = dict()
users = dict()
edges = []

with open('C:/Users/PC/Desktop/export.csv', encoding="UTF-8") as f:
    lines = f.read().splitlines()
    
    for i in range(1, len(lines)):
        tmp = lines[i].split(",")
        edges.append((tmp[1], tmp[0]))
  
# Create graph object and add nodes
g = nx.DiGraph()
g.add_edges_from(
    edges)

# Copy the graph
h = g.copy()
it = 1
  
d_avg = 0
count = 0
for i in h.nodes():
    users[i] = 0
    d_avg += len(list(h.predecessors(i)))
    count += 1
    
d_avg = d_avg/count

print(d_avg)
print(count)

# Bucket being filled currently
tmp = []

# list of lists of buckets
buckets = []
while (1):
    if it%5==0: print(it)
    
    flag = check(h, it)
    if (flag == 0):
        it += 1
        buckets.append(tmp)
        tmp = []
    if (flag == 1):
        node_set = find_nodes(h, it)
        for each in node_set:
            h.remove_node(each)
            tmp.append(each)
    if (h.number_of_nodes() == 0):
        buckets.append(tmp)
        break

#h.predecessors(node)

for i in range(len(buckets)):
    for j in buckets[i]: k_users[j] = i

k_avg = sum(k_users.values())/len(k_users)

print(d_avg)
print(count)

lamb = k_avg/d_avg

print("lamb: ",lamb)

for edge in edges:
    g[edge[0]][edge[1]]['weight'] = (k_users[edge[0]]+k_users[edge[1]])+lamb*(len(list(g.predecessors(edge[0])))+len(list(g.predecessors(edge[1]))))

for edge in edges:
    users[edge[1]] += g[edge[0]][edge[1]]['weight']

shells = dict(sorted(users.items(), key=lambda item: item[1], reverse=True))
print("LO3")
#print(shells)
print()
print(list(shells.keys())[:150])
