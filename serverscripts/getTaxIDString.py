import sys
import urllib.request

def makeURL(id):
    url = "https://www.ncbi.nlm.nih.gov/taxonomy/?term={}".format(str(id))
    return url

def getContent(id):
    url  = makeURL(id)
    content = urllib.request.urlopen(url)

    return content

def getTaxID(id):
    parser = "ncbi_uid={}&amp;link_uid={}&amp".format(str(id), str(id))
    content = getContent(id)
    for i in content:
        i = str(i)
        if parser in i:
            return (i.split(parser)[1].split(">")[1].split("<")[0])

