import pandas as pd
import csv, sys, math, collections, re, time, json
from ddd import getNames, HelloWorldExample, chunks
import matplotlib.pyplot as plt
from itertools import chain
from neo4j import GraphDatabase
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import joblib
from nltk.sentiment import SentimentIntensityAnalyzer
import operator
from googletrans import Translator
from sex import main_test

translator = Translator()
sia = SentimentIntensityAnalyzer()

sys.path.append("C:/Users/headm/OneDrive/Desktop/csv")

def sign(num):
    if num<0:
        return -1
    return 0

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
        X = vectorizer.transform([tweet])
        MNBpredict = model.predict(X)

        #detection = translator.detect(tweet)
        #time.sleep(1)
        
        #if detection=="pt":
        if MNBpredict[0]=="Negativo": score = -0.5 
        elif MNBpredict[0]=="Positivo": score = 0.5
        #elif detection=="en":
        #    stats = sia.polarity_scores(tweet)
        #    del stats['compound']
        #    sent = max(stats.items(), key=operator.itemgetter(1))[0]
            
        #    if sent == "neg":
        #        score = -0.5
        #    elif sent == "pos":
        #        score = 0.5
        
        for name in m:
            if name in dic: quote_dic[name] += score

dataset = pd.read_csv('C:/Users/headm/OneDrive/Desktop/csv/main.csv',encoding='iso-8859-1')
print("########## File read ##########\n")
tweets = dataset["tweet_text"].values
vectorizer = CountVectorizer(analyzer = "word", tokenizer = 
          None, preprocessor = None, max_features = 5000)
vectorizer.fit_transform(tweets)
model = joblib.load('model.joblib')

rt_dic = dict()
fav_dic = dict()
quote_dic = dict()
dic = dict()
temp = dict()

c = c_ = max_rt = max_fav = max_quote = 0
lst = []

"""
with GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "1234")) as driver:
    with driver.session() as session:
        values = session.read_transaction(HelloWorldExample.getNodes)
        flat_list = list(chain.from_iterable(values))
        
        chunk_list = list(chunks(flat_list, 100))
        
        for c_list in chunk_list:
            names = getNames(json.dumps(main_test(','.join(map(str, c_list)))))
            for name in names: lst.append(name)
        
        #print(chunk_list)
        #for i in range(len(chunk_list)):
        #    names = getNames(json.dumps(main_test(','.join(map(str, chunk_list[i])))))
        #    print(i,":",names)
        
        #print(values)
"""

