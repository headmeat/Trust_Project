from nltk.sentiment import SentimentIntensityAnalyzer
import operator, csv, re

sia = SentimentIntensityAnalyzer()

z = 0

def sentiment(row):
    score = 0
    
    stats = sia.polarity_scores(row[4])
    del stats['compound']
    sent = max(stats.items(), key=operator.itemgetter(1))[0]
        
    if sent == "neg":
        score = -1
    elif sent == "pos":
        score = 1
    
    dic[row[2]] += score
    
lst = ['John_Hempton', 'BarbarianCap', 'muddywatersre', 'AlderLaneeggs', 'CitronResearch', 'BrattleStCap', 'KerrisdaleCap', 'modestproposal1', 'marketfolly', 'ActivistShorts', 'Carl_C_Icahn', 'DonutShorts', 'sprucepointcap', 'BluegrassCap', 'NoonSixCap', 'WallStCynic', 'GothamResearch', 'herbgreenberg', 'valuewalk', 'UnionSquareGrp', 'PlanMaestro', 'FatTailCapital', 'ShortSightedCap', 'footnoted', 'zerohedge', 'FundyLongShort', 'DumbLuckCapital', 'Hedge_FundGirl', 'PresciencePoint', 'DavidSchawel', 'fundiescapital', 'ActAccordingly', 'MicroFundy', 'BergenCapital', 'EdBorgato', 'RodBoydILM', 'activiststocks', 'firstadopter', 'WSJ', 'xuexishenghuo', 'cablecarcapital', 'probesreporter', 'GrantsPub', 'business', 'AureliusValue', 'davidein', 'plainview_', 'TMTanalyst', 'manualofideas', 'QTRResearch', 'matt_levine', 'LibertyRPF', 'FCFYield', 'GlaucusResearch', 'PhilipEtienne', 'HedgeyeENERGY', 'TigreCapital', 'CopperfieldRscr', 'adoxen', 'mjmauboussin', 'TruthGundlach', 'bespokeinvest', 'UnderwaterCap', 'schaudenfraud', 'JohnHuber72', 'mark_dow']

#for i in lst:
#    print(i)

