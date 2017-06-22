import sys
import urllib.request

def makeURL(id):
    url = "http://purl.obolibrary.org/obo/MI_{}".format(str(id))
    return url

def getContent(id):
    url  = makeURL(id)
    content = urllib.request.urlopen(url)

    return content

def getDBID(id):

    content = getContent(id)
    for i in content:
        i = str(i)
        if parser in i:
            return (i.split(parser)[1].split(">")[1].split("<")[0])

