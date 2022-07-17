import pandas as pd
import csv, sys, math, collections, re, time, json, copy
from ddd import getNames, HelloWorldExample, chunks
import matplotlib.pyplot as plt
from itertools import chain
import pickle
from neo4j import GraphDatabase
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import joblib
from nltk.sentiment import SentimentIntensityAnalyzer
import operator
#from googletrans import Translator
from sex import main_test

#translator = Translator()
#sia = SentimentIntensityAnalyzer()

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

model = joblib.load('model.joblib')
vectorizer = CountVectorizer(decode_error = "replace", vocabulary = pickle.load(open('vectorizer.pkl', "rb")))

rt_dic = dict()
pr_dic = dict()
str_dic = dict()
fav_dic = dict()
quote_dic = dict()
dic = dict()
temp = dict()
act_ids = ['18155304', '14125476', '3948041', '16814640', '14502233', '43340817', '14994303', '36396848', '52725585', '28178092', '17937117', '15494380', '39687985', '24742820', '43555052', '23489975', '10000822', '31209800', '57398778', '48186490', '43967367', '15768105', '49488784', '28866082', '28342530', '23653153', '50701654', '60178147', '5520952', '657863', '37050345', '17923624', '26801512', '26235265', '11064722', '46437670', '35856249', '17240425', '27881842', '12652472', '17962903', '9604032', '49121796', '24248212', '50073002', '10842792', '35921755', '16468704', '25595508', '25519102', '35607867', '28562620', '31806999', '15095537', '19554706', '14230524', '21111883', '51506907', '46782613', '57390371', '56200081', '43884797', '19020694', '55548734', '13971982', '16334137', '49168641', '38633762', '41773347', '53247667', '53239149', '55238206', '55448904', '42315303', '36723065', '43270207', '56820343', '52240537', '58410849', '58365140', '53981462', '61194166', '56296013', '58922978', '30868707', '36232311', '45346627', '46456579', '53335039', '53357476', '48001571', '30036903', '44986845', '58680146', '16603400', '42278764', '37083096', '42628848', '43740813', '37357471', '52912398', '46245847', '55016263', '60419947', '53938577', '45472713', '40588975', '42408503', '36100632', '32405955', '31902486', '29734515', '56683265', '38016845', '46730358', '38064867', '58833072', '60070854', '40117879', '57913527', '41251147', '56817648', '50475391', '47842235', '58355998', '38072171', '42687168', '57743348', '37723157', '56012182', '53973025', '30705849', '56231323', '57242326', '46312869', '18297088', '47688615', '43023158', '51346362', '36152770', '53550176', '44956828', '22879111', '31392489', '45708227', '15483913', '34171224', '41384170', '20432727', '51509917', '44340677', '48459607', '34394666', '21054053', '54739322', '43208247', '34996429', '46277588', '18633022', '50821343', '46525090', '37075396', '44373966', '60787299', '60206847', '14938818', '29797128', '19058681', '58764406', '8569142', '10152572', '13419722', '23133853', '14213711', '20372050', '35765232', '23514666', '35015510', '40713101', '32172539', '27279878', '45843783', '21929818', '17681513', '6741632', '9255842', '47263956', '34461692', '31201557', '20166847', '9018312', '14946999', '30367771', '28838048', '28445357', '14502789', '35693211', '41036546', '24989174', '48440176', '50654818', '38995168', '49808900', '28904594', '35319602', '31058584', '2182641', '23396761', '55075589', '56193790', '17069521', '8163442', '27710376', '48413266', '57467342', '51471889', '618593', '55770018', '14627558', '15882333', '17041132', '44762111', '29039908', '39623738', '41871999', '53836855', '33976240', '35127843', '41401486', '55702530', '23138341', '24922323', '46104914', '42869016', '18682014', '19691128', '40200735', '35000383', '43133651', '45363692', '14910450', '44924110', '19720801', '58821975', '41553', '13115502', '45238283', '55056510', '36727261', '27419060', '40362590', '51451352', '14718061', '15664281', '1421721', '17877597', '25083518', '14213068', '17332473', '25997705', '30311284', '21207962', '8802752', '51658431', '14746370', '39593575', '22666851', '45719699', '37347539', '40357503', '35099519', '16187595', '38290508', '49879222', '41031095', '19286480', '39139415', '26586520', '50005560', '15432975', '44286640', '20257409', '18219976', '36679967', '55577364', '18248532', '19035226', '36808344', '54152349', '44627459', '55013153', '55717780', '61186412', '35696640', '6583912', '30312303', '25793156', '47395426', '48852495', '44110744', '52106459', '25285165', '38792948', '24898568', '9857332', '16490487', '38604229', '16658554', '29296932', '26842030', '44151874', '58095410', '46267043', '52748996', '31967116', '59643875', '35367337', '56012896', '53744004', '42532540', '55977256', '52771942', '50463844', '46444606', '52532116', '14352519', '43440488', '56220486', '58158381', '9247452', '19460018', '28055231', '35537327', '46537400', '43394391', '44728722', '20600456', '39075832', '31083235', '23532872', '53971402', '54384394', '56225100', '14523801', '9210142', '18749777', '14579710', '18194861', '11734332', '18944193', '43248560', '20193518', '17425310', '40943093', '21219116', '17314377', '48475368', '33636221', '54757562', '19778829', '34486677', '44420317', '33987572', '40015748', '33364183', '16880454', '39264425', '34698616', '41711262', '21430879', '39132808', '14682052', '9588552', '42833707', '18573359', '14571218', '15235269', '54805467', '52844573', '19836309', '39135229', '21956305', '16905622', '12357272', '18428863', '17064825', '46896740', '32831104', '48869568', '20361466', '17032762', '19353490', '17040070', '27874497', '24873979', '50563145', '16971496', '35778683', '14570217', '23946713', '31042974', '14423947', '14446323', '14438094', '26344678', '16586929', '17161096', '25498492', '8644072', '16578538', '15960154', '25594369', '8187282', '34608455', '32802909', '14681561', '14463937', '14832455', '8472842', '18017903', '14950171', '20739434', '15246107', '18678811', '21649841', '52108736', '15771724', '14725070', '19660771', '8847742', '19303338', '26850931', '22089856', '26618823', '16688459', '51304712', '9838582', '17882488', '20712646', '26958411', '14071028', '17812433', '18090714', '14222779', '14533920', '15034608', '10742472', '10221382', '9139562', '22215418', '33717446', '20936592', '23437679', '15386141', '15033850', '16212452', '28517897', '20056190', '26646492', '14089464', '18322411', '47776233', '18840036', '36649613', '15112178', '12800192', '15911319', '14715466', '14332985', '19326419', '14062158', '14881412', '25859825', '8759302', '17232573', '10276742', '15111414', '22858797', '24773240', '17092005', '13559202', '14443663', '14989413', '14095455', '24775609', '17258401', '16906986', '34688416', '8208762', '21903552', '16730013', '8957832', '13468632', '8901532', '25122490', '13879982', '12829542', '4464931', '22813273', '11147212', '8453492', '12601192', '7944792', '5533842', '6314802', '4489651', '6668042', '8193202', '1677721', '1891391', '19156312', '14427649', '3291621', '14111048', '9093792', '9318702', '13393912', '17364109', '10683412', '8944372', '19644905', '16045538', '7316892', '18760980', '18419133', '9720272', '14962720', '12108482', '6107152', '10074252', '18885480', '23219316', '23758960', '31498951', '16622621', '8778342', '20765015', '20515331', '13226972', '8252082', '14624461', '18146683', '11325162', '31001364', '13099302', '778097', '22724451', '12462542', '25573374', '14144430', '16395324', '9459372', '17449985', '23469870', '25607001', '14641887', '46477826', '36919049', '16206980', '12708372', '16502808', '16738833', '16294017', '35902931', '16017872', '14511320', '16243838', '19232681', '17487043', '9880822', '35967493', '19413717', '8856372', '15845600', '35918251', '17157163', '17576418', '12907752', '15304514', '7098532', '11844462', '9427502', '42635498', '3550481', '14749366', '17706969', '15040240', '21168344', '11946682', '17804782', '25491440', '23597124', '16341710', '12886792', '22275261', '19420804', '46031359', '17074445', '41098426', '30058868', '26841567', '29509944', '32991852', '14143374', '10226052', '17675497', '30757125', '14652106', '12206232', '15082884', '27800328', '14590132', '17746550', '18107817', '29762381', '10907922', '7116712', '17486232', '14932565', '18407780', '5389772', '16143293', '15524519', '14650624', '24696064', '23323423', '20629301', '24232174', '11991572', '25090102', '17043347', '14143813', '28634856', '15111691', '15067571', '31041288', '33966457', '20704801', '31353373', '21057785', '14391978', '44957632', '56935432', '33036023', '32446253', '16547585', '15691934', '15390773', '34326210', '9042862', '19300169', '20794802', '17663800', '41006145', '17193128', '15778341', '9360152', '10490192', '9892542', '26522566', '36645861', '36648662', '39089182', '46379654', '50883044', '15599769', '1204101', '16015140', '17079719', '18237109', '823692', '16192335', '17682482', '26621305', '35433365', '18475928', '17575823', '20590450', '34142774', '42498563', '26008670', '47966233', '14887047', '14525839', '23365850', '19341589', '10325972', '572', '6486892', '1160561', '1551291', '8093332', '6506272', '6665802', '14124402', '8434702', '23591764', '34592606', '23193129', '18671789', '14754376', '19547019', '17631203', '7518442', '16795139', '16814960', '24433652', '33221026', '49968050', '15384035', '16866835', '41869474', '18272721', '19244882', '15835368', '19044122', '11126932', '17726063', '14363356', '15128114', '21390398', '16437673', '16111281', '20790149', '18293413', '17043255', '25785638', '37254806', '21303814', '33580927', '14720221', '23455332', '14362191', '25589110', '20062577', '8861882', '9358472', '19487437', '41952276', '26924671', '19787845', '9555122', '16415215', '22662739', '8115312', '19660389', '30910887', '14981982', '25133850', '17488005', '19720750', '24808115', '19464107', '17952006', '35395752', '30228473', '54929593', '18192571', '18819223', '32275388', '16897274', '27899098', '37329391', '26588764', '8310472', '20564095', '8696812', '24371501', '17033834', '49464469', '15821294', '41479891']
c = c_ = max_rt = max_fav = max_quote = 0
usernames=dict()
users = ["silviolach","malvados","rosana","miriamleitao","MariaRita","NoticiasdaTV","boninho","BolaDoPanico","youngporra","fabiorabin","brunomotta","barbaragancia","Pretinho_Basico","JosiCastro73","vitonez","bmantovani","ivancapelli","LucasdiGrassi","fabio_seixas","flaviogomes69","JPdeOliveira","SoninhaFrancine","AntonioPizzonia","mauriciodesousa","silvioluiz","gugakuerten","LucianoBurti","bananinhadany","paulocoelho","kevinrose","h3lio","maxpapis","mariomoraesf","MercedesAMGF1","bolanascostas","esportenews","CBF_Futebol","revistasuper","CantadasCharlie","SporTV","renato_gaucho","multishow","BrazilWorldTV","sabrina_sato","daniredetv","geglobo","TO_DE_OLHO","sitevagalume","MixtapeOficial","hevo84","CassesOficial","vitorsergio","weboxygen","marca","justdemi","ladygaga","ddlovato","montanhadaniel","bixajacare","fabiannesangalo","_Mikael","halonferreira","oidiversao","Maudox","madamemim0","GreenpeaceBR","JOSI_F","mtvmanaus","MallandroSergio","menDigodigO","DanyLicinha","mlauradevides","babiwinchester","cleversong","lucasparaujo","Alishow","leeandroalemao","oliferraro","RodrigoTakasaki","vanfsiqueira","portalyoba","vinil_oficial","PatrickMachado0","brunozarb","Viniderossi","lemefelipe7","brandaosandes","Thi_Valle","marciolimasej","lopeskatiane","ricardosredoja","darlanvet","zeaugustorocha","Rherdan","Bittnick","AFSauer","renatosorin","michellepaulina","Marcio_Shadows","kachromiec","Tulio_andrade","William_Castro","chescofd_","DRIMONTS","ltrielli","afonsonem","BrunoJabs","programageracao","felipesinoble","KleberAugusto1","eduka","claudiocult","pp_luiz","AdmHelga","denisveneno","almeida_bruno","davidsilva10","AninhaGomez05","natyzinhas","djalexbaxter","david_cec","Niiiiiine","susoares","clauloria","Luane_M","KedaoRTM","roger_vanutt","FraciscoMedeir","fredhetori","minhafilhaa","RafsPsh","gabrielmafia","vetfiscal","HerreraUck","cheshirenats","rafinhabastos","jornalhoje","LucianoHuck","Junior_Lima","marcosmion","TheoBecker8","descargaoficial","grandepremio","caldeiraodohuck","decheers","TaniaOliveira","SabrinaSato","rodrigovesgo","MarcoLuque","SandyLeah","NelsonPiquet","rubarrichello","TonyKanaan","emicida","DSRika","siteEgo","joseserra_","angelicaksy","astridfontenell","FePaesLeme","noelylima","renanmendis","eduardoal","ifiorentino","nato157","Tessalia","showdavida","aplusk","KikoKLB","lini","Xpock","jbanguela","betosilva","DaniloGentili","lobaoeletrico","programapanico","lapena","nando_reis","oceara","Danibey","meligeni","BSenna","globoesporteSP","yokoono","MarceloTas","OscarFilho","cortezrafa","andreolifelipe","BandJornalismo","naosalvo","CGalochas","MariMoon","santoEvandro","TomFletcher","DougiePoynter","ivetesangalo","PretaGil","brunogagliasso","Pitty","TomCavalcante1","vluxemburgo","anapaulavuoto","DjAlineRocha","BSurfistinha","SE_Palmeiras","chibimartins","stevenbjohnson","heidimontag","furlanluciana","MayraQuitero","RafaFerrer","MTVBrasil","manomenezes","luiztsilva","alysontl","wakawakawe","DarthVader","celsoportioli","sigaPalmeiras","conka","Enxaquecakid","MarceloAvestruz","frestadajanela","ratinhodosbt","oficialkellykey","good_witchlove","LucianaGimenez","robmasic","_INRICRISTO","dani_luque","BrunoCCardoso","clubemondoverde","Palmeiras","PalmeirasNOW","carolzara","locomotives","stugio","vitorbirner","RobertoLJustus","Fake_Pasquale","walterlongo","jornaldacbn","supergospel","virtual_gospel","abduzeedo","vickybeeching","Daniel_mendes20","andressveloso","dotpcorp","joseagripino","karinafalzoni","YouTobaTV","BonecaoDoPosto","tec_EXAME","Cardoso","OCriador","netmovies","pedrojovelli","fikdik_net","blogueador","paulostudio2002","RevistaEpoca","g1","Legendarios","AltaFidelidade0","dizplaynet","StefanyCury","brdicas","pegueopomboagr","cakedalilih","ajcampos01","sitedomau","AlanBbk","pesquisas_real","tensoblog","marceloleitner","biaurel","ComeuTudinho","humbertomilk","noticiastimao","AlfinetePeixoto","Eliana","RedeGlobo","ANAMARIABRAGA","SProdutividade","metropolitanafm","oficial89fm","smnhzw","WanessaRecife","Corinthians","LaisRoncoli","fabiofdias","rockfeminino","comediamm","fabiochaves","WelderMM","segueotorto","orafaoliver","barbixas","guiavegano","lucasrogenski","santistaroxo","marcioballas","casseta","brunastuta","alexpaim","Supbruh419","mvbill","centraldorap","jarule","alefegoncalves","reegin","CarolinaaSilva","Tomateraz","gaabfernandes","AnaSilvaSantos","nataliamafemo","FehPrado","_rafaellacioffi","HiigorCioffi","ukwalem","escrevegabi","ARTESANALBAR","liiramos","isa_medeiros","thais_smp","liiperas","isabatista","beccabernardes","maestrobilly","BispoMacedo","WalcyrCarrasco","SergioMarone","cacarosset","ahickmann","CesarFilho","SBTonline","Ta_ais","geerocha","nxzerooficial","Caco_Grandino","DiFerrero","daniel_weksler","imogenheap","luciocorrea","vulgodudu","apyus","dishumor","maAmelia_","joaoanzanello","pdanker","bupereira","renano7","nath_caz","batucando","fernandobarc","WeimarFreitas","R_Pascarella","sleymank","fhmedeiros","dicastro","marcelofelicio","fabiocaveira","nicorezende","marcioehrlich","alvarodrigues","DAdecristo","marcelo_pradal","opizza","rafael_genu","rafatech","mfaraujo","AndreBotelho","dezvio","rr_custom_toys","juliataunay","scooter_girl","nicocartuns","almwagner","JakeTrevisan","VRGuerreiro","vazadaquibaby","oproprioboomer","kumpera","LeozitoBHZ","radiorot","biramiranda","Silviolach_favs","JotaFF","Roberto_SP","_denisesmiranda","mateuslana","binccp","andreyanogueira","ricardowagner","420bits","amandarezende","macielera","Andremineiro","oliveirarenan","Hora_Amanda","monteiroorangel","sandrofortunato","MilaMiloca","innocenc1o","isafrac","salveselvas","ghizellini","guipacheco","vitorio_tomaz","LeoNicolay","cassianochaves","freire_giselle","febril","reidamoda","aimicarajo","tomaspinheiro","EricEustaquio","danilolima","marcocentenaro","luninha","MGABRIELLI","llanmelo","maybetmarangon","bichokrulla","bruxaOD","fernandfreitas","paulocezar","G7CiaDeComedia","bazarpamplona","AleYoussef","Ideia_Musical","manubarem","Urublog","zobaran","Ramsesantunes","enriquejimenez","raphaelcrespo","julianapotiens","Bianca_Cheshire","DaniMartLivros","sophiacomph","Adriana_Torres","felipetavares","carlinha","fabioangelus","carolmilters","kellenlopes","nortonlimajr","AlexEngPro","adrianaemery","Dilma2010","ponteplural","marcelosbs","FaustoSalvadori","flaviavalsani","raulfranco14","iquecartoonist","Palilooo","giordanoat","ju_ribeiro","democraciafut","mfr_daniel","papodegordo","erikgustavo","viva_","daialeide","jujubalandia","sergiomaggi","cebraic","bancodoplaneta","djmulher","alex_costa","nilothiago","_raphaelbispo","agradoce","anaerthal","tambotech","felipeguiara","chris_gar","alejung","davirocha","fabioraphael","crispassinato","pegabizu","andrepancione","RicardoProchnow","Robertodelorena","eduardocruz","portalrodao","3dgarage","jodambros","rcassano","fabilovate","viajantecosmico","coisasemanal","slapmusica","ivanneto","coletivu","digitaldrops","gustavoramos","ComoFunciona","gustavojreige","liacamargo","mrmanson","GFortes","Camiseteria","Helton","NickEllis","gpavoni","teatrotpa","rdlmda","diegoaquelelah","iGeracao","comlimao","carlacoutinho","rponcebr","BipMe","chicobarney","viniciuskmax","MobMobMedia","arnaldobranco","Castrezana","castrinho","MaiteLemos","msoma","VerdesTrigos","liaamancio","daniellecruz","charlinemessa","BigBrotherBra11","criativo","AgitoCampinas","e_eu_com_isso","VitDantas","richardbarros","politicaqpariu","pulsarte","MiloCerri","lossio","perolaspolitica","diegocamara","bebendo","semanaotimismo","miltonjung","joildo","allanbobcat","sanseverini","LazaroFreire","desencannes","caligraffiti","leoluz","vitroleiros","segundoplano","CBonamigo_blog","veiotarado","jamiul","ramirofreitas","dinacosta","romani83","MarinaMiyazaki","tiodino","joaopedroramos","imwi","zedocaixao","tonydemarco","montemor","camicarnicelli","oi_oficial","eduardoviveiros","AdneTRIP","BONEKAANDFLAVIO","revistatrip","cypolzer","virtae","investbolsa","ulissesmattos","viniciusjau","serginhovieira","marcusnegrao","opss","Lila_Vr","Yasminmantsoni","luciana","rventurelli","CyntiaBravo","brukapires","AgenciaWise","Rosanina","pilandia","luzinhapr","camilaflorencio","GuzzMartins","renatamotta","xonglee","marcelo_almeida","DitoEmCena","lau_cilento","fernandotubbs","SrAssuncao","julianoromao","rogeriocasado","RelatorioOta","CrazySS","marcelohenrique","jornalodia","edusan_br","didif","FelipePasarelli","BenLudmer","kazasama","marcelohk","Deeercy","zxyproject","seuguimaraes","Pablo_Peixoto","fisgus","crof_errante","lucascimino","chrisvidoto","LuisGuilherme","thiagotrips","reginajj","interaubis","belladasemana","mathevso","revista_M","glauhelena","Bianca_Leao","muriloandrade","o_camarguinho","LisaStarbuck","felipe_navarro","tfmoralles","jcvasc","GiPimenta","talessousa","JorgeBarbosa","Doug_bada","otaviomesquita","moniquereid","NicolleRodrigs","diegorio40","gusmills","Lghickmann","giselerebelo","claudiaflores","luthome","gi_groff","leotorres","jbenarros","FilippoCarmona","prosopopeio","jucaponi","bessaluna","modanamusica","marcussilva","leooon","RenatoBacon","tukadalive","samara7days","Andy_Lima","balbs_s","carolmaglio","xDjuan","lpiva","AndreArruda","FlavinhoRio","carlosferreira","MichelArouca","anareczek","bonfatto","luiz_granata","esustentavel","DillCopeti","carolinamaia","JosePadilha","marcelocoli","CarolLobianco","felrodrigues","Joseluisvaz","tatycople","marianamatos","cobralillo","riqfreire","MarianaCardoso","papodehomem","crisdias","oct","fseixas","biagranja","comunicadores","cmerigo","garotasemfio","pedrodoria","bluebusbr","cacabortoletto","S250O","muitolegal","dressajordano","luisnassif","ritchieguy","jpcuenca","hkozaka","Ancelmocom","PatriciaKogut","katiaandrade","julio_hungria","atilafrancucci","erlichman","Rafa_Rosa","desenrola_filme","RealClecio","luizmarinho","boatealouca","miuradaniel","gustones","mariana__","malulenzi","MaziMoreno","RitaJoaoFazenda","Ednucci","saporra","fredlessa","Soalves","LUCIOCARDOSO","felipegodoy","tricomania","hellencarol","leo_filipo","rodrigocesarini","felipeflexa","sgondim","ClaudiaPenteado","ronaldobayer","gaiba","JaimeOhana","Sergiomgo","mollima","Gestao_Inovacao","patlopes3","sdamascenosilva","tomateness","RafaFeelMkt","interney","georgellis","gabiruska","danilovsk","charles_asilva","luizadolfo","flaviarisi","aneenha","be_duarte","guidorneles","mateuscgs","DalilaTardelli","rickyshake","jujulugao","Joaoerthal","gutograca","vulgobarreto","olhar37","DigosPaim","Arrebol","vinicius3w","manoelamanual","alexprimo","lyondhur","aouila","endemicos","leosobral","rvrezini"]