lst = ['queridoleitor', 'silviolach', 'malvados', 'rosana', 'antoniotabet', 'folha_zapping', 'miriamleitao', 'MariaRita', 'NoticiasdaTV', 'boninho', 'BolaDoPanico', 'rinovackoficial', 'youngporra', 'fabiorabin', 'brunomotta', 'barbaragancia', 'Pretinho_Basico', 'JosiCastro73', 'mileyxyzcy25349', 'Allison234cs', 'vitonez', 'bmantovani', 'ivancapelli', 'LucasdiGrassi', 'fabio_seixas', 'flaviogomes69', 'JPdeOliveira', 'f1brasilclube', '1aa2a', 'SoninhaFrancine', 'WWF_Brasil', 'lostinlost', 'diogomainardi', 'AntonioPizzonia', 'jairoliveira', 'WellingtonMuniz', 'mauriciodesousa', 'silvioluiz', 'gugakuerten', 'LucianoBurti', 'bananinhadany', 'paulocoelho', 'McLarenF1', 'RealHughJackman', 'MariahCarey', 'Newsweek', 'colinmeloy', 'Cheezburger', 'coldplay', 'BreakingNews', 'CBOE', 'nprpolitics', 'Schwarzenegger', 'kevinrose', 'TonyRobbins', 'dickc', 'kevin_nealon', 'PaulaAbdul', 'h3lio', 'DanicaPatrick', 'maxpapis', 'jpmontoya', 'dotFernando', 'danwheldon', 'mariomoraesf', 'portalf1_PT', 'MercedesAMGF1', 'F1Deck', 'tessababee7', 'dxgokehuir', 'freezeads', 'Katiebr1', 'bolanascostas', 'esportenews', 'CBF_Futebol', 'futpedia', 'revistasuper', 'babadonet', 'CantadasCharlie', 'SporTV', 'renato_gaucho', 'multishow', 'stylecars', 'BrazilWorldTV', 'loveletdie', 'sabrina_sato', 'daniredetv', 'geglobo', 'lutabrazuca', 'TO_DE_OLHO', 'sitevagalume', 'chapozica', 'djdownloads', 'MixtapeOficial', 'hevo84', 'CassesOficial', 'jorgeiggor', 'vitorsergio', 'newebooks', 'richstyles', 'espn', 'weboxygen', 'pcfromzero', 'marymagdalan', 'StarzUncut', 'Kylie_Munoz', 'SteveNash', 'LeoTheNardDog', 'yelyahwilliams', 'marca', 'hispanicdime', 'ItsMoneybags', 'TextArtPrint', 'serenawilliams', 'justdemi', 'NBA', 'ashleytisdale', 'PerezHilton', 'ladygaga', 'jtimberlake', 'taylorswift13', 'MandyJiroux', 'mitchelmusso', 'billyraycyrus', 'EmilyOsment', 'BrandiCyrus', 'jonasbrothers', 'ddlovato', 'pamfoundation', 'arcadevi', 'ibjombooxm', 'Brooklyn_Ricci', 'UrsaRCompanio', 'inupup', 'bigeyeonsports', 'ChrisBonn86', 'steaksauce2z', 'montanhadaniel', 'ogeraldinez', 'bixajacare', 'fabiannesangalo', 'victor5013', 'masbach', 'satinovongola', '_Mikael', 'luann_carvalho', 'halonferreira', 'oidiversao', 'Maudox', 'ReallThiago', 'madamemim0', 'GreenpeaceBR', 'aryfranklin', 'JOSI_F', '9eyecat', 'Pi_14559295066', 'buziosfm', 'mtvmanaus', 'MallandroSergio', 'David_BlackWolf', 'menDigodigO', 'DanyLicinha', 'luanaviessa', 'Jrprestes', 'mlauradevides', 'igoorfellix', 'frediee', 'babiwinchester', 'cleversong', 'PaulistanaSerra', 'lucasparaujo', 'Alemao775', 'Alishow', 'leeandroalemao', 'oliferraro', 'RodrigoTakasaki', 'vanfsiqueira', 'portalyoba', 'vinil_oficial', 'PatrickMachado0', 'leandro_10', 'brunozarb', 'aless_nichols', 'BertaCWimbis', 'Viniderossi', 'da_yel', 'Naanda32', 'elvesnaves', 'lemefelipe7', 'brandaosandes', 'Thi_Valle', 'shaianedoimo', 'WellingtonGTR34', 'Diogohunter', 'marciolimasej', 'yayjeo', 'douglaswill', 'lopeskatiane', 'iranimarques', 'wagnerlayb', 'ricardosredoja', 'adrianamarkes', 'darlanvet', 'zeaugustorocha', 'MrDude81', 'Rherdan', 'youcantseeit', 'Qryca', 'Bittnick', 'Ti_iih', 'allan_vernier', 'AFSauer', 'rudenet', 'renatosorin', 'michellepaulina', 'Marcio_Shadows', 'Henri_Diop', 'bettacandido', 'TammyCodato', 'rygeo', 'kachromiec', 'Tulio_andrade', 'William_Castro', 'chescofd_', 'DRIMONTS', 'ltrielli', 'EduOtto', 'lufranca', 'afonsonem', 'BrunoJabs', 'Gabriel270281', 'programageracao', 'felipesinoble', 'universolouco', 'KleberAugusto1', 'eduka', 'claudiocult', '_Zeh__', 'pp_luiz', 'negopretozina', 'AdmHelga', 'Jonhyswq', 'Vini_Bad', 'denisveneno', 'Phiih', 'almeida_bruno', 'davidsilva10', 'diego_cogu', 'bre_nell', 'saulojg', 'AninhaGomez05', 'natyzinhas', 'djalexbaxter', '_anaclaudia91', 'Prycka', 'david_cec', 'Niiiiiine', 'giselasharon', 'karollys', 'susoares', 'sergiocm39', 'clauloria', 'Adnaw8', 'LupinOficial', 'Luane_M', 'KedaoRTM', 'roger_vanutt', 'FraciscoMedeir', 'fredhetori', 'tonytche', 'minhafilhaa', 'RafsPsh', 'gabrielmafia', 'vetfiscal', 'HerreraUck', 'VADINHODONAFLOR', 'odamitse', 'cheshirenats', 'liporoni', 'rafinhabastos', 'jornalhoje', 'Silvio_So_Brotu', 'srbarbosa', 'LucianoHuck', 'Junior_Lima', 'marcosmion', 'TheoBecker8', 'descargaoficial', 'ellenmatonghh', 'JustPlainKcf8', 'josecordova', 'grandepremio', 'caldeiraodohuck', 'decheers', 'TaniaOliveira', 'SabrinaSato', 'rodrigovesgo', 'MarcoLuque', 'SandyLeah', 'NelsonPiquet', 'rubarrichello', 'TonyKanaan', 'emicida', 'SnoopDogg', 'Tyrese', 'iamwill', 'Diddy', 'souljaboy', 'britneyspears', 'tenniskatre9f', 'newmediadeb7i', 'DSRika', 'siteEgo', 'joseserra_', 'angelicaksy', 'astridfontenell', 'FePaesLeme', 'noelylima', 'renanmendis', 'eduardoal', 'superbald', 'Emma10le', 'marisaorth', 'RicardoJr2009', 'ifiorentino', 'nato157', 'dicapratudo', 'Tessalia', 'jimjonescapo', 'SHAQ', 'showdavida', 'LIFE', 'iTunesTrailers', 'alyankovic', 'nytimes', 'TWTFM', 'BITech', 'BBCClick', 'AmyJoMartin', 'GStephanopoulos', 'gtdguy', 'threadless', 'aplusk', 'om', 'JessicaSimpson', 'RyanSeacrest', 'ashleesimpson', 'dannymasterson', 'KikoKLB', 'vinevieira', 'pantaum', 'Alan_editor', 'rafaaguileia', 'StiveRodrigues', 'wagnerseguros', 'xValim', 'Hugo_Resende', 'djdanielsecco', 'claudiobrio', 'carolpupim', 'guiborattomusic', 'jamesjl', 'lini', 'Xpock', 'jbanguela', 'twittatriz', 'rodriguesnelson', 'betosilva', 'DaniloGentili', 'polvilho_cesar', 'lobaoeletrico', 'programapanico', 'oanagitsek1', 'minadosgames', 'lapena', 'nando_reis', 'HugoGloss', 'oceara', 'Danibey', 'meligeni', 'BSenna', 'globoesporteSP', 'mayracardi', 'giudju', 'paloza', 'yokoono', 'BarackObama', 'jimmyfallon', 'freddurst', 'Oprah', 'neytude', 'elciofig', 'dmalevato', 'myegah', 'BetoDevides', 'MarceloTas', 'OscarFilho', 'cqc__', 'ro_15861848284', 'cortezrafa', 'andreolifelipe', 'BandJornalismo', 'na_halia', 'marcelotaz', 'claraelisatex', 'BrunoSwell', 'chairpage', 'lucastex', 'chelseahandler', 'OrlandoMagic', 'Kodak_smil93621', 'thalytazenatti', 'leticia_gs', 'kalu_reatto', 'rpaul81', 'ellen_btg', 'Sih_andressa', 'marinapanda', 'naosalvo', 'CGalochas', 'MariMoon', 'tarsocadore', 'santoEvandro', 'TbirdRadioShow', 'amadafoca', 'FrancysH', 'RSabrina', 'thitooo', 'Lii_Caroline96', 'RaphaelNeumann', 'anaIaura', 'TomFletcher', 'mcflyharry', 'McFLYAddiction', 'DougiePoynter', 'itsDannyJones', 'giselewalter', 'FrankieBridge', 'mcflymusic', 'MrsGiFletcher', 'Starbucks', 'liamgallagher', 'TheEllenShow', 'katyperry', 'PammyRodriguez', 'lsiarom', 'giifraanca', 'lays_flavia', 'srtaTata', 'biabioca', 'hburlamaqui', 'MaozinhaMoretti', 'penarua', 'mamakino_', 'cartolafc', 'fabigoncalves', 'OPOSICAO_JA', 'cdieckmann', 'gilbertogil', 'ivetesangalo', 'PretaGil', 'brunogagliasso', 'isabeloliveiraa', 'Pitty', 'TomCavalcante1', 'vluxemburgo', 'anapaulavuoto', 'DjAlineRocha', 'BSurfistinha', 'SE_Palmeiras', 'chibimartins', 'cella_couto', 'brubssbeatriz', 'Playboy', 'amazonmusic', 'thelittleidiot', 'sockington', 'CoryBooker', 'DellOutlet', 'lancearmstrong', 'stevenbjohnson', 'JerryBrownGov', 'anamariecox', 'Nightline', 'noushskaugen', 'algore', 'petewentz', 'enews', 'NFL', 'angleesoup', 'Lakers', 'joesebok', 'heidimontag', '_Renatinha', 'renatinha_s', 'christinealves', 'RafaOricchio', 'herecomeseffy', 'todasexta', 'eusoudaiana', 'laisdinhani', 'furlanluciana', 'MayraQuitero', 'camila_klitzke', 'RafaFerrer', 'MTVBrasil', '50cent', 'manomenezes', 'sorayadarabi', 'digg', 'davidgregory', 'MrKRudd', 'CMEGroup', 'CBSNews', 'LennyKravitz', 'JonathasComTH', 'luiztsilva', 'adrielicarla', 'edu_f_schuster', 'lakers__one', 'alysontl', 'JuuLio_NettoO', 'bompsiquiatra', 'wakawakawe', 'DarthVader', 'eujessicaflores', 'MTV', 'Google', 'Twitter', 'Pink', 'celsoportioli', '15minutos', 'sigaPalmeiras', 'conka', 'Enxaquecakid', 'MarceloAvestruz', 'frestadajanela', 'ratinhodosbt', 'oficialkellykey', 'good_witchlove', 'LucianaGimenez', 'robmasic', 'Jean_Spacki', 'glorinhamaria', 'karinabacchi', '_INRICRISTO', 'dani_luque', 'BrunoCCardoso', 'clubemondoverde', 'Palmeiras', 'PalmeirasNOW', 'carolzara', 'locomotives', 'stugio', 'DarleneZschech', 'droff', 'vitorbirner', 'RobertoLJustus', 'Fake_Pasquale', 'walterlongo', 'jornaldacbn', 'supergospel', 'virtual_gospel', 'abduzeedo', 'caseycorum', 'crowdermusic', 'Delirious', 'leelandmooring', 'MUTEMATH', 'vickybeeching', 'michaelwsmith', 'christomlin', 'paulbaloche', 'leelandofficial', 'amygrant', 'MartinSmithTV', 'CompassionArt', 'matt_redman', 'timhughes77', 'Daniel_mendes20', 'andressveloso', 'vinheta_ronaldo', 'RafaelNMarques', 'vagandonogoogle', 'dotpcorp', 'fabianommf', 'joseagripino', 'karinafalzoni', 'YouTobaTV', 'BonecaoDoPosto', 'tec_EXAME', 'Cardoso', 'luizagomes', 'fabiaof1', 'OCriador', 'geraldoneto', 'netmovies', 'pedrojovelli', 'fikdik_net', 'blogueador', 'ffffabio', 'paulostudio2002', 'RevistaEpoca', 'g1', 'Tuinter_AVISOS', 'PedroTourinho', 'Legendarios', 'AltaFidelidade0', 'noteu_', 'dizplaynet', 'StefanyCury', 'brdicas', 'benemansoni', 'pegueopomboagr', 'cakedalilih', 'confessopequei', 'ajcampos01', 'LeonardoLMendes', 'claudiaclaudia', 'perucadosilvio', 'abonecainflavel', 'sitedomau', 'AlanBbk', 'pesquisas_real', 'tensoblog', 'eprontofalei', 'KiabboO', 'marceloleitner', 'TurmaDoBolovo', 'ROC4LIFE', 'gatodehotel', 'biaurel', 'ComeuTudinho', 'humbertomilk', 'noticiastimao', 'leilalopes', 'AlfinetePeixoto', 'Eliana', 'marcelomedici', 'RedeGlobo', 'ANAMARIABRAGA', 'SProdutividade', 'metropolitanafm', 'babi', 'Base55Sportadve', 'tvbandeirantes', 'oficial89fm', 'smnhzw', 'WanessaRecife', 'Corinthians', 'LaisRoncoli', 'TI_King', 'PrincessLd2672', 'fabiofdias', 'tatortats214759', 'rockfeminino', 'comediamm', 'fabiochaves', 'gafanhoto', 'WelderMM', 'joao_gordo', 'RogerioMorgado', 'segueotorto', 'orafaoliver', 'eCartorios', 'barbixas', 'guiavegano', 'CNN', 'jhbcampos', 'lucasrogenski', 'santistaroxo', 'kleberD', 'santos_fc', 'marcioballas', 'globocom', 'casseta', 'brunastuta', 'alexpaim', 'alison', 'AlisonFreed', 'johnlegend', 'johngreen', 'paulfeig', 'nprscottsimon', 'Padmasree', 'drdrew', 'UKCoachCalipari', 'Supbruh419', 'AlisonKrauss', 'safollmann', 'cacausouza', 'matheus_lgt', 'edu', 'mvbill', 'centraldorap', 'Eminem', 'Lloydbanks', 'thisis50', 'TonyYayo', 'fatjoe', 'smoss', 'jarule', 'wyclef', 'alefegoncalves', 'luiiz_fernaando', 'reegin', 'CarolinaaSilva', 'raulfadel', 'irmadodado', 'Tomateraz', 'rpradosilva', 'gaabfernandes', 'AnaSilvaSantos', 'Juuhlooiira', 'nataliamafemo', 'FehPrado', 'GabyBorrego', '_rafaellacioffi', 'HiigorCioffi', 'JheysonR', 'aln_azevedo', 'Juxshadow', 'DiiSantos', 'ukwalem', 'escrevegabi', 'rafaelabou', 'ARTESANALBAR', 'bibisampaio', 'liiramos', 'miguells', 'Liziiiie', 'isa_medeiros', 'thais_smp', 'rocks_allan', 'Larry_Amaral', 'millionaire8', 'lucasroveri', 'liiperas', 'gabicapucci', 'isabatista', 'nakedz', 'marcelastock', 'vanguardamix', 'beccabernardes', 'renanmachuca', 'maestrobilly', 'ospaparazzi', 'BispoMacedo', 'WalcyrCarrasco', 'cissa_guimaraes', 'yogaeveganismo', 'SergioMarone', 'sheronmenezzes', 'cacarosset', 'ahickmann', 'CesarFilho', 'celsoportiolli', 'SBTonline', 'jorgearagao', 'LoserSerra', 'm_camelo', 'willian_james', 'Iambabixavier', 'Ta_ais', 'descargamtv', 'geerocha', 'nxzerooficial', 'twithirteen', 'Caco_Grandino', 'DiFerrero', 'daniel_weksler', 'FiRicardo', 'renansdc', 'CountingCrows', 'GMA', 'dooce', 'pitchfork', 'imogenheap', 'ABC', 'joelmchale', 'richardpbacon', '292anjosjuntos', 'alinemariano', 'juuhmiranda', 'heathergarner2', 'luciocorrea', 'vulgodudu', 'BandaEstreita', 'rlachter', 'apyus', 'dishumor', 'maAmelia_', 'joaoanzanello', 'AJ07mm', 'pdanker', 'bupereira', 'renano7', 'alisonjsilva', 'nath_caz', 'batucando', 'fernandobarc', 'WeimarFreitas', 'R_Pascarella', 'sleymank', 'fhmedeiros', 'dicastro', 'marcelofelicio', 'fabiocaveira', 'nicorezende', 'marcioehrlich', 'alvarodrigues', 'DAdecristo', 'EDUMACHAD0', 'cariocasdomundo', 'marcelo_pradal', 'opizza', 'rafael_genu', 'oltaipi', 'mau_silvestre', 'rafatech', 'TGauto', 'elyaldo', '_HYPE_', 'paulo040870', 'mfaraujo', 'AndreBotelho', 'dezvio', 'klebber', 'deborafala', 'rr_custom_toys', 'juliataunay', 'scooter_girl', 'nicocartuns', 'havilson', 'resoslideman', 'almwagner', 'JakeTrevisan', 'mararosani', 'VRGuerreiro', 'vazadaquibaby', 'oproprioboomer', 'kumpera', 'ricardoluizjr', 'LeozitoBHZ', 'radiorot', 'lucasravaiani', 'biramiranda', 'Silviolach_favs', 'JotaFF', 'Roberto_SP', '_denisesmiranda', 'mariqb', 'marciojrn', 'caionantes', 'lusweet', 'rafaelsimoes', 'GUEDES_PEDRO', 'frantic5100', 'Ferdecastro', 'motivese', 'gabrielgodinho', 'RogerioAAbreu', 'Alvim777', 'leandromargoto', 'JeSuspensorios', 'gscomputer', 'tarci_andrade', 'camillafotos', 'gisele_arantes', 'marlenitahuerta', 'carolmbueno', 'rodrigoandradeo', 'mateuslana', 'binccp', 'tlborges', 'Srakesry', 'carlaandrea', 'ganeshlenin', 'andreyanogueira', 'gcantarelli', 'DANILOSER', '_Gisele_', 'felippemendonca', 'erikapatolino', 'LucasCardoso', 'lelezinga', 'MumuNayah', 'ricardowagner', 'douglasbdasilva', 'nadiamdm', '_edumartin', '420bits', 'loreslara', 'amandarezende', 'macielera', 'Andremineiro', 'oliveirarenan', 'Hora_Amanda', 'monteiroorangel', 'sandrofortunato', 'MilaMiloca', 'innocenc1o', 'isafrac', 'salveselvas', 'ghizellini', 'guipacheco', 'vitorio_tomaz', 'LeoNicolay', 'FilomenaFrinzi', 'cassianochaves', 'freire_giselle', 'mltemp', 'febril', 'reidamoda', 'aimicarajo', 'tomaspinheiro', 'EricEustaquio', 'danilolima', 'marcocentenaro', 'luninha', 'MGABRIELLI', 'llanmelo', 'maybetmarangon', 'bichokrulla', 'pedromarcio', 'ivegodoy', 'bruxaOD', 'fernandfreitas', 'paulocezar', 'G7CiaDeComedia', 'bazarpamplona', 'AleYoussef', 'Ideia_Musical', 'PlaceIn', 'manubarem', 'Urublog', 'zobaran', 'Ramsesantunes', 'enriquejimenez', 'agentesmith', 'raphaelcrespo', 'julianapotiens', 'Bianca_Cheshire', 'DaniMartLivros', 'o_presidente', 'sophiacomph', 'talkinhead', 'lilianep', 'Adriana_Torres', 'felipetavares', 'bobsheep', 'Patimeireles', 'carlinha', 'fabioangelus', 'juli_martins', 'carolmilters', 'kellenlopes', 'nortonlimajr', 'AlexEngPro', 'adrianaemery', 'senhoritarosa', 'Dilma2010', 'ponteplural', 'marcelosbs', 'FaustoSalvadori', 'flaviavalsani', 'raulfranco14', 'm3ddla', 'iquecartoonist', 'Palilooo', 'giordanoat', 'ju_ribeiro', 'democraciafut', 'mfr_daniel', 'papodegordo', 'erikgustavo', 'viva_', 'elisandries', '50cnews', 'daialeide', 'luizfogaca', 'jujubalandia', 'evelyndionisio', 'sergiomaggi', 'cebraic', 'blogpdigital', 'bancodoplaneta', 'nadamaischato', 'djmulher', 'motelhj', 'alex_costa', 'RenataV', 'claudiasimas', 'fabioazevedo', 'JulioGuedes_13', 'nilothiago', '_raphaelbispo', 'agradoce', 'jahtempudim', 'blogdomello', 'somdoroque', 'Uniti', 'omarmotta', 'anaerthal', 'BrazilBot', 'MechLite', 'camiseta', 'OCapeta', 'caldeiracustica', 'tambotech', 'felipeguiara', 'vetorial', 'chris_gar', 'andrecaos', 'alejung', 'DiadoSexo', 'davirocha', 'fabioraphael', 'portalbbel', 'euprofessor', 'crispassinato', 'kakario', 'adilsonfuzo', 'odeioacordarced', 'pegabizu', 'andrepancione', 'arthurbras', 'WebMotors', 'enxame', 'RicardoProchnow', 'Robertodelorena', 'eduardocruz', 'belezamundial', 'zoc3', 'portalrodao', '3dgarage', 'jodambros', 'rusberti', 'rcassano', 'fabilovate', 'jiguryo', 'viajantecosmico', 'coisasemanal', 'slapmusica', 'ivanneto', 'coletivu', 'OzManiacos', 'badstalker', 'contatow2pod', 'digitaldrops', 'museando', 'oandrepassamani', 'gustavoramos', 'ComoFunciona', 'gustavojreige', 'liacamargo', 'mrmanson', 'GFortes', 'Camiseteria', 'pastormoises', 'Helton', 'NickEllis', 'gpavoni', 'teatrotpa', 'rdlmda', 'celsorocca', 'belenos', 'diegoaquelelah', 'iGeracao', 'comlimao', 'midiasblog1', 'carlacoutinho', 'rponcebr', 'apsonn', 'BipMe', 'chicobarney', 'viniciuskmax', 'MobMobMedia', 'arnaldobranco', 'Castrezana', 'lazcolors', 'boladegude', 'Gordonerd', 'castrinho', 'MaiteLemos', 'msoma', 'ronaldrios', 'VerdesTrigos', 'audreyy', 'juliana_cunha', 'liaamancio', 'daniellecruz', 'ApocalipseNow', 'charlinemessa', 'BigBrotherBra11', 'wendellcarvalho', 'criativo', 'lukstrindade', 'AgitoCampinas', 'e_eu_com_isso', 'VitDantas', 'FernandaLizardo', 'tuitbsb', 'richardbarros', 'politicaqpariu', 'pulsarte', 'MiloCerri', 'lossio', 'agenteinforma', 'perolaspolitica', 'diegocamara', 'bebendo', 'macedo', 'semanaotimismo', 'redlavor', 'miltonjung', 'joildo', 'allanbobcat', 'sanseverini', 'LazaroFreire', 'desencannes', 'caligraffiti', 'diretorcriacao', 'laripaschoal', 'leoluz', 'vitroleiros', 'gnaisse', 'segundoplano', 'andersonfer', 'CBonamigo_blog', 'adaniella', 'deboranasciutti', 'veiotarado', 'wcima', 'jamiul', 'franciscoleite', 'ramirofreitas', 'dinacosta', 'romani83', 'MarinaMiyazaki', 'macumbex', 'tiodino', 'seufelipe', 'joaopedroramos', 'canteseuamor', 'imwi', 'zedocaixao', 'tonydemarco', 'montemor', 'camicarnicelli', 'oi_oficial', 'eduardoviveiros', 'AdneTRIP', 'BONEKAANDFLAVIO', 'revistatrip', 'odissipador', 'cypolzer', 'torusestore', 'virtae', 'AAZPerfumes', 'investbolsa', 'ulissesmattos', 'viniciusjau', 'LUCIANORB', 'serginhovieira', 'thiagolemos', 'marcusnegrao', 'opss', 'Lila_Vr', 'Yasminmantsoni', 'luciana', 'danimorreale', 'rventurelli', 'ibelli', 'CyntiaBravo', 'brukapires', 'AgenciaWise', 'Rosanina', 'pilandia', 'luzinhapr', 'camilaflorencio', 'GuzzMartins', 'renatamotta', 'xonglee', 'snuchine', 'feliz_ddj', 'marcelo_almeida', 'renatavencato', 'DitoEmCena', 'lau_cilento', 'fernandotubbs', 'SrAssuncao', 'julianoromao', 'rogeriocasado', 'RelatorioOta', 'fabianofls', 'CrazySS', 'SOS_ANIMAISB_RJ', 'vtnc', 'drlawton', 'isddera', 'marcelohenrique', 'ambousai', 'jornalodia', 'TonyCarrado', 'FilhotedePomboO', 'edusan_br', 'fiquepobre', 'didif', 'seguinatico', 'FelipePasarelli', 'kauan_matheus', 'NaraLima', 'tavaresflamengo', 'Dipliz_rock', 'BenLudmer', 'kazasama', 'urtigas112', 'rodrigobrower', 'alinemanso', 'muguardians', 'piangers', 'marcelohk', 'jorgecurtis', 'kellygirao', 'evcl', 'minhalmacanta', 'vitorfigenio', 'lamarca_rock', 'editoramonstro', 'BrownBagApp', 'Deeercy', 'ttats', 'zxyproject', 'seuguimaraes', 'Pablo_Peixoto', 'nighthoje', 'fisgus', 'crof_errante', 'lucascimino', 'aads23', 'chrisvidoto', 'LuisGuilherme', 'marcelabragaia', 'falsoeneas', 'thiagotrips', 'reginajj', 'interaubis', 'belladasemana', 'mathevso', 'anythingyon', 'revista_M', 'glauhelena', 'Bianca_Leao', 'muriloandrade', 'o_camarguinho', 'LisaStarbuck', 'blogcerebrodb', 'felipe_navarro', 'tfmoralles', 'jcvasc', 'nacionpachamama', 'GiPimenta', 'amaurijr', 'naradecampos', 'sinhainsana', 'BocAbrida', 'vitormarcio', 'talessousa', 'JorgeBarbosa', 'Doug_bada', 'otaviomesquita', 'LeoJaime', 'AnaElisaVilar', 'fabiiobezerra', 'ThiagoMeDiego', 'BiahNunes', 'jordanramos_', 'moniquereid', 'eduazambuja', 'sarne_y', 'pbftaboao', 'NicolleRodrigs', 'diegorio40', 'araujo_consult', 'Babaz100', 'gusmills', 'Lghickmann', 'giselerebelo', 'claudiaflores', 'barrilpub', 'ronnykassio', 'luthome', 'gi_groff', 'leotorres', 'jbenarros', 'FilippoCarmona', 'prosopopeio', 'jucaponi', 'bessaluna', 'modanamusica', 'marcussilva', 'leooon', 'Jeffersond1', 'RenatoBacon', 'andrelennon', 'tukadalive', 'samara7days', 'Andy_Lima', 'balbs_s', 'carolmaglio', 'xDjuan', 'lpiva', 'Tytta_07', 'jeanerikadad', 'jjaaqs', 'nigelgoodman', 'samueledson', 'IsaacHilton', 'MhelMarrer', 'tatinhana', 'cleoci', 'sergioranalli', 'AndreArruda', 'danprata', 'mulhergorila', 'ffabiseixas', 'leonaressi', 'rosanafortes', 'FlavinhoRio', 'carlosferreira', 'MichelArouca', 'gilsinhoOoO', 'RotaBR', 'voxalot', 'bbarbarahh', 'tudodecri', 'anareczek', 'hcvale', 'TropicalBeats', 'bonfatto', 'thomazmolina', 'llsanches', 'luiz_granata', 'esustentavel', 'DillCopeti', 'carolinamaia', 'JosePadilha', 'marcelocoli', 'CarolLobianco', 'felrodrigues', 'Joseluisvaz', 'tatycople', 'ronymeisler', 'emailstorage', 'marianamatos', 'TeaWithTash', 'cobralillo', 'riqfreire', 'Anarfabeto', 'MarianaCardoso', 'mahmilanezi', 'JUDAOcombr', 'papodehomem', 'crisdias', 'oct', 'fseixas', 'biagranja', 'comunicadores', 'cmerigo', 'garotasemfio', 'pedrodoria', 'omelete', 'bluebusbr', 'cacabortoletto', 'S250O', 'muitolegal', 'dressajordano', 'Gabanistico', 'ArteFoliaLazer', 'luisnassif', 'ritchieguy', 'guiredator', 'jpcuenca', 'makocarraro', 'hkozaka', 'Ancelmocom', 'PatriciaKogut', 'katiaandrade', 'julio_hungria', 'OMandaChuva', 'nakid', 'atilafrancucci', 'marcoschaves', 'michelebc', 'anticherry', 'cynthiastr', 'ivnamoraes', 'alex_fischer', 'erlichman', 'nayaranacks', 'Rafa_Rosa', 'desenrola_filme', 'RealClecio', 'luizmarinho', 'AlineLove', 'boatealouca', 'paulafortes', 'Clipestesia', 'miuradaniel', 'gustones', 'alicenolustre', 'mariana__', 'malulenzi', 'MaziMoreno', 'RitaJoaoFazenda', 'patriciarocha', 'andremcarvalho', 'LesboaParty', 'Ednucci', 'saporra', 'fredlessa', 'Soalves', 'LUCIOCARDOSO', 'felipegodoy', 'tricomania', 'denisrigotti', 'hellencarol', 'ferreple', 'leo_filipo', 'MarianaMaria', 'rodrigocesarini', 'felipeflexa', 'sgondim', 'biakleinpaul', 'ClaudiaPenteado', 'ronaldobayer', 'gaiba', 'JaimeOhana', 'Sergiomgo', 'mollima', 'Gestao_Inovacao', 'patlopes3', 'sdamascenosilva', 'tomateness', 'cmm_charity', 'RafaFeelMkt', 'aBarba', 'interney', 'bpinaud', 'Perdo_Ho', 'georgellis', 'MigraineInfo', 'marcelomuraro', 'cajuamigo', 'gabiruska', 'Tatofeipa', 'cacife', 'lilidutra', 'IsasS', 'Lutcha', 'diego_pale', 'brunapaixao', 'pedrow', 'pesujo_rj', 'p_tiefenthaler', 'Ramyras', 'danilovsk', 'charles_asilva', 'Mi_Ardala', 'guibonarett', 'aldemar2', 'luizadolfo', 'anaenne', 'flaviarisi', 'aneenha', 'dmaia', 'be_duarte', 'guidorneles', 'taticouto', 'mateuscgs', 'DalilaTardelli', 'Ga_Bernardino', 'rickyshake', 'jujulugao', 'Joaoerthal', 'FabiTavernard', 'gutograca', 'vulgobarreto', 'DuelingPianos', 'olhar37', 'hattie_', 'jackheadaches', 'DigosPaim', 'Arrebol', 'vinicius3w', 'manoelamanual', 'alexprimo', 'lyondhur', 'rcc_br', 'aouila', 'endemicos', 'leosobral', 'ricardoeesv', 'kennedymac69591', 'PrincessLd17964', 'christianosell', 'rcrippa', 'SuperRadioativo', 'rvrezini', 'andreheiden', 'escutehatchi', 'bandanociva', 'jaja_everest', 'suelenmara', 'gabicds', 'reneragostini', 'LorettaRealtor', 'BreiterM']

