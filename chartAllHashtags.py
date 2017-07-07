#!/usr/bin/python2.7
# -*- coding: utf_8 -*-

import psycopg2
import psycopg2.extras
import csv
import sys
import collections
from operator import itemgetter
from datetime import datetime, date, time
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
 
# Mit diesem Programm wird ein Balkendiagramm mit den Haeufigkeiten aller Hashtags an einem Tag erstellt.

# Erstellt eine Verbindung zum Server und der Datenbank
conn = psycopg2.connect("host='agdbs-edu01.imp.fu-berlin.de' port='5432' dbname='American_Election' user='student' password='password'") 

print "Verbindung mit Datenbank erfolgreich"

cur = conn.cursor()

cur.execute("SELECT t.t_time, e.hashtag_name FROM enthaelt e, tweet t WHERE e.t_id = t.t_id ORDER BY t.t_id; ")
hashtag = cur.fetchall() # Speichert alle Reihen des SQL-Abfrage in Tupeln in einer Liste
cur.close() # Die Verbindung wird wieder beendet


# Alle Daten(Dates) werden von datime in einen String umgewandelt und in einer Liste gespeichert
allDates = []
for i in range(len(hashtag)):
	d = hashtag[i][0]
	allDates += [d.strftime('%Y, %m, %d')]

#Zaehlt die Anzahl gleicher Dates in einem Dictionary:
counter = collections.Counter(allDates)

#Der Dictionary wird nach den Keys in lexikograpischer Ordung geordnet
# und als Liste von Tupeln zusammen mit den Values gespeichert
sortedList = sorted(counter.items(), key=itemgetter(0))

dateKey = []
dateValue = []
# Die sortierte Liste wird druchgegangen und auf zwei Listen aufgeteilt
# In dateKey werden die Dates gespeichert und in dateValue die Haeufigkeiten 
for i in range(len(sortedList)):
	dateKey.append(sortedList[i][0])
	dateValue.append(sortedList[i][1])
print dateKey
print dateValue


# Hier wird ein einfaches Balkendiagramm mit den Haeufigkeiten erstellt
objects = dateKey
yPos = np.arange(len(objects))
performance = dateValue
 
plt.bar(yPos, performance, align='center', alpha=0.3)
plt.xticks(yPos, objects, rotation="vertical")
plt.ylabel('Haeufigkeit')
plt.title('Haeufigkeit aller Hashtags pro Tag')
plt.show()