for i in range(len(users)):
    usernames[users[i]] = act_ids[i]
ids = dict([(value, key) for key, value in usernames.items()])

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

with GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "1234")) as driver:
    print("Running pagerank...")
    with driver.session() as session:
        print("Which topic network would you like to select? -1 for all topics.")
        topic = int(input())
        print("TOPIC",topic)
        if topic==-1:
            values = session.read_transaction(HelloWorldExample.pageRank)
            
            for i in range(len(values)):
                pr_dic[values[i][0]._properties["t_id"]] = values[i][1]
        else: 
            values = session.read_transaction(HelloWorldExample.prTopic, topic)
            
            for i in range(len(values)):
                pr_dic[values[i][0]] = values[i][1]
        #for i in range(len(values)):
            #pr_dic[values[i][0]._properties["t_id"]] = values[i][1]            

regex = "(?<=^|(?<=[^a-zA-Z0-9-_\.]))(@[A-Za-z]+[A-Za-z0-9-_]+)"
filename = 'C:/Users/headm/OneDrive/Desktop/python/twitter_pt.csv'
with open(filename, 'r', encoding='iso-8859-1') as csv_file, open('C:/Users/headm/OneDrive/Desktop/csv/outta_space.csv', 'r', encoding='iso-8859-1'):
    print("Skimming thru "+filename+" file...\n")
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}\n')

        #try:
        if "@" in row[4]: sentiment(row[4])
        #except Exception: 
            #print("ERROR:",row)

        if row[2] in dic:
            if row[7].isnumeric(): 
                fav_dic[row[2]] += int(row[7])*0.25
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

    max_value = max(rt_dic.values())+max(fav_dic.values())+max(quote_dic.values())

    for key in list(dic):
        try:
            if rt_dic[key]!=0 or fav_dic[key]!=0:
                #파주놈꺼
                dic[key] = (((math.log(int(rt_dic[key])+1)/math.log(max(rt_dic.values()))+math.log(int(fav_dic[key])+1)/math.log(max(fav_dic.values()))+sign(quote_dic[key]*math.log(abs(int(quote_dic[key]))+1)/math.log(max(quote_dic.values())))))/math.log(max_value))
                #윤씨꺼
                #dic[key] = (math.exp((int(rt_dic[key])+int(fav_dic[key]))/(int(rt_dic[key])+int(fav_dic[key]))))*0.181818181
            else: del dic[key]
            
            temp[key] = solution(temp[key])
        except Exception as e: 
            print("LINE 131:",e)
    
        
    max_v = max(dic.values()) 
    max_r = max(temp.values())
    max_pr = max(pr_dic.values())
    
    sub_dic = copy.deepcopy(dic)
    sub_sub_dic = copy.deepcopy(dic)
    
    for key in list(sub_dic):
        #상호작용 + h-index
        sub_dic[key] = sub_dic[key]/max_v#/2+temp[key]/max_r/2
    
    print(pr_dic)    
    
    print("Adding Social Activity Score & h-index score...")
    for key in list(dic):
        val = dic[key]
        dic[key] = val/max_v/2+temp[key]/max_r/2
        sub_sub_dic[key] = val/max_v/2+temp[key]/max_r/4
    
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
    
    try:
        print(len(dic))
        x = np.arange(len(dic))
        plt.figure(figsize=(15, 5))
        plt.bar(x, dic.values(), width=1.0)
        plt.xticks(x, dic.keys())
        plt.show()
    except Exception as e: print(e)
    
    print("Adding PageRank score to total...")
    for key in list(pr_dic):
        #pr_dic key: 숫자, dic key @이름
        print(key, type(key))
        key_="@"+ids[str(key)]        
        try: pr_dic[key] = pr_dic[key]/max_pr/4+sub_sub_dic[key_]
        except Exception:print("!")
            
    print("AVG:",sum(pr_dic.values())/len(pr_dic))
    
    #print(sorted(dic.items(), key = lambda item: item[1]))
    
    print(max(pr_dic.values()))

    try:
        print(len(pr_dic))
        x = np.arange(len(pr_dic))
        plt.figure(figsize=(15, 5))
        plt.bar(x, pr_dic.values(), width=1.0)
        plt.xticks(x, pr_dic.keys())
        plt.show()
    except Exception as e: print(e)
    
    sub_dic = sorted(sub_dic.items(), key = lambda item: item[1], reverse=True)
    dic = sorted(dic.items(), key = lambda item: item[1], reverse=True)
    pr_dic = sorted(pr_dic.items(), key = lambda item: item[1], reverse=True)
    
    scores = []
    
    for score in pr_dic:
        scores.append((ids[str(score[0])], score[1]))
    
    print(sub_dic[:16])
    print(dic[:16])
    print(scores[:16])
    print(int(len(sub_dic)*0.3), int(len(dic)*0.3), int(len(pr_dic)*0.3))
