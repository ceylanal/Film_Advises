
import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
import os



# Gömülü Veri Seti (CSV dosyasındaki gerçek veriler ve Top 10 için atanmış poster yolları)
CSV_DATA = """Const,Your Rating,Date Rated,Title,Original Title,URL,Title Type,IMDb Rating,Runtime (mins),Year,Genres,Num Votes,Release Date,Directors,poster_path
tt0133093,9,2026-01-01,"Matrix","The Matrix",https://www.imdb.com/title/tt0133093,Movie,8.7,136,1999,"Action, Sci-Fi",2215161,"1999-09-03","Lana Wachowski,Lilly Wachowski"
tt0276919,8,2025-12-21,"Kibirli Kasaba","Dogville",https://www.imdb.com/title/tt0276919,Movie,8.0,171,2003,"Drama, Crime",167053,"2003-12-05","Lars von Trier"
tt1596345,7,2025-10-26,"Şah Mat","Pawn Sacrifice",https://www.imdb.com/title/tt1596345,Movie,7.0,115,2014,"Drama, Biography, Sport, Thriller, History",53517,"2015-10-02","Edward Zwick"
tt1120985,7,2025-10-11,"Aşk ve Küller","Blue Valentine",https://www.imdb.com/title/tt1120985,Movie,7.3,112,2010,"Romance, Drama",222907,"2011-07-08","Derek Cianfrance"
tt1492966,7,2025-09-25,"Louie","Louie",https://www.imdb.com/title/tt1492966,TV Series,8.5,22,2010,"Comedy, Drama",84894,"2010-06-29",
tt6226232,7,2025-09-25,"Young Sheldon","Young Sheldon",https://www.imdb.com/title/tt6226232,TV Series,7.7,30,2017,"Comedy",141550,"2017-10-27",
tt0208092,7,2025-09-17,"Kapışma","Snatch",https://www.imdb.com/title/tt0208092,Movie,8.2,104,2000,"Comedy, Crime",965791,"2000-11-10","Guy Ritchie"
tt0172495,7,2025-09-17,"Gladyatör","Gladiator",https://www.imdb.com/title/tt0172495,Movie,8.5,155,2000,"Adventure, Drama, Action",1818812,"2000-05-19","Ridley Scott"
tt0088763,8,2025-09-17,"Geleceğe Dönüş","Back to the Future",https://www.imdb.com/title/tt0088763,Movie,8.5,116,1985,"Comedy, Sci-Fi, Adventure",1427635,"1987-02-14","Robert Zemeckis"
tt0120689,7,2025-09-17,"Yeşil Yol","The Green Mile",https://www.imdb.com/title/tt0120689,Movie,8.6,189,1999,"Crime, Fantasy, Mystery, Drama",1535473,"2000-03-17","Frank Darabont"
tt0137523,9,2025-09-17,"Dövüş Kulübü","Fight Club",https://www.imdb.com/title/tt0137523,Movie,8.8,139,1999,"Drama, Crime, Thriller",2553738,"1999-12-10","David Fincher"
tt1375666,8,2025-09-17,"Başlangıç","Inception",https://www.imdb.com/title/tt1375666,Movie,8.8,148,2010,"Sci-Fi, Thriller, Action, Adventure",2768124,"2010-07-30","Christopher Nolan"
tt0167261,9,2025-09-17,"Yüzüklerin Efendisi: İki Kule","The Lord of the Rings: The Two Towers",https://www.imdb.com/title/tt0167261,Movie,8.8,179,2002,"Drama, Adventure, Fantasy",1925425,"2002-12-20","Peter Jackson"
tt0120737,9,2025-09-17,"Yüzüklerin Efendisi: Yüzük Kardeşliği","The Lord of the Rings: The Fellowship of the Ring",https://www.imdb.com/title/tt0120737,Movie,8.9,178,2001,"Drama, Adventure, Fantasy",2169403,"2001-12-21","Peter Jackson"
tt0108052,8,2025-09-17,"Schindler'in Listesi","Schindler's List",https://www.imdb.com/title/tt0108052,Movie,9.0,195,1993,"Biography, History, Drama",1565552,"1994-03-04","Steven Spielberg"
tt0167260,9,2025-09-17,"Yüzüklerin Efendisi: Kralın Dönüşü","The Lord of the Rings: The Return of the King",https://www.imdb.com/title/tt0167260,Movie,9.0,201,2003,"Drama, Adventure, Fantasy",2131597,"2003-12-19","Peter Jackson"
tt0068646,8,2025-09-17,"Baba","The Godfather",https://www.imdb.com/title/tt0068646,Movie,9.2,175,1972,"Crime, Drama",2190710,"1973-10","Francis Ford Coppola"
tt0111161,8,2025-09-17,"Esaretin Bedeli","The Shawshank Redemption",https://www.imdb.com/title/tt0111161,Movie,9.3,142,1994,"Drama",3138432,"1995-03-10","Frank Darabont"
tt0773262,6,2025-08-18,"Dexter","Dexter",https://www.imdb.com/title/tt0773262,TV Series,8.6,60,2006,"Crime, Drama, Mystery, Thriller",902338,"2006-10-01",
tt0425118,9,2025-08-14,"I Know This Much Is True","I Know This Much Is True",https://www.imdb.com/title/tt0425118,TV Mini Series,8.1,60,2020,"Drama",26856,"2020-05-10",
tt3032476,9,2025-08-13,"Better Call Saul","Better Call Saul",https://www.imdb.com/title/tt3032476,TV Series,9.0,45,2015,"Crime, Drama",791309,"2016-09-22",
tt1586680,10,2025-08-06,"Shameless","Shameless",https://www.imdb.com/title/tt1586680,TV Series,8.5,60,2011,"Comedy, Drama",325950,"2011-01-09","assets/posters/shameless.jpg"
tt1210166,8,2025-08-06,"Kazanma Sanatı","Moneyball",https://www.imdb.com/title/tt1210166,Movie,7.6,133,2011,"Drama, Sport, Biography",500610,"2011-12-09","Bennett Miller"
tt0075314,8,2025-08-06,"Taksi Şoförü","Taxi Driver",https://www.imdb.com/title/tt0075314,Movie,8.2,114,1976,"Crime, Drama",1009332,"1980-10-14","Martin Scorsese"
tt1343092,7,2025-08-06,"Muhteşem Gatsby","The Great Gatsby",https://www.imdb.com/title/tt1343092,Movie,7.2,143,2013,"Drama, Romance",634957,"2013-05-17","Baz Luhrmann"
tt6751668,9,2025-08-06,"Parazit","Gisaengchung",https://www.imdb.com/title/tt6751668,Movie,8.5,132,2019,"Drama, Thriller",1128410,"2019-11-01","Bong Joon Ho"
tt2397535,9,2025-08-06,"Zamanın Ötesinde","Predestination",https://www.imdb.com/title/tt2397535,Movie,7.4,97,2014,"Sci-Fi, Thriller, Drama, Action",330075,"2021-06-02","Michael Spierig,Peter Spierig"
tt0248654,10,2025-07-24,"Six Feet Under","Six Feet Under",https://www.imdb.com/title/tt0248654,TV Series,8.7,60,2001,"Comedy, Drama",164731,"2001-06-03","assets/posters/sixfeetunder.jpg"
tt7660850,7,2025-06-19,"Succession","Succession",https://www.imdb.com/title/tt7660850,TV Series,8.8,60,2018,"Drama, Comedy",341968,"2018-06-03",
tt11267076,5,2025-06-19,"Dayı: Bir Adamın Hikâyesi","Dayi: Bir Adamin Hikayesi",https://www.imdb.com/title/tt11267076,Movie,6.2,125,2021,"Action, Adventure, Drama",3390,"2021-12-10","Ugur Bayraktar"
tt2005151,8,2025-06-12,"Vurguncular","War Dogs",https://www.imdb.com/title/tt2005151,Movie,7.1,114,2016,"Comedy, Drama, War, Crime, Biography",290061,"2016-08-19","Todd Phillips"
tt0425080,6,2025-06-03,"Güz Sancisi","Güz Sancisi",https://www.imdb.com/title/tt0425080,Movie,6.1,112,2009,"Drama",2700,"2009-01-23","Tomris Giritlioglu"
tt0827503,6,2025-06-01,"Hokkabaz","Hokkabaz",https://www.imdb.com/title/tt0827503,Movie,7.4,122,2006,"Comedy, Drama",36225,"2006-10-20","Ali Taner Baltaci,Cem Yilmaz"
tt10272386,7,2025-05-26,"Baba","The Father",https://www.imdb.com/title/tt10272386,Movie,8.2,97,2020,"Drama, Mystery",239114,"2021-09-17","Florian Zeller"
tt0290673,7,2025-05-25,"Dönüş Yok","Irréversible",https://www.imdb.com/title/tt0290673,Movie,7.3,97,2002,"Crime, Mystery, Drama, Thriller",160316,"2002-11-29","Gaspar Noé"
tt1663202,8,2025-05-24,"Diriliş","The Revenant",https://www.imdb.com/title/tt1663202,Movie,8.0,156,2015,"Adventure, Drama, Western",934143,"2016-01-22","Alejandro G. Iñárritu"
tt7653254,9,2025-04-10,"Evlilik Hikayesi","Marriage Story",https://www.imdb.com/title/tt7653254,Movie,7.9,137,2019,"Drama, Romance",367694,"2019-12-06","Noah Baumbach"
tt0099077,8,2025-04-05,"Uyanışlar","Awakenings",https://www.imdb.com/title/tt0099077,Movie,7.8,121,1990,"Biography, Drama",174490,"1991-05-10","Penny Marshall"
tt28607951,8,2025-04-05,"Anora","Anora",https://www.imdb.com/title/tt28607951,Movie,7.4,139,2024,"Drama, Comedy, Romance",256051,"2024-11-01","Sean Baker"
tt28756876,9,2025-03-22,"Einstein ve Atom Bombası","Einstein and the Bomb",https://www.imdb.com/title/tt28756876,Movie,6.2,76,2024,"Documentary, History",4352,"2024-02-16","Anthony Philipson"
tt4084744,8,2025-01-21,"Bitva za Sevastopol","Bitva za Sevastopol",https://www.imdb.com/title/tt4084744,Movie,7.0,110,2015,"Biography, Drama, War, Romance, Action, History",15063,"2015-04-02","Sergey Mokritskiy"
tt21029674,10,2025-01-07,"Cezailer","Cezailer",https://www.imdb.com/title/tt21029674,TV Series,7.2,45,2022,"Drama",576,"2022-09-29","assets/posters/cezailer.jpg"
tt0482571,8,2024-12-28,"Prestij","The Prestige",https://www.imdb.com/title/tt0482571,Movie,8.5,130,2006,"Drama, Thriller, Mystery, Sci-Fi",1562202,"2006-12-22","Christopher Nolan"
tt0086465,3,2024-12-27,"Zengin ve Sefil","Trading Places",https://www.imdb.com/title/tt0086465,Movie,7.5,116,1983,"Comedy",180031,"1983-06-08","John Landis"
tt9764362,7,2024-12-12,"The Menu","The Menu",https://www.imdb.com/title/tt9764362,Movie,7.2,107,2022,"Horror, Thriller, Comedy",483742,"2022-11-18","Mark Mylod"
tt7405458,3,2024-11-30,"Hayata Röveşata Çeken Adam","A Man Called Otto",https://www.imdb.com/title/tt7405458,Movie,7.5,126,2022,"Comedy, Drama",204376,"2023-03-03","Marc Forster"
tt11315808,8,2024-11-14,"Joker: İkili Delilik","Joker: Folie à Deux",https://www.imdb.com/title/tt11315808,Movie,5.2,138,2024,"Musical, Thriller, Drama",176713,"2024-10-04","Todd Phillips"
tt1045658,8,2024-11-14,"Umut Işığım","Silver Linings Playbook",https://www.imdb.com/title/tt1045658,Movie,7.7,122,2012,"Comedy, Drama, Romance",768303,"2013-01-04","David O. Russell"
tt1850419,6,2024-11-11,"Gergedan Mevsimi","Fasle kargadan",https://www.imdb.com/title/tt1850419,Movie,6.3,88,2012,"Drama, Thriller",7565,"2012-10-26","Bahman Ghobadi"
tt1753866,7,2024-09-24,"Gişe Memuru","Gise Memuru",https://www.imdb.com/title/tt1753866,Movie,6.4,96,2010,"Drama",4863,"2011-05-06","Tolga Karaçelik"
tt0408017,7,2024-09-24,"Mustafa Hakkinda Hersey","Mustafa Hakkinda Hersey",https://www.imdb.com/title/tt0408017,Movie,7.5,119,2004,"Thriller, Drama",10110,"2004-03-19","Çagan Irmak"
tt0263438,9,2024-09-23,"Her Şey Çok Güzel Olacak","Her Sey Çok Güzel Olacak",https://www.imdb.com/title/tt0263438,Movie,8.1,107,1998,"Drama, Comedy",29816,"1998-11-27","Ömer Vargi"
tt1051907,9,2024-09-23,"Kabadayı","Kabadayi",https://www.imdb.com/title/tt1051907,Movie,7.8,140,2007,"Drama, Crime",25620,"2007-12-14","Ömer Vargi"
tt0875595,9,2024-09-23,"Kader","Kader",https://www.imdb.com/title/tt0875595,Movie,7.7,103,2006,"Drama",19846,"2006-11-17","Zeki Demirkubuz"
tt0200654,8,2024-09-23,"Gemide","Gemide",https://www.imdb.com/title/tt0200654,Movie,7.9,102,1998,"Crime, Drama",17135,"1998-12-04","Serdar Akar"
tt0880502,10,2024-09-23,"Yaşamın Kıyısında","Auf der anderen Seite",https://www.imdb.com/title/tt0880502,Movie,7.7,116,2007,"Drama",35235,"2007-10-26","Fatih Akin"
tt1347521,8,2024-09-23,"Günesi Gördüm","Günesi Gördüm",https://www.imdb.com/title/tt1347521,Movie,6.6,120,2009,"Drama",11584,"2009-03-13","Mahsun Kirmizigül"
tt1740299,8,2024-09-23,"Yüksek Şatodaki Adam","The Man in the High Castle",https://www.imdb.com/title/tt1740299,TV Series,7.9,60,2015,"Sci-Fi, Drama, Thriller",120396,"2015-11-24",
tt7318202,5,2024-09-15,"Kelebekler","Kelebekler",https://www.imdb.com/title/tt7318202,Movie,7.3,117,2018,"Drama, Comedy",20938,"2018-03-30","Tolga Karaçelik"
tt4309356,8,2024-09-15,"Sarmaşık","Sarmasik",https://www.imdb.com/title/tt4309356,Movie,7.9,104,2015,"Drama, Thriller, Fantasy",14552,"2015-12-04","Tolga Karaçelik"
tt1558877,7,2024-09-08,"Vavien","Vavien",https://www.imdb.com/title/tt1558877,Movie,7.5,100,2009,"Thriller, Comedy, Drama",14611,"2009-12-18","Durul Taylan,Yagmur Taylan"
tt1596363,9,2024-09-08,"Büyük Açık","The Big Short",https://www.imdb.com/title/tt1596363,Movie,7.8,130,2015,"Drama, Biography, Comedy, History",529419,"2016-01-08","Adam McKay"
tt2194499,8,2024-09-06,"Zamanda aşk","About Time",https://www.imdb.com/title/tt2194499,Movie,7.8,123,2013,"Drama, Fantasy, Romance, Comedy, Sci-Fi",425633,"2013-10-04","Richard Curtis"
tt1895587,8,2024-09-02,"Spotlight","Spotlight",https://www.imdb.com/title/tt1895587,Movie,8.1,129,2015,"Drama, Crime, Biography",529541,"2016-01-29","Tom McCarthy"
tt0095016,6,2024-09-02,"Zor Ölüm","Die Hard",https://www.imdb.com/title/tt0095016,Movie,8.2,132,1988,"Thriller, Action",1017802,"1990-01-26","John McTiernan"
tt0476735,10,2024-08-22,"Babam ve Oğlum","Babam ve Oglum",https://www.imdb.com/title/tt0476735,Movie,8.2,108,2005,"Drama, Family",99595,"2005-11-18","Çagan Irmak","assets/posters/babamveoglum.jpg"
tt2608224,8,2024-08-13,"Kelebeğin Rüyası","Kelebegin Rüyasi",https://www.imdb.com/title/tt2608224,Movie,7.6,138,2013,"Drama, Biography, History, Romance",25904,"2013-02-22","Yilmaz Erdogan"
tt1523515,5,2024-08-07,"Neşeli Hayat","Neseli Hayat",https://www.imdb.com/title/tt1523515,Movie,6.1,100,2009,"Drama",7921,"2009-11-27","Yilmaz Erdogan"
tt8543390,8,2024-08-07,"Modern Love","Modern Love",https://www.imdb.com/title/tt8543390,TV Series,7.9,30,2019,"Comedy, Romance, Drama",39605,"2019-10-18",
tt0405094,7,2024-08-06,"Başkalarının Hayatı","Das Leben der Anderen",https://www.imdb.com/title/tt0405094,Movie,8.4,137,2006,"Drama, Thriller, Mystery",439279,"2007-03-09","Florian Henckel von Donnersmarck"
tt2106476,9,2024-08-05,"Onur Savaşı","Jagten",https://www.imdb.com/title/tt2106476,Movie,8.3,115,2012,"Drama",401924,"2013-10-18","Thomas Vinterberg"
tt0816692,9,2024-08-04,"Yıldızlararası","Interstellar",https://www.imdb.com/title/tt0816692,Movie,8.7,169,2014,"Sci-Fi, Adventure, Drama",2453942,"2014-11-07","Christopher Nolan"
tt0114369,8,2024-08-04,"Yedi","Se7en",https://www.imdb.com/title/tt0114369,Movie,8.6,127,1995,"Mystery, Drama, Crime, Thriller",1983191,"1996-02-16","David Fincher"
tt0099685,7,2024-08-04,"Sıkı Dostlar","GoodFellas",https://www.imdb.com/title/tt0099685,Movie,8.7,145,1990,"Biography, Crime, Drama",1369076,"1990-12-28","Martin Scorsese"
tt10366460,7,2024-08-04,"CODA","CODA",https://www.imdb.com/title/tt10366460,Movie,8.0,111,2021,"Drama, Music, Comedy",201879,"2021-08-13","Sian Heder"
tt23849204,9,2024-07-26,"Bitmeyen Sınav","12th Fail",https://www.imdb.com/title/tt23849204,Movie,8.7,147,2023,"Drama, Biography",165170,"2023-10-27","Vidhu Vinod Chopra"
tt5593384,7,2024-07-20,"Tõde ja õigus","Tõde ja õigus",https://www.imdb.com/title/tt5593384,Movie,7.9,165,2019,"Drama",5442,"2019-02-22","Tanel Toom"
tt0102926,7,2024-07-11,"Kuzuların Sessizliği","The Silence of the Lambs",https://www.imdb.com/title/tt0102926,Movie,8.6,118,1991,"Crime, Drama, Horror, Thriller",1691183,"1991-10-11","Jonathan Demme"
tt14859416,7,2024-07-01,"Kurak Günler","Kurak Günler",https://www.imdb.com/title/tt14859416,Movie,7.5,129,2022,"Drama, Thriller",14329,"2022-12-09","Emin Alper"
tt15239678,9,2024-06-30,"Dune: Çöl Gezegeni Bölüm İki","Dune: Part Two",https://www.imdb.com/title/tt15239678,Movie,8.4,166,2024,"Adventure, Drama, Sci-Fi, Action",703991,"2024-03-01","Denis Villeneuve"
tt14533970,8,2024-06-30,"Prens","Prens",https://www.imdb.com/title/tt14533970,TV Series,8.5,45,2023,"Comedy, History",15334,"2023-06-16",
tt20603316,7,2024-06-30,"Var Bunlar","Var Bunlar",https://www.imdb.com/title/tt20603316,TV Series,8.1,20,2022,"Comedy",5191,"2022",
tt2861424,10,2024-06-18,"Rick ve Morty","Rick and Morty",https://www.imdb.com/title/tt2861424,TV Series,9.0,23,2013,"Animation, Adventure, Comedy, Sci-Fi",679885,"2013-12-02",
tt3398228,9,2024-06-18,"BoJack Horseman","BoJack Horseman",https://www.imdb.com/title/tt3398228,TV Series,8.8,25,2014,"Animation, Comedy, Drama",224852,"2014-08-22",
tt2562232,8,2024-06-09,"Birdman veya (Cahilliğin Umulmayan Erdemi)","Birdman or (The Unexpected Virtue of Ignorance)",https://www.imdb.com/title/tt2562232,Movie,7.7,119,2014,"Comedy, Drama",692517,"2015-02-27","Alejandro G. Iñárritu"
tt0073486,10,2024-05-25,"Guguk Kuşu","One Flew Over the Cuckoo's Nest",https://www.imdb.com/title/tt0073486,Movie,8.6,133,1975,"Drama",1145040,"1981-04-20","Milos Forman"
tt0472954,8,2024-02-10,"It's Always Sunny in Philadelphia","It's Always Sunny in Philadelphia",https://www.imdb.com/title/tt0472954,TV Series,8.8,22,2005,"Comedy",277575,"2005-08-04",
tt5037996,7,2024-02-10,"Bulantı","Bulanti",https://www.imdb.com/title/tt5037996,Movie,6.2,112,2015,"Drama",3271,"2015-10-02","Zeki Demirkubuz"
tt19653180,8,2024-02-08,"Leyla'nın Kardeşleri","Baradaran-e Leila",https://www.imdb.com/title/tt19653180,Movie,7.9,165,2022,"Drama",18430,"2022-08-24","Saeed Roustayi"
tt5985288,7,2024-02-08,"Ekşi Elmalar","Eksi Elmalar",https://www.imdb.com/title/tt5985288,Movie,7.1,114,2016,"Drama, History",8523,"2016-10-28","Yilmaz Erdogan"
tt13287846,8,2024-01-25,"Napolyon","Napoleon",https://www.imdb.com/title/tt13287846,Movie,6.3,158,2023,"Biography, Action, Drama, War, Adventure, History",181993,"2023-11-24","Ridley Scott"
tt1827487,8,2024-01-22,"Bir Zamanlar Anadolu'da","Bir Zamanlar Anadolu'da",https://www.imdb.com/title/tt1827487,Movie,7.8,157,2011,"Drama, Crime, Thriller",53224,"2011-09-23","Nuri Bilge Ceylan"
tt2758880,8,2024-01-22,"Kış Uykusu","Kis Uykusu",https://www.imdb.com/title/tt2758880,Movie,8.0,196,2014,"Drama",58389,"2014-06-13","Nuri Bilge Ceylan"
tt13231544,9,2024-01-22,"Kuru Otlar Üstüne","Kuru Otlar Üstüne",https://www.imdb.com/title/tt13231544,Movie,7.7,197,2023,"Drama",18842,"2023-09-29","Nuri Bilge Ceylan"
tt0498097,7,2024-01-22,"Iklimler","Iklimler",https://www.imdb.com/title/tt0498097,Movie,7.1,97,2006,"Drama",15043,"2006-10-20","Nuri Bilge Ceylan"
tt13521006,7,2024-01-22,"Korkuyorum","Beau Is Afraid",https://www.imdb.com/title/tt13521006,Movie,6.6,179,2023,"Drama, Comedy, Thriller, Horror",76892,"2023-06-09","Ari Aster"
tt8772262,7,2023-12-31,"Ritüel","Midsommar",https://www.imdb.com/title/tt8772262,Movie,7.1,148,2019,"Horror, Drama, Mystery, Thriller",472173,"2019-07-26","Ari Aster"
tt0115940,8,2023-12-16,"Yaz Öyküsü","Conte d'été",https://www.imdb.com/title/tt0115940,Movie,7.6,113,1996,"Drama, Comedy, Romance",11663,"1996-06-05","Éric Rohmer"
tt9418878,7,2023-11-20,"Kız Kardeşler","Kiz Kardesler",https://www.imdb.com/title/tt9418878,Movie,7.4,108,2019,"Drama",5152,"2019-09-13","Emin Alper"
tt16968450,6,2023-10-28,"Şeker Henry'nin İnanılmaz Öyküsü","The Wonderful Story of Henry Sugar",https://www.imdb.com/title/tt16968450,Short,7.4,40,2023,"Short, Adventure, Comedy, Drama",85736,"2023-09-27","Wes Anderson"
tt5462602,7,2023-10-28,"Aşk Denen Hastalık","The Big Sick",https://www.imdb.com/title/tt5462602,Movie,7.5,120,2017,"Comedy, Romance, Drama",149077,"2018-04-05","Michael Showalter"
tt3741834,9,2023-10-13,"Lion","Lion",https://www.imdb.com/title/tt3741834,Movie,8.0,118,2016,"Drama, Biography",263955,"2017-02-03","Garth Davis"
tt5052448,8,2023-10-13,"Kapan","Get Out",https://www.imdb.com/title/tt5052448,Movie,7.8,104,2017,"Horror, Mystery, Thriller",796194,"2017-04-21","Jordan Peele"
tt0332280,9,2023-10-13,"Not Defteri","The Notebook",https://www.imdb.com/title/tt0332280,Movie,7.8,123,2004,"Romance, Drama",674920,"2021-03-11","Nick Cassavetes"
tt7286456,9,2023-10-13,"Joker","Joker",https://www.imdb.com/title/tt7286456,Movie,8.3,122,2019,"Crime, Drama, Thriller",1662431,"2019-10-04","Todd Phillips"
tt1964624,8,2023-10-13,"Evde","Dans la maison",https://www.imdb.com/title/tt1964624,Movie,7.3,105,2012,"Thriller, Mystery, Drama",35717,"2013-05-24","François Ozon"
tt1392170,8,2023-10-13,"Açlık Oyunları","The Hunger Games",https://www.imdb.com/title/tt1392170,Movie,7.2,142,2012,"Adventure, Sci-Fi, Thriller, Action",1067252,"2012-03-23","Gary Ross"
tt8228288,9,2023-10-13,"Platform","El hoyo",https://www.imdb.com/title/tt8228288,Movie,7.0,94,2019,"Thriller, Sci-Fi, Horror, Mystery",318142,"2020-03-20","Galder Gaztelu-Urrutia"
tt0213847,9,2023-10-13,"Malena","Malèna",https://www.imdb.com/title/tt0213847,Movie,7.4,108,2000,"War, Romance, Drama",123250,"2001-05-04","Giuseppe Tornatore"
tt3011894,9,2023-10-13,"Asabiyim Ben","Relatos salvajes",https://www.imdb.com/title/tt3011894,Movie,8.1,122,2014,"Comedy, Thriller, Drama",235058,"2015-03-06","Damián Szifron"
tt2278388,7,2023-10-13,"Büyük Budapeşte Oteli","The Grand Budapest Hotel",https://www.imdb.com/title/tt2278388,Movie,8.1,99,2014,"Comedy, Drama",951926,"2014-04-11","Wes Anderson"
tt1258197,7,2023-09-28,"Sınav","Exam",https://www.imdb.com/title/tt1258197,Movie,6.7,101,2009,"Thriller, Mystery, Crime",133350,"2010-06-17","Stuart Hazeldine"
tt8267604,9,2023-09-27,"Kefernahum","Capharnaüm",https://www.imdb.com/title/tt8267604,Movie,8.4,126,2018,"Drama",121623,"2019-01-25","Nadine Labaki"
tt1832382,8,2023-09-27,"Bir Ayrılık","Jodaeiye Nader az Simin",https://www.imdb.com/title/tt1832382,Movie,8.3,123,2011,"Drama",275183,"2011-07-01","Asghar Farhadi"
tt0790636,8,2023-09-26,"Sınırsızlar Kulübü","Dallas Buyers Club",https://www.imdb.com/title/tt0790636,Movie,7.9,117,2013,"Drama, Biography",543335,"2013-11-22","Jean-Marc Vallée"
tt0361862,7,2023-09-24,"Makinist","The Machinist",https://www.imdb.com/title/tt0361862,Movie,7.6,101,2004,"Thriller, Drama",437304,"2005-03-04","Brad Anderson"
tt1723811,7,2023-09-23,"Utanç","Shame",https://www.imdb.com/title/tt1723811,Movie,7.2,101,2011,"Drama",215383,"2012-02-03","Steve McQueen"
tt5109784,7,2023-09-22,"Anne!","Mother!",https://www.imdb.com/title/tt5109784,Movie,6.6,121,2017,"Drama, Mystery, Horror",265211,"2017-09-29","Darren Aronofsky"
tt1179933,7,2023-09-22,"Canavar Yolu No: 10","10 Cloverfield Lane",https://www.imdb.com/title/tt1179933,Movie,7.2,103,2016,"Drama, Sci-Fi, Thriller, Horror",379871,"2016-04-01","Dan Trachtenberg"
tt0144084,8,2023-09-22,"Amerikan Sapığı","American Psycho",https://www.imdb.com/title/tt0144084,Movie,7.6,102,2000,"Crime, Horror, Drama, Comedy",816827,"2001-03-09","Mary Harron"
tt2737304,7,2023-09-22,"Bird Box","Bird Box",https://www.imdb.com/title/tt2737304,Movie,6.6,124,2018,"Horror, Mystery, Sci-Fi",416293,"2018-12-21","Susanne Bier"
tt6644200,7,2023-09-22,"Sessiz Bir Yer","A Quiet Place",https://www.imdb.com/title/tt6644200,Movie,7.5,90,2018,"Drama, Horror, Sci-Fi",647472,"2018-04-13","John Krasinski"
tt1285016,7,2023-09-22,"Sosyal Ağ","The Social Network",https://www.imdb.com/title/tt1285016,Movie,7.8,120,2010,"Drama, Biography",808916,"2010-10-22","David Fincher"
tt4972582,8,2023-09-22,"Parçalanmış","Split",https://www.imdb.com/title/tt4972582,Movie,7.3,117,2016,"Thriller, Horror",611662,"2017-02-17","M. Night Shyamalan"
tt0945513,7,2023-09-22,"Yaşam Şifresi","Source Code",https://www.imdb.com/title/tt0945513,Movie,7.5,93,2011,"Sci-Fi, Thriller, Action, Drama, Mystery",576935,"2011-04-08","Duncan Jones"
tt2802144,7,2023-09-22,"Kingsman: Gizli Servis","Kingsman: The Secret Service",https://www.imdb.com/title/tt2802144,Movie,7.7,129,2014,"Adventure, Action, Comedy, Thriller",768183,"2015-03-13","Matthew Vaughn"
tt0454876,8,2023-09-22,"Pi'nin Yaşamı","Life of Pi",https://www.imdb.com/title/tt0454876,Movie,7.9,127,2012,"Drama, Adventure, Fantasy",694341,"2012-12-28","Ang Lee"
tt0470752,7,2023-09-22,"Ex Machina","Ex Machina",https://www.imdb.com/title/tt0470752,Movie,7.7,108,2014,"Drama, Sci-Fi, Thriller",629887,"2021-05-16","Alex Garland"
tt0816711,7,2023-09-22,"Dünya Savaşı Z","World War Z",https://www.imdb.com/title/tt0816711,Movie,7.0,116,2013,"Action, Adventure, Horror, Sci-Fi",772918,"2013-06-21","Marc Forster"
tt1790864,7,2023-09-22,"Labirent: Ölümcül Kaçış","The Maze Runner",https://www.imdb.com/title/tt1790864,Movie,6.8,113,2014,"Sci-Fi, Mystery, Thriller, Action",552659,"2014-09-19","Wes Ball"
tt2872732,7,2023-09-22,"Lucy","Lucy",https://www.imdb.com/title/tt2872732,Movie,6.4,89,2014,"Action, Sci-Fi, Thriller",571955,"2014-08-08","Luc Besson"
tt1706620,8,2023-09-22,"Kar Küreyici","Snowpiercer",https://www.imdb.com/title/tt1706620,Movie,7.1,126,2013,"Sci-Fi, Thriller, Action",415754,"2013-08-01","Bong Joon Ho"
tt2543164,7,2023-09-22,"Geliş","Arrival",https://www.imdb.com/title/tt2543164,Movie,7.9,116,2016,"Sci-Fi, Drama, Mystery",846268,"2016-11-11","Denis Villeneuve"
tt0480249,7,2023-09-22,"Ben Efsaneyim","I Am Legend",https://www.imdb.com/title/tt0480249,Movie,7.2,101,2007,"Drama, Sci-Fi, Thriller, Horror",866087,"2008-01-25","Francis Lawrence"
tt1631867,8,2023-09-22,"Yarının Sınırında","Edge of Tomorrow",https://www.imdb.com/title/tt1631867,Movie,7.9,113,2014,"Action, Sci-Fi, Adventure",794185,"2014-06-06","Doug Liman"
tt3659388,8,2023-09-22,"Marslı","The Martian",https://www.imdb.com/title/tt3659388,Movie,8.0,144,2015,"Sci-Fi, Adventure, Drama",992128,"2015-10-02","Ridley Scott"
tt1355644,10,2023-09-22,"Uzay Yolcuları","Passengers",https://www.imdb.com/title/tt1355644,Movie,7.0,116,2016,"Sci-Fi, Drama, Thriller, Romance",488072,"2017-01-13","Morten Tyldum","assets/posters/passengers.jpg"
tt1677720,7,2023-09-22,"Başlat","Ready Player One",https://www.imdb.com/title/tt1677720,Movie,7.4,140,2018,"Sci-Fi, Action, Adventure",533475,"2018-03-30","Steven Spielberg"
tt13238346,9,2023-09-22,"Başka Bir Hayatta","Past Lives",https://www.imdb.com/title/tt13238346,Movie,7.8,105,2023,"Drama, Romance",166033,"2023-12-08","Celine Song"
tt14452776,10,2023-09-21,"The Bear","The Bear",https://www.imdb.com/title/tt14452776,TV Series,8.5,30,2022,"Drama, Comedy",299553,"2022-10-05",
tt0081505,8,2023-09-21,"Cinnet","The Shining",https://www.imdb.com/title/tt0081505,Movie,8.4,146,1980,"Drama, Horror",1206570,"1980-05-23","Stanley Kubrick"
tt0477348,8,2023-09-19,"İhtiyarlara Yer Yok","No Country for Old Men",https://www.imdb.com/title/tt0477348,Movie,8.2,122,2007,"Thriller, Crime, Drama",1166073,"2008-03-07","Ethan Coen,Joel Coen"
tt0816442,8,2023-09-19,"Kitap Hırsızı","The Book Thief",https://www.imdb.com/title/tt0816442,Movie,7.5,131,2013,"Drama, War",146767,"2014-02-07","Brian Percival"
tt4016934,8,2023-09-17,"Hizmetçi","Ah-ga-ssi",https://www.imdb.com/title/tt4016934,Movie,8.1,145,2016,"Drama, Romance, Thriller",197440,"2017-08-11","Park Chan-wook"
tt1817273,7,2023-09-16,"Babadan Oğula","The Place Beyond the Pines",https://www.imdb.com/title/tt1817273,Movie,7.3,140,2012,"Drama, Crime, Thriller",305618,"2013-06-07","Derek Cianfrance"
tt0109830,9,2023-09-14,"Forrest Gump","Forrest Gump",https://www.imdb.com/title/tt0109830,Movie,8.8,142,1994,"Romance, Drama",2454031,"1994-11-11","Robert Zemeckis"
tt0264464,9,2023-09-14,"Sıkıysa Yakala","Catch Me If You Can",https://www.imdb.com/title/tt0264464,Movie,8.1,141,2002,"Drama, Biography, Crime",1207657,"2003-01-31","Steven Spielberg"
tt0120382,7,2023-09-14,"Truman Show","The Truman Show",https://www.imdb.com/title/tt0120382,Movie,8.2,103,1998,"Comedy, Drama",1339829,"1998-10-16","Peter Weir"
tt0253474,9,2023-09-14,"Piyanist","The Pianist",https://www.imdb.com/title/tt0253474,Movie,8.5,150,2002,"Biography, Music, Drama, War",997810,"2003-02-28","Roman Polanski"
tt0362227,7,2023-09-14,"Terminal","The Terminal",https://www.imdb.com/title/tt0362227,Movie,7.4,128,2004,"Drama, Comedy, Romance",528162,"2004-09-10","Steven Spielberg"
tt0993846,9,2023-09-14,"Para Avcısı","The Wolf of Wall Street",https://www.imdb.com/title/tt0993846,Movie,8.2,180,2013,"Crime, Drama, Biography, Comedy",1747533,"2014-02-07","Martin Scorsese"
tt1119646,7,2023-09-14,"Felekten Bir Gece","The Hangover",https://www.imdb.com/title/tt1119646,Movie,7.7,100,2009,"Comedy",914522,"2009-07-10","Todd Phillips"
tt2713180,7,2023-09-14,"Fury","Fury",https://www.imdb.com/title/tt2713180,Movie,7.6,134,2014,"Action, Drama, War",597702,"2014-10-24","David Ayer"
tt1219289,7,2023-09-14,"Limit Yok","Limitless",https://www.imdb.com/title/tt1219289,Movie,7.4,105,2011,"Thriller, Sci-Fi",640342,"2011-03-18","Neil Burger"
tt12058584,8,2023-09-14,"Satranç","Schachnovelle",https://www.imdb.com/title/tt12058584,Movie,6.8,110,2021,"Drama, Thriller, War",5446,"2021-12-10","Philipp Stölzl"
tt0454921,9,2023-09-14,"Umudunu Kaybetme","The Pursuit of Happyness",https://www.imdb.com/title/tt0454921,Movie,8.0,117,2006,"Drama, Biography",609917,"2007-03-02","Gabriele Muccino"
tt0162222,7,2023-09-14,"Yeni Hayat","Cast Away",https://www.imdb.com/title/tt0162222,Movie,7.8,143,2000,"Romance, Drama, Adventure",680587,"2001-02-23","Robert Zemeckis"
tt1454468,7,2023-09-14,"Yerçekimi","Gravity",https://www.imdb.com/title/tt1454468,Movie,7.7,91,2013,"Sci-Fi, Thriller, Drama",892973,"2013-10-11","Alfonso Cuarón"
tt1010048,8,2023-09-14,"Milyoner","Slumdog Millionaire",https://www.imdb.com/title/tt1010048,Movie,8.0,120,2008,"Drama, Romance, Crime",904659,"2009-02-27","Danny Boyle,Loveleen Tandan"
tt2084970,8,2023-09-14,"Enigma","The Imitation Game",https://www.imdb.com/title/tt2084970,Movie,8.0,114,2014,"Drama, Biography, Thriller, War",868880,"2015-02-20","Morten Tyldum"
tt1727824,8,2023-09-14,"Bohemian Rhapsody","Bohemian Rhapsody",https://www.imdb.com/title/tt1727824,Movie,7.9,134,2018,"Biography, Drama, Music",636614,"2018-11-02","Bryan Singer"
tt2980516,7,2023-09-14,"Her Şeyin Teorisi","The Theory of Everything",https://www.imdb.com/title/tt2980516,Movie,7.7,123,2014,"Drama, Biography, Romance",504351,"2015-02-27","James Marsh"
tt1798709,8,2023-09-14,"Aşk","Her",https://www.imdb.com/title/tt1798709,Movie,8.0,126,2013,"Romance, Sci-Fi, Drama",718654,"2014-02-14","Spike Jonze"
tt0105323,8,2023-09-14,"Kadın Kokusu","Scent of a Woman",https://www.imdb.com/title/tt0105323,Movie,8.0,156,1992,"Drama",363231,"1993-03-12","Martin Brest"
tt0110413,8,2023-09-14,"Sevginin Gücü","Léon",https://www.imdb.com/title/tt0110413,Movie,8.5,110,1994,"Action, Drama, Crime, Thriller",1335803,"1995-04-28","Luc Besson"
tt2180339,7,2023-09-14,"Derin Sular","Deep Water",https://www.imdb.com/title/tt2180339,Movie,5.5,115,2022,"Thriller, Drama, Mystery, Crime, Romance",69066,"2022-03-18","Adrian Lyne"
tt1446714,9,2023-09-12,"Prometheus","Prometheus",https://www.imdb.com/title/tt1446714,Movie,7.0,124,2012,"Adventure, Sci-Fi, Mystery",690296,"2012-06-01","Ridley Scott"
tt0758758,8,2023-09-12,"Özgürlük Yolu","Into the Wild",https://www.imdb.com/title/tt0758758,Movie,8.0,148,2007,"Drama, Adventure, Biography",690727,"2007-10-19","Sean Penn"
tt0097165,7,2023-09-12,"Ölü Ozanlar Derneği","Dead Poets Society",https://www.imdb.com/title/tt0097165,Movie,8.1,128,1989,"Comedy, Drama",629625,"1990-04-13","Peter Weir"
tt2267998,9,2023-09-12,"Kayıp Kız","Gone Girl",https://www.imdb.com/title/tt2267998,Movie,8.1,149,2014,"Thriller, Drama, Mystery",1151716,"2014-10-10","David Fincher"
tt2024544,9,2023-09-12,"12 Yıllık Esaret","12 Years a Slave",https://www.imdb.com/title/tt2024544,Movie,8.1,134,2013,"Drama, History, Biography",778271,"2014-01-24","Steve McQueen"
tt0266697,7,2023-09-12,"Bill'i Öldür: Bölüm 1","Kill Bill: Vol. 1",https://www.imdb.com/title/tt0266697,Movie,8.2,111,2003,"Action, Thriller, Crime",1285552,"2004-01-02","Quentin Tarantino"
tt0268978,7,2023-09-12,"Akıl Oyunları","A Beautiful Mind",https://www.imdb.com/title/tt0268978,Movie,8.2,135,2001,"Biography, Mystery, Drama",1042954,"2002-03-08","Ron Howard"
tt0469494,9,2023-09-12,"Kan Dökülecek","There Will Be Blood",https://www.imdb.com/title/tt0469494,Movie,8.2,158,2007,"Drama",696138,"2008-02-15","Paul Thomas Anderson"
tt6966692,7,2023-09-12,"Yeşil Rehber","Green Book",https://www.imdb.com/title/tt6966692,Movie,8.2,130,2018,"Drama, Biography, Comedy, Music",666991,"2018-11-30","Peter Farrelly"
tt0066921,8,2023-09-12,"Otomatik Portakal","A Clockwork Orange",https://www.imdb.com/title/tt0066921,Movie,8.2,136,1971,"Crime, Sci-Fi",928006,"1996-03-15","Stanley Kubrick"
tt0086250,7,2023-09-12,"Yaralı Yüz","Scarface",https://www.imdb.com/title/tt0086250,Movie,8.3,170,1983,"Crime, Drama",998470,"1985-12-02","Brian De Palma"
tt0093058,8,2023-09-12,"Full Metal Jacket","Full Metal Jacket",https://www.imdb.com/title/tt0093058,Movie,8.2,116,1987,"Drama, War",841093,"1995-10-06","Stanley Kubrick"
tt0211915,7,2023-09-12,"Amelie","Le fabuleux destin d'Amélie Poulain",https://www.imdb.com/title/tt0211915,Movie,8.3,122,2001,"Romance, Comedy",832123,"2001-11-23","Jean-Pierre Jeunet"
tt0119217,9,2023-09-12,"Can Dostum","Good Will Hunting",https://www.imdb.com/title/tt0119217,Movie,8.3,126,1997,"Romance, Drama",1186595,"1998-05-01","Gus Van Sant"
tt0086879,9,2023-09-12,"Amadeus","Amadeus",https://www.imdb.com/title/tt0086879,Movie,8.4,160,1984,"Drama, Music, Biography",462568,"1987-11","Milos Forman"
tt1853728,10,2023-09-12,"Zincirsiz","Django Unchained",https://www.imdb.com/title/tt1853728,Movie,8.5,165,2012,"Western, Drama",1850476,"2013-02-01","Quentin Tarantino"
tt1675434,9,2023-09-12,"Can Dostum","Intouchables",https://www.imdb.com/title/tt1675434,Movie,8.5,112,2011,"Comedy, Drama",1010125,"2012-05-11","Olivier Nakache,Éric Toledano"
tt2582802,9,2023-09-12,"Whiplash","Whiplash",https://www.imdb.com/title/tt2582802,Movie,8.5,106,2014,"Drama, Music",1125168,"2015-01-16","Damien Chazelle"
tt0119177,9,2023-09-12,"Gattaca","Gattaca",https://www.imdb.com/title/tt0119177,Movie,7.7,106,1997,"Sci-Fi, Drama, Thriller",343027,"1997-10-24","Andrew Niccol"
tt7322224,10,2023-09-12,"Hüzün Üçgeni","Triangle of Sadness",https://www.imdb.com/title/tt7322224,Movie,7.2,147,2022,"Drama, Comedy",211397,"2022-10-28","Ruben Östlund"
tt3464902,7,2023-09-12,"The Lobster","The Lobster",https://www.imdb.com/title/tt3464902,Movie,7.1,119,2015,"Romance, Sci-Fi, Drama, Thriller",328449,"2015-12-25","Yorgos Lanthimos"
tt0387808,9,2023-09-12,"Ahmaklar","Idiocracy",https://www.imdb.com/title/tt0387808,Movie,6.5,84,2006,"Adventure, Comedy, Sci-Fi, Thriller",210762,"2007-01-25","Mike Judge"
tt0105236,10,2023-09-12,"Rezervuar Köpekleri","Reservoir Dogs",https://www.imdb.com/title/tt0105236,Movie,8.3,99,1992,"Crime, Thriller",1157036,"1993-05-21","Quentin Tarantino"
tt0110912,10,2023-09-12,"Ucuz Roman","Pulp Fiction",https://www.imdb.com/title/tt0110912,Movie,8.8,154,1994,"Crime, Drama",2398457,"1995-04-14","Quentin Tarantino","assets/posters/pulpfiction.jpg"
tt0421715,9,2023-09-12,"Benjamin Button'ın Tuhaf Hikayesi","The Curious Case of Benjamin Button",https://www.imdb.com/title/tt0421715,Movie,7.8,166,2008,"Romance, Drama, Fantasy",737235,"2009-02-06","David Fincher"
tt0112471,10,2023-09-12,"Gün Doğmadan","Before Sunrise",https://www.imdb.com/title/tt0112471,Movie,8.1,101,1995,"Comedy, Romance, Drama",370734,"1995-05-19","Richard Linklater","assets/posters/gündogmadan.jpg"
tt1233381,8,2023-09-12,"Üç Maymun","Üç Maymun",https://www.imdb.com/title/tt1233381,Movie,7.3,109,2008,"Drama",23966,"2008-10-24","Nuri Bilge Ceylan"
tt0346094,10,2023-09-12,"Uzak","Uzak",https://www.imdb.com/title/tt0346094,Movie,7.5,110,2002,"Comedy, Drama",24440,"2002-12-20","Nuri Bilge Ceylan","assets/posters/uzak.jpg"
tt6628102,10,2023-09-12,"Ahlat Ağacı","Ahlat Agaci",https://www.imdb.com/title/tt6628102,Movie,8.0,188,2018,"Drama",30284,"2018-06-01","Nuri Bilge Ceylan","assets/posters/ahlatagaci.jpg"
tt1322930,9,2023-09-12,"Issiz Adam","Issiz Adam",https://www.imdb.com/title/tt1322930,Movie,6.8,113,2008,"Drama, Romance",25235,"2008-11-07","Çagan Irmak"
tt0107653,8,2023-09-12,"Naked","Naked",https://www.imdb.com/title/tt0107653,Movie,7.7,131,1993,"Comedy, Drama",48070,"1993-11-05","Mike Leigh"
tt0338751,7,2023-09-12,"Göklerin Hakimi","The Aviator",https://www.imdb.com/title/tt0338751,Movie,7.5,170,2004,"Biography, Drama",402899,"2005-02-18","Martin Scorsese"
tt0959337,9,2023-09-12,"Hayallerin Peşinde","Revolutionary Road",https://www.imdb.com/title/tt0959337,Movie,7.3,119,2008,"Drama, Romance",233742,"2009-02-27","Sam Mendes"
tt4034228,9,2023-09-12,"Yaşamın Kıyısında","Manchester by the Sea",https://www.imdb.com/title/tt4034228,Movie,7.8,137,2016,"Drama",348936,"2017-02-03","Kenneth Lonergan","assets/posters/yasaminkiyisindaa.jpg"
tt4975722,7,2023-09-12,"Ay Işığı","Moonlight",https://www.imdb.com/title/tt4975722,Movie,7.4,111,2016,"Drama",348155,"2017-02-17","Barry Jenkins"
tt10370710,7,2023-09-12,"Dünyanın En Kötü İnsanı","Verdens verste menneske",https://www.imdb.com/title/tt10370710,Movie,7.7,128,2021,"Comedy, Drama, Romance",120169,"2021-11-19","Joachim Trier"
tt0419887,9,2023-09-12,"Uçurtma avcısı","The Kite Runner",https://www.imdb.com/title/tt0419887,Movie,7.6,128,2007,"Drama",84674,"2008-03-21","Marc Forster"
tt1571401,9,2023-09-12,"Die Vermessung der Welt","Die Vermessung der Welt",https://www.imdb.com/title/tt1571401,Movie,5.7,119,2012,"Drama, Biography, History",3343,"2012-10-25","Detlev Buck"
tt11813216,9,2023-09-12,"The Banshees of Inisherin","The Banshees of Inisherin",https://www.imdb.com/title/tt11813216,Movie,7.7,114,2022,"Drama, Comedy",289633,"2023-02-03","Martin McDonagh"
"""
# Top 10 için kısa açıklamalar (IMDb ID -> 1 cümle)
TOP10_DESCRIPTION_MAP = {
    "tt0476735": "Bir baba ile oğulun yıllara yayılan, yürek burkan hikâyesi.",
    "tt4034228": "Kaybın ardından gelen sessizlik ve yas üzerine derin bir drama.",
    "tt0346094": "İnsan yalnızlığını sade ve çarpıcı bir dille anlatan bir başyapıt.",
    "tt21029674": "Adalet, vicdan ve güç ilişkileri üzerine sert bir anlatı.",
    "tt0112471": "Bir gecede başlayan, zamana yayılan unutulmaz bir aşk.",
    "tt1355644": "Uzayda geçen yalnızlık ve hayatta kalma üzerine felsefi bir yolculuk.",
    "tt0110912": "Suç dünyasını parçalara ayıran ikonik ve stilize bir anlatı.",
    "tt1586680": "Disfonksiyonel bir ailenin kara mizahla örülü hikâyesi.",
    "tt0248654": "Ölüm, aile ve hayat üzerine cesur ve sarsıcı bir dizi.",
    "tt6628102": "Taşrada sıkışmışlık, entelektüel çatışma ve içsel arayış."
}

