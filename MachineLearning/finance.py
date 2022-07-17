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
tw_dic = dict()
dic = dict()
temp = dict()
fav_temp = dict()
quote_count = dict()
s_dic = dict()

act_ids = ['15003446', '34939208', '168679374', '223238349', '236953420', '2151247592', '486139568', '355866075', '14173032', '2426574114', '1534167900', '2803822165', '2371952437', '2525906341', '3195244375', '1961333743', '955733059', '14276189', '108021761', '1289436835', '31186367', '2177224099', '472600930', '18223590', '18856867', '2149782648', '1373568355', '39199749', '884935388', '182642157', '319102548', '35499699', '163537857', '26223938', '1473023792', '807025762708688898', '961797541', '16598957', '3108351', '260943149', '2615610961', '2281127150', '851632189', '34713362', '4464995894', '52849759', '191690478', '40243607', '35770843', '1469603575', '14230772', '702585281', '358482230', '241583523', '40909981', '211951561', '2235043482', '1431342590', '267317705', '633238141', '861619895485726722', '28571999', '25410160', '21241717', '820534716', '286654612']
c = c_ = max_rt = max_fav = max_quote = 0
lst = []
usernames=dict()
lst = ['John_Hempton', 'BarbarianCap', 'muddywatersre', 'AlderLaneeggs', 'CitronResearch', 'BrattleStCap', 'KerrisdaleCap', 'modestproposal1', 'marketfolly', 'ActivistShorts', 'Carl_C_Icahn', 'DonutShorts', 'sprucepointcap', 'BluegrassCap', 'NoonSixCap', 'WallStCynic', 'GothamResearch', 'herbgreenberg', 'valuewalk', 'UnionSquareGrp', 'PlanMaestro', 'FatTailCapital', 'ShortSightedCap', 'footnoted', 'zerohedge', 'FundyLongShort', 'DumbLuckCapital', 'Hedge_FundGirl', 'PresciencePoint', 'DavidSchawel', 'fundiescapital', 'ActAccordingly', 'MicroFundy', 'BergenCapital', 'EdBorgato', 'RodBoydILM', 'activiststocks', 'firstadopter', 'WSJ', 'xuexishenghuo', 'cablecarcapital', 'probesreporter', 'GrantsPub', 'business', 'AureliusValue', 'davidein', 'plainview_', 'TMTanalyst', 'manualofideas', 'QTRResearch', 'matt_levine', 'LibertyRPF', 'FCFYield', 'GlaucusResearch', 'PhilipEtienne', 'HedgeyeENERGY', 'TigreCapital', 'CopperfieldRscr', 'adoxen', 'mjmauboussin', 'TruthGundlach', 'bespokeinvest', 'UnderwaterCap', 'schaudenfraud', 'JohnHuber72', 'mark_dow']
#lst = ['John_Hempton', 'BarbarianCap', 'AlderLaneeggs', 'modestproposal1', 'ActivistShorts', 'DonutShorts', 'sprucepointcap', 'BluegrassCap', 'NoonSixCap', 'WallStCynic', 'herbgreenberg', 'valuewalk', 'UnionSquareGrp', 'PlanMaestro', 'FatTailCapital', 'ShortSightedCap', 'footnoted', 'zerohedge', 'FundyLongShort', 'DumbLuckCapital', 'Hedge_FundGirl', 'PresciencePoint', 'DavidSchawel', 'fundiescapital', 'ActAccordingly', 'MicroFundy', 'EdBorgato', 'RodBoydILM', 'activiststocks', 'firstadopter', 'WSJ', 'xuexishenghuo', 'cablecarcapital', 'probesreporter', 'business', 'plainview_', 'TMTanalyst', 'manualofideas', 'FCFYield', 'HedgeyeENERGY', 'adoxen', 'bespokeinvest', 'schaudenfraud', 'JohnHuber72', 'mark_dow']

#lst = ['Nike', 'LouisVuitton', 'Hermes_Paris', 'gucci', 'adidas', 'TiffanyAndCo', 'ZARA', 'hm', 'lululemon', 'Moncler', 'CHANEL', 'ROLEX', 'Prada', 'swarovski', 'Burberry', 'RalphLauren', 'TOMFORD', 'thenorthface', 'Levi’s', 'VictoriasSecret', 'newbalance', 'MichaelKors', 'tjmaxx', 'ASOS', 'UnderArmour', 'Coach', 'Nordstrom']
for i in range(len(lst)):
    usernames[lst[i]] = act_ids[i]

for name in lst:
    temp["@"+name] = []
    tw_dic["@"+name] = 0

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

with GraphDatabase.driver("bolt://localhost:11003", auth=("neo4j", "1234")) as driver:
    with driver.session() as session:
        values = session.read_transaction(HelloWorldExample.pageRank)
        for i in range(len(values)):
            pr_dic[values[i][0]._properties["username"]] = values[i][1]
        
        values = session.read_transaction(HelloWorldExample.f_getFollowers, temp)
        fol_dic = values

