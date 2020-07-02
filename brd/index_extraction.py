import numpy as np
import pandas as pd
import codecs, time, os, random, sys, re
import brd_index_extract_pagelist as extractor
np.set_printoptions(threshold=np.inf)

# a list of texts that wrongly attributed to headings. Keep updating
wrong_headings = ['Findley','Maiden rites','Laughing space','More wandering stars','The Science Actional dinosaur','Visions from the edge','Not to be taken at night','Contemporary Russian prose','Black sunlight','Updike','The secret history of the Lord of','Dear friends','Germane are','If you can','Reed, L The terrible twos','Fantastic creatures','Moorcock, M Byzantium endures','Monsignor Quixote','Queneau, R, We always treat women too well','More wandering stars','Pereecutions','Greenberg, J A season of delight','Hunter, E, Love, Dad','Acosta, Uriel','Alexander, the Or eat','Johnson, Albert','Lettow-Vorbeck, Paul von','Miyamoto, Musashi','Knowles, J Peace breaks out','Common ground','Mlcrocosmic tales','They came from outer space','On heroes and tombs','Voices In time','Earthly powers','The clowns of God','The clan of the cave bear','Collins, L The fifth horseman','The Great science Action series','Arensberg, A Sister Wolf','The middle ground','Stories from the Canadian North','Stories of Quebec','Bogmail','Crlchton, M Congo','Colegate, L The shooting party','Sister Wolf','Tar baby','Auchincloss, L The cat and the king','Monroe, Marilyn','Panagoulie, Alexandra','Saint-Simon, Louia de Bouvroy, due de','The rat on Are','Calvin, John','Corpentier, Michel','Dartoin, Charles Robert','David, Kino of Israel','Freud, Sigmund','Oodrio, Saint','Louie XIV, King of France','Moravia, A Time of desecration','Starry messenger','Tales of Hulan River','Dahl, R My Uncle Oswald','Bug-eyed monsters','Isaac Asimov presents the great science fiction','The last safari','The book of Jamaica','The Edgar winners','The 13 crimes of science fiction','Hochhuth, R A German love story','The top of the hill','Another part of','The girl in a swing','The treasure of Sainte Foy','The transit of Venus','WlnterreLse','Run to the waterfall','Hardcastle','Nevj Hampshire','The Delphinium girl','Rhodes, R The last safari','Great Canadian adventure stories','Voices of discord','Poggenpuhl family','Alan, R The Beirut pipeline','The Monster in the mirror','Great Canadian adventure stories','Pasternak, Boris Ltonidovich','The lead soldiers','Van Herk, A Judith','An Anthology of modern Turkish short storlee','The Royal guest, and other classical Danish','Arguedas, J- M- Deep rivers','Cuentos: an anthology of short stories from','Having been there','The Faber book of animal stories','Hardwick, E- Sleepless nights','McConkey, J, The tree house confessions','McLendon, J- Deathwork','Isaacs, S- Compromising positions','Auchincloss, L- The country cousin','Yashar Kemal- The undying grass','Hearon, S- A prince of a fellow','Plunkett, J- Farewell companions','Oates, J, C- Son of the morning','Linzee, D- Death in Connecticut','Masters, J- The Himalayan concerto','Best from the rest of the world','Martin, G- Goat, wolf, and the crab','Yenne Velt: the great works of Jewish fantasy','Amundsen, Roald Enaelbregt Gravning','Caroline Amelia Elizabeth, consort','Tenne Velt: the great works of Jewish fantasy','West Point','The confessions','In guilt and glory','Twelve German novellas','Anguedas, J- M- Deep rivers','Gash, J, Gold by Gemini','Millennial women','Running proud','Solo faces','Kiss of the spider woman','Verdict of thirteen','Paddy no more','Running proud','The year of the French','Jaffe, R Class reunion','Barton, M- A reckoning','Rivac','Maclnnes, H- Prelude to terror','Harnack, C- Limits of the land','Cook, James','Dolton family','Gilmore, Gary','Simonides of Ceos','Stalin, Joseph','William Makepeace Thackeray','Schoeman, K- Promised land','Christian, C, The Pendragon','Palmer, L- The red raven','Hardwick, E- Sleepless nights''McLendon, J- Deathwork','Action','The Novel today','Towards a poetics of Action','Haaen','Mortal friends','Adams, R M AfterJoyce','Debray, R- Undesirable alien','BerVlCe Turkish','Solo: women on woman alone','Galactic dreamers','Study war no more','Kafka','Coltrane, J- Talon','Seymour, G- Kingfisher','Ajar, E- Momo','Kanluk, Y- Rockinghorse','Martin, M- The final conclave','Kohout, P- White book','The Arts and beyond','Epps, G- The shad treatment','Injury time','Bums, R- Speak for the dead','Davidson, L- Murder games','The tall stones','Brain, R Kolonlalagent','Bona Kong','Schwamm, E- Adjacent lives','Ozark Mountains','Trifonov, Y- The long goodbye','Katzenbach, M The grab','Myrer, A- The laat convertible','Forbes, C- Avalanche express','Follett, K Eye of the needle','SchoendoerfTer','Juan the landless','Lying low','Myrer, A- The last convertible','Raskin, J- Underground','Sitting Bull, Dakota chief','Ftesh & blood','Shadows on our skin','Paradise Alley','Manning, O- The danger tree','Robinson, J- Perdido','The flounder','The sun and the moon','The mutual friend','Dolby, George','New world for','Cheever, J, Falconer','Auchinclo','Yenne Velt: tl','Jaffe, R, Last chance','In the looking glass','Mllitoe, A- Widower s son','Henissart, P- Winter spy','Guest, J- Ordinary people','Ashes out of hope','Donoso, J- Sacred families','Beyond the gaslight','Souls in metal','Women of wonder','Fringe of leaves','Trevor, w Children of Dynmouth','Mclnerny, R- Her death of cold','Sanders, L Second deadly sin','Chhever, J, Falconer','Fowles, J- Daniel Martin','Pueblo Indians','Ashes out of hope','Instant in the wind','Sacred families','Ashantl doll','Harris, M- Balloonist','Drabble, M- Ice age','Holland, I- DeMaury papers','Found, lost, found','Lerner','Wew world for Simon Ashkenasy','Quilt','Whlttemore, E- Sinai tapestry','Year the lights came on','Vonnegut, K Slapstick','Sclascla, L One way or another','Israel, P- French kiss','Horemheb, King of Eevpt','Drury, A, Return to Thebes','Malzel, Johann Nepomuk','Mono Lisa','Scott, Robert Falcon','Cahlll','Earth angels','Innocent','Clli','Dark lady','Trew, A- Ultimatum','Custer, George Armstrong','Custer','Chukovskaya, L Going under','An tl gray','Run to starlight','Universe ahead','Gentleman traitor','Anchinclo','Jacob the liar','Boys from Brazil','Berllnguer and the professor','Brief life','Turtle diary','Crime on her mind','Tales of student life','Berlinguer and the professor','Barnard, C Unwanted','Clewlston teat','Oodd','Jhab','Ozarks','Fishermen','Dead of winter','Some things weird and wicked','Sh','Philby, Harold Adrian Russell','Schliemann, Sophie Kastromenos','Tubman, Harriet Ross','WolUtonecraft, ilarv','Godwin, William','Hammett, Dashiell','Ibn Fadlan, Ahmad','John of Lancaster, 1st Duke of','Bedford','Spies','Sad geraniums, and other','Annlv','Borchert','Bee Short stories','House of Lords','Fall Creek massacre, JSti','Se','Eire','Adams, William','Beckford. William','Olive. Robert Olive, Baron','Farouk I, King of Egypt','Joan of Arc, Saint','HaSek. J. Good','Konlng, H. JDea/t','Cermani','Egleton, C. iSoni','Gett v','Shaara. M. TCllle','Gulliver, S. Vulcar','Kotzwinkle. W. Fs','Rechy, J. Fourth aj','Wilson. A. As If','Hlstc','Crimean','Eraser, G. M- Fla','Gardner, M. Flight o','Gold minei','Wagoner, D. Road tc','Brautlgan, R. Hawkl','Howatch, S. Caaholn','Unsworth, B. Moo','Future, Sto','Hersey, J. My petltic','Kllse. T. S. Last Wes','Gam','Koenlg, L. Little gii','Logan, J. Very nearest','Logan, J. Very neare','Jones. R F. Blood sport','Nossack. H. E. To th','Flnan','Erdman. P. E. Silver be','Williams, A. Berla pape','Funeral rites and','Sabatler. R Three mint','Salamanca, J. R. Embar','Jacobson, D. Wonder-v','Farm li','Family chroi','Fathers ar','Goldman, W. Princess br','Faulkner. W. Flags In t','Harwood, R Articles of fa','Logan J. Very nearest','Julian. Governor of Ceuta','Princip, Gavrilo','Richard III, Kino of Enoland','Edward IV, Kino of Enoland','Gordon, Charles Georoe','Henry V. Kino of Enoland','Henry VII, Kino of Enoland','Beria. Lavrenti','Burr. Aaron','David. Kino of Israel','Edward IV, Kino of Enoland','Elizabeth, consort of','Lelchuk, A. American','Aaron Burr','Arthur. King','Augustus. Emperor of Rome','Theodore II, Xeuus of Ethiopia','Whistler, James Abbott MoNeitt','Mao. Tsf-tung','Mary I, Queen of England','Nero, Emperor of Rome', 'Nicodemus','Spencer. Philip','Stuart, Francis','Torres, Camtlo','Beacons Held, Benjamin','Disraeli. 1st Earl of','Fox. George','Gullv. James Manby','Henrv V, Xing of England','Judas I scar lot','Wolpert. S. Error of judgm','Alcibiades','Andr£e, Salomon August','Pepys, Bamuel','Philip II, King of Macedonia','Raynald of Ch&tillon','Btalin, Iotif','Foster, Augustus John','Roman Empire','Bollingsworth, Lydia','Merlin','Nicholas II, Czar of Russia','Fielding, Henry','Fields, William Claude','Solzhenllsyn. A. Stories and','Freud, Bigmund','Ludwig II, King of Bavaria','Raleigh, Bir Walter','Richard III, King of England','Oakee. P. Miracles','Redol, A. Man with seven','Buck. P. S. Three daughters of','Collins, Michael','Elizabeth of Hungary, Saint','Lambrakis, Gregory','Mozart, Johann Chrvsostom','Byron. George Gordon Noel','Byron, 6th Baron','Joan, Queen of Sicily','McGill, Peter Hermano','Richard I, King of England','Svevo. I. Short sentimental','Kuznetsov, AnatalU Pctrovich','Marion, Francis','Nefertvte. Queen of Egypt','Turner, Nat','Annual l','Amenhetpp IV. King of Egypt','Augustine, Saint, Bp. of Hippo','Emperor of Rome','Hucldlcston, Christy Rudd','Katcher. L. Blind cave','Lewis. N. Small war mac','Torquemada, Tomas de','Uriah the Hittite','Telia, Ouiseppe','Shame, shame on the Johnson','Askew, Anne','Brown, Margaret Duggans Ware','Hitler, Adolf','Landru, Henri D6sri','Plato','Jesus Christ','Sappho','Lock ridge, R. Emp','Ruark. R. Honey','Go','Nero, Emperor of Borne','Seneca, Lucius Annaeus','Wylie. P. They both','Adams, Abigail','Adams, John','Bohemond I, Prince of Antioch','Cicero, Marcus Tullius','Kelsey, Nancy','TarnovskaGL, Maria. Nikolaevna','Schulz. B. Street of ci','Winter of','Love you','Ellin, S. Blessington','Sheehan. E. R. F. Kingdom of','Lindsay. D. Voyage to','Schulz. B. Steet of ci','Julian, the Apostate, Emperor','More, Anne','Peter, Saint','Rodin, Auguete','Shahjahan, Emperor of India','TarnovsakaGL, Maria. Nikolaevna','Zelle, Margaretha Oeertruida','Baolioni, Qiampaolo','Berenice','Catharine Howard, consort','Olark, Oeorge Rogers','Donne, John','Henry VIII, King of England','Savory. T. Penny for','Bauser, Kaspar','Hugues, Victor','Pericles','Samxnn. Judae of Israel','Wvnkoop, Edward Wanshear','Balcombe, Betsv','Damien de Veuster, Joseph','King of Macedonia','Federico II, Kino of Sicily','Hamilton, Emma, Lady','Hamilton, Sir William','Horbach, M. Yesterday was doom','Zoshchenko. M. Scenes from the','Simon. P.-H. End','Mighty and their','Blstob. P. Warriors for the','Huguenin, J. R. Other side of','SwilHno, Jack','Tyndale, William','Weatherford, William','Winttanlev, Garrard','Perry, Oliver Hazard','Pilate, Pontius','Badcliffe, Charles','Rousseau, Jean Jacques','Shakespeare, WiJJiam','Smith, Joseph','Houston, Samuel','Joseph, of Arimathea','Kean, Edmund','Maximilian, Emperor of Mexico','Newman, John Henry, Cardinal','Emperor of Mexico','Crane, Stephen','Dickens, Charles','Edward III, King of England','Gandhi, Mohandas Karamohand','Gogh, Vincent van','Etaln, queen of Tara','Gold. H. Optimist','Annual i','Davtdovioh tlronshtiiin','Wilkinson, James','Lincoln, Mary Todd','Luke, Saint','Luke Saint','Mary, Virgin','Oglethorpe, James Edward','Sidney, Sir Philip','Trotsky, Leon, originally Lev','Arnold, Benedict','Attito','Beethoven, Karl van','Beethoven, Lttdwip van','Champa, John','Elizabeth I, Queen of England','Lee, Robert Edward','Hubbard, T. L. W. Ba','Howard, J. A. Murd','Vtrillo, Maurice','Lepidus, Marcus Aemilius','Lewis, Merlwether','Margaretha, of Austria, regent','Pocahontas','Sulla, Lucius Cornelius','Ulvsses','Haughery, Margaret Gaffney','Jacob the patriarch','Jephthah, fudge of Israel','Kane, Elisha Kent','Leif Ericsson','Clark, William','Dousman, Hercules Louis','Elisabeth I, queen of England','Francis of Assist, Saint','Batshepsut, queen of Egypt','Aristotle','Baleao, Honort de','Boadicea, queen','BrinviTliers, Marie Madeleine','Caesar, Oaius Julius','Campbell, Alexander','Marquand, J. P. Life at Happy','Raleigh, Sir Walter','Richard III, king of England','Robert I. king of Scotland','Borel, Agnes','William I, the Conqueror, king','Conqueror, king of England','Michelangelo Buonarroti','Moore, Sir John','Pepys, Samuel','Rachel, originally Elisa Felix','Ghimtiy, Jeanne Marie Ignace','Du Una de Rivery, Aimfe','Isabella of France, consort of','Jackson, Thomas Jonathan','John of Austria','King of England','Audubon, John James','Augustine, Saint, lip of Hippo','Beethoven, Ludwig van','Bianco, Andrea','Bronte, family','Oauguin, Paul','Armstrong, C. Dream','Arnold, R. Skeletons','Kelland, C. B. Murder','La Farge, C. Beauty for','Annual) . _ _ rn','Zenobia, queen of Palmyra','Wolfgang Amadeus','Philip IV, king of France','Rawlings, John Aaron','Robert I, king of Scotland','Serra, Junipero','Thaddeus Juan, bp, of Isfahan','Mendelssohn-Bartholdy, Felix','Moberg, Vilhelm','Modigliani, Amedeo','Montezuma, Carlos','Morgan, Sir Henry','Mozart, Johann Chrysostom','Liszt, Franz','Louis XI, king of France','Louis XV, king of France','MoLovghUn, John','Malcolm III, king of Bcotland','Malibran, Maria Felioita','Hosea, the prophet','Hosce, Samuel Gridley','Hunter, John','Hunter, William','Lafltte, Jean','Laveau, Marie','Lenclos, Anne, called Ninon de','Oaugain, Paul','Greene, Nathanael','Hadrian, emperor of Rome','Henry V, king of England','Hood, John Bell','Cleopatra, queen of Egypt','Duplessis, Marie','Henri/ II, King of England','Devereux, countess of','Esther, queen of Persia','Augustine, Baint','Boyd, Belle','Burns, .Robert','Catherine I, empress of Russia','Oenci, Beatrioe','Christina, queen of Sweden','Mttrrictti. Joaquin','Teach, Edward','Thaddeus Juan, ftp, of Isfahan','Untiiiuin, Paul','Hamilton. Smma, lady','Hannibal','Hood, John Bett','Louis XIV, king of France','Marina','Uendelssohn-Bartholdy, Felix','Jiojul. Belle','Catherine /, empress of Russia','Cenoi, Beatrice','Edward II, king of England','Henry 11, King of England','Severn, Joseph','Stuart, James Swell Brown','Lincoln, Altuhnm','Haft, Front','Louis XI, kino of France','Director of Chile','Paul I, emperor of Russia','Payne, John Howard','Burnt, Robert','Deborah, judge of Israel','Duplestit, Marie','Howe, Samuel Oridlev','Keats, John','Lenclos, Anne, called \lnun de','Rousseau, Jean-Jacques','Tartini, Giuseppe','Devereaux, countess of','Estienne, Robert','Francis Xavier, Saint','Joseph, Nez Perci chief','More, Sir Thomas, Saint','Gobelin, Marquise de','Cellini, Benvenuto','Clay, Henry','Columbus, Christopher','Drake, Sir Francis','Elizabeth I, queen of England','Montexuma, Carlos','Morgan, Bir Henry','Paul, Saint','Philip II, king of Spain','Rowlings, John Aaron','Rohan, Tancride de','Timur, the great','Askf, Robert','Augustine, Saint','BrontS family','Hamilton, Elizabeth Schuyler','Lane, Joseph','Loyola, Ignatius of, Saint','Roos, K. Murder in any lar','Piozzi, Mrs Hester Lynch','Richard II, king of England','Semmelteeis, Ignac Fulop','Tohaikovski, Peter Ilyitch','Thomas Aquinas, Baint','Whitman, Marcus','Lecouvreur, Adrienne','Luther, Martin','MoDonogh, John','Mary Magdalene, Saint','Mendeleev, Dimitrii Ivanovioh','Murrieta, Joaquin','Compere, Samuel','Orenville, Sir Richard','Hearn, Lafcadio','Johnson, Sir William','London, Letitia Elizabeth','Davis, Samuel','Delacroix, Eugene','Desjardins, Alphonse','Franklin, Benjamin','French, Daniel Chester','Cards, Francisco Tomds','Blennerhassett, Harman','Booth, John Wilkes','Bruckner, Anton','Henry II, king of Prance','Charles II, king of England','Coeur, Jacques','Alexander I, emperor of Russia','Andersen, Hans Christian','At tic u.i, Titus Pomponius','Baudelmre, Charles','Blackwell, Antoinette Brown','Thomas Aquinas, Saint','Toulouse-Lautrec Monfa, Henri','Marie Raymond de','Williams, Roger','James IV, king of Scotland','Judd, Oerrit Parmalee','McDonogh, John','MacNutt, Francis Augustus','Montez, Lola','PiossA, Mrs Hester Lynch','Alexander 1, emperor of Russia','Catherine of Siena, Saint','Gompers, Samuel','Helena, Saint','Hillstrom, Joseph','Noble, John','Semmelweis, Ignao Fulop','Stuart, Gilbert','Borgia, Cesare','Disraeli, Benjamin','Grey, Lady Jane','Monies, Lola','Morgan, Henry','Mut rittla, Joaguin','Nightingale, Florence','Alexander the Great','Anne Boleyn, queen consort of','Henry Till','Atticus, Titus Pomponius','AttUa','Austen, Jane','Blennerhassett, Barman','Patrick, Saint','Rimbaud, Jean Nicolas Arthur','Stevenson, Robert Louis','James I, king of Scotland','Judith, princess of France','Kemble, Frances Anne','Mary Stuart, queen of Boots','Mendeleev, Dimitril Ivanovich','Carroll, Anna Ella','Crompton, Samuel','Din-is. Samuel','Delacroix, Engine','Grenville, Sir Richard','Jackson, Andrew','Abraham, the patriarch','Allen, Ethan','Baudelaire, Charles','Benjamin, Judah Philip','Caesar, Caius Julius','Campbell, Archibald','Oarces, Francisco Tomds','Hermenegildo','Beam, Lafcadio','Johnson, Andrew','Law, John','Louis XII, king of France','Rubens, Peter-Paul','Andersen, Bans Christian','Blood, Thomas','Burns, Robert','Ciiniir, Jacques','Debs, Eugene Victor','Flannigan, Mrs Katherine Mary','Zenger, John Peter','Pent','Pushkin, Aleksandr Serpieevich','Richard I, king of England','Bacagawea','Smith, John','Thoreau, Henry David','Villon, Franyois','Mansfield, Katherine','Mary Stuart, queen of Scots','Hilton, John','Morton, William Thomas Green','Poe, Edgar Allan','Isabel I, queen of Spain','Josephus, Flavlus','Lafarge, Mme Marie Fortunie','Lisa, Manuel','Machinrelli, Niccolo','Dante Alighieri','David, king of Israel','Douglass, Frederick','Ferdinand T, king of Spain','Grant, Ulyaaea Simpson','Houlanger, Georges Ernest','Bowie, James','Casanova de Eeingalt, Oiacoma','Girolamo','Culpeper, Nicholas','Ouster, George Armstrong','Altgeld, John Peter','Anne of Cleves','Baranov, Alekaandr Andreevich','Bernadette Koutiirous, Saint','Elizabeth, queen of England','Josephine','Richard T, king of England','Swift, Jonathan','Flinders, Matthew','Lafarge, lime Marie Fortunie','Lincoln, Thomas','Mary Magdalen, Saint','Milton, John','Yell, Archibald','Raranov, Alek.iandr Andreevich','Brannan, Samuel','Brent, Margaret','Cutter, Oeorge Armstrong','Dante Alighicri','Ce you','Sabatinl, R. The sword','Stephenson, G. Spring','Steele, J. Co','Williamson, T. R. North after','Where nothing ever happens','Meersch, M. van der. When the','Train, A. C. Manhattan murde','Skrine','Spotsv','Stribli','Tsiang','Brown','Burllni','MacMu','Attlwill','Annut','Geller','Ann','Georg','Grant','Green','Grims','Lewis','Macdo','Skrine''Spotsv','Fern','Lulai','Ellsbi','Albee','Appel','Butle','Cabel','Finne','Furnu','Lev','Bro','Call','Clai','Will','Bon','Elio','Le','Lew','Ar','Whi','Eddi','Greg','Henc','Howes, R -j','Irwln, -VV i','Forbes, R. Tl','Gask. A. The','Cask, A. Jud','Gayle. N. Det','Gayle. N. Sei','Hammett. r','Biam','Field, P. Grit','Gray, \\V. lit','Stevens, j','Fielding, A. Ti','Flynn. B. Lad','Moln&r, F a','Bialk, B. On \\v','Strobel. M. Fe','Mundy, T. Fu','Conner, R. Sa','Bridge, A., pi','Lucas, B. Sta','Rabener, J. Cor','Get','He','Feiner, R. Cat','Tempskl, A. voi','Kamban, G. Vi','Grey, Z. Thund','Frai','Andrews, A. Ml','Caldwell, E. Joi','Lindsay, C. Quc','Glaeser, E. Las','Mann, H. Hill','Corle, E. Fig','Mason, V. ~w','Roth, H. Gal','Gollomb. J. t','Weathenvax','Adamlc, L. Qi','Blake, £2., ps','Lion, H. The','Spitzer, A. Tl','Zara, 1L.. TiU-s','See','MacMullan','Boyd, J. Re','De La Roc','Cram, M. Fc','Flct','Oil','Lu','Bit','Cod','Foe','Oiri','Jon','Mat','Seyi','Thii','Tun','App','Barr','Bars','So','Cann','Char','Cunn','Fairt','Farni','Fores','Gibbs','Jeffri','Jeffrii','Kenni','Che','Marqi','Meyni','Parkn','Scogg','Wheal','Fernar','Fesslei','Hopkin','Annu','Flandrs','Worthir','Addlngto','My','Collections','Brgggn, A. Wind between the', 'Underngian. F. B. On a passing', 'Richardson, H: H. Fortunes of',
                  'Military servitude and', 'Humphrey, Z. Home', 'Mr', 'States in war-time', 'Strange story of William',
                  'Son of', 'Island of', 'Nathan. it', 'Adventures in', 'When the king losses his',
                  'Short stories from', 'Famous detective']
