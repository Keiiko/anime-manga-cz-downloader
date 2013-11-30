import urllib2
import re
import os

print 'napis start("http://www.anime-manga.cz/manga...")'

def start(url)
    nahled(url)

def stahniHtml(url):
    f = urllib2.urlopen(url)
    obsah = f.read()
    f.close()
    return obsah

def odkazya(url):
    global nazevserie
    print "Stahovani hlavni stranky... ",
    stranka = stahniHtml(url)
    print "Hotovo."
    print "Vyhledavani kapitol... ",
    odkazy = re.findall(r'<a href="(http://www.anime-manga.cz/manga.*?)"',stranka)
    nazevserie = re.search(r'<title>(.*?)</title>',stranka).group(1).replace(" | Anime - Manga", "")
    print "Hotovo."
    print "Manga "+nazevserie
    return odkazy

def nahled(url):
    global chapter
    global currpatch1
    odkazy = odkazya(url)
    for odkaz in odkazy:
        currpatch1 = odkaz.replace("index.html", "")
        chapter = re.search(r'.*/(.*?)/index',odkaz).group(1)
        print "Kapitola "+chapter
        print "Stahovani nahledu kapitoly... ",
        nahledhtml = stahniHtml(odkaz)
        print "Hotovo."
        print "Vyhledavani odkazu stranky... ",
        tabulka = re.search(r'<!-- Thumbnail images -->(.*?)class="xsmalltxt"',nahledhtml, re.DOTALL).group(1)
        nahledyurl = re.findall(r'<a href="(.*?)"',tabulka)
        print "Hotovo."
        kapitola(nahledyurl)
        
def kapitola(nahledyurl):
    for kapitolasmallurl in nahledyurl:
        kapitolafullurl = currpatch1 + kapitolasmallurl
        getobrazek(kapitolafullurl)

def getobrazek(kapitolafullurl):
    global imgname
    print "Vyhledavani odkazu obrazku... ",
    obrazekshorturl = re.search(r'<img id="slide" src="(.*?)".*?>',stahniHtml(kapitolafullurl)).group(1).replace("../", "")
    imgname = obrazekshorturl
    print "Hotovo."
    obrazekfullurl = currpatch1 + obrazekshorturl
    #print obrazekfullurl
    ulozitobr(obrazekfullurl)
        
def ulozitobr(obrazekfullurl):
    print "Ukladani obrazku "+obrazekfullurl+"... ", 
    currentpatch = os.path.expanduser("~")+"\\Downloads\\anime-manga.cz downloader\\"+nazevserie+"\\"+chapter+"\\"
    createDir(currentpatch)
    imgData = urllib2.urlopen(obrazekfullurl).read()
    output = open(currentpatch+imgname,'wb')
    output.write(imgData)
    output.close()
    print "Hotovo."
        
def createDir(path):
    if os.path.exists(path) != True:
        os.makedirs(path)
