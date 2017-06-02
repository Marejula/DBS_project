#!/usr/bin/python2.7
# -*- coding: utf_8 -*-

#DBS Project2-Daten importieren in Datenbank
import psycopg2
import psycopg2.extras
import csv
import sys

conn = psycopg2.connect("host='localhost' port='5432' dbname='election' user='postgres' password='postgres'") #Dieses Modul erstellt die Verbindung mit der gegebenen Datenbank

print "Connection to database is successful"

cur = conn.cursor() #Der Befehl öffnet ein cursor, das die Datenbankoperationen ausführen wird


#Hiermit werden die Daten aus der Datei tweets.csv in die Relation tweets in die Datenbank Election reinkopiert.
tweets = open("tweets.csv", 'r')
cur.copy_from(tweets, 'tweet', sep=';', null='', size=8192, columns=('handle', 't_text', 'is_retweet', 'original_author', 't_time', 'in_reply_to_screen_name', 'is_quote_status', 'retweet_count', 'favorite_count'))
# Es wird jedoch immer eine Fehlermeldung ausgegeben

#Dieses Einfügen der Daten funktioniert:
hashtags = open("hashtags.csv", 'r')
cur.copy_from(hashtags, 'hashtag', sep=';', null='', size=8192)


#Funktioniert nicht, wegen Fremdschlüssel. Da die 'tweet'-Ralation noch nicht gefüllt ist:
enthaelt = open("enthaelt.csv", 'r')
cur.copy_from(enthaelt, 'enthaelt', sep=';', null='', size=8192)

tweets.close()
hashtags.close()
enthaelt.close()
conn.commit()
conn.close()
