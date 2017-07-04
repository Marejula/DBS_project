import pandas as pd # Python Data Analysis Library
import numpy as np # Scientific Computing
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt # Python 2D plotting library

# Einlesen aller Tweetnummern und Hashtags aus der Enthaelt-Tabelle
df = pd.read_csv('kopie.csv')
tweetnr = df['nr']
hashtags = df['hashtag']

# alle unikate Hashtags in Liste
unihash = list(set(hashtags))
# Anzahl an verschiedenen unikaten Hashtags
nr_hashtags = len(unihash)
# Kreuztabelle Anzahl x Anzahl mit 0 initialisiert
ct = np.zeros([nr_hashtags, nr_hashtags])

# Gib jedem Hashtag eine Id; jede Id ist Index in ct-Tabelle
hash_ids = {}
for i, t in enumerate(unihash):
    hash_ids[t] = i
    
# np arrays aus Tweetnummern und Hashtags
npt = np.array(tweetnr)
nph = np.array(hashtags)

# alle einzelnen Tweetnummern
tweets_set = set(tweetnr)

# Auftreten der Hashtags gruppiert und entsprechend Fuellen der Kreuztabelle
for t in tweets_set:
    auftreten = nph[np.argwhere(npt==t)]
    #print auftreten
    for h in auftreten:
        for h2 in auftreten:            
            ct[hash_ids[h[0]], hash_ids[h2[0]]] = ct[hash_ids[h[0]], hash_ids[h2[0]]] + 1
# Normalisierung der Kreuztabelle (zeilenweise nichtidiagonale Elemente/diagonales Element; diagonale Elemente = 1)
ct_std = ct / np.diag(ct, 0)
#print ct_std

# Kmeans auf Kreuztabelle -> Zuordnung der Hashindices zu Klassen
# Auffaellig ist, dass die meisten Hashtags in einer Klasse landen 
# (Die Klasse mit sich eher unaehnlichen Hashtags bzw. Rest)
# Schlussfolgerung: kmeans ist fuer den Datensatz nicht so gut geeignet.
kmeans = KMeans(n_clusters=5, random_state=5).fit(ct_std)
print kmeans.labels_

#Visualisierung mit Hauptkomponentenanalyse (PCA) 2 Komponenten fuer 2dim Plot
# Bestaetigt die Annahme, dass das Clustering nicht so schoen ist. Die roten Punkte sind Hashtags, die ahenlich 
# unaehnlich sind. Achtung: Skalierung!
pca = PCA(n_components=2)
pca.fit(ct_std)

fig, ax = plt.subplots()
cdict = {'red': 0, 'green': 1, 'blue': 2, 'yellow': 3, 'orange': 4}

for color in ['red', 'green', 'blue', 'yellow', 'orange']:
    ind = cdict[color]
    now_y = pca.components_[0][kmeans.labels_ == ind]
    now_x = pca.components_[1][kmeans.labels_ == ind]
    ax.scatter(now_y, now_x, c=color,label=color)

ax.grid(True)

plt.show()
fig.savefig('plot1.png')

# rot: Gemischt
# blau Republikaner: #mattschlapp #jenniferrubin #gop
# gelb: #trump #carrier #jobs #ford #mexico
# gruen: #trump2016
# orange: #utahprimary #mormon #trumpcountry #utah4trump #utah

inv_map = {v: k for k, v in hash_ids.iteritems()}

cluster_locs = np.where(kmeans.labels_ == 2)[0]
for loc in cluster_locs:
    print inv_map[loc]
    
# Test: Eine moegliche Verbesserung durch Heuristik:
# Alle Eintraege in der Matrix, die nicht 0 sind, in 1 umwandeln.
# Verlust an Information aber Hashtags werden aehnlicher.
onesmatrix_full = np.copy(ct_std)
onesmatrix_full[onesmatrix_full != 0] = 1

# Heuristik gibt etwas bessere Verteilung
kmeans = KMeans(n_clusters=5, random_state=5).fit(onesmatrix_full)
print kmeans.labels_

# PCA gibt optisch ein ganz gutes Ergebnis.
pca = PCA(n_components=2)
pca.fit(onesmatrix_full)

fig, ax = plt.subplots()
cdict = {'red': 4, 'green': 1, 'blue': 2, 'yellow': 3, 'orange': 0}

for color in ['red', 'green', 'blue', 'yellow', 'orange']:
    ind = cdict[color]
    now_y = pca.components_[0][kmeans.labels_ == ind]
    now_x = pca.components_[1][kmeans.labels_ == ind]
    ax.scatter(now_y, now_x, c=color)

ax.legend()
ax.grid(True)

plt.show()
fig.savefig('plot2.png')

# Um zu testen, ob die Klassen auch sinvoll sind, Ausgabe der Hashtags der blauen Klasse:
# Trumpbezogene-Hashtags -> gute Klasse
# Zum Vgl. gruene Klasse eher gemischt
# gelbe Klasse auch Trump: #votetrump #makeamericagreatagain
# orange: Trump: #utahprimary #mormon #trumpcountry #utah4trump #utah
# rot: #trump2016

cluster_locs = np.where(kmeans.labels_ == 2)[0]
#cluster_locs

for loc in cluster_locs:
    print inv_map[loc]
    
