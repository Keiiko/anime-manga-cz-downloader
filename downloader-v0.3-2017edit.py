import urllib2
import re
import os

def stahniHtml(url):
    try:
        f = urllib2.urlopen(url)
        obsah = f.read()
        f.close()
    except urllib2.HTTPError, e:
        print
        print "Chyba pri stahovani z ", url, ":", e.code, e.msg
        print
        obsah = ""
    return obsah

def nahled(url):
    global chapter
    global currpatch1
    odkazy = vyberodkazux(url)
    for odkaz in odkazy:
        currpatch1 = odkaz.replace("index.html", "")
        chapter = re.search(r'.*/(.*?)/index',odkaz).group(1)
        print "Kapitola "+chapter
        print "  Stahovani nahledu kapitoly... ",
        nahledhtml = stahniHtml(odkaz)
        print "Hotovo."
        print "  Vyhledavani odkazu stranky... ",
        tabulka = re.search(r'<!-- Thumbnail images -->(.*?)class="xsmalltxt"',nahledhtml, re.DOTALL).group(1)
        nahledyurl = re.findall(r'<a href="(.*?)"',tabulka)
        print "Hotovo."
        kapitola(nahledyurl)
    print
    print "Vsechna stahovani dokoncena."
    finalpatch = os.path.expanduser("~")+"\\Downloads\\anime-manga.cz-downloader\\"+nazevserie+"\\" 
    print "Ulozeno do: "+finalpatch
    os.startfile(finalpatch)
    
def kapitola(nahledyurl):
    for kapitolasmallurl in nahledyurl:
        kapitolafullurl = currpatch1 + kapitolasmallurl
        getobrazek(kapitolafullurl)

def getobrazek(kapitolafullurl):
    global imgname
    print "    Vyhledavani odkazu obrazku... ",
    obrazekshorturl = re.search(r'<img id="slide" src="(.*?)".*?>',stahniHtml(kapitolafullurl)).group(1).replace("../", "")
    imgname = obrazekshorturl
    print "Hotovo."
    obrazekfullurl = currpatch1 + obrazekshorturl
    #print obrazekfullurl
    ulozitobr(obrazekfullurl)
        
def ulozitobr(obrazekfullurl):
    print "    Ukladani obrazku "+obrazekfullurl+"... ", 
    currentpatch = os.path.expanduser("~")+"\\Downloads\\anime-manga.cz-downloader\\"+nazevserie+"\\"+chapter+"\\"
    createDir(currentpatch)
    imgData = urllib2.urlopen(obrazekfullurl).read()
    output = open(currentpatch+imgname,'wb')
    output.write(imgData)
    output.close()
    print "Hotovo."
        
def createDir(path):
    if os.path.exists(path) != True:
        os.makedirs(path)


### 18+ rozsireni ###

def vyberodkazux(url):
    global nazevserie    
    print "Stahovani hlavni stranky... ",
    stranka = stahniHtml(url)
    print "Hotovo."
    print "Vyhledavani kapitol... ",
    odkazy = odkazya(stranka) + odkazyb(stranka)
    nazevserie = re.search(r'<title>(.*?) *\| Anime - Manga.*?</title>',stranka).group(1).replace("    ", "").replace("   ", " ").replace("  ", " ")
    print "Hotovo."
    print
    print
    print "Manga "+nazevserie
    print
    return odkazy

def odkazya(stranka):
    odkazy1 = re.findall(r'<a href="(http://anime-manga.cz/manga.*?)"', stranka)
    odkazy2 = re.findall(r'<a href="(http://www.anime-manga.cz/manga.*?)"',stranka)
    odkazy = odkazy1 + odkazy2
    return odkazy
   
def odkazyb(stranka):
    odkazy18 = re.findall(r'<a href="(http://anime-manga.cz/\d[^/]*?)"|<a href="(http://www.anime-manga.cz/\d[^/]*?)"|<a href="(http://anime-manga.cz/[^/]*?\d)"|<a href="(http://www.anime-manga.cz/[^/]*?\d)"', stranka)   
    odkazy = []
    print
    print
    for odkaz18 in odkazy18:
        for i in range(4):
            if odkaz18[i]!= '':
                print "Nalezen odkaz: " + odkaz18[i]
                stranka18 = stahniHtml(odkaz18[i])
                test = re.search(r'<a href="(.*?anime-manga.cz/manga.*?)"',stranka18)
                if test is not None:
                    odkazy.append(test.group(1))
    return odkazy


print "Anime-manga.cz Downloader"
xurl = raw_input('stahnout mangu s url: http://www.anime-manga.cz/')
nahled("http://www.anime-manga.cz/"+xurl)
