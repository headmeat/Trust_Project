import csv, sys, math, re, copy
from ddd import HelloWorldExample
import matplotlib.pyplot as plt
from neo4j import GraphDatabase
import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer
import operator

sia = SentimentIntensityAnalyzer()

sys.path.append("C:/Users/headm/OneDrive/Desktop/csv")

def sign(num):
    if num<0:
        return -1
    return 1

def solution(citations):
    if len(citations)==0:return 0
    
    citations.sort()
    l = len(citations)
    for i in range(l):
        if citations[i] >= l-i:
            # 논문이 인용된 횟수(h번 이상) >= 인용된 논문의 개수(h개 == h번)
            return l-i
    return 0
 
def sentiment(tweet):
    regex = "(?<=^|(?<=[^a-zA-Z0-9-_\.]))(@[A-Za-z]+[A-Za-z0-9-_]+)"
    score = 0
    m = re.findall(regex, tweet)
    
    if m:
        stats = sia.polarity_scores(tweet)

        del stats['compound']
        sent = max(stats.items(), key=operator.itemgetter(1))[0]

        #score를 0.5로 하면 15/8/11 총 34/64
        #score를 1로 하면 14/10/12 총 36/64
    
        if sent == "neg":
            score = -1
        elif sent == "pos":
            score = 1
            
        for name in m:
            if name in dic: 
                quote_count[name] += 1
                quote_dic[name] += score

def self_sentiment(row):
    score = 0
    
    stats = sia.polarity_scores(row[4])
    del stats['compound']
    sent = max(stats.items(), key=operator.itemgetter(1))[0]

    #score를 0.5로 하면 15/8/11 총 34/64
    #score를 1로 하면 14/10/12 총 36/64
    #1->changed
    if sent == "neg":
        score = -max(stats.items(), key=operator.itemgetter(1))[1]
    elif sent == "pos":
        score = max(stats.items(), key=operator.itemgetter(1))[1]

    s_dic[row[2]].append(score)

rt_dic = dict()
pr_dic = dict()
fol_dic = dict()
str_dic = dict()
fav_dic = dict()
quote_dic = dict()
dic = dict()
temp = dict()
fav_temp = dict()
quote_count = dict()
s_dic = dict()