# Plotly grafiklerini tamamen statik yapmak için ortak config
PLOTLY_STATIC_CONFIG = {
    "displayModeBar": False,   # Zoom / pan butonları kalkar
    "scrollZoom": False,       # Mouse wheel zoom kapalı
    "doubleClick": False,      # Çift tık reset kapalı
    "staticPlot": True         # TÜM etkileşimleri kapatır (en garanti)
}




# Mobil uyumluluk: sidebar varsayılan kapalı
st.set_page_config(page_title="Film Oylama Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Sadece Top 10 için manuel poster eşlemesi (IMDb ID -> lokal yol)
TOP10_POSTER_MAP = {
    "tt0476735":"assets/posters/babamveoglum.jpg",
    "tt4034228":"assets/posters/yasaminkiyisindaa.jpg",
    "tt0346094":"assets/posters/uzak.jpg",
    "tt21029674": "assets/posters/cezailer.jpg",
    "tt0112471": "assets/posters/gündogmadan.jpg",
    "tt1355644":"assets/posters/passengers.jpg",
    "tt0110912":"assets/posters/pulpfiction.jpg",
    "tt1586680":"assets/posters/shameless.jpg",
    "tt0248654":"assets/posters/sixfeetunder.jpg",
    "tt6628102":"assets/posters/ahlatagaci.jpg",
}

def stil_enjekte_et():
    """Mobil uyumlu CSS: küçük ekranda kolonları stack’le, container padding ve metrikleri optimize et."""
    st.markdown("""
        <style>
            /* Sidebar genişlikleri desktop için aynı kalsın */
            [data-testid="stSidebar"] {
                min-width: 280px;
                max-width: 320px;
            }

            /* Metrik kartları */
            [data-testid="stMetric"] {
                background-color: rgba(255, 255, 255, 0.05);
                padding: 12px;
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            /* Posterler */
            div[data-testid="column"] img {
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
                object-fit: cover;
            }

            /* Mobil: genel padding biraz azalt */
            @media (max-width: 768px) {
                .block-container {
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
            }
        </style>
    """, unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def veri_yukle_cached():
    """CSV parse işlemi pahalı: cache."""
    return pd.read_csv(StringIO(CSV_DATA))

@st.cache_data(show_spinner=False)
def kolon_tespit_et_cached(df: pd.DataFrame):
    """Kolon tespiti cache."""
    df = df.copy()

    puan_kolonu = next((c for c in df.columns if 'your rating' in c.lower()), None)
    if not puan_kolonu:
        puan_kolonu = next((c for c in df.columns if ('puan' in c.lower() or 'rating' in c.lower()) and 'imdb' not in c.lower()), None)

    tespit_edilenler = {
        'id': next((c for c in df.columns if c.lower() in ['const', 'imdb id', 'imdbid', 'tconst']), None),
        'puan': puan_kolonu,
        'yil': next((c for c in df.columns if any(a in c.lower() for a in ['year', 'yıl'])), None),
        'tur': next((c for c in df.columns if any(a in c.lower() for a in ['genres', 'genre', 'tür'])), None),
        'isim': next((c for c in df.columns if c.lower() == 'title'), None) or df.columns[0],
        'orijinal_isim': next((c for c in df.columns if c.lower() in ['original title', 'original_title'] or 'original' in c.lower()), None),
        'poster_path': next((c for c in df.columns if 'poster_path' in c.lower()), None),
    }

    if tespit_edilenler['puan']:
        df[tespit_edilenler['puan']] = pd.to_numeric(df[tespit_edilenler['puan']], errors='coerce')
    if tespit_edilenler['yil']:
        df[tespit_edilenler['yil']] = pd.to_numeric(df[tespit_edilenler['yil']], errors='coerce')

    if tespit_edilenler['puan']:
        df.dropna(subset=[tespit_edilenler['puan']], inplace=True)

    return tespit_edilenler, df

def sidebar_filtreleri(df, kolonlar):
    f_df = df.copy()
    st.sidebar.subheader("Analiz Filtreleri")

    if kolonlar['puan']:
        min_v, max_v = float(df[kolonlar['puan']].min()), float(df[kolonlar['puan']].max())
        secilen_puan = st.sidebar.slider("Puan Aralığı (Your Rating)", min_v, max_v, (min_v, max_v))
        f_df = f_df[(f_df[kolonlar['puan']] >= secilen_puan[0]) & (f_df[kolonlar['puan']] <= secilen_puan[1])]

    if kolonlar['yil']:
        valid_years = df[kolonlar['yil']].dropna()
        if not valid_years.empty:
            min_y, max_y = int(valid_years.min()), int(valid_years.max())
            secilen_yil = st.sidebar.slider("Yıl Aralığı", min_y, max_y, (min_y, max_y))
            f_df = f_df[(f_df[kolonlar['yil']] >= secilen_yil[0]) & (f_df[kolonlar['yil']] <= secilen_yil[1])]

    if kolonlar['tur']:
        tur_serisi = df[kolonlar['tur']].fillna("Bilinmiyor").astype(str)
        tekil_turler = sorted(list(set([t.strip() for satır in tur_serisi for t in satır.split(',') if t.strip()])))
        secilen_turler = st.sidebar.multiselect("Film Türleri", tekil_turler)
        if secilen_turler:
            maske = f_df[kolonlar['tur']].astype(str).apply(lambda x: any(t in x for t in secilen_turler))
            f_df = f_df[maske]

    return f_df

def dashboard_grafikleri(df, kolonlar):
    if df.empty:
        return

    # --- Puan Dağılımı ---
    if kolonlar['puan']:
        st.subheader("Puan Dağılımı")
        fig_hist = px.histogram(
            df,
            x=kolonlar['puan'],
            nbins=20,
            labels={kolonlar['puan']: 'Puan'},
            template="plotly_dark"
        )
        fig_hist.update_layout(bargap=0.1)
        st.plotly_chart(
            fig_hist,
            use_container_width=True,
            config=PLOTLY_STATIC_CONFIG
        )

    col1, col2 = st.columns(2)

    # --- Yıllara Göre Ortalama Puan ---
    if kolonlar['yil'] and kolonlar['puan']:
        with col1:
            st.subheader("Yıllara Göre Ortalama Puan")
            yil_df = df.dropna(subset=[kolonlar['yil']])
            if not yil_df.empty:
                yil_gruplu = yil_df.groupby(kolonlar['yil'])[kolonlar['puan']].mean().reset_index()
                fig_yil = px.line(
                    yil_gruplu,
                    x=kolonlar['yil'],
                    y=kolonlar['puan'],
                    markers=True,
                    labels={
                        kolonlar['yil']: 'Yıl',
                        kolonlar['puan']: 'Ortalama Puan'
                    },
                    template="plotly_dark"
                )
                st.plotly_chart(
                    fig_yil,
                    use_container_width=True,
                    config=PLOTLY_STATIC_CONFIG
                )

    # --- Türlere Göre Ortalama Puan ---
    if kolonlar['tur'] and kolonlar['puan']:
        with col2:
            st.subheader("Türlere Göre Ortalama Puan")
            tur_df = df.copy()
            tur_df[kolonlar['tur']] = tur_df[kolonlar['tur']].fillna("").astype(str)
            tur_df['gecici_tur'] = tur_df[kolonlar['tur']].str.split(',')
            tur_df = tur_df.explode('gecici_tur')
            tur_df['gecici_tur'] = tur_df['gecici_tur'].str.strip()
            tur_df = tur_df[tur_df['gecici_tur'] != ""]

            if not tur_df.empty:
                tur_gruplu = (
                    tur_df
                    .groupby('gecici_tur')[kolonlar['puan']]
                    .mean()
                    .reset_index()
                    .sort_values(by=kolonlar['puan'], ascending=False)
                )

                fig_tur = px.bar(
                    tur_gruplu,
                    x='gecici_tur',
                    y=kolonlar['puan'],
                    labels={
                        'gecici_tur': 'Tür',
                        kolonlar['puan']: 'Ortalama Puan'
                    },
                    template="plotly_dark"
                )

                st.plotly_chart(
                    fig_tur,
                    use_container_width=True,
                    config=PLOTLY_STATIC_CONFIG
                )

def dashboard_metrikleri(df, kolonlar):
    if kolonlar['puan'] and not df.empty:
        ort_puan = df[kolonlar['puan']].mean()
        st.metric(label="Filtrelenmiş Veri Ortalama Puanı (Your Rating)", value=f"{ort_puan:.2f}")

def get_poster_source_for_top10(imdb_id: str) -> str:
    fallback = "https://via.placeholder.com/150x220?text=No+Poster"
    if not isinstance(imdb_id, str) or not imdb_id.strip():
        return fallback
    path = TOP10_POSTER_MAP.get(imdb_id.strip(), "")
    if path and os.path.exists(path):
        return path
    return fallback

def _get_device_mode():
    """
    Streamlit JS ile gerçek ekran genişliğini okumak standart şekilde mümkün değil.
    Bu nedenle basit bir mobil modu seçicisi ekliyoruz (varsayılan Auto).
    Auto: geniş ekran mantığı; Mobil: tek kolon ağırlıklı.
    """
    with st.sidebar:
        st.markdown("---")
        mode = st.radio("Görünüm", ["Auto", "Mobil"], index=0, horizontal=True)
    return mode

def dashboard_tablolar(df, kolonlar, view_mode: str):
    """
    KURAL:
    - Top 10: Poster GÖSTER.
    - Veri Listesi: Poster ASLA GÖSTERME.
    Mobil optimizasyon:
    - Top10: Auto=4 kolon, Mobil=2 kolon (çok dar ekranda 1)
    - Veri listesi: Mobilde tek kolon (bilgi + puan alt alta)
    """

    if kolonlar['puan'] and not df.empty:
        st.subheader("En Yüksek Puan Verdiğim 10 Film/Diziler")
        top_10 = df.sort_values(by=kolonlar['puan'], ascending=False).head(10)

        # Mobilde daha az kolon
        if view_mode == "Mobil":
            row_size = 2
        else:
            row_size = 4

        for i in range(0, len(top_10), row_size):
            grid_cols = st.columns(row_size)
            batch = top_10.iloc[i:i + row_size]

            for idx, (_, row) in enumerate(batch.iterrows()):
                with grid_cols[idx]:
                    with st.container(border=True):
                        imdb_id = row.get(kolonlar['id']) if kolonlar['id'] else None
                        img_src = get_poster_source_for_top10(str(imdb_id) if imdb_id is not None else "")
                        st.image(img_src, width=150, use_container_width=False)
                        st.markdown(f"**{row[kolonlar['isim']]}**")
                        st.caption(f"⭐ {row[kolonlar['puan']]:.1f}")
                        # Kısa açıklama (sadece Top 10)
                        desc = TOP10_DESCRIPTION_MAP.get(str(imdb_id), "")
    if desc:
        st.caption(desc)


    st.markdown("---")

    st.subheader("En düşük puan verdiklerim")
    bottom_10 = df.sort_values(by=kolonlar['puan'], ascending=True).head(10)
    st.table(bottom_10[[kolonlar['isim'], kolonlar['puan']]])

    st.markdown("---")
    st.subheader("TÜM OYLADIĞIM FİLMLER ve DİZİLER")

    if not df.empty:
        for _, row in df.iterrows():
            with st.container(border=True):

                # Mobilde stacked layout
                if view_mode == "Mobil":
                    # Bilgi
                    baslik = row[kolonlar['isim']]
                    orijinal_baslik = None
                    if kolonlar['orijinal_isim'] and pd.notna(row[kolonlar['orijinal_isim']]):
                        orijinal_baslik = row[kolonlar['orijinal_isim']]

                    if orijinal_baslik and str(orijinal_baslik) != str(baslik):
                        st.markdown(f"**{orijinal_baslik}**")
                        st.caption(f"{baslik}")
                    else:
                        st.markdown(f"**{baslik}**")

                    meta = []
                    if kolonlar['yil'] and pd.notna(row[kolonlar['yil']]):
                        meta.append(str(int(row[kolonlar['yil']])))
                    if kolonlar['tur']:
                        meta.append(str(row[kolonlar['tur']]))
                    if meta:
                        st.text(" • ".join(meta))

                    # Puan alt satıra
                    if kolonlar['puan']:
                        st.metric("Puan", f"{row[kolonlar['puan']]:.1f}")

                else:
                    # Desktop (mevcut davranış korunur)
                    col_info, col_rate = st.columns([5, 1])

                    with col_info:
                        baslik = row[kolonlar['isim']]
                        orijinal_baslik = None
                        if kolonlar['orijinal_isim'] and pd.notna(row[kolonlar['orijinal_isim']]):
                            orijinal_baslik = row[kolonlar['orijinal_isim']]

                        if orijinal_baslik and str(orijinal_baslik) != str(baslik):
                            st.markdown(f"**{orijinal_baslik}**")
                            st.caption(f"{baslik}")
                        else:
                            st.markdown(f"**{baslik}**")

                        meta = []
                        if kolonlar['yil'] and pd.notna(row[kolonlar['yil']]):
                            meta.append(str(int(row[kolonlar['yil']])))

                        if kolonlar['tur']:
                            meta.append(str(row[kolonlar['tur']]))
                        if meta:
                            st.text(" • ".join(meta))

                    with col_rate:
                        if kolonlar['puan']:
                            st.metric("Puan", f"{row[kolonlar['puan']]:.1f}")

def main():
    stil_enjekte_et()
    st.title("Film Oylama Analitik Paneli")
    st.markdown("_Veri seti üzerinden dinamik filtreleme ve görsel analiz arayüzü._")
    st.markdown("---")

    view_mode = _get_device_mode()

    try:
        ham_df = veri_yukle_cached()
    except Exception as e:
        st.error(f"Veri yükleme hatası: {str(e)}")
        return

    st.success(f"Toplam {len(ham_df)} adet film gömülü sistemden başarıyla yüklendi.")

    kolon_bilgisi, temiz_df = kolon_tespit_et_cached(ham_df)

    if not kolon_bilgisi['puan']:
        st.error("Hata: CSV dosyasında 'Your Rating' kolonu bulunamadı.")
        return

    sonuc_df = sidebar_filtreleri(temiz_df, kolon_bilgisi)

    if sonuc_df.empty:
        st.warning("Seçilen filtre kriterlerine uygun film bulunamadı. Lütfen filtreleri gevşetiniz.")
        return

    st.info(f"Şu an filtrelenmiş {len(sonuc_df)} adet film görüntüleniyor.")

    st.sidebar.markdown("---")
    csv_data = sonuc_df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 Filtrelenmiş Veriyi İndir",
        data=csv_data,
        file_name="filtered_movies.csv",
        mime="text/csv",
        help="Mevcut filtreleme sonuçlarını CSV dosyası olarak bilgisayarınıza indirir."
    )

    dashboard_metrikleri(sonuc_df, kolon_bilgisi)
    dashboard_grafikleri(sonuc_df, kolon_bilgisi)
    st.write("")
    dashboard_tablolar(sonuc_df, kolon_bilgisi, view_mode)

if __name__ == "__main__":
    main()
