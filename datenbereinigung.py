#!/usr/bin/python2.7
# -*- coding: utf_8 -*-

import csv
import re

with open('american-election-tweets.csv','rb') as csvIn, open('tweets.csv','wb') as csvOut, open('hashtagsAll.csv', 'wb') as csvOutHashtag:
# Es ist wichtig, dass der 'delimiter' der csv-Dateien auf ';' gesetzt wird, da sonst in der Spalte 'text' bei jedem Komma eine neue Spalte angefangen wird.
    reader = csv.reader(csvIn, delimiter=';')
    writer = csv.writer(csvOut, delimiter=';', quoting=csv.QUOTE_ALL)
    writer2 = csv.writer(csvOutHashtag, delimiter=';')

# Wie schon aus der Nachtragung zur 1.Iterartion, beschränken wir uns auf die Spalten:
# handle, text, is_reweet, original_author, time, in_reply_to_screen_name, is_quote_status, favourite_count,  retweet_count

    for line in reader:
# Die erste Zeile wird nicht eingefügt. In der 'text'-Spalte werden die Zeilenumbrüche entfernt, damit ein String entsteht. Und für is_retweet und is_quote_status werde die Bool-Werte großgeschrieben, damit SQL sie erkennt.
	if line[0] == 'handle': continue
        writer.writerow((line[0], line[1].replace('\n','   '), line[2].upper(), line[3], line[4], line[5], line[6].upper(), line[7], line[8]))

# Sucht die Hashtags der Einträge von Spalte 'text' und speichert die als liste in 'hashtags'. 
# Verwendet dafür einen ragulären Ausdruck. 
# Hier treten die Fehler auf
	HashtagStart = set([i for i in line[1].split() if i.startswith("#")])
	TweetHashtags = list(set([re.sub(r"(\W+)$", "", j) for j in HashtagStart]))
    	#for i in range(0, len(TweetHashtags)):
	#	TweetHashtags[i] = TweetHashtags[i].lower()
	writer2.writerow(TweetHashtags)
    
csvIn.close()
csvOut.close()
csvOutHashtag.close()


# In der 'hashtagAll.csv' haben die Fehler in den Hashtags manuell behoben, die aufgetreten sind. Soweit wir gesehen haben waren es insgesamt 4.
with open('hashtagsAll.csv', 'rb') as csvInHashtag, open('hashtags.csv', 'wb') as csvOutHashtagOne:
    reader2 = csv.reader(csvInHashtag, delimiter=';')
    writer3 = csv.writer(csvOutHashtagOne, delimiter=';')

# Die ganzen Hashtags werden zunächst in einer Liste gespeichert, in der alle Buchstaben klein geschrieben sind, 
# damit die set()-Funktion gleiche Hashtags erkennen kann und diese nur einmal in die Menge einfügt. 
# Am Ende gibt das eine Liste in der jeder Hashtag genau einmal vorkommt.
    liste = []
    for row in reader2:
	for i in range(0, len(row)):
		row[i] = row[i].lower()	
	liste = list(set(liste + row))
    

    for i in range(0, len(liste)):
# Damit die einzelnen Einträge aus 'liste' in einer Spalte geschrieben werden:
    	writer3.writerow([liste[i]])

csvInHashtag.close()
csvOutHashtagOne.close()



with open('hashtagsAll.csv', 'rb') as csvInEnthaelt, open('enthaelt.csv', 'wb') as csvOutEnthaelt:
    reader3 = csv.reader(csvInEnthaelt, delimiter=';')
    writer4 = csv.writer(csvOutEnthaelt, delimiter=';')
# Die 'hashtagAll.csv'-Datei wird so verändert, dass alle leeren Spalten rausgeworfen werden und eine extra Spalte mit dem vorherigen Zeilenindex eingefügt wird. Und die Hashtags einzeln mit Zeilenindex gespeichert
# Mit 'enthaelt.csv' kann dann die enthealt-Relation erstellt werden.
# Zudem werden noch alle Buchstaben klein geschrieben, damit die Hastags mit denen aus 'hashtags.csv' verglichen werden können.
    
    i = 1
    liste2 = []
    for row in reader3:
	if any(row):
	    for j in range(0, len(row)):
		row[j] = row[j].lower()
	    	liste2 = list(liste2 + [(i,row[j])])
	i += 1
    for k in range(0, len(liste2)):
	    writer4.writerow(liste2[k])


csvInEnthaelt.close()
csvOutEnthaelt.close()


