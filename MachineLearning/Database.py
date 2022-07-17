import sys, json
from sex import get_user_information, main_test, main_test2
from itertools import chain
sys.path.append('C:/Users/headm/OneDrive/Desktop')
sys.path.append('C:/Users/headm/OneDrive/Desktop/Scweet-master/Scweet-master/Scweet')
from scweet import scrap
from user import get_user_information, get_users_following, get_users_followers
from neo4j import GraphDatabase

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def getIds(lst):
    #lst = lst.replace('\'', r'\"').replace('\n', r'''\n''')
    ids = []
    x = json.loads(lst)

    for i in range(len(x)):
        ids.append(x[i]["id"])
        
    return ids

def getNames(lst):
    #lst = lst.replace('\'', r'\"').replace('\n', r'''\n''')
    names = []
    x = json.loads(lst)

    for i in range(len(x)):
        names.append(x[i]["username"])
        
    return names

class HelloWorldExample:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
        
    @staticmethod
    def insertNode(tx, username):
        query = "MERGE (n:Node {username:\""+username+"\"}) RETURN n"
        tx.run(query)
    
    @staticmethod
    def getFollowers(tx, t_ids):
        dic = dict()
        for t_id in t_ids:
            query = "MATCH ()-[r]->(n:Node) WHERE n.t_id="+str(t_id)+" RETURN COUNT(r)"
            dic[t_id] = tx.run(query).values()[0][0]
        return dic
    
    @staticmethod
    def insertRel(tx, u1, u2, weight):
        if weight == -1:
            query = "MATCH (a:Node {id:"+u1+"}) MATCH (b:Node {id:"+u2+"}) MERGE (a)-[:FOLLOWS]->(b)"
        elif weight>0:
            query = "MATCH (a:Node),(b:Node) WHERE a.id="+str(u1)+" AND b.id="+str(u2)+" CREATE (a)-[r:FOLLOWS{followers:"+str(weight)+"}]->(b) RETURN r"
        tx.run(query)
    
    @staticmethod
    def t_id2id(tx, t_ids):
        ids = []
        act = []
        for t_id in t_ids:
            query = "MATCH (n:Node) WHERE n.t_id="+str(t_id)+" RETURN n.id"
            try: 
                ids.append(tx.run(query).values()[0][0])
                act.append(t_id)
            except Exception: pass
        print(act)
        return ids
    
    @staticmethod
    def prTopic(tx, topic):
        res = tx.run("CALL gds.graph.exists(\'topicGraph"+str(topic)+"\') YIELD exists;")
        
        query = "CALL gds.graph.create.cypher(\'topicGraph"+str(topic)+"\', 'MATCH (n:Node { topic: "+str(topic)+" }) RETURN id(n) as id\', \'MATCH (a:Node)-[r:FOLLOWS]->(b:Node) WHERE a.topic="+str(topic)+" AND b.topic="+str(topic)+" RETURN id(a) as source, id(b) as target\');"
        query2 = "CALL gds.pageRank.stream(\'topicGraph"+str(topic)+"\') YIELD nodeId, score RETURN gds.util.asNode(nodeId).t_id AS t_id, score ORDER BY score DESC, t_id ASC"

        if not res: tx.run(query)
        result = tx.run(query2)
            
        return result.values()
    
    #불필요(테스트 X)
    @staticmethod
    def checkRel(tx, u1, u2):
        query = "MATCH  (a:Node {username: \""+u1+"\"}), (b:Node {username: \""+u2+"\"}) RETURN EXISTS( (a)-[:FOLLOWS]->(b) )"
        result = tx.run(query)
        return result
    
    @staticmethod
    def getNodes(tx):
        result = []
        #result = tx.run("MATCH (n:Node) RETURN n.t_id")
        values = tx.run("MATCH (n:Person) RETURN n.name")
        for i in values: result.append(i[0])
        return result
    
    @staticmethod
    def getTopicNodes(tx, topic):
        query = "MATCH (n:Node) WHERE n.topic="+str(topic)+" RETURN n.t_id"
        result = tx.run(query)
        return result.values()
    
    @staticmethod
    def pageRank(tx):
        res = tx.run("CALL gds.graph.exists(\'TwitterGraph\') YIELD exists;")
        if not res.values()[0][0]: tx.run("CALL gds.graph.create('TwitterGraph', 'Node', 'FOLLOWS')")
        
        result = tx.run("CALL gds.pageRank.stream('TwitterGraph') YIELD nodeId, score RETURN gds.util.asNode(nodeId) AS name, score ORDER BY score DESC, name ASC")
        return result.values() #[0], [1], ... access
    
    @staticmethod
    def setTopics(tx, t_id, topic):
        query = "MATCH (n:Node {t_id: "+t_id+"}) SET n.topic ="+str(topic)
        tx.run(query)