#h = ['DavidSchawel', 'BarbarianCap', 'AlderLaneeggs', 'WallStCynic', 'BluegrassCap', 'NoonSixCap', 'MicroFundy', 'mark_dow', 'modestproposal1', 'RodBoydILM', 'WSJ', 'John_Hempton', 'business', 'muddywatersre', 'valuewalk', 'herbgreenberg', 'schaudenfraud', 'PlanMaestro', 'EdBorgato', 'adoxen', 'DonutShorts', 'CitronResearch', 'HedgeyeENERGY', 'bespokeinvest', 'footnoted', 'matt_levine', 'zerohedge', 'BrattleStCap', 'UnionSquareGrp', 'FatTailCapital', 'mjmauboussin', 'firstadopter', 'AureliusValue', 'GrantsPub', 'Hedge_FundGirl', 'xuexishenghuo', 'manualofideas', 'DumbLuckCapital', 'fundiescapital', 'JohnHuber72', 'cablecarcapital', 'FundyLongShort', 'ActAccordingly', 'BergenCapital', 'Carl_C_Icahn', 'plainview_', 'KerrisdaleCap', 'marketfolly', 'QTRResearch', 'ShortSightedCap', 'probesreporter', 'TMTanalyst', 'PhilipEtienne', 'PresciencePoint', 'ActivistShorts', 'GothamResearch', 'FCFYield', 'LibertyRPF', 'GlaucusResearch', 'activiststocks', 'CopperfieldRscr', 'TigreCapital', 'davidein', 'sprucepointcap', 'TruthGundlach', 'UnderwaterCap']
tst = list({'@zerohedge': 329726, '@WSJ': 318229, '@business': 88851, '@modestproposal1': 41547, '@AlderLaneeggs': 39470, '@BluegrassCap': 19316, '@mark_dow': 17575, '@WallStCynic': 17172, '@NoonSixCap': 12279, '@BarbarianCap': 12232, '@PlanMaestro': 11925, '@DavidSchawel': 10406, '@John_Hempton': 9842, '@EdBorgato': 8663, '@valuewalk': 7991, '@DonutShorts': 6834, '@RodBoydILM': 6484, '@bespokeinvest': 6066, '@schaudenfraud': 4443, '@herbgreenberg': 3884, '@FatTailCapital': 3831, '@mjmauboussin': 3370, '@DumbLuckCapital': 2914, '@Carl_C_Icahn': 2578, '@firstadopter': 2233, '@activiststocks': 2203, '@JohnHuber72': 2073, '@plainview_': 1891, '@adoxen': 1730, '@MicroFundy': 1450, '@CitronResearch': 1408, '@matt_levine': 1397, '@FCFYield': 993, '@fundiescapital': 884, '@cablecarcapital': 879, '@xuexishenghuo': 855, '@manualofideas': 773, '@HedgeyeENERGY': 707, '@UnionSquareGrp': 700, '@ActivistShorts': 695, '@probesreporter': 672, '@AureliusValue': 641, '@sprucepointcap': 501, '@ShortSightedCap': 493, '@muddywatersre': 484, '@QTRResearch': 429, '@ActAccordingly': 413, '@GrantsPub': 401, '@footnoted': 378, '@marketfolly': 367, '@BergenCapital': 356, '@KerrisdaleCap': 305, '@BrattleStCap': 302, '@PresciencePoint': 285, '@LibertyRPF': 284, '@TMTanalyst': 260, '@Hedge_FundGirl': 252, '@FundyLongShort': 160, '@PhilipEtienne': 129, '@GlaucusResearch': 124, '@GothamResearch': 100, '@CopperfieldRscr': 59, '@davidein': 5, '@TigreCapital': 4, '@TruthGundlach': 0, '@UnderwaterCap': 0})
h = ['BarbarianCap', 'zerohedge', 'WallStCynic', 'modestproposal1', 'muddywatersre', 'WSJ', 'marketfolly', 'AlderLaneeggs', 'ShortSightedCap', 'business', 'KerrisdaleCap', 'BluegrassCap', 'matt_levine', 'John_Hempton', 'Carl_C_Icahn', 'DavidSchawel', 'MicroFundy', 'FatTailCapital', 'firstadopter', 'CitronResearch', 'sprucepointcap', 'BrattleStCap', 'valuewalk', 'ActAccordingly', 'NoonSixCap', 'footnoted', 'DonutShorts', 'herbgreenberg', 'ActivistShorts', 'EdBorgato', 'Hedge_FundGirl', 'activiststocks', 'PlanMaestro', 'xuexishenghuo', 'UnionSquareGrp', 'GothamResearch', 'cablecarcapital', 'TMTanalyst', 'mark_dow', 'FundyLongShort', 'RodBoydILM', 'DumbLuckCapital', 'mjmauboussin', 'AureliusValue', 'FCFYield', 'GrantsPub', 'LibertyRPF', 'fundiescapital', 'JohnHuber72', 'PresciencePoint', 'schaudenfraud', 'davidein', 'plainview_', 'bespokeinvest', 'probesreporter', 'HedgeyeENERGY', 'manualofideas', 'PhilipEtienne', 'BergenCapital', 'TigreCapital', 'adoxen', 'QTRResearch', 'CopperfieldRscr', 'GlaucusResearch', 'TruthGundlach', 'UnderwaterCap']
y = ['Carl_C_Icahn', 'WSJ', 'CitronResearch', 'mjmauboussin', 'BrattleStCap', 'zerohedge', 'matt_levine', 'TigreCapital', 'business', 'modestproposal1', 'EdBorgato', 'JohnHuber72', 'KerrisdaleCap', 'davidein', 'GrantsPub', 'FCFYield', 'FatTailCapital', 'NoonSixCap', 'BluegrassCap', 'muddywatersre', 'QTRResearch', 'AureliusValue', 'LibertyRPF', 'AlderLaneeggs', 'PlanMaestro', 'GothamResearch', 'BarbarianCap', 'cablecarcapital', 'herbgreenberg', 'WallStCynic', 'mark_dow', 'BergenCapital', 'marketfolly', 'bespokeinvest', 'schaudenfraud', 'ShortSightedCap', 'DavidSchawel', 'GlaucusResearch', 'HedgeyeENERGY', 'manualofideas', 'firstadopter', 'ActivistShorts', 'John_Hempton', 'DonutShorts', 'valuewalk', 'TMTanalyst', 'CopperfieldRscr', 'Hedge_FundGirl', 'PhilipEtienne', 'PresciencePoint', 'fundiescapital', 'RodBoydILM', 'plainview_', 'sprucepointcap', 'UnionSquareGrp', 'xuexishenghuo', 'footnoted', 'DumbLuckCapital', 'ActAccordingly', 'adoxen', 'probesreporter', 'FundyLongShort', 'MicroFundy', 'activiststocks', 'TruthGundlach', 'UnderwaterCap']
dic = dict()
#print(lst[44:66])
"""
for i in range(len(lst)):
    lst[i] = "@"+lst[i]
"""

high = lst[:22]
med = lst[22:44]
low = lst[44:]



q = len(h)
#print(lst[22:44])
a = 0
#print(q)
q = 8
k = 8
r=0
lst3 = lst[:22]
h3 = h[:22]
y3 = y[:22]
tst3 = tst[:22]
print(":22")

for i in tst3:
    if i[1:] in lst3:
        r+=1
print("R",r)
temp = []
t = 22

""" #accuracy and recall for plotting graph
for i in range(0, 66):
    a = 0
    b = 0
    c = 0
    print("i:",i)
    for j in range(0, i+1):
        if j<=16 and h[j] in high: a+=1
        if j>16 and j<=49 and h[j] in med: 
            #b+=1
            #t=44
            pass
        if j>49 and h[j] in low: 
            c+=1
            t=66
    print(a+b+c)
    temp.append((a+b+c)/(t))
print(temp)
"""

for i in y3:
    if i in lst3: a+=1
#print(a)
a=0

for i in h3:
    if i in lst3: a+=1
print(a)
a=0
for i in y3:
    if i in lst3: a+=1
print(a)

print("22:44")
lst3 = lst[22:44]
h3 = h[22:44]
y3=y[22:44]
tst3 = tst[22:44]

a = 0
r=0
for i in tst3:
    if i[1:] in lst3:
        r+=1
#print("R",r)

for i in h3:
    if i in lst3: a+=1
print(a)
a=0
for i in y3:
    if i in lst3: a+=1
print(a)
a=0

print("22:44")
lst3 = lst[44:]
h3 = h[44:]
y3=y[44:]

for i in h3:
    if i in lst3: a+=1
print(a)
a=0

for i in y3:
    if i in lst3: a+=1
print(a)
a=0

"""
with open('C:/Users/headm/OneDrive/Desktop/fin/fin_jy.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    
    for row in csv_reader:
        z+=1
        if row[2] in dic:
            sentiment(row)

ab = []

for i in dic.values():
    ab.append(abs(i))

mx = max(ab)

for i in list(dic):
    dic[i] = dic[i] / mx

print(dic)
"""