act_ids = ['15003446', '34939208', '168679374', '223238349', '236953420', '2151247592', '486139568', '355866075', '14173032', '2426574114', '1534167900', '2803822165', '2371952437', '2525906341', '3195244375', '1961333743', '955733059', '14276189', '108021761', '1289436835', '31186367', '2177224099', '472600930', '18223590', '18856867', '2149782648', '1373568355', '39199749', '884935388', '182642157', '319102548', '35499699', '163537857', '26223938', '1473023792', '807025762708688898', '961797541', '16598957', '3108351', '260943149', '2615610961', '2281127150', '851632189', '34713362', '4464995894', '52849759', '191690478', '40243607', '35770843', '1469603575', '14230772', '702585281', '358482230', '241583523', '40909981', '211951561', '2235043482', '1431342590', '267317705', '633238141', '861619895485726722', '28571999', '25410160', '21241717', '820534716', '286654612']
c = c_ = max_rt = max_fav = max_quote = 0
lst = []
usernames=dict()
#lst = ['John_Hempton', 'BarbarianCap', 'muddywatersre', 'AlderLaneeggs', 'CitronResearch', 'BrattleStCap', 'KerrisdaleCap', 'modestproposal1', 'marketfolly', 'ActivistShorts', 'Carl_C_Icahn', 'DonutShorts', 'sprucepointcap', 'BluegrassCap', 'NoonSixCap', 'WallStCynic', 'GothamResearch', 'herbgreenberg', 'valuewalk', 'UnionSquareGrp', 'PlanMaestro', 'FatTailCapital', 'ShortSightedCap', 'footnoted', 'zerohedge', 'FundyLongShort', 'DumbLuckCapital', 'Hedge_FundGirl', 'PresciencePoint', 'DavidSchawel', 'fundiescapital', 'ActAccordingly', 'MicroFundy', 'BergenCapital', 'EdBorgato', 'RodBoydILM', 'activiststocks', 'firstadopter', 'WSJ', 'xuexishenghuo', 'cablecarcapital', 'probesreporter', 'GrantsPub', 'business', 'AureliusValue', 'davidein', 'plainview_', 'TMTanalyst', 'manualofideas', 'QTRResearch', 'matt_levine', 'LibertyRPF', 'FCFYield', 'GlaucusResearch', 'PhilipEtienne', 'HedgeyeENERGY', 'TigreCapital', 'CopperfieldRscr', 'adoxen', 'mjmauboussin', 'TruthGundlach', 'bespokeinvest', 'UnderwaterCap', 'schaudenfraud', 'JohnHuber72', 'mark_dow']
lst = ['Nike', 'LouisVuitton', 'Hermes_Paris', 'gucci', 'adidas', 'TiffanyAndCo', 'ZARA', 'hm', 'lululemon', 'Moncler', 'CHANEL', 'ROLEX', 'Prada', 'swarovski', 'Burberry', 'RalphLauren', 'TOMFORD', 'thenorthface', 'LEVIS', 'VictoriasSecret', 'newbalance', 'MichaelKors', 'tjmaxx', 'ASOS', 'UnderArmour', 'Coach', 'Nordstrom', 'SKECHERSUSA', 'ca_europe', 'Chopard', 'dolcegabbana', 'LouboutinWorld', 'omegawatches', 'footlocker', 'ray_ban', 'Macys', 'VeraWang', 'Dior', 'PUMA', 'SteveMadden', 'AEO', 'armani', 'NineWest', 'Fendi', 'UrbanOutfitter', 'Ferragamo', 'HUGOBOSS', 'OldNavy', 'Primark']
fol = {'@Nike':8400000, '@LouisVuitton':7700000, '@Hermes_Paris':98200, '@gucci':6200000, '@adidas':3900000, '@TiffanyAndCo':1600000, '@ZARA':1300000, '@hm':8100000, '@lululemon':1000000, '@Moncler':1100000, '@CHANEL':13200000, '@ROLEX':859500, '@Prada':1300000, '@swarovski':214200, '@Burberry':8200000, '@RalphLauren':2300000, '@TOMFORD':131300, '@thenorthface':489700, '@LEVIS':756700, '@VictoriasSecret':10700000, '@newbalance':259400, '@MichaelKors':3400000, '@tjmaxx':357500, '@ASOS':1000000, '@UnderArmour':950100, '@Coach':616400, '@Nordstrom':714800, '@SKECHERSUSA': 47400, '@ca_europe':78000, '@Chopard':155800, '@dolcegabbana':5300000, '@LouboutinWorld':2900000, '@omegawatches':241000, '@footlocker':1500000, '@ray_ban':432700, '@Macys':909100, '@VeraWang':841900, '@Dior':8300000, '@PUMA':1700000, '@SteveMadden':72600, '@AEO':583500, '@armani':3500000, '@NineWest':46400, '@Fendi':801200, '@UrbanOutfitter':951000, '@Ferragamo':507800, '@HUGOBOSS':689700, '@OldNavy':336800, '@Primark':257800}
for i in range(len(lst)):
    usernames[lst[i]] = act_ids[i]

for name in lst:
    temp["@"+name] = []

try:
    for i in range(len(lst)):
        s_dic["@"+lst[i]] = []
        rt_dic["@"+lst[i]] = 0
        fav_dic["@"+lst[i]] = 0
        quote_dic["@"+lst[i]] = 0
        dic["@"+lst[i]]=0
        quote_count["@"+lst[i]] = 0
except Exception as e:
    print(e)
