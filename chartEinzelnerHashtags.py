#!/usr/bin/python2.7
# -*- coding: utf_8 -*-

import psycopg2
import psycopg2.extras
import csv
import sys
import collections
from operator import itemgetter
from datetime import datetime, date, time
import sys
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np

#In diesem Programm wird ueber die Console ein Hashtagname eingelesen und dessen Haeufigkeit an bestimmten Tagen in einem Balkendiagramm dargestellt.
 
# Erstellt eine Verbindung zum Server und der Datenbank
conn = psycopg2.connect("host='agdbs-edu01.imp.fu-berlin.de' port='5432' dbname='American_Election' user='student' password='password'") #Dieses Modul erstellt die Verbindung mit der gegebenen Datenbank

print "Verbindung mit Datenbank erfolgreich"

cur = conn.cursor()

cur.execute("SELECT DISTINCT e.hashtag_name, t.t_time FROM enthaelt e, tweet t WHERE e.t_id = t.t_id ORDER BY e.hashtag_name, t.t_time;")
hashtag = cur.fetchall()

# Speichert alle Reihen des SQL-Abfrage in Tupeln in einer Liste
cur.close() # Die Verbindung wird wieder beendet

# Nimmt das 2.Argument der Consolen-Eingabe
gesHashtag = sys.argv[1]

# Alle Daten(Dates) des Hashtags von gesHashtag werden von datime 
# in einen String umgewandelt und in einer Liste gespeichert.

hashtagDates = []
for i in range(len(hashtag)):
	d = hashtag[i][1]
	if hashtag[i][0] == gesHashtag:
		hashtagDates += [d.strftime('%y, %m, %d')]

if hashtagDates == []: # Durch diese Abfrage wird erfasst, ob der gawaehlte Hashtag in unserer Datenbank vorhanden ist.
	print 'Dieser Hashtag ist nicht aufrufbar!'
else:
# Wenn der Hashtag vorhanden ist, wird Anzahl gleicher Dates in einem Dictionary gespeichert:
	counter = collections.Counter(hashtagDates)

#Der Dictionary wird nach den Keys in lexikograpischer Ordung geordnet
# und als Liste von Tupeln zusammen mit den Values gespeichert
	sortedList = sorted(counter.items(), key=itemgetter(0))

# Die sortierte Liste wird druchgegangen und auf zwei Listen aufgeteilt
# In dateKey werden die Dates gespeichert und in dateValue die Haeufigkeiten 
	dateKey = []
	dateValue = []
	for i in range(len(sortedList)):
		dateKey.append(sortedList[i][0])
		dateValue.append(sortedList[i][1])

# Hier wird ein einfaches Balkendiagramm mit den Haeufigkeiten erstellt mit der Hilfe von dem Paket matplotlib.pyplot.
	objects = dateKey
	yPos = np.arange(len(objects))
	performance = dateValue
 
	plt.bar(yPos, performance, align='center', alpha=0.5)
	plt.xticks(yPos, objects, rotation="vertical")
	plt.ylabel('Haeufigkeit')
	plt.title('Haufigkeit von ' +gesHashtag+ 'pro Tag')
 
	plt.show()
