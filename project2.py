#!/usr/bin/python2.7
# -*- coding: utf_8 -*-

#DBS Project2-Daten importieren in Datenbank
import psycopg2
import psycopg2.extras
import csv
import sys

conn = psycopg2.connect("host='agdbs-edu01.imp.fu-berlin.de' port='5432' dbname='American_Election' user='student' password='password'") #Dieses Modul erstellt die Verbindung mit der gegebenen Datenbank

print "Connection to database is successful"

cur = conn.cursor() #Der Befehl öffnet ein cursor, das die Datenbankoperationen ausführen wird


# Hiermit werden die Daten aus der Datei tweets.csv in die Relation tweets in die Datenbank Election reinkopiert.
# Es muss vorher von Hand die erste Spalte von 'tweets.csv' gelöscht werden.
tweets = open("tweets.csv", 'r')
cur.copy_from(tweets, 'tweet', sep=';', null='', size=8192, columns=('t_id','handle', 't_text', 'is_retweet', 'original_author', 't_time', 'in_reply_to_screen_name', 'is_quote_status', 'retweet_count', 'favorite_count'))
tweets.close()

# Hiermit werden die Hashtags eingelesen:
hashtags = open("hashtags.csv", 'r')
cur.copy_from(hashtags, 'hashtag', sep=';', null='', size=8192)
hashtags.close()

# Die Daten aus "enthaelt.csv" werden importiert
enthaelt = open("enthaelt.csv", 'r')
cur.copy_from(enthaelt, 'enthaelt', sep=';', null='', size=8192)
enthaelt.close()


conn.commit()
conn.close()
