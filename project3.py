import psycopg2
import psycopg2.extras
import csv
import sys
import collections
from collections import Counter

conn = psycopg2.connect("host='agdbs-edu01.imp.fu-berlin.de' port='5432' dbname='American_Election' user='student' password='password'") #Dieses Modul erstellt die Verbindung mit der gegebenen Datenbank

print "Connection to database is successful"

cur = conn.cursor()

cur.execute("SELECT * FROM enthaelt")
hashtag = cur.fetchall()

pairs = []
for i in range(len(hashtag)):
	for k in range(len(hashtag)):
		if (hashtag[i][0] == hashtag[k][0]) and (i!=k):
			pairs += [(hashtag[i][1],hashtag[k][1])]
	
# Speichert die Paare in test.csv
item_length = len(pairs[0])
with open('test.csv', 'wb') as test_file:
  file_writer = csv.writer(test_file, delimiter=';')
  for i in range(item_length):
    for row in pairs:
       file_writer.writerow(row)
test_file.close()


with open('test.csv', 'rb') as f:
    data = list(tuple(rec) for rec in csv.reader(f, delimiter=';'))
f.close()

# Die Paar-Haeufigkeit wird gezaehlt und in einer Liste zusammen mit den Paaren gespeichert
counter = collections.Counter(data) 
counted = sorted(counter.items())

# Die Paare werden zusammen mit ihrer Haeufigkeit in einer Liste aus 3-elementigen Tupeln gespeichert
tupled = []
for i in range(len(counted)):
    tupled += [(counted[i][0][0],counted[i][0][1], counted[i][1])]
	
# Speichert die Paare mit der Hauefigkeit in test1.csv
item_length = len(tupled[0])
with open('test1.csv', 'wb') as test_file:
  file_writer = csv.writer(test_file, delimiter=';')
  for i in range(item_length):
    for row in tupled:
       file_writer.writerow(row)
test_file.close()

