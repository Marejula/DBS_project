#DBS Project2-Daten importieren in Datenbank

import psycopg2
import psycopg2.extras
import csv
import sys
conn = psycopg2.connect("host='localhost' port='5432' dbname='election' user='postgres' password='postgres'") #Dieses Modul erstellt die Verbindung mit der gegebenen Datenbank

print "Connection to database is successful"

cur = conn.cursor() #Der Befehl öffnet ein cursor, das die Datenbankoperationen ausführen wird

f = open("/home/aleksandra/Desktop/tweets.csv", 'r')

cur.copy_from(f, 'tweets', sep=';', null='\\N',size=8192)
#Hiermit werden die Daten aus der Datei tweets.csv in die Relation tweets in die Datenbank Election reinkopiert.

f.close()
conn.commit()
conn.close()