t = ""

pr_dic = dict()

def getTopic(topic):
    with GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "1234")) as driver:
        with driver.session() as session:
            sex = []
            if topic==-1: 
                values = session.read_transaction(HelloWorldExample.getNodes)
                for i in values:
                    sex.append(i[0])
            else:
                #values = session.read_transaction(HelloWorldExample.pageRank)
                values = session.read_transaction(HelloWorldExample.getTopicNodes, topic)
                for i in values:
                    sex.append(i[0])
                    
            return sex

def id2Name(ids):
    chunk_list = list(chunks(ids, 100))
    names_list = []
    names = []

    for i in range(len(chunk_list)):
        names_list.append(getNames(json.dumps(main_test(','.join(map(str, chunk_list[i]))))))
    for lst in names_list:
        for name in lst:
            names.append(name)
    return names

def name2Id(names):
    chunk_list = list(chunks(names, 100))
    ids_list = []
    ids = []
    
    for i in range(len(chunk_list)):
        ids_list.append(getIds(json.dumps(main_test2(','.join(map(str, chunk_list[i]))))))
        print(ids_list)
    for lst in ids_list:
        for id_ in lst:
            ids.append(id_)
    return ids

#print(getNames(json.dumps(main_test('49808900'))))

#print(getNames(json.dumps(main_test2('bolanascostas,esportenews,CBF_Futebol'))))
"""
        #pr_dic = sorted(pr_dic.items(), key = lambda item: item[1])
        print(type(pr_dic))

        values = session.read_transaction(HelloWorldExample.getNodes)

        flat_list = list(chain.from_iterable(values))
        
        chunk_list = list(chunks(flat_list, 100))
        
        for c_list in chunk_list:
            print(getNames(json.dumps(main_test(','.join(map(str, c_list))))))

#print(getNames(json.dumps(main_test("19058681"))))

flat_list = ['bolanascostas', 'esportenews', 'CBF_Futebol', 'revistasuper', 'CantadasCharlie', 'SporTV', 'renato_gaucho', 'multishow', 'BrazilWorldTV', 'loveletdie', 'sabrina_sato', 'daniredetv', 'geglobo', 'TO_DE_OLHO', 'sitevagalume', 'MixtapeOficial', 'hevo84', 'CassesOficial', 'jorgeiggor', 'vitorsergio', 'richstyles', 'espn', 'weboxygen', 'pcfromzero', 'marymagdalan', 'StarzUncut',  'SteveNash', 'yelyahwilliams', 'marca', 'ItsMoneybags', 'TextArtPrint', 'serenawilliams', 'justdemi', 'NBA', 'ashleytisdale', 'PerezHilton', 'ladygaga', 'jtimberlake', 'taylorswift13', 'MandyJiroux', 'mitchelmusso', 'billyraycyrus', 'EmilyOsment', 'BrandiCyrus', 'jonasbrothers', 'ddlovato', 'pamfoundation', 'bigeyeonsports', 'montanhadaniel', 'bixajacare', 'fabiannesangalo', '_Mikael', 'halonferreira', 'oidiversao', 'Maudox', 'madamemim0', 'GreenpeaceBR', 'JOSI_F', 'mtvmanaus', 'MallandroSergio', 'menDigodigO', 'DanyLicinha', 'luanaviessa', 'mlauradevides', 'babiwinchester', 'cleversong', 'lucasparaujo', 'Alishow', 'leeandroalemao', 'oliferraro', 'RodrigoTakasaki', 'vanfsiqueira', 'portalyoba', 'vinil_oficial', 'PatrickMachado0', 'brunozarb', 'aless_nichols', 'Viniderossi', 'elvesnaves', 'lemefelipe7', 'brandaosandes', 'Thi_Valle', 'marciolimasej', 'lopeskatiane', 'ricardosredoja', 'darlanvet', 'zeaugustorocha', 'MrDude81', 'Rherdan', 'Bittnick', 'AFSauer', 'renatosorin', 'michellepaulina', 'Marcio_Shadows', 'kachromiec', 'Tulio_andrade', 'William_Castro', 'chescofd_', 'DRIMONTS', 'ltrielli', 'afonsonem', 'BrunoJabs', 'programageracao', 'felipesinoble', 'KleberAugusto1', 'eduka', 'claudiocult', 'pp_luiz', 'AdmHelga', 'denisveneno', 'almeida_bruno', 'davidsilva10', 'AninhaGomez05', 'natyzinhas', 'djalexbaxter', 'david_cec', 'Niiiiiine', 'susoares', 'clauloria', 'Luane_M', 'KedaoRTM', 'roger_vanutt', 'FraciscoMedeir', 'fredhetori', 'minhafilhaa', 'RafsPsh', 'gabrielmafia', 'vetfiscal', 'HerreraUck', 'cheshirenats', 'rafinhabastos', 'jornalhoje', 'srbarbosa', 'LucianoHuck', 'Junior_Lima', 'marcosmion', 'TheoBecker8', 'descargaoficial', 'josecordova', 'grandepremio', 'caldeiraodohuck', 'decheers', 'TaniaOliveira', 'SabrinaSato', 'rodrigovesgo', 'MarcoLuque', 'SandyLeah', 'NelsonPiquet', 'rubarrichello', 'TonyKanaan', 'emicida', 'SnoopDogg', 'Tyrese', 'iamwill', 'Diddy', 'souljaboy', 'britneyspears', 'DSRika', 'siteEgo', 'joseserra_', 'angelicaksy', 'astridfontenell', 'FePaesLeme', 'noelylima', 'renanmendis', 'eduardoal', 'marisaorth', 'ifiorentino', 'nato157', 'Tessalia', 'jimjonescapo', 'SHAQ', 'showdavida', 'LIFE', 'iTunesTrailers', 'alyankovic', 'nytimes', 'BITech', 'BBCClick', 'AmyJoMartin', 'GStephanopoulos', 'gtdguy', 'threadless', 'aplusk', 'om', 'JessicaSimpson', 'RyanSeacrest', 'ashleesimpson', 'dannymasterson', 'KikoKLB', 'vinevieira', 'rafaaguileia', 'Hugo_Resende', 'djdanielsecco', 'jamesjl', 'lini', 'Xpock', 'jbanguela', 'twittatriz', 'rodriguesnelson', 'betosilva', 'DaniloGentili', 'lobaoeletrico', 'programapanico', 'minadosgames', 'lapena', 'nando_reis', 'oceara', 'Danibey', 'meligeni', 'BSenna', 'globoesporteSP', 'paloza', 'yokoono', 'BarackObama', 'jimmyfallon', 'Oprah', 'neytude', 'dmalevato', 'MarceloTas', 'OscarFilho', 'cqc__', 'cortezrafa', 'andreolifelipe', 'BandJornalismo', 'na_halia', 'BrunoSwell', 'lucastex', 'chelseahandler', 'OrlandoMagic', 'thalytazenatti', 'rpaul81', 'ellen_btg', 'naosalvo', 'CGalochas', 'MariMoon', 'tarsocadore', 'santoEvandro', 'TbirdRadioShow', 'amadafoca', 'FrancysH', 'RSabrina', 'Lii_Caroline96', 'RaphaelNeumann', 'TomFletcher', 'mcflyharry', 'McFLYAddiction', 'DougiePoynter', 'itsDannyJones', 'giselewalter', 'FrankieBridge', 'mcflymusic', 'MrsGiFletcher', 'Starbucks', 'liamgallagher', 'TheEllenShow', 'katyperry', 'giifraanca', 'hburlamaqui', 'MaozinhaMoretti', 'cartolafc', 'cdieckmann', 'gilbertogil', 'ivetesangalo', 'PretaGil', 'brunogagliasso', 'isabeloliveiraa', 'Pitty', 'TomCavalcante1', 'vluxemburgo', 'anapaulavuoto', 'DjAlineRocha', 'BSurfistinha', 'SE_Palmeiras', 'chibimartins', 'cella_couto', 'brubssbeatriz', 'Playboy', 'amazonmusic', 'thelittleidiot', 'sockington', 'CoryBooker', 'DellOutlet', 'lancearmstrong', 'stevenbjohnson', 'JerryBrownGov', 'anamariecox', 'Nightline', 'noushskaugen', 'algore', 'petewentz', 'enews', 'NFL', 'angleesoup', 'Lakers', 'joesebok', 'heidimontag', '_Renatinha', 'renatinha_s', 'laisdinhani', 'furlanluciana', 'MayraQuitero', 'camila_klitzke', 'MTVBrasil', '50cent', 'manomenezes', 'sorayadarabi', 'digg', 'davidgregory', 'MrKRudd', 'CMEGroup', 'CBSNews', 'LennyKravitz', 'luiztsilva', 'alysontl', 'wakawakawe', 'DarthVader', 'eujessicaflores', 'MTV', 'Google', 'Twitter', 'Pink', 'celsoportioli', 'sigaPalmeiras', 'conka', 'Enxaquecakid', 'MarceloAvestruz', 'frestadajanela', 'ratinhodosbt', 'oficialkellykey', 'good_witchlove', 'LucianaGimenez', 'robmasic', '_INRICRISTO', 'dani_luque', 'BrunoCCardoso', 'clubemondoverde', 'Palmeiras', 'PalmeirasNOW', 'locomotives', 'stugio', 'DarleneZschech', 'droff', 'vitorbirner', 'RobertoLJustus', 'Fake_Pasquale', 'walterlongo', 'jornaldacbn', 'supergospel', 'virtual_gospel', 'abduzeedo', 'caseycorum', 'crowdermusic', 'Delirious', 'leelandmooring', 'MUTEMATH',
'vickybeeching', 'michaelwsmith', 'christomlin', 'leelandofficial', 'amygrant', 'MartinSmithTV', 'CompassionArt', 'matt_redman', 'timhughes77', 'Daniel_mendes20', 'andressveloso', 'dotpcorp', 'joseagripino', 'karinafalzoni', 'YouTobaTV', 'BonecaoDoPosto', 'tec_EXAME', 'Cardoso', 'luizagomes', 'OCriador', 'netmovies', 'pedrojovelli', 'fikdik_net', 'blogueador', 'paulostudio2002', 'RevistaEpoca', 'g1', 'Tuinter_AVISOS', 'Legendarios', 'AltaFidelidade0', 'dizplaynet', 'StefanyCury', 'brdicas', 'pegueopomboagr', 'cakedalilih', 'ajcampos01', 'sitedomau', 'AlanBbk', 'pesquisas_real', 'tensoblog', 'KiabboO', 'marceloleitner', 'TurmaDoBolovo', 'ROC4LIFE', 'biaurel', 'ComeuTudinho', 'humbertomilk', 'noticiastimao', 'leilalopes', 'AlfinetePeixoto', 'Eliana', 'RedeGlobo', 'ANAMARIABRAGA', 'SProdutividade', 'metropolitanafm', 'oficial89fm', 'smnhzw', 'WanessaRecife', 'Corinthians', 'LaisRoncoli', 'fabiofdias', 'rockfeminino', 'comediamm', 'fabiochaves', 'WelderMM', 'segueotorto', 'orafaoliver', 'barbixas', 'guiavegano', 'CNN', 'lucasrogenski', 'santistaroxo', 'kleberD', 'marcioballas', 'casseta', 'brunastuta', 'alexpaim', 'alison', 'AlisonFreed', 'johnlegend', 'paulfeig', 'nprscottsimon', 'Padmasree', 'drdrew', 'UKCoachCalipari', 'Supbruh419', 'AlisonKrauss', 'mvbill',
'centraldorap', 'Eminem', 'Lloydbanks', 'thisis50', 'TonyYayo', 'fatjoe', 'smoss', 'jarule', 'wyclef', 'alefegoncalves', 'reegin', 'CarolinaaSilva', 'Tomateraz', 'gaabfernandes', 'AnaSilvaSantos', 'nataliamafemo', 'FehPrado', 'HiigorCioffi', 'Juxshadow', 'DiiSantos', 'escrevegabi', 'rafaelabou', 'ARTESANALBAR', 'liiramos', 'miguells', 'isa_medeiros', 'Larry_Amaral', 'millionaire8', 'liiperas', 'isabatista', 'nakedz', 'vanguardamix', 'beccabernardes', 'renanmachuca', 'maestrobilly', 'ospaparazzi', 'BispoMacedo', 'WalcyrCarrasco', 'cissa_guimaraes', 'SergioMarone', 'sheronmenezzes', 'cacarosset', 'ahickmann', 'CesarFilho', 'SBTonline', 'jorgearagao', 'm_camelo', 'willian_james', 'Iambabixavier', 'Ta_ais', 'descargamtv', 'geerocha', 'nxzerooficial', 'twithirteen', 'Caco_Grandino', 'DiFerrero', 'daniel_weksler', 'FiRicardo', 'renansdc', 'CountingCrows', 'GMA', 'dooce', 'pitchfork', 'imogenheap', 'ABC', 'joelmchale', 'richardpbacon',  'alinemariano']

names = ['ActivistShorts', 'Carl_C_Icahn', 'DonutShorts', 'sprucepointcap', 'BluegrassCap', 'NoonSixCap', 'WallStCynic', 'GothamResearch', 'herbgreenberg', 'valuewalk', 'UnionSquareGrp']

chunk_list = list(chunks(flat_list, 100))

for i in range(len(chunk_list)):
    names = getNames(json.dumps(main_test2(','.join(map(str, chunk_list[i])))))
    print(i,":",names)


for i in range(len(names)):
    print(names)
    length = len(names)
    i = 0
    while i<length:
        dlfma = names[i]
        print("Scraping for user:",names[i])
        try:
            scrap(start_date="2017-01-01", max_date="2017-12-31", from_account = names[i],interval=1, headless=True, hashtag=None).to_csv('finance.csv',mode='a',encoding='utf-8-sig')#previously creep1.csv
            i+=1
        except Exception: 
            print("Stopped at:",dlfma)

#values = [[18107817, 29762381, 10907922, 7116712, 17486232, 14932565, 18407780, 5389772, 15524519, 14650624, 24696064, 23323423, 15349746, 20629301, 24232174, 11991572, 25090102, 17043347, 14143813, 28634856, 15111691, 15067571, 31041288, 27331718, 34286925]]
#values = [[15524519, 14650624, 24696064, 23323423, 15349746, 20629301, 24232174, 11991572, 25090102, 17043347, 14143813, 28634856, 15111691, 15067571, 31041288, 27331718, 34286925]]

#values = [[14143374, 51617148, 21141277, 36141745, 10226052, 12170712, 17675497, 38785016, 49794607, 30757125, 40025449, 14652106, 23133853, 12206232, 15742703, 39045317, 43101221, 27800328, 26535875, 38368266, 14590132, 28720091, 20992262, 33526156, 46372480, 17746550, 14210460, 18107817, 29762381, 10907922, 7116712, 17486232, 14932565, 18407780, 5389772, 15524519, 14650624, 24696064, 23323423, 15349746, 20629301, 24232174, 11991572, 25090102, 17043347, 14143813, 28634856, 15111691, 15067571, 31041288, 27331718, 34286925]]
#values = [[44169649, 9800452, 40661492, 26842720, 24019684, 28667734, 36798102, 29777955, 17538529, 23068777, 9775262, 19353490, 17040070, 27957153, 41846671, 28184388, 21093278, 27874497, 21084998, 26476878, 27388187, 40053390, 45821155, 28339071, 49453058, 16799548, 24601862, 24873979]]
#values = [['9018312', '14946999', '40423822', '30367771', '22644063', '52816227', '39970966', '37002862', '37229305', '20854191', '28838048', '32385762', '21318259', '28445357', '28845997', '29864894', '22668242', '46466740', '23460700', '30973', '21181713', '15846407', '21447363', '45829228', '53410345', '40947374', '10075202', '27482113', '14907774', '14502789', '35693211', '41036546', '45077958', '24989174', '48440176', '50654818', '38995168', '49808900', '28904594', '35319602', '31058584', '30060518', '39862015', '15677036', '14740219', '14464766', '1468401', '15808765', '5688592', '16727535', 
values = [['2182641', '19418459', '11640472', '19740592', '14049880', '17220934', '16264006', '2883841', '19426551', '24458677', '20346956', '25038085', '23396761', '16153772', '14728147', '46913600']]

lst1 = ['bolanascostas', 'esportenews', 'CBF_Futebol', 'revistasuper', 'CantadasCharlie', 'SporTV', 'renato_gaucho', 'multishow', 'BrazilWorldTV', 'loveletdie', 'sabrina_sato', 'daniredetv', 'geglobo', 'TO_DE_OLHO', 'sitevagalume', 'MixtapeOficial', 'hevo84', 'CassesOficial', 'jorgeiggor', 'vitorsergio', 'richstyles', 'espn', 'weboxygen', 'pcfromzero', 'marymagdalan', 'StarzUncut',  'SteveNash', 'yelyahwilliams', 'marca', 'ItsMoneybags', 'TextArtPrint', 'serenawilliams', 'justdemi', 'NBA', 'ashleytisdale', 'PerezHilton', 'ladygaga', 'jtimberlake', 'taylorswift13', 'MandyJiroux', 'mitchelmusso', 'billyraycyrus', 'EmilyOsment', 'BrandiCyrus', 'jonasbrothers', 'ddlovato', 'pamfoundation', 'bigeyeonsports', 'montanhadaniel', 'bixajacare', 'fabiannesangalo', '_Mikael', 'halonferreira', 'oidiversao', 'Maudox', 'madamemim0', 'GreenpeaceBR', 'JOSI_F', 'mtvmanaus', 'MallandroSergio', 'menDigodigO', 'DanyLicinha', 'luanaviessa', 'mlauradevides', 'babiwinchester', 'cleversong', 'lucasparaujo', 'Alishow', 'leeandroalemao', 'oliferraro', 'RodrigoTakasaki', 'vanfsiqueira', 'portalyoba', 'vinil_oficial', 'PatrickMachado0', 'brunozarb', 'aless_nichols', 'Viniderossi', 'elvesnaves', 'lemefelipe7', 'brandaosandes', 'Thi_Valle', 'marciolimasej', 'lopeskatiane', 'ricardosredoja', 'darlanvet', 'zeaugustorocha', 'MrDude81', 'Rherdan', 'Bittnick', 'AFSauer', 'renatosorin', 'michellepaulina', 'Marcio_Shadows', 'kachromiec', 'Tulio_andrade', 'William_Castro', 'chescofd_', 'DRIMONTS', 'ltrielli', 'afonsonem', 'BrunoJabs', 'programageracao', 'felipesinoble', 'KleberAugusto1', 'eduka', 'claudiocult', 'pp_luiz', 'AdmHelga', 'denisveneno', 'almeida_bruno', 'davidsilva10', 'AninhaGomez05', 'natyzinhas', 'djalexbaxter', 'david_cec', 'Niiiiiine', 'susoares', 'clauloria', 'Luane_M', 'KedaoRTM', 'roger_vanutt', 'FraciscoMedeir', 'fredhetori', 'minhafilhaa', 'RafsPsh', 'gabrielmafia', 'vetfiscal', 'HerreraUck', 'cheshirenats', 'rafinhabastos', 'jornalhoje', 'srbarbosa', 'LucianoHuck', 'Junior_Lima', 'marcosmion', 'TheoBecker8', 'descargaoficial', 'josecordova', 'grandepremio', 'caldeiraodohuck', 'decheers', 'TaniaOliveira', 'SabrinaSato', 'rodrigovesgo', 'MarcoLuque', 'SandyLeah', 'NelsonPiquet', 'rubarrichello', 'TonyKanaan', 'emicida', 'SnoopDogg', 'Tyrese', 'iamwill', 'Diddy', 'souljaboy', 'britneyspears', 'DSRika', 'siteEgo', 'joseserra_', 'angelicaksy', 'astridfontenell', 'FePaesLeme', 'noelylima', 'renanmendis', 'eduardoal', 'marisaorth', 'ifiorentino', 'nato157', 'Tessalia', 'jimjonescapo', 'SHAQ', 'showdavida', 'LIFE', 'iTunesTrailers', 'alyankovic', 'nytimes', 'BITech', 'BBCClick', 'AmyJoMartin', 'GStephanopoulos', 'gtdguy', 'threadless', 'aplusk', 'om', 'JessicaSimpson', 'RyanSeacrest', 'ashleesimpson', 'dannymasterson', 'KikoKLB', 'vinevieira', 'rafaaguileia', 'Hugo_Resende', 'djdanielsecco', 'jamesjl', 'lini', 'Xpock', 'jbanguela', 'twittatriz', 'rodriguesnelson', 'betosilva', 'DaniloGentili', 'lobaoeletrico', 'programapanico', 'minadosgames', 'lapena', 'nando_reis', 'oceara', 'Danibey', 'meligeni', 'BSenna', 'globoesporteSP', 'paloza', 'yokoono', 'BarackObama', 'jimmyfallon', 'Oprah', 'neytude', 'dmalevato', 'MarceloTas', 'OscarFilho', 'cqc__', 'cortezrafa', 'andreolifelipe', 'BandJornalismo', 'na_halia', 'BrunoSwell', 'lucastex', 'chelseahandler', 'OrlandoMagic', 'thalytazenatti', 'rpaul81', 'ellen_btg', 'naosalvo', 'CGalochas', 'MariMoon', 'tarsocadore', 'santoEvandro', 'TbirdRadioShow', 'amadafoca', 'FrancysH', 'RSabrina', 'Lii_Caroline96', 'RaphaelNeumann', 'TomFletcher', 'mcflyharry', 'McFLYAddiction', 'DougiePoynter', 'itsDannyJones', 'giselewalter', 'FrankieBridge', 'mcflymusic', 'MrsGiFletcher', 'Starbucks', 'liamgallagher', 'TheEllenShow', 'katyperry', 'giifraanca', 'hburlamaqui', 'MaozinhaMoretti', 'cartolafc', 'cdieckmann', 'gilbertogil', 'ivetesangalo', 'PretaGil', 'brunogagliasso', 'isabeloliveiraa', 'Pitty', 'TomCavalcante1', 'vluxemburgo', 'anapaulavuoto', 'DjAlineRocha', 'BSurfistinha', 'SE_Palmeiras', 'chibimartins', 'cella_couto', 'brubssbeatriz', 'Playboy', 'amazonmusic', 'thelittleidiot', 'sockington', 'CoryBooker', 'DellOutlet', 'lancearmstrong', 'stevenbjohnson', 'JerryBrownGov', 'anamariecox', 'Nightline', 'noushskaugen', 'algore', 'petewentz', 'enews', 'NFL', 'angleesoup', 'Lakers', 'joesebok', 'heidimontag', '_Renatinha', 'renatinha_s', 'laisdinhani', 'furlanluciana', 'MayraQuitero', 'camila_klitzke', 'MTVBrasil', '50cent', 'manomenezes', 'sorayadarabi', 'digg', 'davidgregory', 'MrKRudd', 'CMEGroup', 'CBSNews', 'LennyKravitz', 'luiztsilva', 'alysontl', 'wakawakawe', 'DarthVader', 'eujessicaflores', 'MTV', 'Google', 'Twitter', 'Pink', 'celsoportioli', 'sigaPalmeiras', 'conka', 'Enxaquecakid', 'MarceloAvestruz', 'frestadajanela', 'ratinhodosbt', 'oficialkellykey', 'good_witchlove', 'LucianaGimenez', 'robmasic', '_INRICRISTO', 'dani_luque', 'BrunoCCardoso', 'clubemondoverde', 'Palmeiras', 'PalmeirasNOW', 'locomotives', 'stugio', 'DarleneZschech', 'droff', 'vitorbirner', 'RobertoLJustus', 'Fake_Pasquale', 'walterlongo', 'jornaldacbn', 'supergospel', 'virtual_gospel', 'abduzeedo', 'caseycorum', 'crowdermusic', 'Delirious', 'leelandmooring', 'MUTEMATH',
'vickybeeching', 'michaelwsmith', 'christomlin', 'leelandofficial', 'amygrant', 'MartinSmithTV', 'CompassionArt', 'matt_redman', 'timhughes77', 'Daniel_mendes20', 'andressveloso', 'dotpcorp', 'joseagripino', 'karinafalzoni', 'YouTobaTV', 'BonecaoDoPosto', 'tec_EXAME', 'Cardoso', 'luizagomes', 'OCriador', 'netmovies', 'pedrojovelli', 'fikdik_net', 'blogueador', 'paulostudio2002', 'RevistaEpoca', 'g1', 'Tuinter_AVISOS', 'Legendarios', 'AltaFidelidade0', 'dizplaynet', 'StefanyCury', 'brdicas', 'pegueopomboagr', 'cakedalilih', 'ajcampos01', 'sitedomau', 'AlanBbk', 'pesquisas_real', 'tensoblog', 'KiabboO', 'marceloleitner', 'TurmaDoBolovo', 'ROC4LIFE', 'biaurel', 'ComeuTudinho', 'humbertomilk', 'noticiastimao', 'leilalopes', 'AlfinetePeixoto', 'Eliana', 'RedeGlobo', 'ANAMARIABRAGA', 'SProdutividade', 'metropolitanafm', 'oficial89fm', 'smnhzw', 'WanessaRecife', 'Corinthians', 'LaisRoncoli', 'fabiofdias', 'rockfeminino', 'comediamm', 'fabiochaves', 'WelderMM', 'segueotorto', 'orafaoliver', 'barbixas', 'guiavegano', 'CNN', 'lucasrogenski', 'santistaroxo', 'kleberD', 'marcioballas', 'casseta', 'brunastuta', 'alexpaim', 'alison', 'AlisonFreed', 'johnlegend', 'paulfeig', 'nprscottsimon', 'Padmasree', 'drdrew', 'UKCoachCalipari', 'Supbruh419', 'AlisonKrauss', 'mvbill',
'centraldorap', 'Eminem', 'Lloydbanks', 'thisis50', 'TonyYayo', 'fatjoe', 'smoss', 'jarule', 'wyclef', 'alefegoncalves', 'reegin', 'CarolinaaSilva', 'Tomateraz', 'gaabfernandes', 'AnaSilvaSantos', 'nataliamafemo', 'FehPrado', 'HiigorCioffi', 'Juxshadow', 'DiiSantos', 'escrevegabi', 'rafaelabou', 'ARTESANALBAR', 'liiramos', 'miguells', 'isa_medeiros', 'Larry_Amaral', 'millionaire8', 'liiperas', 'isabatista', 'nakedz', 'vanguardamix', 'beccabernardes', 'renanmachuca', 'maestrobilly', 'ospaparazzi', 'BispoMacedo', 'WalcyrCarrasco', 'cissa_guimaraes', 'SergioMarone', 'sheronmenezzes', 'cacarosset', 'ahickmann', 'CesarFilho', 'SBTonline', 'jorgearagao', 'm_camelo', 'willian_james', 'Iambabixavier', 'Ta_ais', 'descargamtv', 'geerocha', 'nxzerooficial', 'twithirteen', 'Caco_Grandino', 'DiFerrero', 'daniel_weksler', 'FiRicardo', 'renansdc', 'CountingCrows', 'GMA', 'dooce', 'pitchfork', 'imogenheap', 'ABC', 'joelmchale', 'richardpbacon',  'alinemariano']

dlfma = ""

values = 

for c in chunk_list:
    names = getNames(json.dumps(main_test(','.join(map(str, chunk_list[c])))))
    length = len(names)
    i = 0
    while i<length:
        dlfma = names[i]
        print("Scraping for user:",names[i])
        try:
            scrap(start_date="2017-01-01", max_date="2017-12-31", from_account = names[i],interval=1, headless=True, hashtag=None).to_csv('finance.csv',mode='a',encoding='utf-8-sig')#previously creep1.csv
            i+=1
        except Exception: 
            print("Stopped at:",dlfma)

try:
    for val in values:
        names = getNames(json.dumps(main_test(','.join(map(str, val)))))
        print(names)
        #for name in names:
            #dlfma = name
            #print("Scraping for user:",name)
            #scrap(start_date="2010-01-01", max_date="2010-12-31", from_account = name,interval=1, headless=True, hashtag=None).to_csv('creep203.csv',mode='a',encoding='utf-8-sig')
except Exception: print("Stopped at ", dlfma)

#flat_list = list(chain.from_iterable(values))
#main_test(','.join(map(str, flat_list[1])))

#chunk_list = list(chunks(flat_list, 100))
#print(chunk_list)

for val in values:
    names = getNames(json.dumps(main_test(','.join(map(str, val)))))
    for name in names:
        print(name)
"""
