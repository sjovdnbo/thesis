import urllib.request as request
import zipfile
import sys
# ------------------ locations ------------------
#dip: manueel te downloaden

#todo:  reactome, reactome fi-s  http://reactomews.oicr.on.ca:8080/ReactomeRESTfulAPI/ReactomeRESTFulAPI.html
#overgeslaan: bindingdb: enkel binding met kleine moleculen etc? ///apid: concatenatie van mind, biogrid en hprd /// I2D: predicted interactions
#               zinc db: enkel small molecules /// genemania: plat /// chembl: small molecules /// molcon :http://88.80.187.10/ random site??? /// mbinfo??? https://www.mechanobio.info/
#               ebi-goa-nonintact en ebi-goa-mirna niet
#
"""
hpidb: geen link mogelijk
uniprot: http://www.uniprot.org/uniprot/?query=reviewed:yes+go:5515
    enkel source binder, niet target in data!
"""

#text files
textFiles = {}
textFiles["intAct"] = "ftp://ftp.ebi.ac.uk/pub/databases/intact/current/psimitab/intact.txt"  #werkt
textFiles["mint"] = "http://mint.bio.uniroma2.it/mitab/MINT_MiTab.txt" #werkt
textFiles["virhostnet"] = "http://virhostnet.prabi.fr:9090/psicquic/webservices/current/search/query/"+"*" #werkt niet
textFiles["bar"] = "http://bar.utoronto.ca:9090/psicquic/webservices/current/search/query/"+"*"  #werkt niet
textFiles["bhf-ucl"] = "http://www.ebi.ac.uk/Tools/webservices/psicquic/bhf-ucl/webservices/current/search/query/*" #werkt
textFiles["mentha"] = "http://mentha.uniroma2.it:9090/psicquic/webservices/current/search/query/*"

#downloads
textDownloads = {}
textDownloads["mpi"] = "http://jcvi.org/mpidb/download.php?&pname=&species_txtbox=&species_select=&dbsource=&cvname=&confidence_structure=&confidence_method=&confidence_interologs=&confidence_purification=&confidence_evidences=&submit=Search&__utmt=1&__utma=79309195.1295422092.1476435200.1477559384.1477583858.3&__utmb=79309195.2.10.1477583858&__utmc=79309195&__utmz=79309195.1476435200.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"
textFiles["dip"] = "http://dip.doe-mbi.ucla.edu/dip/File.cgi?FN=2016/tab25/dip20160731.txt"

#zip files
zipDownloads = {}
zipDownloads["mentha"] = "http://mentha.uniroma2.it/dumps/organisms/all.zip"
zipDownloads["biogrid"] = "https://thebiogrid.org/downloads/archives/Release%20Archive/BIOGRID-3.4.141/BIOGRID-ALL-3.4.141.mitab.zip"
#gzip files
gzipDownloads = {}
gzipDownloads["InnateDB"] = "http://www.innatedb.com/download/interactions/innatedb_ppi.mitab.gz"
gzipDownloads["HPRD_db"] = "http://hprd.org/edownload/HPRD_PSIMI_041310"  #tar.gz
gzipDownloads["MATRIX_DB"] = "http://matrixdb.univ-lyon1.fr/download/matrixdb_CORE.tab.gz"
gzipDownloads["REACTOME_DB"] = "http://www.reactome.org/download/current/homo_sapiens.interactions.txt.gz" #probleem: enkel human weeral, andere species: enkel via orthologie vastgelegd
#only to open on server!
#STRING_DB = "/group/biocompdb/Databases/STRING/protein.links.full.v10.txt.gz"
#------------------- functions -----------------
def readURL(url):
    #input: string of url
    #output: list of lines from site
    out = []
    try:
        fileHandle = request.urlopen(url)
        for i in fileHandle:
            #print(i)
            out.append(i)
        fileHandle.close()
    except IOError:
        print('Cannot open URL')
        out = []
    return out

def listToMiTab(list):
    string = ""
    for i in list:
        i = str(i).strip("b'").strip("\\n'")
        i = i.split('\\t')
        for j in i:
            string+=str(j)
            string+="\t"
        string+='\n'
    return string
def writeToFile(filename, content):
    with open(filename,"w") as fh:
        fh.write(content)
        fh.close()

#--------------------script----------------------
#textfiles processing
for i in textFiles.items():
    print("fetching:",i[0],"\n\t\t URL:",i[1])
    content = listToMiTab(readURL(i[1]))
    writeToFile(i[0]+".mitab",content)


