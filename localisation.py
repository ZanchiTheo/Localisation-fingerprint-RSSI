#import des librairies 
import serial
import string
import numpy as np
import json
import operator
from operator import itemgetter
import re

# Déclaration du pattern pour trier les AP par nom
pattern = re.compile("AP[0-9]")

# Interaction avec l'utilisateur pour savoir sur quel port écouter
x = "n"
# On fait une boucle tant que l'utilisateur ne valide pas son choix
while x != "o":
    print("Entrez le numéro de port série de votre ESP (COM10 par exemple) :")
    # Input du port
    numPort = input()
    print("Vous avez choisi le port " + numPort + " Confirmer ? o/n :")
    # Input de la validation
    x = input()

# On déclare le port série avec la valeur rentrée par l'utilisateur
# On entoure d'un try catch au cas-où la valeur rentrée par l'utilisateur n'est pas valide
try:
    ser = serial.Serial(numPort, 9600)
except:
    print("La valeur du port rentrée n'est pas valide")

# Boucle principale du script
while True:
    # On récupère le message de l'esp82 
    line = ser.readline()

    # On convertit en string le message reçu
    result = str(line, 'utf-8')
    #print(result)

    # On supprime le premier '/' ainsi que le \n\r de la fin du message
    result = result[1:-2]
    #print(result)

    # On divise le string en un tableau de string en utilisant le marqueur '/'
    result = str.split(result, '/')
    #print(result)

    # On boucle sur chaque case du tableau afin de les diviser en deux parties : le nom de l'AP 
    # et la puissance associée à cet AP
    final = []
    for s in result:
        s = str.split(s, ',')
        final.append(s)
    #print(final)

    # On boucle sur chaque case du tableau final afin de ne garder que
    # les noms des AP que l'on utilise pour se localiser dans la variable listAP
    listAP = []
    data = []
    for s in final:
        if pattern.match(s[0]):
            listAP.append(s)
    
    # Le tableau listAP est composé des AP : AP1, AP2, AP3, AP4, AP5
    # On trie le tableau afin de les avoir dans le bon ordre
    listAP = sorted(listAP, key=itemgetter(0))

    # On boucle sur le tableau listAP afin de ne garder dans le tableau data que la valeur des puissances
    for s in listAP:
        data.append(int(s[1]))
    #print(listAP)
    print(data)

    # Script de localisation
    with open('APdatas.json') as json_file:
        # On récupère le contenu du fichier Json
        data = np.array(data)
        dataJ = json.load(json_file)
        res=[]

        # On boucle sur toutes les positions de référence enregistrées dans le fichier Json
        for count,p in enumerate( dataJ['Position']):
            # Pour chaque position de référence : 
            # on calcule l'erreur par différence de norme de vecteur : 
            # norme(vecteur des puissances mesurées) - norme(vecteur des datas du fichier Json)
            res.append(("Accesspoint: "+list(p.values())[0],abs(np.linalg.norm(data)-np.linalg.norm(list(p.values())[1:]))))
        
        # Tri par erreur la moins élevée            
        res.sort(key = operator.itemgetter(1))

        # La première case du tableau res contient la position qui est jugée la plus proche par l'algorithme
        #print (res)
    
    