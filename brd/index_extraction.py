import numpy as np
import pandas as pd
import codecs, time, os, random, sys, re
import brd_index_extract_pagelist as extractor
np.set_printoptions(threshold=np.inf)

# a list of texts that wrongly attributed to headings. Keep updating
wrong_headings = ['Oarces, Francisco Tomds','Hermenegildo','Beam, Lafcadio','Johnson, Andrew','Law, John','Louis XII, king of France','Rubens, Peter-Paul','Anderson, Bans Christian','Blood, Thomas','Burns, Robert','Ciinirr, Jacques','Debs, Eugene Victor','Flannigan, Mrs Katherine Mary','Zenger, John Peter','Pent','Pushkin, Aleksandr Serpieevich','Richard I, king of England','Bacagawea','Smith, John','Thoreau, Henry David','Villon, Franyois','Mansfield, Katherine','Mary Stuart, queen of Scots','Hilton, John','Morton, William Thomas Green','Poe, Edgar Allan','Isabel I, queen of Spain','Josephus, Flavlus','Lafarge, Mme Marie Fortunie','Lisa, Manuel','Machinrelli, Niccolo','Dante Alighieri','David, king of Israel','Douglass, Frederick','Ferdinand T, king of Spain','Grant, Ulyaaea Simpson','Houlanger, Georges Ernest','Bowie, James','Casanova de Eeingalt, Oiacoma','Girolamo','Culpeper, Nicholas','Ouster, George Armstrong','Altgeld, John Peter','Anne of Cleves','Baranov, Alekaandr Andreevich','Bernadette Koutiirous, Saint','Elizabeth, queen of England','Josephine','Richard T, king of England','Swift, Jonathan','Flinders, Matthew','Lafarge, lime Marie Fortunie','Lincoln, Thomas','Mary Magdalen, Saint','Milton, John','Yell, Archibald','Raranov, Alek.iandr Andreevich','Brannan, Samuel','Brent, Margaret','Cutter, Oeorge Armstrong','Dante Alighicri','Ce you','Sabatinl, R. The sword','Stephenson, G. Spring','Steele, J. Co','Williamson, T. R. North after','Where nothing ever happens','Meersch, M. van der. When the','Train, A. C. Manhattan murde','Skrine','Spotsv','Stribli','Tsiang','Brown','Burllni','MacMu','Attlwill','Annut','Geller','Ann','Georg','Grant','Green','Grims','Lewis','Macdo','Skrine''Spotsv','Fern','Lulai','Ellsbi','Albee','Appel','Butle','Cabel','Finne','Furnu','Lev','Bro','Call','Clai','Will','Bon','Elio','Le','Lew','Ar','Whi','Eddi','Greg','Henc','Howes, R -j','Irwln, -VV i','Forbes, R. Tl','Gask. A. The','Cask, A. Jud','Gayle. N. Det','Gayle. N. Sei','Hammett. r','Biam','Field, P. Grit','Gray, \\V. lit','Stevens, j','Fielding, A. Ti','Flynn. B. Lad','Moln&r, F a','Bialk, B. On \\v','Strobel. M. Fe','Mundy, T. Fu','Conner, R. Sa','Bridge, A., pi','Lucas, B. Sta','Rabener, J. Cor','Get','He','Feiner, R. Cat','Tempskl, A. voi','Kamban, G. Vi','Grey, Z. Thund','Frai','Andrews, A. Ml','Caldwell, E. Joi','Lindsay, C. Quc','Glaeser, E. Las','Mann, H. Hill','Corle, E. Fig','Mason, V. ~w','Roth, H. Gal','Gollomb. J. t','Weathenvax','Adamlc, L. Qi','Blake, £2., ps','Lion, H. The','Spitzer, A. Tl','Zara, 1L.. TiU-s','See','MacMullan','Boyd, J. Re','De La Roc','Cram, M. Fc','Flct','Oil','Lu','Bit','Cod','Foe','Oiri','Jon','Mat','Seyi','Thii','Tun','App','Barr','Bars','So','Cann','Char','Cunn','Fairt','Farni','Fores','Gibbs','Jeffri','Jeffrii','Kenni','Che','Marqi','Meyni','Parkn','Scogg','Wheal','Fernar','Fesslei','Hopkin','Annu','Flandrs','Worthir','Addlngto','My','Collections','Brgggn, A. Wind between the', 'Underngian. F. B. On a passing', 'Richardson, H: H. Fortunes of',
                  'Military servitude and', 'Humphrey, Z. Home', 'Mr', 'States in war-time', 'Strange story of William',
                  'Son of', 'Island of', 'Nathan. it', 'Adventures in', 'When the king losses his',
                  'Short stories from', 'Famous detective']
headings_with_subheading = ['European war', 'Historical novels', 'Locality, Novels of', 'Legends and folktale']
# a list of subheadings, ususally name of places. Keep updating