# a list of subheadings, ususally name of places. Keep updating

subheadings = ['Weaf Virginia','Zimbabwe','Musashl','Mains','Manitoba stories','Soviet Union','Jews In Germany','Jews In the Soviet Union','East German short stories','Firestarter','Eowt','Hong Kono','Gordon','Cairo','Jews In Hungary','Jews in Russia','Extortion','Midnight','Persecutions','Kindergarten','Jewish in Germany','Juvenile literature','Anticipations','Galactic empires','Alexandra','Romania','Tinsel','Beet','King and rulers','Afrioa','Indian* of South','Negroes in England','Ceremony','Jews In the Southern States','Io wa','Senegal','Southern States','Jews fn Germany','Jews In Montreal','Jews In Peru','Custer','World War, 193S-19it','Swedo-Flnnish short stories','Yugoslavian','Oerman','Icelandic short stories','Puritans','Ordinary people','Classical','Malawi','Middle West','Hes','Arctic reoion','Snow walker','Harinirto','Orarks','Architecture','Swedo-Finnlsh short stories','Georpia','Scotch','Treatment','Afrikaani','Annlv','Borchert','Africa. Wett','For East','Bong Kong','Ireland. Republic of','Itrael','Macao','Mittittippi','United Btatee','Pheatante','Negroes in the West Indies','Ireland. Northern','SffWt','Africa. East','Bees','Rabbits','Sepoy Rebellion','Asia. Southeastern','Northern Ireland','Negroes In Africa','Negroes In Egypt','Evanish','Hawks','Pigs','Western','Grossbach','Jews In Canada','Jews in Germany','Napoleonic Ware','Cheetahs','Jews In Italy','Jews in Spain','Oreat Britain','British Honduras','Farocse','Frenoh','Georgian','Social and moral questions','Woman','Technique','Moon','Outer space','United State*','Serbo-Croatian','Bwediah','Africa, Bouth','Europe, Eastern','Ghana','Nigeria','Bears','Fiahea','Gazelles','Social and moral Questions','Frenoft','Carribbean Area','Sargasso Sea','Tunisia','Mongols','Jews In Austria','Jews in Europe','Dolphins','Bortea','East Prussia','Germanv','Indian Ocean','Malaysia','New Meacico','Afrikaans','Bulgarian','Oriental','Bulgaria','Malavtia','Southwest','Aegean Islands','Asia, Southwestern','Austro-Hungarian border','Bulgaria','Caribbean ared','Foaces','Indie','Coloraao','Euvpt','Enuland','Hauyaiian Islands','Ivdiina','Vietnam','Yemen','Indochina, Frenoh','Inquisition','Sicilv','Jews In Africa','Jews In Russia','Black Sea','Costa Rica','Kuwait','Penguins','Agency','Thailand','Irass','Amazon River','Baja California','Baltio states','Carribean area','El Salvador','Jamaioa','Laos','Long Island Bound','Hall','Maldive Islands','Haldeman','Cruaadea','Church history','Nativity','Jews In Egypt','Jews in Palestine','Ferrets','Kidnapping','Monkeys','Passenger pigeons','Snakes','New Bngland','FrencJi','Uoghrebi','Middle Aoet','Northwest, Old','Bono Kong','Luxembourg','Maloya','MeeHoo','Near Bast','New Bangland','Mauriac','Cots','Great auk','Germ on','Icelandio','Portuouete','Rutrian','Berbo-Oroat','Spanith','Atia','Cambodia','Canada, Northern','Franca','Georoia','Ifeio England','PortuflOl','Zanzibar','Africa. South','Groat Britain','Grtaot','South African War, lS99-190t','Jews in Austria','Jews in Canada','Jews in England','Jews In Europe','Jews in Hungary','Buffaloes','Cattle','Oryx','Bioilv','Jews In South Africa','Czech','Malavalam','Berbo-Croat','Latin America','Mediterranean area','Oceania','Bootland','Glpsc','Africa, South','Balkan States','Gibraltar','Indoohina','Jews In Czechoslovakia','Jews In England','Jews in Poland','Binge','Jews In South America','Middle Ages','Napoleonic Wars','Reformation','Bioliv','Bethnal','Doot','Boos','Parrots','Whales','Benpatt','Nonoigtao','Fiii','Gettysburg, Battle of','Jtalv','Smith Carolina','Sowt','Bungarv','New Caledonia','Norwau','Biottll','Rats','Sometime','Cxech','Persian','Nepal','Del','Mal','Eovvt','Bnaland','Lewis and Clark expedition','Poeatam','Ruaaia','Brltiah Guiana','Cyprus','Germanu','Malava','Moluccas','Cati','Don','Andorra','Hong Kong','Martinique','Segregation','Flights','New Hebrides','North Dakota','Pakistan','South Beas','Teaas','Viet Nam','Wight, Isle of','Anatolia','Asia, Southeastern','British Ouiana','Caribbean area','Corfu','Estonia','Indochina, French','Indonesia','Judea','Monaco','Oali/ornia','Early Christiana','Hanaeatic league','Hispaniola','Judea','JftMOWi','Palmyra','Punio wars','Sharks','Jew* In Germany','Jews In Poland','Alps','Brittoh Quiana','Faroe Island','Lebanon','Majorca','Middle East','Puerto Hico','South Beat','Japanttt','Middle, ages','Nicaragua','South- America','Walet','Conquistadores','Bispaniola','Korean war, nso','Mexioo','Northwest, Paoiflo','Africa, East','Korea','New Hebridet','Rutaia','Sardinia','Sealt','Babylonia','Napoleonic wart','Catalonia','Indochina','Minorca','Natal','Nev> Hampshire','North Africa','Wast Indies','Panama Canal','United Statet','Africa, Wett','Alia','Mozambique','Bouth Africa','Azores','British Guiana','Ouba','Lithuania','Latin','Ozechoslovakia','Himalaya Mountains','Net; ado','Okinawa','Bouth Sea islands','Teacas','Annual','Oanada','Early Christians','Sepoy rebellion','Seals','Abyssinia','Guam','Iran','Bioily','Trinidad','Romanian','Transvaal','Vnitod States','Indian war','Oeark mountains','Stool','Transvaal','Oreek','Israel','Trebizond, Empire of','Man/land','Nino Hampshire','Tripoli','Arabic','Easter island','Mediterranean Sea','Serbo-Croat','Spanish civil war, J9.1B-l9.iy','Albania','Great Plains region','Illinoii','Indn-Chimi, French','Madagascar','Panama canal','Patagonia','Sahara desert','Smith America','Vtah','Built','Dogi','Honei','Vff','Jeruialcm','Htxico','Alatka','Aleutian Islands','Aritona','Brattt','Santo Domingo','South Seas','Dontek','Gorman','Africa, French West','Tlanin islands','Brcutil','Qreeoe','Qerman','Rutsian','Bai/pt','Hank','Uruguay','Polith','Ruttian','Epvpt','Missouri river','Control America','Colombia','CoZorodo','Mississippi valley','Smith. John','Charles V, emperor of the Holy','Roman empire','Paine, Thomas','Sacayawea','Great Plaint region','Libya','Nan tucket','Netherlands Indies','Puerto Rico','Yugoslavia','Moses','Koheson, Paul','Rubens, Sir Peter Paul','Villon, Francois','Hamilton, Emma, lady','Jo.iephua, Flavins','Mansfield, Katharine','Mary Stuart, queen of Soots','Bernadette Souoirous, Saint','Boulanger, Georges Ernest','Jean Marie','Crockett, David','Dickinson, Emily','Czechoslovakian','Samoan islands','Sark','Virgin Islands','Aland ialanda','Alaaka','Alaace','Aran ialanda','Arctio regions','Nova Scotia','Taughan, Benry','Women in business','Stories about','North America','Oftio','West','Kepler, Johann','Paganini, Niccolb','Parris, Samuel','Stiegel, Benry William','Fersen, Hans Axel von, gre/ve','Galilei, Galileo','Glendower, Owen','Jones, John Paul','Doas','Borsss','Clark, George Rogers','Deburau, Jean Gaspard','Elisha ben Abuyah','Bahamas','Northwest, Paoifio','Ukraine','Napoleonio wars','Northwest, Pacific','Shakespeare, William','Socrates','Vaughan, Henry','Washington, George','Kepler, Johnun','Lamb, Charles','Lincoln, Abraham','Paaanini, Niooolo','Parria, Samuel','Ufe','Bronte family','Clark, George Rogeri','Klislia ben Abuyah','Graf, Frau Theresa Heimrath','Indians of South America','Oats','Sorfc','Virgin Inlands','Ws»t Virginia','Bermuda islands','Bessarabia','Nantucket','Near East','Hampshire','Samoan Islands','Wart','Whaling','Supernatural phenomena','European war','Genoa','Ohio valley','Arctic regiont','Carolines','QaUcia','Greek, Modern','Russo-Japanese war','Mules','Squirrels','Byzantine empire','Delaware','Nevi Mexico','Transylvania','Barbary states','Aland islands','Oarollnaa','Dakotaa','Galicia','Mnlay archipelago','Shipwrecks','Birds','Middle ogee','Cttchotlovakian','Indo-OMna','Malay archipelago','Porto Rico','Siam','Channel islands','Czechoslovakia','Dakotas','Dutoh East Indies','Honduras','Africa, West','Antarctio regions','Arkansas','Asia, Central','Bramti','Canary islands','Napoleonic ware','Punic wars','Waterloo, Battle of','Apes','Chamois','Coyotes','Deer','Elephants','Raccoons','Wolverines','Wolves','Citchoilovakian','Rwisian','Ukrainian','Jugoslavia','Macedonia','Mississippl','Ozark mountains','Prince Edward Island','Hawaiiat','Africa, Central','Antarctic regions','Asia','Asin, Central','Bttlknn states','Bermuda inlands','Napoleonic wars','Paraguay','Punic tears','Rif revolt','Horsm','Lions','Reindeer','Tigers','Guatemala','Bali','Bolivia','Europe','Himalaya mountains','Mallorca','Pitcaim island','Rhode Island','Rhodes','Sumatra','Tasmania','Dant*k','Bebreto','Canary Islands','Caribbean tea','Ctecho-Slovakia','Indo-China, French','Jamaica','Orkney islands','Itorocoo','Scotia','Rhode Itland','Tahiti','Tunis','Utah','Yukon','Religious psychology','Spanifh','Bermuda','Caribbean sea','Ecuador','Himalayas','Hindustan','Isle of Wight','Malay Archipelago','Flandert','Haiti','Cats','Dogs','Foxes','Horses','Icelandic','Sesuto','Prince Edward island','Slam','Silesia','Cenrral America','Indo-Ohina','Kurdistan','Liberia','Malay Peninsula','Mississippi River','Aleutian islands','Amazon river','Basque country','Burgundy','Cape May','Capri','Carolinas','Bosnia','Oarolinas','Spanish America','Tyrol','Rumanian','Italv','MiiltiH Peninsula','Manchuria','Mongolia','Provence','Rumania','Sahara Desert','Brazil','Saxony','Afghanistan','Alabama','Channel Islands','Flanders','French Guiana','Formosa','Geneva','Malaya','Rhodesia','Riviera','Alatko','Alsace','Arabia','Assyria','Bay of Fundy','Cape Mny','Dutch East Indies','Carthage','Crete','Serbia','United Stales','Companionate marriage','Philippine islands','St Louis','Sioilv','Snutli Africa','Spate','Tibet','Vancouver island','Hebrides','Malta','Maryland','Morocco','New Hampshire','Newfoundland','Normandy','Panama','OaroHnat','Africa, North','Gape Cod','Cleveland','Cornwall','East Indies','Hawaiian islands','Madrid','Vein England','Xcw Mexico','Peking','Peru','Kan Francisco','Wyoming','Copenhagen','Dalmatia','Dublin','Great Lakes region','Idaho','Indo- China','Itle of Man','Arctic regions','Bagdad','Bavaria','Bucharest','Oapri','Oarolinaa','Central America','Crusades','Note Orleans','Bpatn','Chinese','Chechoslovakian','PoUth','West Indict','Witconsin','Wyominu','Yucatan','Neic England','Hew Guinea','Oklahoma','Ontario','Persia','Rio de Janeiro','Venl&s','Monte Carlo','Near Eatt','Uatne','Ualava','Manila','Uari/land','Mosaachutettt','Jfeoico','Uitslttippi','Greenland','Indo China','Isle of Uan','Kantas','Lapland','Long Itland','Louiiiana','Alaika','Borneo','Itrilisli Columbia','Charleston','Croatia','Esthonla','Far Edit','Oaul','Home','Scandinavia','Wett Indies','Ciechoslovakian','Sicily','South sens','Syria','Viri/inia','Cambridge','Cave Cod','Florence','Illinois','InAo China','Koine','New Enylanil','Rtusia','Acadia','Poltoh','Stoediih','Metrico','New York','Borne','Vienna','Wala','West Indiei','Indo-CMna','Iowa','Lapand','London','Manitoba','Xew Enuland','New Guinea','New Jersey','Balkan states','Went Indies','Algiers','Berlin','Burma','Esthonia','Ethiopia','Hawaii','Ktissian','West Indies','Louisville','Hear East','Hew England','Salem','Singapore','Koutlt Africa','South Dakota','Gaul','Argentina','British Columbia','Brittany','Budapest','Crotia','Glasgow','Isle of Man','Hungarian','Portuguete','Servian','Nor wan','Quebec','San Francitco','Texas','Watts','Ceylon','Ituly','Uaryland','Massachusetts','Nevada','Hew Knylunil','Xortli Carolina','America','Danith','Finnish','Roumanian','Kussian','Vermont','Wett Virginia','Wiscontin','Son Francisco','Siberia','Bovth Africa','Snain','Tat mania','Tennessee','Venezuela','Mississippi','Montana','Weie Orleani','New Zealand','Norway','Porte','Rangoon','BraMil','Brooklyn','Colorado','Corsica','Dakota','Epvft','Par Bait','Finland','Java','Maine','Hussion','United State t','Hunyary','Parit','Byzantium','Mii/ille aget','Ultt0vri','Netli erlandt','Portuyal','Balkan', 'Itoumunian', 'New Mexico', 'Philippine Islands', 'Imeden', 'Syracuse', 'Algeria', 'Baltimore',
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
nextheadings = ['Fiction and repetition. Miller, J. H.','Fiction as wisdom. Stock, L · , ,','Field guide to North American rocks and','Fiction and the ways of knowing. Fleishman, A.','Fiction and the Action industry. Sutherland, J. A','Fiction and the Action industry. Sutherland, J. A','Fiction as knowledge. McCormick, J.','Fiction and the camera eye. Spiegel, A.','Fiction, English. See English Action','Fiction & the colonial experience. Meyers. J.','Fiction of Jack London. Walker. D. L. (Ag "73)','Fiction, American. See American Action','Finance, Personal . . ...','Fiction, American. See American fiction','Fiction of E. M. Forster. Thomson, G. H. (Ja','Fiction; v. 1 of Southern writing in the sixties.','Fiction in public libraries, 1S76-1900. Carrier,','Field, Noel Havlland','Fiction of the forties. Elslnger. C. B. (Mr\'64)','Field, James Thomas','Field administration in the United Nations','Field guide to reptiles and amphibians. Conant,','Fiction and the unconscious. Lesser, S. O. (Ap','Fiction fights the Civil war. Lively. R. A.','Fiction factory. Reynolds. Q. J. (Mr \'6*)','Fiction factory. Reynolds. Q. J. (Mr \'6*)','Fiction goes to court. Blausteln, A, P.. ed.','Field full of people. Hazel, R. (D \'54)','Fiddle, a sword, and a lady. Spaldlng, A.','Fiddling cowboy In search of gold. Regll, A.','Flddlefoot. Glidden, F. D. (Ag \'49) _','Fiddler crab and the sand dollar. Henle, M. E.','Flddlefoot. Glidden, F. D. (Ag \'49)','Fidus Achatea. Eng title of: Paris of Troy.','Field guide to the birds. [2d rev & enl ed].','Fiction catalog, 1941. (My \'43)','Fifty years of_ best sellers. 1896-1945. Hackett.','Fiddler In the sky. Homeland, K. (Je \'44)','Fiction catalog. 1941. (My \'43)','Fiddle Longspay. Bledsoe, W. (Ag \'42)','Fiction writing self-taught. Hoffman, A. S.','Field of honor. St Johns, A. (S \'38)','Field, Cyrus West','Fiddler\'s coin. Abbott, J. L. (S \'34)','Fields of Gomorrah. White, N. (N \'35)','Fiddler\'s coin. Abbott, J. L,. (S \'34)','Field book of the shore fishes of Bermuda.','Fifteen and five. Bernstein. A. (Ag \'32)','Fiddler. Mlllln, S. G. (S \'29)','Field, David Dudley','Fiddler. Mlllin. S. G. (S \'29)','Field book of common ferns. Durand, H. (D','Fiction as she is wrote. Knox, E. G: V. (D','Field book of common rocks and minerals.','Field, Eugene','Fiddler\'s luck. Schauffler, R. H. (Jl JO)','Fiddler\'s luck. Schauﬂier, R. H. (Jl \'20)','Fiddier\'s luck. _ Schauﬂ\'ler, R. H. (.11 \'20)', 'Field ambulance sketches. (N \'19',
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
pattern2 = re.compile("[A-Z][ ]?[a-z]+")
pattern2_1 = re.compile(" [A-Z][ ]?[a-z]+")
pattern2_2 = re.compile("[.:]\s[A-Z][ ]?[a-z]+")


year = ['1921','1922','1923','1924','1925','1926','1927','1928','1929','1930','1931','1932','1933','1934','1935','1936','1937','1938','1939','1940','1941','1942','1943','1944','1945','1946','1947','1948','1949','1950','1951','1952','1953','1954','1955','1956','1957','1958','1959','1962','1963','1964','1965','1966','1967','1968','1969','1970','1971','1972','1973','1974','1975','1976','1977','1978','1979','1980','1981','1982','1983']
suffix = ['32106019850368','32106019610374','32106019610382','32106019610390','32106019610408','32106019610416','32106019610424','32106019610432','32106019610440','32106019610457','39015078261180','32106019610465','32106019610473','32106019610481','32106019610499','39015078261230','32106019610507','32106019610515','32106019610523','32106019610531','39015078261289','32106019610549','32106019610556','32106019610564','32106019610572','32106019610580','32106019610598','32106019610606','32106019610614','39015078261370','39015078261388','32106019610622','32106019610630','32106019610648','32106019610655','39015078261438','32106019610663','32106019610671','32106019610689','39015078261495','32106019848347','39015078261511','39015078261529','39015078261537','39015078261552','39015078261560','39015078261578','39015078261586','39015078261594','39015078261610','39015078261628','39015078261636','39015078261685','39015078261693','39015078261701','39015078261719','39015078261727','39015078261735','30000114363868','39015078261750','39015078261768']

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
    volume1972=0
    volume1976_and_later=0
    volume1983=0
    if(year=='1935'):
        volume1935=1
    if(year=='1944'):
        volume1944=1
    if(year=='1972'):
        volume1972=1
    if(int(year)>=1976):
        volume1976_and_later=1
    if(year=='1983'):
        volume1983=1
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
    headingcount_fiction_about = 0
    headingcount_fiction_genre = 0
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
                if(volume1983==1):
                    print(pagelist[i][j])
                if(volume1976_and_later==0):
                    bookcount += pagelist[i][j].count('(')  # how many books are there in the index in total
                else:
                    if('.' in pagelist[i][j]):
                        bookcount+=1
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

            if (text[j] == "Fiction (books about)" or text[j] == "Fiction (Books about)"):
                for k in range(10):
                    print(text[j+k])
                for k in list(range(1, linelength - j)):
                    if (text[j + k] == "Fiction (classified by subject)" or text[j+k]=='Fiction (classified according to subject)' or text[j+k]=='Fiction (c\'assifled according to subject)'):  # if fiction section_about ends
                        break
                    if (text[j + k] == "Fiction"):
                        text[j+k] = "Fiction (classified by subject)"
                        break
                    if (volume1935==1 and text[j+k]=='1161'):
                        text[j + k-1] = "Fiction (classified by subject)"
                        text[j + k] = "Animal stories"
                        break
                    if volume1976_and_later==0 and '(' in text[j + k]:
                        bookcount_fiction_about += 1
                    elif(volume1976_and_later==1 and '.' in text[j+k]):
                        bookcount_fiction_about+=1
                    if ((volume1976_and_later==0 and len(text[j + k]) > 1 and len(text[k + j]) <= 30 and '(' not in text[
                        k + j] and '\'' not in text[
                        k + j]) or (volume1976_and_later==1 and len(text[j + k]) > 1 and '.' not in text[
                        k + j] and '\'' not in text[
                        k + j])):  # must be at least 2 characters, no more than 25 characters (avoiding titles not finished in a line to be included, not including '(' to avoid OCR error) # next line beginning with non-characterized character
                        if (text[k + j][0] >= 'A' and text[k + j][0] <= 'Z' and text[k + j][1] >= 'a' and
                                text[k + j][1] <= 'z' and (
                                        text[k + j][-1] >= 'a' and text[k + j][-1] <= 'z' or text[
                                    k + j] == ':') and text[k + j] not in subheadings and text[
                                k + j] not in wrong_headings and text [k+j][-11:]!='Collections' and text[k+j][0:13]!='United States' and text[k+j][0:13]!='United State*' and text[k+j][0:13]!='United Btates' and text[k+j][0:13]!='United Slutcs' and text[k+j][0:12]!='United 8tate' and text[k+j][-13:]!='United States' and text[k+j][0:6]!='France' and text[k+j][0:6]!='Russia' and text[k+j][0:7]!='America' and text[k+j][0:7]!='England' and text[k+j][0:7]!='Britain' and text[k+j][0:13]!='Great Britain' and text[k+j][0:13]!='Qreat Britain' and text[k+j][0:7]!='Germany' and text[k+j][0:7]!='Austria' and (text[k+j][0:12]!='Soviet Union' or text[k+j][13:]!='1911-19tl, Revolution') and (text[k+j][0:6]!='States' or text[k+j][-18:]!='Nineteenth century') and (text[k+j][0:11]!='Inquisition' or text[k+j][12:17]!='Spain') and text[k+j][0:11]!='Set Fiction' and text[k+j][0:11]!='Bee Fiction' and (text[k+j][0:7]!='Fiction' or text[k+j][8:17]!='Ciintinui') and (text[k+j][0:3]!='Pru' or text[k+j][5:7]!='io' and (text[k+j][0:7]!='Fiction' or text[k+j][8:13]!='Youth') and (text[k+j][0:7]!='Fiction' or text[k+j][8:22]!='Mental illness') and (text[k+j][0:7]!='Fiction' or text[k+j][8:27]!='United States. Navy') and (text[k+j][0:7]!='Fiction' or text[k+j][8:21]!='Race problems') and (text[k+j][0:7]!='Fiction' or text[k+j][8:21]!='Psychiatrists') and (text[k+j][0:7]!='Fiction' or text[k+j][8:16]!='Surgeons') and (text[k+j][0:7]!='Fiction' or text[k+j][8:17]!='Espionage') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Chicago. University') and (text[k+j][0:7]!='Fiction' or text[k+j][10:]!='Oxiord. University') and (text[k+j][0:7]!='Fiction' or text[k+j][10:]!='School life') and (text[k+j][0:7]!='Fiction' or text[k+j][10:]!='Vassar College') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='College life') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Catholic priests') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Poets') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Teachers') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Spies') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Allegories') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Navaho Indians') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='International intrigue') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Poker') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Espionage') and (text[k+j][0:11]!='Sea Fiction' or text[k+j][12:]!='Feminism') and (text[k+j][0:11]!='Sea Fiction' or text[k+j][12:]!='Politics') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Atomic warfare') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Homosexuality') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Atomic submarines') and (text[k+j][0:26]!='Swados, H. Story for Teddy' or text[k+j][-3:]!='and') and (text[k+j][0:11]!='Sea Fiction' or text[k+j][12:]!='Refugees') and (text[k+j][0:7]!='Germanv' or text[k+j][8:]!='Nasi movement') and (text[k+j][0:5]!='Papua' or text[k+j][6:]!='New Guinea'))):  # For wrong headings, ignore them; first character A-Z, second a-z (avoiding "BOOK REVIEW DIGEST"), last a-z or 0-9 (eg "Adams, Henry, 1838-1918")
                            if (len(text[
                                        k + j]) >= 4):  # Sometimes a heading contains no books, but direct to "See other sections"
                                if (text[k + j][:4] in ['See ', 'Sec ', 'Sac ']):
                                    continue
                            if len(text[j + k]) >= 9:  # not "xxx-Continued"
                                if (text[j + k][-9:] in ['Continued', 'Continucd','Uontinued','Continual',' ontinued']):
                                    continue
                            fiction_headings.append(text[k + j])  # Otherwise, add that heading into the list or (text[k+j][0:7]=='Fiction' and text[k+j][10:]=='Vassar College')
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
                        headingcount_fiction_about+=1
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
            if (text[j] == "Fiction (classified by subject)" or text[j]=='Fiction (classified according to subject)' or text[j]=='Fiction (c\'assifled according to subject)'):
                for k in list(range(1, linelength - j)):
                    if (text[j + k] in nextheadings or text[j+k][0:28]=='Fiction as wisdom. Stock, L '):  # if fiction section ends
                        break
                    if volume1976_and_later==0 and '(' in text[j + k]:
                        bookcount_fiction_genre += 1
                    elif(volume1976_and_later==1 and '.' in text[j+k]):
                        bookcount_fiction_genre +=1
                    if text[j+k]=='Women\'s army corps' or text[j+k]=='World war, 1939-' or text[j+k]=='World war, 1939-1945' or text[j+k]=='World war, 1939-1946':
                        fiction_headings.append(text[k + j])  # Otherwise, add that heading into the list
                        fiction_books.append(
                            [])  # add an empty list to the booklist, to match the headinglist
                        count += 1  # to count the number of lists in the booklist
                    elif ((volume1976_and_later ==0 and len(text[j + k]) > 1 and len(
                                text[k + j]) <= 30 and '(' not in text[
                                 k + j] and '\'' not in text[
                                 k + j]) or (volume1976_and_later == 1 and len(text[j + k]) > 1 and '.' not in text[
                            k + j] and '\'' not in text[
                                                 k + j])):  # must be at least 2 characters, no more than 25 characters (avoiding titles not finished in a line to be included, not including '(' to avoid OCR error) # next line beginning with non-characterized character
                        if (text[k + j][0] >= 'A' and text[k + j][0] <= 'Z' and text[k + j][1] >= 'a' and
                                    text[k + j][1] <= 'z' and (text[k + j][-1] >= 'a' and text[k + j][-1] <= 'z' or text[k + j] == ':') and text[k + j] not in subheadings and text[
                                k + j] not in wrong_headings and text [k+j][-11:]!='Collections' and text[k+j][0:13]!='United States' and text[k+j][0:13]!='United State*' and text[k+j][0:13]!='United Btates' and text[k+j][0:13]!='United Slutcs' and text[k+j][0:12]!='United 8tate' and text[k+j][-13:]!='United States' and text[k+j][0:6]!='France' and text[k+j][0:6]!='Russia' and text[k+j][0:7]!='America' and text[k+j][0:7]!='England' and text[k+j][0:7]!='Britain' and text[k+j][0:13]!='Great Britain' and text[k+j][0:13]!='Qreat Britain' and text[k+j][0:7]!='Germany' and text[k+j][0:7]!='Austria' and (text[k+j][0:12]!='Soviet Union' or text[k+j][13:]!='1911-19tl, Revolution') and (text[k+j][0:6]!='States' or text[k+j][-18:]!='Nineteenth century') and (text[k+j][0:11]!='Inquisition' or text[k+j][12:17]!='Spain') and text[k+j][0:11]!='Set Fiction' and text[k+j][0:11]!='Bee Fiction' and (text[k+j][0:7]!='Fiction' or text[k+j][8:17]!='Ciintinui') and (text[k+j][0:3]!='Pru' or text[k+j][5:7]!='io' and (text[k+j][0:7]!='Fiction' or text[k+j][8:13]!='Youth') and (text[k+j][0:7]!='Fiction' or text[k+j][8:22]!='Mental illness') and (text[k+j][0:7]!='Fiction' or text[k+j][8:27]!='United States. Navy') and (text[k+j][0:7]!='Fiction' or text[k+j][8:21]!='Race problems') and (text[k+j][0:7]!='Fiction' or text[k+j][8:21]!='Psychiatrists') and (text[k+j][0:7]!='Fiction' or text[k+j][8:16]!='Surgeons') and (text[k+j][0:7]!='Fiction' or text[k+j][8:17]!='Espionage') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Chicago. University') and (text[k+j][0:7]!='Fiction' or text[k+j][10:]!='Oxiord. University') and (text[k+j][0:7]!='Fiction' or text[k+j][10:]!='School life') and (text[k+j][0:7]!='Fiction' or text[k+j][10:]!='Vassar College') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='College life') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Catholic priests') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Poets') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Teachers') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Spies') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Allegories') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Navaho Indians') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='International intrigue') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Poker') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Espionage') and (text[k+j][0:11]!='Sea Fiction' or text[k+j][12:]!='Feminism') and (text[k+j][0:11]!='Sea Fiction' or text[k+j][12:]!='Politics') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Atomic warfare') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Homosexuality') and (text[k+j][0:7]!='Fiction' or text[k+j][8:]!='Atomic submarines') and (text[k+j][0:26]!='Swados, H. Story for Teddy' or text[k+j][-3:]!='and') and (text[k+j][0:11]!='Sea Fiction' or text[k+j][12:]!='Refugees') and (text[k+j][0:7]!='Germanv' or text[k+j][8:]!='Nasi movement') and (text[k+j][0:5]!='Papua' or text[k+j][6:]!='New Guinea'))):  # For wrong headings, ignore them; first character A-Z, second a-z (avoiding "BOOK REVIEW DIGEST"), last a-z or 0-9 (eg "Adams, Henry, 1838-1918")
                            if (len(text[
                                        k + j]) >= 4):  # Sometimes a heading contains no books, but direct to "See other sections"
                                if (text[k + j][:4] in ['See ', 'Sec ', 'Sac ']):
                                    continue
                            if len(text[j + k]) >= 9:  # not "xxx-Continued"
                                if (text[j + k][-9:] in ['Continued', 'Continucd','Uontinued','Continual',' ontinued']):
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
                        headingcount_fiction_genre += 1
                        print('<\heading "%s">' % fiction_headings[
                            k])  # print headings and all the content of each heading
                        count = -1
                        for m in list(range(len(fiction_books[k]))):
                            if(fiction_headings[k]=='Women' or [k]=='Young people' or fiction_headings[k]=='Youth' or fiction_headings[k]=='Zionism' or fiction_headings[k]=='Zoological gardens' or fiction_headings[k]=='Women in Industry' or fiction_headings[k]=='World war, 1939-' or fiction_headings[k]=='Weird stories' or fiction_headings[k]=='World war, 1939-1946' or fiction_headings[k]=='World war, 1939-1945' or fiction_headings[k]=='Whaling industry' or fiction_headings[k]=='Writers' or fiction_headings[k]=='Zoological specimens' or fiction_headings[k]=='Collection and preservation'):
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
        print(headingcount_fiction_about)
        print(headingcount_fiction_genre)
        print(index_startpage, index_endpage)

    if flag == 0:  # if the volume doesn't have an index, print it out and end
        print('Volume number %d: no index found in this volume' % (volume_id))
        index_startpage[i] = 'N/A'
        index_endpage[i] = 'N/A'

#if __name__ == '__main__':
#    main()