for name in lst:
    temp["@"+name] = []

try:
    for i in range(len(lst)):
        rt_dic["@"+lst[i]] = 0
        fav_dic["@"+lst[i]] = 0
        quote_dic["@"+lst[i]] = 0
        dic["@"+lst[i]]=0
        
except Exception as e:
    print(e)
"""
with open('C:/Users/headm/OneDrive/Desktop/csv/twitter_pt.csv', 'r', encoding="iso-8859-1") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    sex = ""
    
    try:
        for i in range(len(lst)):
            rt_dic["@"+lst[i]] = 0
            fav_dic["@"+lst[i]] = 0
            quote_dic["@"+lst[i]] = 0
            dic["@"+lst[i]]=0
        
    except Exception as e:
        print("Except: ",sex)
        print(e)
"""

regex = "(?<=^|(?<=[^a-zA-Z0-9-_\.]))(@[A-Za-z]+[A-Za-z0-9-_]+)"
with open('C:/Users/headm/OneDrive/Desktop/csv/twitter3.csv', 'r', encoding='iso-8859-1') as csv_file, open('C:/Users/headm/OneDrive/Desktop/csv/outta_space.csv', 'r', encoding='iso-8859-1'):
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
            if row[7].isnumeric(): 
                fav_dic[row[2]] += int(row[7])*0.25
            if row[8].isnumeric(): 
                rt_dic[row[2]] += int(row[8])
                temp[row[2]] = int(row[8])
                
        line_count += 1
        #print(line_count)
            #0:tweet_#_of_user, 1:userscreen, 2:username, 3:timestamp, 4:text, 5:emojis, 6:comments, 7:likes, 8:retweets 9:image_link, 10:tweet_url
            #print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            #line_count += 1
    print(f'Processed {line_count} lines.')

    dic_sort = sorted(dic.items(), key = lambda item: item[1], reverse=True) #issa list
    
    """
    for key in list(dic):
        if fav_c[key]!=0: fav_dic[key] = fav_dic[key]/fav_c[key]
        if rt_c[key]!=0: rt_dic[key] = rt_dic[key]/rt_c[key]
    """

    max_value = max(rt_dic.values())+max(fav_dic.values())+max(quote_dic.values())
    
    rt_sort = sorted(rt_dic.items(), key = lambda item: item[1])
    fav_sort = sorted(fav_dic.items(), key = lambda item: item[1])
    cou=0
    
    for key in list(dic):
        try:
            if rt_dic[key]!=0 or fav_dic[key]!=0:
                #파주놈꺼
                dic[key] = (((math.log(int(rt_dic[key])+1)/math.log(max(rt_dic.values()))+math.log(int(fav_dic[key])+1)/math.log(max(fav_dic.values()))+sign(quote_dic[key]*math.log(abs(int(quote_dic[key]))+1)/math.log(max(quote_dic.values())))))/math.log(max_value))
                #윤씨꺼
                #dic[key] = (math.exp((int(rt_dic[key])+int(fav_dic[key]))/(int(rt_dic[key])+int(fav_dic[key]))))*0.181818181
            else: del dic[key]
            
            #temp[key] = solution(temp[key])
        except Exception as e: 
            print("LINE 131:",e)
    
    max_v = max(dic.values()) 
    #max_r = max(temp.values())
    
    for key in list(dic):
        dic[key] = dic[key]/max_v/2#+temp[key]/max_r/2
    
    #print(sorted(dic.i;ems(), key=lambda item: item[1]))
    #@allanbobcat, @marcelofelicio
    
    print("AVG:",sum(dic.values())/len(dic))

    try:
        print(len(dic))
        x = np.arange(len(dic))
        plt.figure(figsize=(15, 5))
        plt.bar(x, dic.values(), width=0.8)
        plt.xticks(x, dic.keys())
        plt.show()
    except Exception as e: print(e)