subheadings = ['Easter island','Mediterranean Sea','Serbo-Croat','Spanishcivil war, J9.1B-l9.iy','Albania','Great Plains region','Illinoii','Indn-Chimi, French','Madagascar','Panama canal','Patagonia','Sahara desert','Smith America','Vtah','Built','Dogi','Honei','Vff','Jeruialcm','Htxico','Alatka','Aleutian Islands','Aritona','Brattt','Santo Domingo','South Seas','Dontek','Gorman','Africa, French West','Tlanin islands','Brcutil','Qreeoe','Qerman','Rutsian','Bai/pt','Hank','Uruguay','Polith','Ruttian','Epvpt','Missouri river','Control America','Colombia','CoZorodo','Mississippi valley','Smith. John','Charles V, emperor of the Holy','Roman empire','Paine, Thomas','Sacayawea','Great Plaint region','Libya','Nan tucket','Netherlands Indies','Puerto Rico','Yugoslavia','Moses','Koheson, Paul','Rubens, Sir Peter Paul','Villon, Francois','Hamilton, Emma, lady','Jo.iephua, Flavins','Mansfield, Katharine','Mary Stuart, queen of Soots','Bernadette Souoirous, Saint','Boulanger, Georges Ernest','Jean Marie','Crockett, David','Dickinson, Emily','Czechoslovakian','Samoan islands','Sark','Virgin Islands','Aland ialanda','Alaaka','Alaace','Aran ialanda','Arctio regions','Nova Scotia','Taughan, Benry','Women in business','Stories about','North America','Oftio','West','Kepler, Johann','Paganini, Niccolb','Parris, Samuel','Stiegel, Benry William','Fersen, Hans Axel von, gre/ve','Galilei, Galileo','Glendower, Owen','Jones, John Paul','Doas','Borsss','Clark, George Rogers','Deburau, Jean Gaspard','Elisha ben Abuyah','Bahamas','Northwest, Paoifio','Ukraine','Napoleonio wars','Northwest, Pacific','Shakespeare, William','Socrates','Vaughan, Henry','Washington, George','Kepler, Johnun','Lamb, Charles','Lincoln, Abraham','Paaanini, Niooolo','Parria, Samuel','Ufe','Bronte family','Clark, George Rogeri','Klislia ben Abuyah','Graf, Frau Theresa Heimrath','Indians of South America','Oats','Sorfc','Virgin Inlands','Ws»t Virginia','Bermuda islands','Bessarabia','Nantucket','Near East','Hampshire','Samoan Islands','Wart','Whaling','Supernatural phenomena','European war','Genoa','Ohio valley','Arctic regiont','Carolines','QaUcia','Greek, Modern','Russo-Japanese war','Mules','Squirrels','Byzantine empire','Delaware','Nevi Mexico','Transylvania','Barbary states','Aland islands','Oarollnaa','Dakotaa','Galicia','Mnlay archipelago','Shipwrecks','Birds','Middle ogee','Cttchotlovakian','Indo-OMna','Malay archipelago','Porto Rico','Siam','Channel islands','Czechoslovakia','Dakotas','Dutoh East Indies','Honduras','Africa, West','Antarctio regions','Arkansas','Asia, Central','Bramti','Canary islands','Napoleonic ware','Punic wars','Waterloo, Battle of','Apes','Chamois','Coyotes','Deer','Elephants','Raccoons','Wolverines','Wolves','Citchoilovakian','Rwisian','Ukrainian','Jugoslavia','Macedonia','Mississippl','Ozark mountains','Prince Edward Island','Hawaiiat','Africa, Central','Antarctic regions','Asia','Asin, Central','Bttlknn states','Bermuda inlands','Napoleonic wars','Paraguay','Punic tears','Rif revolt','Horsm','Lions','Reindeer','Tigers','Guatemala','Bali','Bolivia','Europe','Himalaya mountains','Mallorca','Pitcaim island','Rhode Island','Rhodes','Sumatra','Tasmania','Dant*k','Bebreto','Canary Islands','Caribbean tea','Ctecho-Slovakia','Indo-China, French','Jamaica','Orkney islands','Itorocoo','Scotia','Rhode Itland','Tahiti','Tunis','Utah','Yukon','Religious psychology','Spanifh','Bermuda','Caribbean sea','Ecuador','Himalayas','Hindustan','Isle of Wight','Malay Archipelago','Flandert','Haiti','Cats','Dogs','Foxes','Horses','Icelandic','Sesuto','Prince Edward island','Slam','Silesia','Cenrral America','Indo-Ohina','Kurdistan','Liberia','Malay Peninsula','Mississippi River','Aleutian islands','Amazon river','Basque country','Burgundy','Cape May','Capri','Carolinas','Bosnia','Oarolinas','Spanish America','Tyrol','Rumanian','Italv','MiiltiH Peninsula','Manchuria','Mongolia','Provence','Rumania','Sahara Desert','Brazil','Saxony','Afghanistan','Alabama','Channel Islands','Flanders','French Guiana','Formosa','Geneva','Malaya','Rhodesia','Riviera','Alatko','Alsace','Arabia','Assyria','Bay of Fundy','Cape Mny','Dutch East Indies','Carthage','Crete','Serbia','United Stales','Companionate marriage','Philippine islands','St Louis','Sioilv','Snutli Africa','Spate','Tibet','Vancouver island','Hebrides','Malta','Maryland','Morocco','New Hampshire','Newfoundland','Normandy','Panama','OaroHnat','Africa, North','Gape Cod','Cleveland','Cornwall','East Indies','Hawaiian islands','Madrid','Vein England','Xcw Mexico','Peking','Peru','Kan Francisco','Wyoming','Copenhagen','Dalmatia','Dublin','Great Lakes region','Idaho','Indo- China','Itle of Man','Arctic regions','Bagdad','Bavaria','Bucharest','Oapri','Oarolinaa','Central America','Crusades','Note Orleans','Bpatn','Chinese','Chechoslovakian','PoUth','West Indict','Witconsin','Wyominu','Yucatan','Neic England','Hew Guinea','Oklahoma','Ontario','Persia','Rio de Janeiro','Venl&s','Monte Carlo','Near Eatt','Uatne','Ualava','Manila','Uari/land','Mosaachutettt','Jfeoico','Uitslttippi','Greenland','Indo China','Isle of Uan','Kantas','Lapland','Long Itland','Louiiiana','Alaika','Borneo','Itrilisli Columbia','Charleston','Croatia','Esthonla','Far Edit','Oaul','Home','Scandinavia','Wett Indies','Ciechoslovakian','Sicily','South sens','Syria','Viri/inia','Cambridge','Cave Cod','Florence','Illinois','InAo China','Koine','New Enylanil','Rtusia','Acadia','Poltoh','Stoediih','Metrico','New York','Borne','Vienna','Wala','West Indiei','Indo-CMna','Iowa','Lapand','London','Manitoba','Xew Enuland','New Guinea','New Jersey','Balkan states','Went Indies','Algiers','Berlin','Burma','Esthonia','Ethiopia','Hawaii','Ktissian','West Indies','Louisville','Hear East','Hew England','Salem','Singapore','Koutlt Africa','South Dakota','Gaul','Argentina','British Columbia','Brittany','Budapest','Crotia','Glasgow','Isle of Man','Hungarian','Portuguete','Servian','Nor wan','Quebec','San Francitco','Texas','Watts','Ceylon','Ituly','Uaryland','Massachusetts','Nevada','Hew Knylunil','Xortli Carolina','America','Danith','Finnish','Roumanian','Kussian','Vermont','Wett Virginia','Wiscontin','Son Francisco','Siberia','Bovth Africa','Snain','Tat mania','Tennessee','Venezuela','Mississippi','Montana','Weie Orleani','New Zealand','Norway','Porte','Rangoon','BraMil','Brooklyn','Colorado','Corsica','Dakota','Epvft','Par Bait','Finland','Java','Maine','Hussion','United State t','Hunyary','Parit','Byzantium','Mii/ille aget','Ultt0vri','Netli erlandt','Portuyal','Balkan', 'Itoumunian', 'New Mexico', 'Philippine Islands', 'Imeden', 'Syracuse', 'Algeria', 'Baltimore',
               'BroOklyn', 'Detroit', 'Hawaiian Islands', 'Long Island', 'Heeico', 'Michigan', 'Flem\xef\xac\x82h',
               'Prussia', 'Austria', 'Balkans', 'Hungary', 'Poland', 'Asiatic Turkey', 'Austrla-Hungary', 'Brazll',
               'Richard', 'Georgla', 'Great Lakes', 'Clammer and', 'Newport', 'South Sea Islands', 'Turkey', 'Bohemia',
               'Portugal', 'Rome under Nero', 'Labrador', 'Latin Amerth', 'Malay peninsula', 'North Carolina',
               'South America', 'South Sea islands', 'Sweden', 'Afrtoa', 'Arabian coast', 'Asia Minor',
               'Constantinople', 'Cuba', 'Greece', 'Untted smm', 'Early Christiane', 'Netherlands', 'Palestine',
               'New Memo', 'Bohemian', 'Greek', 'Hebrew', 'Norwegian', 'Polish', 'Portuguese', 'Yiddish', 'Germany',
               'Great Britain', 'United States', 'Babylon', 'Crimean war', 'Denmark', 'England', 'France', 'Iceland',
               'India', 'Napoleonic era', 'Rome', 'Russia', 'Scotland', 'Spain', 'Alaska', 'Australia',
               'Bahama islands', 'California', 'Canada', 'Chile', 'Egypt', 'Georgia', 'Holland', 'Indiana', 'Ireland',
               'Japan', 'Kansas', 'Kentucky', 'Lorraine', 'Missouri', 'Nebraska', 'New England', 'New Orleans',
               'Oregon', 'Pennsylvania', 'Philadelphia', 'South A lrlca', 'Venice', 'Wales', 'West Virginia',
               'Wisconsin', 'Danish', 'Dutch', 'French', 'German', 'Italian', 'Japanese', 'Russian', 'Sanskrit',
               'Spanish', 'Swedish', 'Belgium', 'Cnnurla', 'Cape Colony', 'Emmi', 'Italy', 'Jerusalem', 'Middle ages',
               'Flemish', 'Irish', 'Adirondacks', 'Africa', 'Arizona', 'Armenia', 'Boston', 'Email', 'Cape Cod',
               'Chicago', 'China', 'Connecticut', 'Far East', 'Florida', 'Louisiana', 'Mexico', 'Minnesota',
               'Mississippi river', 'New chlmul', 'Ohio', 'Paris', 'Philippine islandn', 'San Francisco',
               'South Africa', 'South Carolina', 'South seas', 'Switzerland', 'Virginia']
