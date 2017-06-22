#! /software/shared/modulefiles/general/python/x86_64/2.7.2
import MySQLdb
import ConfigParser
import subprocess

inputAnnotation = open("annotation.csv")
inputAnnot_sources = open("annot_sources.csv")


def connect_myqsl(inifile):
    # read inifile
    config = ConfigParser.ConfigParser()
    config.read(inifile)
    username = config.get("Database", "username")
    pswd = config.get("Database", "password")
    db = config.get("Database", "db")
    url = config.get("Database", "url")
    portname = int(config.get("Database", "port"))

    # connect
    cnx = MySQLdb.connect(user=username, passwd=pswd, host=url, db=db, port=portname)
    cur = cnx.cursor()
    return cur


def addlineAnnotation(line):
    line = line.strip().split(",")
    ins = "INSERT INTO annotation (gene_id, species, transcript, coord_cds, start, stop, coord_transcript, seq, strand, chr, type, check_transcript, check_protein,transl_table) " \
          "VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(line[0], line[1], line[2], line[3], int(line[4].strip("'")), int(line[5].strip("'")),
                               line[6], line[7], "'+'",line[9],  line[10], line[11],
                               line[12], int(line[13].strip("'")))
    return ins

def addlineAnnot_sources(line,incr):
    line = line.strip().split(",")

    ins = "INSERT INTO annot_sources (pkey, source, url, species, common_name, shortname, description, paper, pubmed_id, tax_id, mitochondrion, chloroplast, disclaimer) " \
          "VALUES ({},{},{},{},{},{},{},{},'0',{},{},{},{})".format(incr, line[1], line[2], line[3], line[4], line[5], line[6], line[7],  int(line[9].strip("'")),line[10], line[11],
                               line[12])
    return ins
def deleteLines(table):
    return "DELETE FROM {};".format(table)

db_handle = connect_myqsl("db_plaza_interologs_01.ini")
print("uploading annotation database")
db_handle.execute(deleteLines("annot_sources"))
db_handle.execute(deleteLines("annotation"))

for i in inputAnnotation:
    db_handle.execute(addlineAnnotation(i))

print("uploading annotation sources database")
incr = 1
for i in inputAnnot_sources:

    db_handle.execute(addlineAnnot_sources(i,incr))
    incr +=1