#fol_dic = {'@John_Hempton': 55494, '@BarbarianCap': 38922, '@muddywatersre': 205071, '@AlderLaneeggs': 63914, '@CitronResearch': 326133, '@BrattleStCap': 17000, '@KerrisdaleCap': 58860, '@modestproposal1': 73429, '@marketfolly': 51918, '@ActivistShorts': 29695, '@Carl_C_Icahn': 399253, '@DonutShorts': 33347, '@sprucepointcap': 35128, '@BluegrassCap': 43990, '@NoonSixCap': 16804, '@WallStCynic': 67282, '@GothamResearch': 26099, '@herbgreenberg': 378768, '@valuewalk': 62160, '@UnionSquareGrp': 7555, '@PlanMaestro': 20603, '@FatTailCapital': 18353, '@ShortSightedCap': 12674, '@footnoted': 23852, '@zerohedge': 943927, '@FundyLongShort': 5605, '@DumbLuckCapital': 8111, '@Hedge_FundGirl': 7727, '@PresciencePoint': 20673, '@DavidSchawel': 47161, '@fundiescapital': 9161, '@ActAccordingly': 12953, '@MicroFundy': 8526, '@BergenCapital': 27771, '@EdBorgato': 14940, '@RodBoydILM': 11874, '@activiststocks': 9949, '@firstadopter': 46277, '@WSJ': 18824436, '@xuexishenghuo': 3475, '@cablecarcapital': 8361, '@probesreporter': 9583, '@GrantsPub': 46141, '@business': 7248952, '@AureliusValue': 24345, '@davidein': 58800, '@plainview_': 3367, '@TMTanalyst': 12291, '@manualofideas': 24276, '@QTRResearch': 155435, '@matt_levine': 156192, '@LibertyRPF': 17802, '@FCFYield': 7542, '@GlaucusResearch': 9818, '@PhilipEtienne': 9418, '@HedgeyeENERGY': 11076, '@TigreCapital': 1939, '@CopperfieldRscr': 7180, '@adoxen': 5726, '@mjmauboussin': 85671, '@TruthGundlach': 177496, '@bespokeinvest': 123852, '@UnderwaterCap': 2899, '@schaudenfraud': 7592, '@JohnHuber72': 28752, '@mark_dow': 82412}

regex = "(?<=^|(?<=[^a-zA-Z0-9-_\.]))(@[A-Za-z]+[A-Za-z0-9-_]+)"