subheadings = sorted(list(set(subheadings)))
print(subheadings)
# a list of headings that follows the fiction section. Need to add manually each time
nextheadings = ['Fiction catalog, 1941. (My \'43)','Fifty years of_ best sellers. 1896-1945. Hackett.','Fiddler In the sky. Homeland, K. (Je \'44)','Fiction catalog. 1941. (My \'43)','Fiddle Longspay. Bledsoe, W. (Ag \'42)','Fiction writing self-taught. Hoffman, A. S.','Field of honor. St Johns, A. (S \'38)','Field, Cyrus West','Fiddler\'s coin. Abbott, J. L. (S \'34)','Fields of Gomorrah. White, N. (N \'35)','Fiddler\'s coin. Abbott, J. L,. (S \'34)','Field book of the shore fishes of Bermuda.','Fifteen and five. Bernstein. A. (Ag \'32)','Fiddler. Mlllln, S. G. (S \'29)','Field, David Dudley','Fiddler. Mlllin. S. G. (S \'29)','Field book of common ferns. Durand, H. (D','Fiction as she is wrote. Knox, E. G: V. (D','Field book of common rocks and minerals.','Field, Eugene','Fiddler\'s luck. Schauffler, R. H. (Jl JO)','Fiddler\'s luck. Schauﬂier, R. H. (Jl \'20)','Fiddier\'s luck. _ Schauﬂ\'ler, R. H. (.11 \'20)', 'Field ambulance sketches. (N \'19',
                'Field book of insects. Lutz. . E.', 'Fielchrtlips for the cotton-belt. Morgan. J. O.',
                'Fifth wheel. Prouty, 0. H. (Ap \'16)', 'Fifteens thousand miles by stage. Strahorn, C.',
                'Fifty years in Oregon. Geer, T. T. (Jl. \'12.)', 'Field-days in California. Torrey. B. (Ap \'18)',
                'Fiddling girl. Cam bell, D. R. (Jl \'14)', 'Fidelity. Glaspell, S. (My \'15)']  # to be changed
