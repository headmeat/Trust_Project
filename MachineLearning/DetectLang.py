import csv, time
from googletrans import Translator
start = time.time()
count = api_count = miss = 0

translator = Translator()
translator.raise_Exception = True
username = ""
flag = is_eng = False #영어면 True, pt면 False
cursor = 13

with open('C:/Users/headm/OneDrive/Desktop/csv/twitter3.csv', 'r', encoding="utf-8") as in_file, open('C:/Users/headm/OneDrive/Desktop/csv/twitter3.csv', 'r', encoding="utf-8") as in_file2, open('C:/Users/headm/OneDrive/Desktop/python/twitter_en.csv','w', encoding="utf-8", newline='') as out_file, open('C:/Users/headm/OneDrive/Desktop/python/twitter_pt.csv','w', encoding="utf-8", newline='') as out_file2, open('C:/Users/headm/OneDrive/Desktop/csv/twitter3.csv', 'r', encoding="utf-8") as in_file3, open('C:/Users/headm/OneDrive/Desktop/csv/twitter3.csv', 'r', encoding="utf-8") as in_file4, open('C:/Users/headm/OneDrive/Desktop/csv/twitter_pt2.csv','w', encoding="utf-8", newline='') as out_file3, open('C:/Users/headm/OneDrive/Desktop/csv/twitter3.csv', 'r', encoding="utf-8") as in_file5:
    csv_reader = csv.reader(in_file, delimiter=',')
    csv_reader2 = csv.reader(in_file2, delimiter=',')
    csv_reader3 = csv.reader(in_file3, delimiter=',')
    csv_reader4 = csv.reader(in_file4, delimiter=',')
    csv_reader5 = csv.reader(in_file5, delimiter=',')
    csv_writer = csv.writer(out_file, delimiter=',')
    csv_writer2 = csv.writer(out_file2, delimiter=',')
    
    if not flag:
        next(csv_reader2)
        for i in range(5): next(csv_reader3)
        for i in range(10): next(csv_reader4)
        flag = True
    
    for row in csv_reader:
        if count==0:
            csv_writer.writerow(row)
            csv_writer2.writerow(row)
            count+=1
            continue
        
        try:        
            str1 = row[4].replace('님에게 보내는 답글', '')
            str2 = next(csv_reader2)[4].replace('님에게 보내는 답글', '')
            str3 = next(csv_reader3)[4].replace('님에게 보내는 답글', '')
            str4 = next(csv_reader4)[4].replace('님에게 보내는 답글', '')
        except Exception: break
        count+=1
            
        if count%10000==0:
            print("Processing line: ", count,"\n", time.time()-start, "seconds")
        try:
            if int(row[0])==0:                    
                if translator.detect(str1).lang=="en" and translator.detect(str2).lang=="en" and translator.detect(str3).lang=="en" and translator.detect(str4).lang=="en":
                    is_eng = True
                    print("와 씨발!")
                else: is_eng = False

                api_count += 4

                if api_count>100:
                    print("Going to sleep for 60 seconds from", time.time())
                    print("Count:",count)
                    time.sleep(60)
                    api_count = 0
                    
            if is_eng: csv_writer.writerow(row)
            else: csv_writer2.writerow(row)
        except Exception: miss+=1

print("time :", time.time() - start)
print("COUNT:", count)
print("MISS:", miss)
