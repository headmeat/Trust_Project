import csv

sex = set()

c = 0
a = 'utf-8'
aa = 'windows-1252'

#key: userid
#values: tweet_no-0, focus-1, activity-2, pagerank-3, betweenness-4, closeness-5, degree-6, score-7

users = dict()

with open('C:/Users/PC/Desktop/csvs/pagerank.csv', 'r', encoding=a) as f:
    reader = csv.reader(f)
    c = 0
    
    for row in reader:
        if c==0: 
            c+=1
            continue
        
        users[int(row[0])] = [0, 0, 0, row[1], 0, 0, 0, 0]
        
print(len(users))

with open('C:/Users/PC/Desktop/csvs/apeshit.csv', 'r', encoding=a) as file:
    reader = csv.reader(file)
    c = 0
    
    for row in reader:
        if c==0: 
            c+=1
            continue
        c+=1
        row[0] = int(row[0])
        users[row[0]][1] = row[2]
        users[row[0]][2] = row[3]

with open('C:/Users/PC/Desktop/csvs/combined_csv.csv', 'r', encoding=a) as file:
    reader = csv.reader(file)
    c = 0
    
    for row in reader:
        if c==0:
            c+=1
            continue
        c+=1
        row[0] = int(row[0])
        users[row[0]][7] += int(row[4])
        users[row[0]][0] += 1

with open('C:/Users/PC/Desktop/csvs/betweenness.csv', 'r', encoding=a) as file:
    reader = csv.reader(file)
    c = 0
    
    for row in reader:
        if c==0:
            c+=1
            continue
        
        row[0] = int(row[0])
        users[row[0]][4] = row[1]
   
with open('C:/Users/PC/Desktop/csvs/closeness.csv', 'r', encoding=a) as file:
    reader = csv.reader(file)
    c = 0
    
    for row in reader:
        if c==0:
            c+=1
            continue
        
        row[0] = int(row[0])
        users[row[0]][5] = row[1]
     
with open('C:/Users/PC/Desktop/csvs/degree.csv', 'r', encoding=a) as file:
    reader = csv.reader(file)
    c = 0
    
    for row in reader:
        if c==0:
            c+=1
            continue
        
        row[0] = int(row[0])
        users[row[0]][6] = row[1]

avg = 0
#normalization
maxs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

#spread score calculation + find max
for user in users.keys():
    if users[user][0] != 0:
        users[user][7] = users[user][7]/users[user][0]
    for i in range(len(maxs)):
        maxs[i] = max(maxs[i], float(users[user][i]))
    
print(maxs)
    
#key: userid
#values: tweet_no-0, focus-1, activity-2, pagerank-3, betweenness-4, closeness-5, degree-6, score-7

with open('descarte.csv', 'w', newline='', encoding='UTF8') as f:
    # create the csv writer
    writer = csv.writer(f)

    writer.writerow(['userid', 'tweet_no', 'focus', 'activity', 'pagerank', 'betweenness', 'closeness', 'degree', 'score'])

    for user in list(users.keys()):
        lst = [user]
   
        # write a row to the csv file
        if users[user][0] > 0:
            lst.append(float(users[user][0])/maxs[0])
            lst.append(users[user][1])
            lst.append(users[user][2])
            for i in range(3, len(maxs)):
                lst.append(float(users[user][i])/maxs[i])
            lst.append(users[user][7])
            writer.writerow(lst)