nextheadings = sorted(list(set(nextheadings)))
print(nextheadings)

pattern1 = re.compile(
    "[A-Z]['‘]*[a-zé§¢ﬂﬁ]+['‘]*[a-zé§¢ﬂﬁ]*[,.:]*\s[A-Z]*\s*[A-Za-z01][,.:]+\s")  # regular author name, "0" for mistakenly recognized "O", "1" for mistankenly recognized "l", "a-z" for initials for wrongly recognized capitla letters
pattern1_1 = re.compile(
    "[A-Z]['‘]*[a-zé§¢ﬂﬁ]+['‘]*[a-zé§¢ﬂﬁ]*[-][A-Z][a-zé§¢ﬂﬁ]+[']*[a-zé§¢ﬂﬁ]*[,.:]*\s[A-Z]*\s*[A-Za-z01][,.:]+\s")  # names like "Kaye-Smith"
pattern1_2 = re.compile(
    "[A-Z]['‘]*[a-zé§¢ﬂﬁ]+['‘]*[a-zé§¢ﬂﬁ]*[A-Z][a-zé§¢ﬂﬁ]+[']*[a-zé§¢ﬂﬁ]*[,.:]*\s[A-Z]*\s*[A-Za-z01][,.:]+\s")  # names like "McArthur"
pattern1_3 = re.compile(
    "[A-Z]['‘]*[a-zé§¢ﬂﬁ]+['‘]*[a-zé§¢ﬂﬁ]*[,.:]*\spseud.")  # names with only a family name and with pseud.
pattern1_4 = re.compile("[A-Z]['‘]*[a-zé§¢ﬂﬁ]+['‘]*[a-zé§¢ﬂﬁ]*[,.:]*\sSir\s[A-Za-z01][,.:]+\s")  # names with "Sir"
pattern1_5 = re.compile(
    "[A-Z]['‘]*[a-zé§¢ﬂﬁ]+['‘]*[a-zé§¢ﬂﬁ]*\s[A-Z][a-zé§¢ﬂﬁ]+['‘]*[a-zé§¢ﬂﬁ]*[,.:]*\s[A-Z]*\s*[A-Za-z01][,.:]+\s")  # family names with two words "Du Puy"
pattern2 = re.compile("[A-Z][a-z]+")
pattern2_1 = re.compile(" [A-Z][a-z]+")
pattern2_2 = re.compile("[.:]\s[A-Z][a-z]+")


year = ['1921','1922','1923','1924','1925','1926','1927','1928','1929','1930','1931','1932','1933','1934','1935','1936','1937','1938','1939','1940','1941','1942','1943','1944','1945','1946','1947']
suffix = ['32106019850368','32106019610374','32106019610382','32106019610390','32106019610408','32106019610416','32106019610424','32106019610432','32106019610440','32106019610457','39015078261180','32106019610465','32106019610473','32106019610481','32106019610499','39015078261230','32106019610507','32106019610515','32106019610523','32106019610531','39015078261289','32106019610549','32106019610556','32106019610564','32106019610572','32106019610580','32106019610598']

length=len(year)
year_suffix=[]
for i in range(length):
    volume=(year[i],suffix[i])
    year_suffix.append(volume)
    