"""
with GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "1234")) as driver:
    with driver.session() as session:
        values = session.read_transaction(HelloWorldExample.pageRank)
        for i in range(len(values)):
            pr_dic[values[i][0]._properties["username"]] = values[i][1]
        
        values = session.read_transaction(HelloWorldExample.f_getFollowers, temp)
        fol_dic = values
"""
regex = "(?<=^|(?<=[^a-zA-Z0-9-_\.]))(@[A-Za-z]+[A-Za-z0-9-_]+)"
with open('C:/Users/headm/OneDrive/Desktop/fin/brands.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')

        #try:
        if "@" in row[4]: sentiment(row[4])
        #except Exception: 
            #print("ERROR:",row)
        
        if row[2] in dic:
            self_sentiment(row)
            if row[7].isnumeric():
                fav_dic[row[2]] += int(row[7])#*0.25
            if row[8].isnumeric():
                rt_dic[row[2]] += int(row[8])
                temp[row[2]].append(int(row[8]))

        line_count += 1
        #print(line_count)
            #0:tweet_#_of_user, 1:userscreen, 2:username, 3:timestamp, 4:text, 5:emojis, 6:comments, 7:likes, 8:retweets 9:image_link, 10:tweet_url
            #print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            #line_count += 1
    print(f'Processed {line_count} lines.')

    dic_sort = sorted(dic.items(), key = lambda item: item[1], reverse=True) #issa list
    y_dic = copy.deepcopy(dic)
    ncr = max(max(fav_dic.values()), max(rt_dic.values()))
    
    max_value = max(fav_dic.values())+max(quote_dic.values())#+max(s_dic.values())
    
    for key in s_dic.keys():
        if len(s_dic[key])!=0:
                    s_dic[key] = np.var(s_dic[key])
        else: s_dic[key] = 100
    for key in list(dic):
        try:
            if rt_dic[key]!=0 or fav_dic[key]!=0:
                #파주놈꺼 math.log(max_value)
                #dic[key] = (((math.log(int(rt_dic[key])+1)/math.log(max(rt_dic.values()))+math.log(int(fav_dic[key])+1)/math.log(max(fav_dic.values()))+sign(quote_dic[key]*math.log(abs(int(quote_dic[key]))+1)/math.log(max(quote_dic.values())))))/math.log(max_value))
                #dic[key] = (sign(s_dic[key])*math.log(abs(int(s_dic[key]))+1)/math.log(max(s_dic.values()))+math.log(int(fav_dic[key])+1)/math.log(max(fav_dic.values()))+sign(quote_dic[key])*math.log(abs(int(quote_dic[key]))+1)/math.log(max(quote_dic.values())))/math.log(max_value)
                dic[key] = (math.log(int(fav_dic[key])+1)/math.log(max(fav_dic.values()))+sign(quote_dic[key])*math.log(abs(int(quote_dic[key]))+1)/math.log(max(quote_dic.values())))/math.log(max_value)
                #윤씨꺼
                #y_dic[key] = math.exp(int(fav_dic[key])+1)/math.exp(max(fav_dic.values()))+sign(quote_dic[key]*math.exp(abs(int(quote_dic[key]))+1)/math.exp(max(quote_dic.values())))))/math.exp(max_value)
                y_dic[key] = (math.exp((int(fav_dic[key])+int(quote_dic[key]))/(fav_dic[key]+quote_count[key]))-1)*(max(fav_dic[key], rt_dic[key])/ncr)
            else: del dic[key]
            
            temp[key] = solution(temp[key])
            
        except Exception as e: 
            print("LINE 131:",e)

    ab = []

    for i in s_dic.values():
        ab.append(abs(i))
        
    max_s = max(ab)
    max_v = max(dic.values()) 
    max_r = max(temp.values())
    min_s = min(s_dic.values())
    max_y = max(y_dic.values())
    max_f = max(fol.values())
    max_f = max(fol.values())
    
    sub_dic = copy.deepcopy(dic)
    h_index = copy.deepcopy(dic)

    for key in list(sub_dic):
        #브랜드 기준 윤진경 10/27
        #상호작용 + h-index
        y_dic[key] = y_dic[key]/max_y
        sub_dic[key] = sub_dic[key]/max_v#/2+temp[key]/max_r/2
        #h_index[key] = h_index[key]/max_v*0.5+temp[key]/max_r*0.5
        #h_index[key] = h_index[key]/max_v*temp[key]/max_r
        #weight = s_dic[key]/max_s
        tr = (min_s)/(s_dic[key])
        
        if math.isnan(tr): tr = 1
            
        h_index[key] = (tr*0.5+h_index[key]/max_v*0.5)*(1-fol[key]/max_f)+temp[key]/max_r*((fol[key]/max_f))
        #아래 수식이 11명/20명, 13명/22명까지 나오는 현재 정보과학회 수식(브랜드 기준 1: 12, 2: 6)
        #h_index[key] = h_index[key]/max_v*0.5+(temp[key]/max_r*(0.5)+fol[key]/max_f*0.5)*0.5
        #h_index[key] = h_index[key]/max_v*((fol[key]/max_f))+temp[key]/max_r*(1-fol[key]/max_f)
        #h_index[key] = h_index[key]/max_v*math.log((fol[key]/max_f)/(max_f))+temp[key]/max_r*(math.log(1-(fol[key])/(max_f)))
        
        #아래 수식도 18/25명 나옴(브랜드까지 보면 이게 더 정확)
        #h_index[key] = (temp[key]/max_r*(0.5)+fol[key]/max_f*0.5)
        #h_index[key] = (temp[key]/max_r*0.5+(fol_dic[key]/max_f)*0.5)
        #h_index[key] = h_index[key]/max_v*0.5+(temp[key]/max_r)*0.5
        
        #아래 수식이 13명/20명, 15명/22명까지 나오는 best
        #h_index[key] = h_index[key]/max_v*0.5+(temp[key]/max_r*(1-fol_dic[key]/max_f)+fol_dic[key]/max_f*pr_dic[key]/max_pr)*0.5
    
    
    
    for key in list(dic):
        dic[key] = dic[key]/max_v/2+temp[key]/max_r/4
    
    print("AVG:",sum(sub_dic.values())/len(sub_dic))
    print(max(sub_dic.values()))

    try:
        print(len(sub_dic))
        x = np.arange(len(sub_dic))
        plt.figure(figsize=(15, 5))
        plt.bar(x, sub_dic.values(), width=1.0)
        plt.xticks(x, sub_dic.keys())
        plt.show()
    except Exception as e: print(e)
    
    print("AVG:",sum(h_index.values())/len(h_index))
    print(max(h_index.values()))

    try:
        print(len(h_index))
        x = np.arange(len(h_index))
        plt.figure(figsize=(15, 5))
        plt.bar(x, h_index.values(), width=1.0)
        plt.xticks(x, h_index.keys())
        plt.show()
    except Exception as e: print(e)
    
    #print(sorted(dic.items(), key = lambda item: item[1]))
    
    try:
        print(len(y_dic))
        x = np.arange(len(y_dic))
        plt.figure(figsize=(15, 5))
        plt.bar(x, y_dic.values(), width=1.0)
        plt.xticks(x, y_dic.keys())
        plt.show()
    except Exception as e: print(e)
    
    sub_dic = sorted(sub_dic.items(), key = lambda item: item[1], reverse=True)
    h_index = sorted(h_index.items(), key = lambda item: item[1], reverse=True)
    dic = sorted(dic.items(), key = lambda item: item[1], reverse=True)
    y_dic = sorted(y_dic.items(), key = lambda item: item[1], reverse=True)
    a=0
    
    test = []
    print()
    print("SUBDIC")
    for key in sub_dic:
        test.append(key[0][1:])
        a+=1
    print(test)
    a = 0
    
    test = []     
    print()
    
    print("HINDEX")
    for key in h_index:
        test.append(key[0][1:])
        a+=1
    print(test)
        
    a=0
    
    test = []
    print()
    
    test = []
    print()
    print("윤진경")
    for key in y_dic:
        test.append(key[0][1:])
        a+=1
    print(test)
