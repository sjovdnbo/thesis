import urllib.request as ur
import sys
# ------------------ locations ------------------
#todo:  reactome, reactome fi-s  http://reactomews.oicr.on.ca:8080/ReactomeRESTfulAPI/ReactomeRESTFulAPI.html
#overgeslaan: bindingdb: enkel binding met kleine moleculen etc? ///apid: concatenatie van mind, biogrid en hprd /// I2D: predicted interactions
#               zinc db: enkel small molecules /// genemania: plat /// chembl: small molecules /// molcon :http://88.80.187.10/ random site??? /// mbinfo??? https://www.mechanobio.info/
#
#
"""
wat met ebi-goa-miRNA en ebi-goa-nonintact?
hpidb: geen link mogelijk
uniprot: http://www.uniprot.org/uniprot/?query=reviewed:yes+go:5515
    enkel source binder, niet target in data!
"""

#text files
INTACT_DB = "ftp://ftp.ebi.ac.uk/pub/databases/intact/current/psimitab/intact.txt"
MINT_DB = "http://mint.bio.uniroma2.it/mitab/MINT_MiTab.txt"
VIRHOSTNET_DB = "http://virhostnet.prabi.fr:9090/psicquic/webservices/current/search/query/*"
DIP_DB = "http://dip.doe-mbi.ucla.edu/dip/File.cgi?FN=2016/tab25/dip20160731.txt"
BAR_db = "http://bar.utoronto.ca:9090/psicquic/webservices/current/search/query/*"
BHF_UCL_DB = "http://www.ebi.ac.uk/Tools/webservices/psicquic/bhf-ucl/webservices/current/search/query/*"
#mpiDB = "http://jcvi.org/mpidb/download.php?&pname=&species_txtbox=&species_select=&dbsource=&cvname=&confidence_structure=&confidence_method=&confidence_interologs=&confidence_purification=&confidence_evidences=&submit=Search&__utmt=1&__utma=79309195.1295422092.1476435200.1477559384.1477583858.3&__utmb=79309195.2.10.1477583858&__utmc=79309195&__utmz=79309195.1476435200.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"

#zip files
MENTHA_DB = "http://mentha.uniroma2.it/doDownload.php?file=organisms/all.zip" #zipfile! unzippen!
BIOGRID_DB = "https://thebiogrid.org/downloads/archives/Release%20Archive/BIOGRID-3.4.141/BIOGRID-ALL-3.4.141.mitab.zip" #controleren of laatste versie
INNATE_DB = "http://www.innatedb.com/download/interactions/innatedb_ppi.mitab.gz"
HPRD_db = "http://hprd.org/edownload/HPRD_PSIMI_041310"
MATRIX_DB = "http://matrixdb.univ-lyon1.fr/download/matrixdb_CORE.tab.gz"
REACTOME_DB = "http://www.reactome.org/download/current/homo_sapiens.interactions.txt.gz" #probleem: enkel human weeral, andere species: enkel via orthologie vastgelegd
#only to open on server!
#STRING_DB = "/group/biocompdb/Databases/STRING/protein.links.full.v10.txt.gz"
#------------------- functions -----------------
def readURL(url):
    #input: string of url
    #output: list of lines from site
    out = []
    try:
        fileHandle = ur.urlopen(url)
        for i in fileHandle:
            out.append(i)
        fileHandle.close()
    except IOError:
        print('Cannot open URL')
        out = []
    return out

def listToMiTab(list):
    string = ""
    for i in list:
        string+=i
        string+="\t"
    string+='\n'
    return string

class PsicquicService:
    def __init__(self,name,restUrl):
        self.name = name
        self.restUrl = restUrl

def readActiveServicesFromRegistry():
    registryActiveUrl = 'http://www.ebi.ac.uk/Tools/webservices/psicquic/registry/registry?action=ACTIVE&format=xml'
    content = readURL(registryActiveUrl)
    contentArray = str(content).split("><")
    services = []
    i = 0
    while i in range(len(contentArray)):
        node = contentArray[i]
        if node[:4]=="name":
            name = node.strip("name")
            name = name.lstrip(">")
            name = name.strip("</")
            i+=2
            node = contentArray[i]
            if node[:7]=='restUrl':
                restUrl = node.strip("restUrl>")
                restUrl = restUrl.strip("</restUrl")

                service = PsicquicService(name, restUrl)
                services.append(service)
        i+=1

    return services
def getXrefByDatabase(line, database):
   fields = line.split('|')
   for field in fields:
       parts = field.split(':')
       db = parts[0]
       value = parts[1].split('(')[0]
       if database == db:
           return value
   else:
    # if no db found, return the first field
        return fields[0]


def queryPsicquic(psicquicRestUrl, query, targetfile):
    psicquicUrl = psicquicRestUrl + "/query/" + query

    print('\t\tURL: ' + psicquicUrl)
    q = readURL(psicquicUrl)
    psicquicResultLines = str(q).split('\\n')
    print('\t\t databasesize: ',len(psicquicResultLines))

    for line in psicquicResultLines:
        line = str(line).strip("'b")
        cols = str(line).split("\\t")
        s = listToMiTab(cols)
        targetfile.write(s)

        #print('\t' + getXrefByDatabase(cols[0], 'uniprotkb') + ' interacts with ' + getXrefByDatabase(cols[1], 'uniprotkb'), "\t", "pubmedID:", cols[8])

# -----------------------------------------------------
query = sys.argv[1]
print(query)
#param:  MI%3A0915%20AND%20MI%3A0045   voor physical interaction en experimental interaction detection
#MI%3A0915%20AND%20MI%3A0045 MI:1047 = protein protein interaction and MI:1054 = experimentally observed

#biogrid key: d999ead44b4af7a4d7273d1bab6db719
services = readActiveServicesFromRegistry()

for service in services:
    print('Service: ' + service.name + ' ================================================================== ')
    targetfile = open(service.name+".mitab",'w')
    queryPsicquic(service.restUrl, query,targetfile)
    targetfile.close()
    print('\n')


"""
gzip -c naam.txt.gzip > naam.txt
head naam.txt > naamhead.txt
"""