import requests, json
import urllib.parse
import csv

api_url = "https://api-adresse.data.gouv.fr/search/?q="

pays_test = ['Allemagne', 'Argentine', 'Australie', 'Autriche', 'Belgique', 'Brésil', 'Canada',
             'Chine', 'Corée du Sud', 'Cuba', 'Danemark', 'Égypte', 'Espagne', 'États-Unis',
             'France', 'Grèce', 'Hong Kong', 'Hongrie', 'Inde', 'Iran', 'Irlande', 'Israël',
             'Italie', 'Japon', 'Mali', 'Mexique', 'Norvège', 'Nouvelle-Zélande', 'Pérou',
             'Pologne', 'Portugal', "République fédérale d'Allemagne", 'Royaume-Uni', 'Russie',
             'Sénégal', 'Suède', 'Suisse', 'Taïwan', 'Tchécoslovaquie', 'Tchéquie', 'Thaïlande',
             'Turquie', 'Yougoslavie', 'Roumanie']

# il faut rajouter union soviétique manuellement dans le csv

res = []
for pays in pays_test:
    r = requests.get(api_url + urllib.parse.quote(pays))
    print(r.content.decode('unicode_escape'))
    res.append({pays: r})

csv_filename = "geocoded_countries.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Pays", "Latitude", "Longitude"])
    csv_writer.writerows(res)