"""
year=1921
def get_directory(dir): # get all documents' directories in the folder
    lists = os.listdir(dir)  # traverse all subfolders in the folder
    length = len(lists)
    path = list(range(length))
    for i in range(length):
        lists.sort(key=lambda x: int(
            x[:-4]))  # sort the arrangement of the volumepages, from 0, 1, 10, 11, 100... to 0, 1, 2, 3, 4...
        path[i] = os.path.join(dir, lists[i])  # concatenate rootdir and this specific volume
    return length,path
def read(x): # read the document
    f=open(x,'r', encoding='UTF-8')
    r=f.read()
    return r
"""
#def main():
for year, suffix in year_suffix:
    volume1935=0
    volume1944=0
    if(year=='1935'):
        volume1935=1
    if(year=='1944'):
        volume1944=1
    volume_id = int(year) - 1904  # volume id
    file1 = open("/media/secure_volume/brd/output_index/volume%i extract.txt" % volume_id, 'w', encoding='utf-8')
    file2 = open("/media/secure_volume/brd/output_index/volume%i discard.txt" % volume_id, 'w', encoding='utf-8')
    pagelist = extractor.extract(suffix)
    pagenumber=len(pagelist)

    #file1 = open("D:\DH collaborative\\book review\data\\volume%i extract.txt" % volume_id, 'w', encoding='utf-8')
    #file2 = open("D:\DH collaborative\\book review\data\\volume%i discard.txt" % volume_id, 'w', encoding='utf-8')
    #pagenumber = get_directory(r'D:\DH collaborative\book review\Library\1921 v.17')[0]
    #path = get_directory(r'D:\DH collaborative\book review\Library\1921 v.17')[1]
    #pagelist=list(range(pagenumber))
    #for i in range(pagenumber):
    #    pagelist[i]=read(path[i])
    #   pagelist[i]=pagelist[i].split('\n')

    bookcount = 0
    bookcount_fiction_about = 0
    bookcount_fiction_genre = 0
    flag = 0
    flag2 = 0

    for i in range(pagenumber):  # read all documents in all volumes
        if (flag2 == 1):
            break
        if (pagelist[i][0][:34].lower() == 'subject, title and pseudonym index' or pagelist[i][0][:23].lower() == 'subject and title index'):  # case insensitive, and two different index titles
            print('Volume number %d: the index begins at page %d' % (
                volume_id, i + 1))  # output is added by 1 to be consistent with the book-no page 0 there
            index_startpage = i
            flag = 1

            for k in range(i, pagenumber):
                if pagelist[k][0][:23].lower() == 'directory of publishers' or len(pagelist[k]) == 0:  # case insensitive, and two different possible type of page after index: another directory, or empty
                    print('Volume number %d: the index ends at page %d' % (
                        volume_id, k))  # no 1 added, since that page is no longer index
                    index_endpage = k
                    flag2=1
                    break

    if flag == 1:  # if the volume has an index, do the following steps
        text = []
        for i in range(index_startpage, index_endpage):
            for j in range(len(pagelist[i])):
                bookcount += pagelist[i][j].count('(')  # how many books are there in the index in total
                if (pagelist[i][j] != ''):
                    text.append(pagelist[i][j])
            linelength=len(text)

        print("Fiction (books about)")
        file1.write("***Fiction (books about)***" + '\n')
        file2.write("***Fiction (books about)***" + '\n')

        for j in range(linelength):  # begin to generate a list of headings within fiction
            fiction_headings = []  # to store the headings
            fiction_books = []  # to store the lines under the heading
            count = -1

            if (volume1944==1 and text[j] == "871"):
                for k in range(1,linelength-j):
                    if(text[j+k]=='Fiction'):
                        text[j + k] = "Fiction (classified by subject)"
                        break

            if (text[j] == "Fiction (books about)"):
                for k in range(10):
                    print(text[j+k])
                for k in list(range(1, linelength - j)):
                    if (text[j + k] == "Fiction (classified by subject)" or text[j+k]=='Fiction (classified according to subject)'):  # if fiction section_about ends
                        break
                    if (text[j + k] == "Fiction"):
                        text[j+k] = "Fiction (classified by subject)"
                        break
                    if (volume1935==1 and text[j+k]=='1161'):
                        text[j + k-1] = "Fiction (classified by subject)"
                        text[j + k] = "Animal stories"
                        break
                    if '(' in text[j + k]:
                        bookcount_fiction_about += 1
                    if len(text[j + k]) > 1 and len(text[k + j]) <= 30 and '(' not in text[
                        k + j] and '\'' not in text[
                        k + j]:  # must be at least 2 characters, no more than 25 characters (avoiding titles not finished in a line to be included, not including '(' to avoid OCR error) # next line beginning with non-characterized character
                        if (text[k + j][0] >= 'A' and text[k + j][0] <= 'Z' and text[k + j][1] >= 'a' and
                                text[k + j][1] <= 'z' and (
                                        text[k + j][-1] >= 'a' and text[k + j][-1] <= 'z' or text[
                                    k + j] == ':')):  # first character A-Z, second a-z (avoiding "BOOK REVIEW DIGEST"), last a-z or 0-9 (eg "Adams, Henry, 1838-1918")
                            if (len(text[
                                        k + j]) >= 4):  # Sometimes a heading contains no books, but direct to "See other sections"
                                if (text[k + j][:4] in ['See ', 'Sec ', 'Sac ']):
                                    continue
                            if len(text[j + k]) >= 9:  # not "xxx-Continued"
                                if (text[j + k][-9:] in ['Continued', 'Continucd','Uontinued','Continual',' ontinued']):
                                    continue
                            if (text[k + j] in subheadings or text[
                                k + j] in wrong_headings or text[k+j][0:13]=='United States' or text[k+j][0:13]=='United State*' or text[k+j][0:13]=='United Slutcs' or text[k+j][0:12]=='United 8tate' or text[k+j][0:6]=='France' or text[k+j][0:6]=='Russia' or text[k+j][0:7]=='America' or text[k+j][0:7]=='England' or text[k+j][0:7]=='Britain' or text[k+j][0:13]=='Great Britain' or text[k+j][0:13]=='Qreat Britain' or text[k+j][0:7]=='Germany' or text[k+j][0:7]=='Austria' or (text[k+j][0:11]=='Inquisition' and text[k+j][12:17]=='Spain') or text[k+j][0:11]=='Set Fiction' or text[k+j][0:11]=='Bee Fiction' or (text[k+j][0:7]=='Fiction' and text[k+j][8:17]=='Ciintinui') or (text[k+j][0:3]=='Pru' and text[k+j][5:7]=='io')):  # For wrong headings, ignore them
                                continue
                            fiction_headings.append(text[k + j])  # Otherwise, add that heading into the list
                            fiction_books.append(
                                [])  # add an empty list to the booklist, to match the headinglist
                            count += 1  # to count the number of lists in the booklist
                    if (text[
                        j + k] in fiction_headings):  # begin to add lines to book list, skip the lines that already in heading list
                        continue
                    elif (
                            count >= 0):  # if there is already a list in the book list (which means there is already list in headings)
                        fiction_books[count].append(text[j + k])  # add texts into the booklist
                length = len(fiction_headings)

                fiction_authors = []  # to store the names of authors
                fiction_titles = []  # to store the names of titles
                fiction_time = []  # to store the time of books
                dictionary = []  # generate a dictionary
                discard = []  # to store discarded lines
                for k in list(range(length)):  # make the four lists have k lists in each
                    fiction_authors.append([])
                    fiction_titles.append([])
                    fiction_time.append([])
                    dictionary.append([])
                    discard.append([])
                if (length > 0):
                    for k in list(range(length)):
                        print('<\heading "%s">' % fiction_headings[
                            k])  # print headings and all the content of each heading
                        count = -1
                        for m in list(range(len(fiction_books[k]))):
                            if ((re.match(pattern1, fiction_books[k][m]) != None) or (re.match(pattern1_3,
                                                                                               fiction_books[k][
                                                                                                   m]) != None)):  # if the line matches with the regular pattern of "author"
                                if (re.search(pattern2, fiction_books[k][m][
                                                        1:]) != None):  # the line must contains contents other than author information
                                    flag = re.search(pattern2, fiction_books[k][m][
                                                               1:]).start()  # find where author ends and title starts
                                    fiction_authors[k].append(fiction_books[k][m][:flag])
                                    fiction_titles[k].append(fiction_books[k][m][flag + 1:])
                                    fiction_time[k].append([])
                                    count += 1
                            elif ((re.match(pattern1_1, fiction_books[k][m]) != None) or (re.match(pattern1_2,
                                                                                                   fiction_books[
                                                                                                       k][
                                                                                                       m]) != None)):  # if the line matches with the pattern of "author" with dash (e.g. "Kaye-Smith") or with a prefix (e.g. "McArthur")
                                if (re.search(pattern2_1, fiction_books[k][m][
                                                          1:]) != None):  # a new pattern to match this case, begin with space, then [A-Z][a-z]+, for titles
                                    flag = re.search(pattern2_1, fiction_books[k][m][
                                                                 1:]).start()  # find where author ends and title starts
                                    fiction_authors[k].append(fiction_books[k][m][:flag + 1])
                                    fiction_titles[k].append(fiction_books[k][m][flag + 2:])
                                    fiction_time[k].append([])
                                    count += 1
                            elif ((re.match(pattern1_4, fiction_books[k][m]) != None) or (re.match(pattern1_5,
                                                                                                   fiction_books[
                                                                                                       k][
                                                                                                       m]) != None)):  # if the line matches with the pattern of "author" with dash (e.g. "Kaye-Smith") or with a prefix (e.g. "McArthur")
                                if (re.search(pattern2_2, fiction_books[k][m][
                                                          1:]) != None):  # a new pattern to match this case, begin with comma or colon, then space, then [A-Z][a-z]+, for titles
                                    flag = re.search(pattern2_2, fiction_books[k][m][
                                                                 1:]).start()  # find where author ends and title starts
                                    fiction_authors[k].append(fiction_books[k][m][:flag + 2])
                                    fiction_titles[k].append(fiction_books[k][m][flag + 3:])
                                    fiction_time[k].append([])
                                    count += 1
                            elif fiction_books[k][m - 1][
                                -1] == '-':  # if not matches with the pattern of "author", if last line ends with run-on line signals
                                if count != -1:  # avoid index out of range
                                    fiction_titles[k][count] = fiction_titles[k][count][:-1] + fiction_books[k][
                                        m]  # deal with run-on lines
                                else:
                                    continue
                            else:
                                if count != -1:  # if not matches with the pattern of "author", and last line not ends with run-on line signal
                                    fiction_titles[k][count] = fiction_titles[k][count] + ' ' + \
                                                               fiction_books[k][
                                                                   m]  # deal with regular lines
                                else:
                                    continue

                        for m in list(range(len(fiction_titles[k]))):
                            for n in list(range(len(fiction_titles[k][m]))):
                                if (fiction_titles[k][m][
                                    n] == '('):  # separate title and time, find where time starts
                                    fiction_time[k][m] = fiction_titles[k][m][n:]
                                    for t in range(len(fiction_time[k][m])):  # find where time ends
                                        if (fiction_time[k][m][t] == ')'):
                                            if (fiction_time[k][m][t + 1:] != ''):
                                                discard[k].append(fiction_time[k][m][t + 1:])
                                            fiction_time[k][m] = fiction_time[k][m][:t + 1]
                                            break
                                    for l in range(n):  # find where title ends
                                        if (fiction_titles[k][m][n - l] >= 'a' and fiction_titles[k][m][
                                            n - l] <= 'z'):
                                            fiction_titles[k][m] = fiction_titles[k][m][:n - l + 1]
                                            break
                                    break

                        dictionary[k] = dict(zip(fiction_authors[k], fiction_titles[k]))  # zip to dictionary
                        #print(dictionary[k])
                        #print(discard[k])
                        num = len(dictionary[k])
                        file1.write('<\heading "%s">' % fiction_headings[k] + '\n')
                        file2.write('<\heading "%s">' % fiction_headings[k] + '\n')
                        for m in range(num):
                            file1.write(fiction_authors[k][m] + '$')
                            file1.write(fiction_titles[k][m] + '\n')
                        for content in discard[k]:
                            file2.write(content + '\n')

        print("Fiction (classified by genre)")
        file1.write('\n'+"***Fiction (classified by genre)***" + '\n')
        file2.write('\n'+"***Fiction (classified by genre)***" + '\n')

        for j in range(linelength):  # begin to generate a list of headings within fiction
            fiction_headings = []  # to store the headings
            fiction_books = []  # to store the lines under the heading
            count = -1
            if (text[j] == "Fiction (classified by subject)" or text[j]=='Fiction (classified according to subject)'):
                for k in list(range(1, linelength - j)):
                    if (text[j + k] in nextheadings):  # if fiction section ends
                        break
                    if '(' in text[j + k]:
                        bookcount_fiction_genre += 1
                    if text[j+k]=='Women\'s army corps' or text[j+k]=='World war, 1939-' or text[j+k]=='World war, 1939-1946':
                        fiction_headings.append(text[k + j])  # Otherwise, add that heading into the list
                        fiction_books.append(
                            [])  # add an empty list to the booklist, to match the headinglist
                        count += 1  # to count the number of lists in the booklist
                    elif len(text[j + k]) > 1 and len(text[k + j]) <= 30 and '(' not in text[
                        k + j] and '\'' not in text[
                        k + j]:  # must be at least 2 characters, no more than 25 characters (avoiding titles not finished in a line to be included, not including '(' to avoid OCR error) # next line beginning with non-characterized character
                        if (text[k + j][0] >= 'A' and text[k + j][0] <= 'Z' and text[k + j][1] >= 'a' and
                                text[k + j][1] <= 'z' and (
                                        text[k + j][-1] >= 'a' and text[k + j][-1] <= 'z' or text[
                                    k + j] == ':')):  # first character A-Z, second a-z (avoiding "BOOK REVIEW DIGEST"), last a-z or 0-9 (eg "Adams, Henry, 1838-1918")
                            if (len(text[
                                        k + j]) >= 4):  # Sometimes a heading contains no books, but direct to "See other sections"
                                if (text[k + j][:4] in ['See ', 'Sec ', 'Sac ']):
                                    continue
                            if len(text[j + k]) >= 9:  # not "xxx-Continued"
                                if (text[j + k][-9:] in ['Continued', 'Continucd','Uontinued','Continual',' ontinued']):
                                    continue
                            if (text[k + j] in subheadings or text[
                                k + j] in wrong_headings or text[k+j][0:13]=='United States' or text[k+j][0:13]=='United State*' or text[k+j][0:13]=='United Slutcs' or text[k+j][0:12]=='United 8tate' or text[k+j][0:6]=='France' or text[k+j][0:6]=='Russia' or text[k+j][0:7]=='America' or text[k+j][0:7]=='England' or text[k+j][0:7]=='Britain' or text[k+j][0:13]=='Great Britain' or text[k+j][0:13]=='Qreat Britain' or text[k+j][0:7]=='Germany' or text[k+j][0:7]=='Austria' or (text[k+j][0:11]=='Inquisition' and text[k+j][12:17]=='Spain') or text[k+j][0:11]=='Set Fiction' or text[k+j][0:11]=='Bee Fiction' or (text[k+j][0:7]=='Fiction' and text[k+j][8:17]=='Ciintinui') or (text[k+j][0:3]=='Pru' and text[k+j][5:7]=='io')):  # For wrong headings, ignore them
                                continue
                            fiction_headings.append(text[k + j])  # Otherwise, add that heading into the list
                            fiction_books.append(
                                [])  # add an empty list to the booklist, to match the headinglist
                            count += 1  # to count the number of lists in the booklist
                    if (text[
                        j + k] in fiction_headings):  # begin to add lines to book list, skip the lines that already in heading list
                        continue
                    elif (
                            count >= 0):  # if there is already a list in the book list (which means there is already list in headings)
                        fiction_books[count].append(text[j + k])  # add texts into the booklist
                length = len(fiction_headings)

                fiction_authors = []  # to store the names of authors
                fiction_titles = []  # to store the names of titles
                fiction_time = []  # to store the time of books
                dictionary = []  # generate a dictionary
                discard = []  # to store discarded lines
                for k in list(range(length)):  # make the four lists have k lists in each
                    fiction_authors.append([])
                    fiction_titles.append([])
                    fiction_time.append([])
                    dictionary.append([])
                    discard.append([])
                if (length > 0):
                    for k in list(range(length)):
                        print('<\heading "%s">' % fiction_headings[
                            k])  # print headings and all the content of each heading
                        count = -1
                        for m in list(range(len(fiction_books[k]))):
                            if(fiction_headings[k]=='Young people' or fiction_headings[k]=='Zionism' or fiction_headings[k]=='Zoological gardens' or fiction_headings[k]=='Women in Industry' or fiction_headings[k]=='World war, 1939-' or fiction_headings[k]=='Weird stories' or fiction_headings[k]=='World war, 1939-1946' or fiction_headings[k]=='Whaling industry' ):
                                print(fiction_books[k][m])
                            if ((re.match(pattern1, fiction_books[k][m]) != None) or (re.match(pattern1_3,
                                                                                               fiction_books[k][
                                                                                                   m]) != None)):  # if the line matches with the regular pattern of "author"
                                if (re.search(pattern2, fiction_books[k][m][
                                                        1:]) != None):  # the line must contains contents other than author information
                                    flag = re.search(pattern2, fiction_books[k][m][
                                                               1:]).start()  # find where author ends and title starts
                                    fiction_authors[k].append(fiction_books[k][m][:flag])
                                    fiction_titles[k].append(fiction_books[k][m][flag + 1:])
                                    fiction_time[k].append([])
                                    count += 1
                            elif ((re.match(pattern1_1, fiction_books[k][m]) != None) or (re.match(pattern1_2,
                                                                                                   fiction_books[
                                                                                                       k][
                                                                                                       m]) != None)):  # if the line matches with the pattern of "author" with dash (e.g. "Kaye-Smith") or with a prefix (e.g. "McArthur")
                                if (re.search(pattern2_1, fiction_books[k][m][
                                                          1:]) != None):  # a new pattern to match this case, begin with space, then [A-Z][a-z]+, for titles
                                    flag = re.search(pattern2_1, fiction_books[k][m][
                                                                 1:]).start()  # find where author ends and title starts
                                    fiction_authors[k].append(fiction_books[k][m][:flag + 1])
                                    fiction_titles[k].append(fiction_books[k][m][flag + 2:])
                                    fiction_time[k].append([])
                                    count += 1
                            elif ((re.match(pattern1_4, fiction_books[k][m]) != None) or (re.match(pattern1_5,
                                                                                                   fiction_books[
                                                                                                       k][
                                                                                                       m]) != None)):  # if the line matches with the pattern of "author" with dash (e.g. "Kaye-Smith") or with a prefix (e.g. "McArthur")
                                if (re.search(pattern2_2, fiction_books[k][m][
                                                          1:]) != None):  # a new pattern to match this case, begin with comma or colon, then space, then [A-Z][a-z]+, for titles
                                    flag = re.search(pattern2_2, fiction_books[k][m][
                                                                 1:]).start()  # find where author ends and title starts
                                    fiction_authors[k].append(fiction_books[k][m][:flag + 2])
                                    fiction_titles[k].append(fiction_books[k][m][flag + 3:])
                                    fiction_time[k].append([])
                                    count += 1
                            elif fiction_books[k][m - 1][
                                -1] == '-':  # if not matches with the pattern of "author", if last line ends with run-on line signals
                                if count != -1:  # avoid index out of range
                                    fiction_titles[k][count] = fiction_titles[k][count][:-1] + fiction_books[k][
                                        m]  # deal with run-on lines
                                else:
                                    continue
                            else:
                                if count != -1:  # if not matches with the pattern of "author", and last line not ends with run-on line signal
                                    fiction_titles[k][count] = fiction_titles[k][count] + ' ' + \
                                                               fiction_books[k][
                                                                   m]  # deal with regular lines
                                else:
                                    continue

                        for m in list(range(len(fiction_titles[k]))):
                            for n in list(range(len(fiction_titles[k][m]))):
                                if (fiction_titles[k][m][
                                    n] == '('):  # separate title and time, find where time starts
                                    fiction_time[k][m] = fiction_titles[k][m][n:]
                                    for t in range(len(fiction_time[k][m])):  # find where time ends
                                        if (fiction_time[k][m][t] == ')'):
                                            if (fiction_time[k][m][t + 1:] != ''):
                                                discard[k].append(fiction_time[k][m][t + 1:])
                                            fiction_time[k][m] = fiction_time[k][m][:t + 1]
                                            break
                                    for l in range(n):  # find where title ends
                                        if (fiction_titles[k][m][n - l] >= 'a' and fiction_titles[k][m][
                                            n - l] <= 'z'):
                                            fiction_titles[k][m] = fiction_titles[k][m][:n - l + 1]
                                            break
                                    break

                        dictionary[k] = dict(zip(fiction_authors[k], fiction_titles[k]))  # zip to dictionary
                        #print(dictionary[k])
                        #print(discard[k])
                        num = len(dictionary[k])
                        file1.write('<\heading "%s">' % fiction_headings[k] + '\n')
                        file2.write('<\heading "%s">' % fiction_headings[k] + '\n')
                        for m in range(num):
                            file1.write(fiction_authors[k][m] + '$')
                            file1.write(fiction_titles[k][m] + '\n')
                        for content in discard[k]:
                            file2.write(content + '\n')

        file1.close()
        file2.close()
        # print(fiction_headings[k],'~',len(dictionary[k])) # print number of each genre
        print(bookcount)
        print(bookcount_fiction_about)
        print(bookcount_fiction_genre)

    if flag == 0:  # if the volume doesn't have an index, print it out and end
        print('Volume number %d: no index found in this volume' % (volume_id))
        index_startpage[i] = 'N/A'
        index_endpage[i] = 'N/A'

#if __name__ == '__main__':
#    main()