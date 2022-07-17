import csv, re, numpy as np, time, sys

from nltk.corpus import stopwords
sys.path.append("C:/Multilingual-Latent-Dirichlet-Allocation-LDA-master/Multilingual-Latent-Dirichlet-Allocation-LDA-master/artifici_lda/logic")
sys.path.append("C:/Multilingual-Latent-Dirichlet-Allocation-LDA-master/Multilingual-Latent-Dirichlet-Allocation-LDA-master")
sys.path.append("C:\Multilingual-Latent-Dirichlet-Allocation-LDA-master")

from artifici_lda.lda_service import train_lda_pipeline_default

def topic(en_comments):
    f = open("C:/Mallet/stoplists/en.txt", "r", encoding="utf-8")
    EN_STOPWORDS = []
    temp = f.read().splitlines()
    
    for line in temp:
        EN_STOPWORDS.append(line.strip())
    #print(PT_STOPWORDS)
    transformed_comments, top_comments, _1_grams, _2_grams = train_lda_pipeline_default(
        en_comments,
        n_topics=6,#3개부터 쭉 늘려가보자
        stopwords=EN_STOPWORDS,
        language='english')
    
    #return (np.argmax(transformed_comments, axis=1), _1_grams)
    return transformed_comments

start = time.time()

user = dict()
lst = ['John_Hempton', 'BarbarianCap', 'muddywatersre', 'AlderLaneeggs', 'CitronResearch', 'BrattleStCap', 'KerrisdaleCap', 'modestproposal1', 'marketfolly', 'ActivistShorts', 'Carl_C_Icahn', 'DonutShorts', 'sprucepointcap', 'BluegrassCap', 'NoonSixCap', 'WallStCynic', 'GothamResearch', 'herbgreenberg', 'valuewalk', 'UnionSquareGrp', 'PlanMaestro', 'FatTailCapital', 'ShortSightedCap', 'footnoted', 'zerohedge', 'FundyLongShort', 'DumbLuckCapital', 'Hedge_FundGirl', 'PresciencePoint', 'DavidSchawel', 'fundiescapital', 'ActAccordingly', 'MicroFundy', 'BergenCapital', 'EdBorgato', 'RodBoydILM', 'activiststocks', 'firstadopter', 'WSJ', 'xuexishenghuo', 'cablecarcapital', 'probesreporter', 'GrantsPub', 'business', 'AureliusValue', 'davidein', 'plainview_', 'TMTanalyst', 'manualofideas', 'QTRResearch', 'matt_levine', 'LibertyRPF', 'FCFYield', 'GlaucusResearch', 'PhilipEtienne', 'HedgeyeENERGY', 'TigreCapital', 'CopperfieldRscr', 'adoxen', 'mjmauboussin', 'TruthGundlach', 'bespokeinvest', 'UnderwaterCap', 'schaudenfraud', 'JohnHuber72', 'mark_dow']
for i in range(len(lst)):
    lst[i] = '@'+lst[i]
    
for name in lst:
    user[name] = ""

with open('C:/fin_jy.csv', 'r', encoding="utf-8") as in_file:
    csv_reader = csv.reader(in_file, delimiter=',')
    
    for row in csv_reader:
        if row[2] in lst:
            user[row[2]] += row[4]

for key in list(user):
    tweet = user[key]
    
    if tweet=="":
        del user[key]
        continue
    tweet = tweet.replace("-\n", "")
    tweet = re.sub('@[^\s]+','',tweet)
    tweet = tweet.replace('님에게 보내는 답글', '')
    tweet = tweet.replace('\n', ' ')
    tweet = re.sub(r"\d+", " ", tweet)
    tweet = re.sub(r'http\S+', '', tweet)
    tweet = re.sub(r"[^\w+#]", " ", tweet)
    tweet = ' '.join([w for w in tweet.split() if len(w)>3])
    tweet = tweet.lower()
    user[key] = re.sub("ct", "t", tweet)

topics = topic(list(user.values()))
print(topics)
print(len(topics))
"""
print(topics[0]) #transformed_comments
print(topics[1]) #_1_grams
"""
print(time.time()-start)