with open('C:/Users/headm/OneDrive/Desktop/fin/fin_jy.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
        
        #try:
        if "@" in row[4]: sentiment(row[4])
        #except Exception: 
            #print("ERROR:",row)
        
        if row[2] in dic and "답글" not in row[4] and "님" not in row[4] and "인용" not in row[4]:
            tw_dic[row[2]]+=1
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
    
    max_value = max(fav_dic.values())+max(quote_dic.values())#+max(rt_dic.values())
    
    for key in s_dic.keys():
        if len(s_dic[key])!=0:
                    s_dic[key] = np.var(s_dic[key])
        else: s_dic[key] = 100
        
        if tw_dic[key] < 30: s_dic[key] = 100
    
    for key in fav_dic.keys():
        if tw_dic[key]>0:
            fav_dic[key] = (fav_dic[key]/tw_dic[key])
    print("이것...")
    print(dic)
    
    for key in list(dic):
        try:
            if rt_dic[key]!=0 or fav_dic[key]!=0:
                #파주놈꺼 math.log(max_value)
                #dic[key] = (((math.log(int(rt_dic[key])+1)/math.log(max(rt_dic.values()))+math.log(int(fav_dic[key])+1)/math.log(max(fav_dic.values()))+sign(quote_dic[key]*math.log(abs(int(quote_dic[key]))+1)/math.log(max(quote_dic.values())))))/math.log(max_value))
                
                #dic[key] = (math.log(int(rt_dic[key])+1)/math.log(max(rt_dic.values()))+math.log(int(fav_dic[key])+1)/math.log(max(fav_dic.values()))+sign(quote_dic[key])*math.log(abs(int(quote_dic[key]))+1)/math.log(max(quote_dic.values())))/math.log(max_value)
                dic[key] = (math.log(int(fav_dic[key])+1)/math.log(max(fav_dic.values()))+sign(quote_dic[key])*math.log(abs(int(quote_dic[key]))+1)/math.log(max(quote_dic.values())))/math.log(max_value)
                #(sign(s_dic[key])*math.log(abs(int(s_dic[key]))+1)/math.log(max(s_dic.values()))+
                #윤씨꺼(math.log(int(s_dic[key])+1)/math.log(max(s_dic.values()))+ +max(s_dic.values())
                #y_dic[key] = math.exp(int(fav_dic[key])+1)/math.exp(max(fav_dic.values()))+sign(quote_dic[key]*math.exp(abs(int(quote_dic[key]))+1)/math.exp(max(quote_dic.values())))))/math.exp(max_value)
                #y_dic[key] = (math.exp((int(fav_dic[key])+int(quote_dic[key]))/(fav_dic[key]+quote_count[key]))-1)*(max(fav_dic[key], rt_dic[key])/ncr)
                y_dic[key] = (1/tw_dic[key])*(math.exp((int(fav_dic[key])*0.25+int(quote_dic[key])*0.5+int(rt_dic[key]*0.75)+fol_dic[key])/(fav_dic[key]+quote_count[key]+rt_dic[key]+fol_dic[key]))-1)*(max(fav_dic[key], rt_dic[key], fol_dic[key], quote_dic[key])/ncr)
            else: 
                del dic[key]
            
            temp[key] = solution(temp[key])
            
        except Exception as e: 
            print("LINE 131:",e)
            print(math.exp((int(rt_dic[key]))))
    print("TEMP:",temp)
    ab = []

"""
rt_dic = {'@zerohedge': 329726, '@WSJ': 318229, '@business': 88851, '@modestproposal1': 41547, '@AlderLaneeggs': 39470, '@BluegrassCap': 19316, '@mark_dow': 17575, '@WallStCynic': 17172, '@NoonSixCap': 12279, '@BarbarianCap': 12232, '@PlanMaestro': 11925, '@DavidSchawel': 10406, '@John_Hempton': 9842, '@EdBorgato': 8663, '@valuewalk': 7991, '@DonutShorts': 6834, '@RodBoydILM': 6484, '@bespokeinvest': 6066, '@schaudenfraud': 4443, '@herbgreenberg': 3884, '@FatTailCapital': 3831, '@mjmauboussin': 3370, '@DumbLuckCapital': 2914, '@Carl_C_Icahn': 2578, '@firstadopter': 2233, '@activiststocks': 2203, '@JohnHuber72': 2073, '@plainview_': 1891, '@adoxen': 1730, '@MicroFundy': 1450, '@CitronResearch': 1408, '@matt_levine': 1397, '@FCFYield': 993, '@fundiescapital': 884, '@cablecarcapital': 879, '@xuexishenghuo': 855, '@manualofideas': 773, '@HedgeyeENERGY': 707, '@UnionSquareGrp': 700, '@ActivistShorts': 695, '@probesreporter': 672, '@AureliusValue': 641, '@sprucepointcap': 501, '@ShortSightedCap': 493, '@muddywatersre': 484, '@QTRResearch': 429, '@ActAccordingly': 413, '@GrantsPub': 401, '@footnoted': 378, '@marketfolly': 367, '@BergenCapital': 356, '@KerrisdaleCap': 305, '@BrattleStCap': 302, '@PresciencePoint': 285, '@LibertyRPF': 284, '@TMTanalyst': 260, '@Hedge_FundGirl': 252, '@FundyLongShort': 160, '@PhilipEtienne': 129, '@GlaucusResearch': 124, '@GothamResearch': 100, '@CopperfieldRscr': 59, '@davidein': 5, '@TigreCapital': 4, '@TruthGundlach': 0, '@UnderwaterCap': 0}
temp = {'@WSJ': 208, '@zerohedge': 170, '@business': 89, '@modestproposal1': 80, '@AlderLaneeggs': 51, '@BluegrassCap': 51, '@WallStCynic': 46, '@NoonSixCap': 44, '@EdBorgato': 44, '@BarbarianCap': 43, '@mark_dow': 41, '@PlanMaestro': 39, '@John_Hempton': 38, '@DavidSchawel': 36, '@mjmauboussin': 35, '@FatTailCapital': 30, '@schaudenfraud': 27, '@JohnHuber72': 26, '@herbgreenberg': 25, '@valuewalk': 25, '@RodBoydILM': 25, '@bespokeinvest': 24, '@DonutShorts': 23, '@CitronResearch': 22, '@firstadopter': 20, '@plainview_': 18, '@DumbLuckCapital': 17, '@Carl_C_Icahn': 15, '@cablecarcapital': 14, '@adoxen': 14, '@muddywatersre': 13, '@AureliusValue': 13, '@FCFYield': 13, '@HedgeyeENERGY': 13, '@fundiescapital': 12, '@GrantsPub': 12, '@manualofideas': 12, '@QTRResearch': 12, '@UnionSquareGrp': 11, '@xuexishenghuo': 11, '@marketfolly': 10, '@ShortSightedCap': 10, '@MicroFundy': 10, '@probesreporter': 10, '@ActivistShorts': 9, '@activiststocks': 9, '@matt_levine': 9, '@LibertyRPF': 9, '@KerrisdaleCap': 8, '@sprucepointcap': 8, '@footnoted': 8, '@Hedge_FundGirl': 8, '@PresciencePoint': 8, '@ActAccordingly': 8, '@BergenCapital': 8, '@TMTanalyst': 8, '@BrattleStCap': 6, '@FundyLongShort': 6, '@GlaucusResearch': 6, '@GothamResearch': 5, '@PhilipEtienne': 5, '@CopperfieldRscr': 4, '@davidein': 1, '@TigreCapital': 1, '@TruthGundlach': 0, '@UnderwaterCap': 0}
tw_dic = {'@zerohedge': 8587, '@AlderLaneeggs': 5954, '@WSJ': 5000, '@mark_dow': 3988, '@business': 3425, '@John_Hempton': 3142, '@WallStCynic': 2884, '@activiststocks': 2881, '@RodBoydILM': 2742, '@valuewalk': 2691, '@DavidSchawel': 2680, '@BluegrassCap': 2478, '@modestproposal1': 2390, '@BarbarianCap': 2215, '@PlanMaestro': 2014, '@DonutShorts': 2013, '@NoonSixCap': 1548, '@bespokeinvest': 1392, '@DumbLuckCapital': 1355, '@schaudenfraud': 1202, '@MicroFundy': 1122, '@adoxen': 936, '@herbgreenberg': 751, '@firstadopter': 638, '@plainview_': 637, '@EdBorgato': 476, '@xuexishenghuo': 454, '@FatTailCapital': 447, '@fundiescapital': 411, '@probesreporter': 406, '@UnionSquareGrp': 267, '@sprucepointcap': 218, '@ActivistShorts': 216, '@HedgeyeENERGY': 213, '@manualofideas': 209, '@footnoted': 203, '@ActAccordingly': 199, '@cablecarcapital': 174, '@ShortSightedCap': 173, '@Hedge_FundGirl': 136, '@JohnHuber72': 130, '@FundyLongShort': 129, '@TMTanalyst': 127, '@PresciencePoint': 116, '@FCFYield': 107, '@LibertyRPF': 91, '@marketfolly': 88, '@mjmauboussin': 84, '@AureliusValue': 81, '@BergenCapital': 59, '@PhilipEtienne': 59, '@muddywatersre': 56, '@QTRResearch': 53, '@GlaucusResearch': 34, '@CitronResearch': 30, '@KerrisdaleCap': 29, '@GrantsPub': 27, '@CopperfieldRscr': 24, '@GothamResearch': 23, '@Carl_C_Icahn': 17, '@matt_levine': 15, '@BrattleStCap': 7, '@davidein': 2, '@TigreCapital': 2, '@TruthGundlach': 0, '@UnderwaterCap': 0}
fol_dic = {'@BarbarianCap': 50, '@WallStCynic': 48, '@muddywatersre': 46, '@modestproposal1': 45, '@marketfolly': 45, '@John_Hempton': 41, '@AlderLaneeggs': 41, '@ShortSightedCap': 41, '@KerrisdaleCap': 40, '@matt_levine': 40, '@Carl_C_Icahn': 39, '@MicroFundy': 39, '@CitronResearch': 38, '@BrattleStCap': 38, '@sprucepointcap': 38, '@BluegrassCap': 38, '@FatTailCapital': 38, '@DavidSchawel': 38, '@firstadopter': 38, '@footnoted': 37, '@ActAccordingly': 37, '@NoonSixCap': 36, '@ActivistShorts': 35, '@DonutShorts': 35, '@herbgreenberg': 35, '@Hedge_FundGirl': 35, '@valuewalk': 34, '@PlanMaestro': 34, '@zerohedge': 34, '@EdBorgato': 34, '@UnionSquareGrp': 33, '@xuexishenghuo': 33, '@GothamResearch': 32, '@FundyLongShort': 31, '@cablecarcapital': 31, '@business': 31, '@TMTanalyst': 31, '@DumbLuckCapital': 30, '@activiststocks': 30, '@WSJ': 30, '@RodBoydILM': 29, '@GrantsPub': 29, '@AureliusValue': 29, '@LibertyRPF': 29, '@FCFYield': 29, '@mjmauboussin': 29, '@TruthGundlach': 29, '@fundiescapital': 28, '@JohnHuber72': 28, '@PresciencePoint': 27, '@davidein': 27, '@mark_dow': 27, '@schaudenfraud': 26, '@plainview_': 25, '@probesreporter': 24, '@HedgeyeENERGY': 24, '@BergenCapital': 23, '@manualofideas': 23, '@PhilipEtienne': 23, '@TigreCapital': 22, '@QTRResearch': 21, '@CopperfieldRscr': 21, '@bespokeinvest': 21, '@GlaucusResearch': 20, '@adoxen': 20, '@UnderwaterCap': 20}
quote_dic = {'@DavidSchawel': 5, '@NoonSixCap': 3, '@MicroFundy': 3, '@mark_dow': 3, '@BarbarianCap': 2, '@AlderLaneeggs': 2, '@BluegrassCap': 2, '@RodBoydILM': 2, '@muddywatersre': 1, '@CitronResearch': 1, '@BrattleStCap': 1, '@modestproposal1': 1, '@WallStCynic': 1, '@fundiescapital': 1, '@GrantsPub': 1, '@AureliusValue': 1, '@matt_levine': 1, '@HedgeyeENERGY': 1, '@adoxen': 1, '@schaudenfraud': 1, '@John_Hempton': 0, '@KerrisdaleCap': 0, '@marketfolly': 0, '@ActivistShorts': 0, '@Carl_C_Icahn': 0, '@DonutShorts': 0, '@sprucepointcap': 0, '@GothamResearch': 0, '@herbgreenberg': 0, '@valuewalk': 0, '@UnionSquareGrp': 0, '@FatTailCapital': 0, '@ShortSightedCap': 0, '@footnoted': 0, '@zerohedge': 0, '@FundyLongShort': 0, '@DumbLuckCapital': 0, '@Hedge_FundGirl': 0, '@PresciencePoint': 0, '@ActAccordingly': 0, '@BergenCapital': 0, '@EdBorgato': 0, '@activiststocks': 0, '@firstadopter': 0, '@WSJ': 0, '@xuexishenghuo': 0, '@cablecarcapital': 0, '@probesreporter': 0, '@business': 0, '@davidein': 0, '@TMTanalyst': 0, '@manualofideas': 0, '@QTRResearch': 0, '@LibertyRPF': 0, '@FCFYield': 0, '@GlaucusResearch': 0, '@PhilipEtienne': 0, '@TigreCapital': 0, '@CopperfieldRscr': 0, '@mjmauboussin': 0, '@TruthGundlach': 0, '@bespokeinvest': 0, '@UnderwaterCap': 0, '@JohnHuber72': 0, '@PlanMaestro': -1, '@plainview_': -1}
fav_dic = {'@John_Hempton': 0.5149586250795671, '@BarbarianCap': 1.6659142212189617, '@muddywatersre': 5.410714285714286, '@AlderLaneeggs': 1.029895868323816, '@CitronResearch': 42.36666666666667, '@BrattleStCap': 13.428571428571429, '@KerrisdaleCap': 5.413793103448276, '@modestproposal1': 4.645606694560669, '@marketfolly': 0.9545454545454546, '@ActivistShorts': 1.6064814814814814, '@Carl_C_Icahn': 70.23529411764706, '@DonutShorts': 0.8464977645305514, '@sprucepointcap': 1.091743119266055, '@BluegrassCap': 1.2013720742534302, '@NoonSixCap': 0.8552971576227391, '@WallStCynic': 1.9244105409153953, '@GothamResearch': 3.130434782608696, '@herbgreenberg': 1.1251664447403462, '@valuewalk': 1.8457822370865848, '@UnionSquareGrp': 0.6367041198501873, '@PlanMaestro': 1.7969215491559087, '@FatTailCapital': 1.512304250559284, '@ShortSightedCap': 0.4277456647398844, '@footnoted': 1.0295566502463054, '@zerohedge': 40.14836380575288, '@FundyLongShort': 0.07751937984496124, '@DumbLuckCapital': 0.05018450184501845, '@Hedge_FundGirl': 0.47794117647058826, '@PresciencePoint': 1.206896551724138, '@DavidSchawel': 1.1421641791044777, '@fundiescapital': 0.2871046228710462, '@ActAccordingly': 0.3969849246231156, '@MicroFundy': 0.22994652406417113, '@BergenCapital': 3.610169491525424, '@EdBorgato': 3.7478991596638656, '@RodBoydILM': 0.49051787016776077, '@activiststocks': 0.3891010065949323, '@firstadopter': 1.3605015673981191, '@WSJ': 58.9172, '@xuexishenghuo': 0.10572687224669604, '@cablecarcapital': 0.47701149425287354, '@probesreporter': 0.958128078817734, '@GrantsPub': 6.518518518518518, '@business': 29.85080291970803, '@AureliusValue': 2.2222222222222223, '@davidein': 0.0, '@plainview_': 0.29827315541601257, '@TMTanalyst': 0.1889763779527559, '@manualofideas': 1.0239234449760766, '@QTRResearch': 1.6226415094339623, '@matt_levine': 8.266666666666667, '@LibertyRPF': 0.3076923076923077, '@FCFYield': 3.682242990654206, '@GlaucusResearch': 1.8235294117647058, '@PhilipEtienne': 0.6101694915254238, '@HedgeyeENERGY': 0.7417840375586855, '@TigreCapital': 1.5, '@CopperfieldRscr': 0.8333333333333334, '@adoxen': 0.20192307692307693, '@mjmauboussin': 10.583333333333334, '@TruthGundlach': 0, '@bespokeinvest': 4.665229885057471, '@UnderwaterCap': 0, '@schaudenfraud': 0.3502495840266223, '@JohnHuber72': 4.053846153846154, '@mark_dow': 1.1988465396188566}
s_dic = {'@BrattleStCap': 100, '@KerrisdaleCap': 100, '@Carl_C_Icahn': 100, '@GothamResearch': 100, '@GrantsPub': 100, '@davidein': 100, '@matt_levine': 100, '@TigreCapital': 100, '@CopperfieldRscr': 100, '@TruthGundlach': 100, '@UnderwaterCap': 100, '@FundyLongShort': 0.1065067443062316, '@Hedge_FundGirl': 0.03223750254108998, '@PlanMaestro': 0.031036922774195327, '@DavidSchawel': 0.03029806298952995, '@footnoted': 0.02900847280933776, '@RodBoydILM': 0.027339471135312536, '@manualofideas': 0.02660195329777249, '@NoonSixCap': 0.026256478852015434, '@adoxen': 0.025709607731344508, '@MicroFundy': 0.025486323082984617, '@herbgreenberg': 0.025210712481006235, '@PhilipEtienne': 0.025026833668486074, '@John_Hempton': 0.02197707434114749, '@mark_dow': 0.02150119300447732, '@HedgeyeENERGY': 0.019583083956005196, '@DumbLuckCapital': 0.019568013872360127, '@schaudenfraud': 0.01784403657797182, '@plainview_': 0.017533914769240624, '@BarbarianCap': 0.01746380901935806, '@EdBorgato': 0.017064198220464656, '@UnionSquareGrp': 0.016623992453253668, '@BergenCapital': 0.015955422579718475, '@BluegrassCap': 0.015235772705864884, '@AlderLaneeggs': 0.015150570630685666, '@TMTanalyst': 0.013256801165602333, '@cablecarcapital': 0.012906135718060511, '@xuexishenghuo': 0.011613513671912901, '@muddywatersre': 0.008924182397959182, '@zerohedge': 0.008390747270136747, '@WallStCynic': 0.007447682715003241, '@firstadopter': 0.0072646055168483015, '@DonutShorts': 0.006814971374589759, '@modestproposal1': 0.0064804580914199685, '@fundiescapital': 0.005875692518988165, '@FatTailCapital': 0.005660133577566577, '@valuewalk': 0.005481360029806055, '@QTRResearch': 0.004702325382698468, '@JohnHuber72': 0.004225215621301774, '@mjmauboussin': 0.00392984297052154, '@bespokeinvest': 0.002660097374467399, '@business': 0.002486599874601736, '@activiststocks': 0.0021340244392849725, '@probesreporter': 0.0018401226188453988, '@ActivistShorts': 0.001231720143175584, '@ActAccordingly': 0.0011809501780258077, '@WSJ': 0.0011624277407599995, '@CitronResearch': 0.0, '@marketfolly': 0.0, '@sprucepointcap': 0.0, '@ShortSightedCap': 0.0, '@PresciencePoint': 0.0, '@AureliusValue': 0.0, '@LibertyRPF': 0.0, '@FCFYield': 0.0, '@GlaucusResearch': 0.0}
y_dic = {'@John_Hempton': 0.0, '@BarbarianCap': 0.0006211044776182741, '@muddywatersre': 0.0007287444973293932, '@AlderLaneeggs': 0.0004831677382003378, '@CitronResearch': 0.006107379308345842, '@BrattleStCap': 0.000497886167785848, '@KerrisdaleCap': 0.0005660593955561067, '@modestproposal1': 0.0023179066829724796, '@marketfolly': 0.0, '@ActivistShorts': 0.0005569260031706532, '@Carl_C_Icahn': 0.029746261711117196, '@DonutShorts': 0.0, '@sprucepointcap': 0.00016776853156927232, '@BluegrassCap': 0.0005933865292392306, '@NoonSixCap': 0.0005594899281321672, '@WallStCynic': 0.0003169766297878938, '@GothamResearch': 0.00013585539086079929, '@herbgreenberg': 0.00010788251900266041, '@valuewalk': 0.0012629851259090639, '@UnionSquareGrp': 0.0, '@PlanMaestro': 0.0, '@FatTailCapital': 0.0002229739217828354, '@ShortSightedCap': 0.0, '@footnoted': 6.408330315197392e-05, '@zerohedge': 0.5227464243883346, '@FundyLongShort': 0.0, '@DumbLuckCapital': 0.0, '@Hedge_FundGirl': 0.0, '@PresciencePoint': 0.00010271606495787873, '@DavidSchawel': 0.0006390178064521491, '@fundiescapital': 9.992200674153811e-05, '@ActAccordingly': 0.0, '@MicroFundy': 0.0001337093652465432, '@BergenCapital': 0.0018209616653128092, '@EdBorgato': 0.0019408234403790144, '@RodBoydILM': 0.00016629385386955354, '@activiststocks': 0.0, '@firstadopter': 0.0002656436213420568, '@WSJ': 1.0, '@xuexishenghuo': 0.0, '@cablecarcapital': 0.0, '@probesreporter': 0.0, '@GrantsPub': 0.000390118554006533, '@business': 0.1618278305488769, '@AureliusValue': 0.00014068814804930042, '@davidein': 0.0, '@plainview_': -5.811190606954413e-05, '@TMTanalyst': 0.0, '@manualofideas': 0.0005970186040389562, '@QTRResearch': 2.8066922448421093e-05, '@matt_levine': 0.0018701972215376453, '@LibertyRPF': 0.0, '@FCFYield': 0.0013804509622974926, '@GlaucusResearch': 0.00017429876648857034, '@PhilipEtienne': 0.0, '@HedgeyeENERGY': 0.00018386642230048164, '@TigreCapital': 3.376107665544424e-05, '@CopperfieldRscr': 0.0, '@adoxen': 6.980862132489737e-05, '@mjmauboussin': 0.008625810266885895, '@TruthGundlach': 0, '@bespokeinvest': 0.0014341480982795222, '@UnderwaterCap': 0, '@schaudenfraud': 0.0001552603319982594, '@JohnHuber72': 0.001991113043114562, '@mark_dow': 0.0005529705248869727}
dic = {'@John_Hempton': 0.10402854877289916, '@BarbarianCap': 0.16577263423837876, '@muddywatersre': 0.08786236558017475, '@AlderLaneeggs': 0.1805926128702399, '@CitronResearch': 0.06580827065045941, '@BrattleStCap': 0.06178743677571983, '@KerrisdaleCap': 0.031139553275845607, '@modestproposal1': 0.11879106286860293, '@marketfolly': 0.02732633651022383, '@ActivistShorts': 0.024058851766645795, '@Carl_C_Icahn': 0.03164721998618765, '@DonutShorts': 0.0696458802866308, '@sprucepointcap': -0.010488792984492568, '@BluegrassCap': 0.16976199045555523, '@NoonSixCap': 0.17300466394923802, '@WallStCynic': 0.14702591928410613, '@GothamResearch': 0.026390218746296355, '@herbgreenberg': 0.10003633557321884, '@valuewalk': 0.10212746990206231, '@UnionSquareGrp': 0.06743840784308486, '@PlanMaestro': 0.0850020562180572, '@FatTailCapital': 0.05202709629445433, '@ShortSightedCap': 0.0265564696074275, '@footnoted': 0.06870207470534193, '@zerohedge': -0.006922439276948613, '@FundyLongShort': 0.05056174318995733, '@DumbLuckCapital': 0.05690159672741389, '@Hedge_FundGirl': 0.05662817805186319, '@PresciencePoint': 0.030439363854007476, '@DavidSchawel': 0.21529244278686596, '@fundiescapital': 0.06317290776484628, '@ActAccordingly': 0.03889094387522048, '@MicroFundy': 0.16610426796387923, '@BergenCapital': 0.05688062920492907, '@EdBorgato': 0.0818654235170247, '@RodBoydILM': 0.17374514556239726, '@activiststocks': 0.012339011637369354, '@firstadopter': 0.05356280473984827, '@WSJ': 0.030821883289433374, '@xuexishenghuo': 0.057451036340242616, '@cablecarcapital': 0.046174039732643606, '@probesreporter': 0.03669721615544143, '@GrantsPub': 0.06561497940103103, '@business': 0.0828887021430451, '@AureliusValue': 0.06575243556603157, '@davidein': 0.0, '@plainview_': 0.03637027758857528, '@TMTanalyst': 0.03173651094635736, '@manualofideas': 0.07582980069145441, '@QTRResearch': 0.03940689111615796, '@matt_levine': 0.06347547240208028, '@LibertyRPF': 0.020711924854613987, '@FCFYield': 0.01785507684783319, '@GlaucusResearch': 0.025484038067397186, '@PhilipEtienne': 0.041130917602383535, '@HedgeyeENERGY': 0.10076783347496457, '@TigreCapital': 0.008526968250961667, '@CopperfieldRscr': 0.01872657560609013, '@adoxen': 0.12519165818356368, '@mjmauboussin': 0.05370967818254875, '@bespokeinvest': 0.09529448977191486, '@schaudenfraud': 0.120737725182117, '@JohnHuber72': 0.05049813455271389, '@mark_dow': 0.19597650199309194}
"""
#for i in s_dic.values():
#   ab.append(abs(i))
min_s = min(s_dic.values())
max_v = max(dic.values())
max_r = max(temp.values())
max_pr = max(pr_dic.values())
max_y = max(y_dic.values())
max_f = max(fol_dic.values())
max_tw = max(tw_dic.values())
max_q = max(quote_dic.values())
sub_dic = copy.deepcopy(dic)
h_index = copy.deepcopy(dic)
"""
print("SEX")
print(dic)
print(max_v)
"""
print()
print("S_DIC")
print({k: v for k, v in sorted(s_dic.items(), key=lambda item: item[1], reverse=True)})
print()
print("FAV_DIC")
print()
print({k: v for k, v in sorted(fav_dic.items(), key=lambda item: item[1], reverse=True)})
print()
print("QUOTE_DIC")
print({k: v for k, v in sorted(quote_dic.items(), key=lambda item: item[1], reverse=True)})
print()
print("FOL_DIC")
print({k: v for k, v in sorted(fol_dic.items(), key=lambda item: item[1], reverse=True)})
print()
print("TW_DIC")
print({k: v for k, v in sorted(tw_dic.items(), key=lambda item: item[1], reverse=True)})
print()
print("H-INDEX")
print({k: v for k, v in sorted(temp.items(), key=lambda item: item[1], reverse=True)})
print("RT_DIC")
print({k: v for k, v in sorted(rt_dic.items(), key=lambda item: item[1], reverse=True)})

fol_dic['KerrisdaleCap'] = 40

for key in list(sub_dic):
    #상호작용 + h-index
    y_dic[key] = y_dic[key]/max_y
    sub_dic[key] = sub_dic[key]/max_v#/2+temp[key]/max_r/2
    #h_index[key] = h_index[key]/max_v*0.5+temp[key]/max_r*0.5
    #h_index[key] = h_index[key]/max_v*temp[key]/max_r
    #weight = s_dic[key]/max_s

    #아래 수식이 11명/20명, 13명/22명까지 나오는 현재 정보과학회 수식
    #h_index[key] = h_index[key]/max_v*0.4+(temp[key]/max_r*(0.3)+fol_dic[key]/max_f*0.7)*0.6
    tr = (min_s+0.1)/(s_dic[key]+0.1)
    
    if math.isnan(tr): tr = 1
        
    #h_index[key] = (tr*0.5+h_index[key]/max_v*0.5)*(1-fol_dic[key]/max_f)+temp[key]/max_r*((fol_dic[key]/max_f))
    #h_index[key] = (tr*((tw_dic[key]/max_tw))+h_index[key]/max_v*(1-tw_dic[key]/max_tw))*(1-fol_dic[key]/max_f)+temp[key]/max_r*((fol_dic[key]/max_f))
    #h_index[key] = (tr*((tw_dic[key]/max_tw))+h_index[key]/max_v*(1-tw_dic[key]/max_tw))*(0.1)+(temp[key]/max_r*0.5+fol_dic[key]*0.5)*(0.9)
    #h_index[key] = (tr*((tw_dic[key]/max_tw))+h_index[key]/max_v*(1-tw_dic[key]/max_tw))*(1-fol_dic[key]/max_f)+(temp[key]/max_r*0.5+fol_dic[key]/max_f*0.5)*(fol_dic[key]/max_f)
    #h_index[key] = (tr*0.5+h_index[key]/max_v*0.5)*(1-tw_dic[key])+(temp[key]/max_r*0.5+fol_dic[key]/max_f*0.5)*(tw_dic[key])
    
    #35명/66명
    #h_index[key] = h_index[key]/max_v*(1-tr)+(temp[key]/max_r*0.5+fol_dic[key]/max_f*0.5)*(tr)
    #36명/66명
    #h_index[key] = h_index[key]/max_v*(tw_dic[key]/max_tw)+(temp[key]/max_r*0.5+fol_dic[key]*0.5)*(1-tw_dic[key]/max_tw)
    #아래도 35명/66명
    #h_index[key] = (h_index[key]/max_v)*(1-tr)+(temp[key]/max_r*0.5+fol_dic[key]/max_f*0.5)*(tr)
    #h_index[key] = (h_index[key]/max_v)*(1-tr)+(temp[key]/max_r*0.5+fol_dic[key]/max_f*0.5)*(tr)
    
    #37명/66명
    #h_index[key] = h_index[key]/max_v*(fol_dic[key]/max_f)+temp[key]/max_r*(1-(fol_dic[key]/max_f))
    #38명/66명
    #h_index[key] = (h_index[key]/max_v)*(tw_dic[key]/max_tw)+(temp[key]/max_r*0.5+fol_dic[key]/max_f*0.5)*(1-tw_dic[key]/max_tw)
    #37명/66명
    #h_index[key] = (h_index[key]/max_v*0.5+tw_dic[key]/max_tw*0.5)*(1-tr)+(temp[key]/max_r*0.5+fol_dic[key]/max_f*0.5)*(tr)
    #42명/66명
    #h_index[key] = (temp[key]/max_r*(1-tr)+fol_dic[key]/max_f*(tr))
    #38명/66명
    #h_index[key] = tr*(tw_dic[key]/max_tw)+(temp[key]/max_r*0.5+fol_dic[key]/max_f*0.5)*(1-tw_dic[key]/max_tw)
    h_index[key] = (tr*0.8+h_index[key]/max_v*0.2)*(tw_dic[key]/max_tw)+(temp[key]/max_r*0.1+fol_dic[key]/max_f*0.9)*(1-tw_dic[key]/max_tw)

    #아래 수식도 18/25명 나옴
    #h_index[key] = (temp[key]/max_r*(0.5)+fol_dic[key]/max_f*0.5)
    #h_index[key] = (temp[key]/max_r*0.5+(fol_dic[key]/max_f)*0.5)
    #h_index[key] = h_index[key]/max_v*0.5+(temp[key]/max_r)*0.5
    
    #아래 수식이 13명/20명, 15명/22명까지 나오는 best
    #h_index[key] = h_index[key]/max_v*0.5+(temp[key]/max_r*(1-fol_dic[key]/max_f)+fol_dic[key]/max_f*pr_dic[key]/max_pr)*0.5)

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

for key in list(dic):
    try: dic[key] += pr_dic[key]/max_pr/4
    except Exception(): pass

print("AVG:",sum(dic.values())/len(dic))
print(max(dic.values()))

#print(sorted(dic.items(), key = lambda item: item[1]))

try:
    print(len(dic))
    x = np.arange(len(dic))
    plt.figure(figsize=(15, 5))
    plt.bar(x, dic.values(), width=1.0)
    plt.xticks(x, dic.keys())
    plt.show()
except Exception as e: print(e)

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
dicasd = {"TW":0, "FOL":0, "RT":0, "FAV":0, "QUOTE":0, "S":0, "H":0}
for i in ['ShortSightedCap', 'footnoted', 'zerohedge', 'FundyLongShort', 'DumbLuckCapital', 'Hedge_FundGirl', 'PresciencePoint', 'DavidSchawel', 'fundiescapital', 'ActAccordingly', 'MicroFundy', 'BergenCapital', 'EdBorgato', 'RodBoydILM', 'activiststocks', 'firstadopter', 'WSJ', 'xuexishenghuo', 'cablecarcapital', 'probesreporter', 'GrantsPub', 'business']:
    sg = 0
    print(i)
    if (min_s+0.1)/(s_dic["@"+i]+0.1)>((min_s+0.1)/(sum(s_dic.values())/len(s_dic))+0.1):
        dicasd["S"] += 1
    if fol_dic["@"+i]>(sum(fol_dic.values())/len(fol_dic)):
        dicasd["FOL"] += 1
    if tw_dic["@"+i]>(sum(tw_dic.values())/len(tw_dic)):
        dicasd["TW"] += 1
    if fav_dic["@"+i]>(sum(fav_dic.values())/len(fav_dic)):
        dicasd["FAV"] += 1
    if rt_dic["@"+i]>(sum(rt_dic.values())/len(rt_dic)):
        dicasd["RT"] += 1
    if quote_dic["@"+i]>(sum(quote_dic.values())/len(quote_dic)):
        dicasd["QUOTE"] += 1
    if temp["@"+i]>(sum(temp.values())/len(temp)):
        dicasd["H"] += 1
print(dicasd)

test = []     
print("뭐")
print(h_index)

print("HINDEX")
#print(max(h_index.values()))
#print(min(h_index.values()))
for key in h_index:
    test.append(key[0][1:])
    #test.append(key)
    a+=1
'TruthGundlach', 'UnderwaterCap'
if 'TruthGundlach' not in test:
    test.append('TruthGundlach')
if 'UnderwaterCap' not in test:
    test.append('UnderwaterCap')

print(test)
  
a=0
#20 / 31 / 17
#70up / 70under~50up / 50 under
test = []
print()

print("윤진경")
for key in y_dic:
    test.append(key[0][1:])
    #test.append(key)
    a+=1
print(test)
