## <span style="color:red">⚠ THIS README IS IN FRENCH, PLEASE USE TRANSLATER IF NEEDED ⚠</span>
<br><br>
![banner](img/readme-banner.png)
<br><br>
![Static Badge](https://img.shields.io/badge/ESIEE%20Paris%20-%20Projet%20E4%20-%20green?style=flat)
![Static Badge](https://img.shields.io/badge/last%20commit%20-%20janurary%202024%20-%20orangered)

#### OUTILS : (Scrapy / MongoDB / Flask / ElasticSearch) via Python; HTML/CSS/JS; Docker

Projet qui récupère les données hébergées sur le site *'senscritique.com'*, les stocke sur une 
base de données Mongo et les affiche à travers une application Web grâce à l'utilisation du package 
Flask. <br>
Pour améliorer le service Web, nous avons également utilisé ElasticSearch, du CSS et du 
JavaScript. Il utilise la technologie Docker pour faciliter sa portabilité et sa reproductibilité.

###### Résultat du projet
![demo](img/demo.gif)

## Guide de l’utilisateur
- [Téléchargement](#1---téléchargement) 
- [Lancer le projet](#2---lancer-le-projet)
- [Utiliser Flask](#3---utiliser-flask)

## Guide du développeur
- [Structure logique](#1---structure-logique-du-projet)
- [Continuer le développement]()


# GUIDE DE L’UTILISATEUR

### Prérequis

Dans un premier temps, regardons, ce que vous devez installer pour pouvoir récupérer et utiliser 
le projet.

Deux outils sont nécessaires :

1) Il faut avoir [Git](https://git-scm.com/download) pour cloner le projet depuis le dépôt en ligne GitHub.
2) Il faut avoir [DockerDesktop](https://www.docker.com/products/docker-desktop/) pour faire 
   fonctionner le projet.

## 1 - Téléchargement

Dans cette partie, nous allons importer le projet disponible sur GitHub dans le but de l’avoir 
sur la machine locale.

Pour ce faire, ouvrez le ‘Git Bash’, vous pouvez le chercher depuis la barre
de recherche de votre système d'exploitation, et rendez-vous dans le dossier où vous désirez stocker
le projet grâce à la commande :
```bash 
$ cd <sous-répertoire désiré>/
```
<br>
Lorsque vous êtes à l'endroit désiré, rentrez la commande suivante dans le 
terminal :

```bash 
$ git clone https://github.com/hugocrt/data_engineering_e4_project
```
![cloning project](img/cloning-project.png)<br>
⚠ Attendez l'importation totale du projet ⚠

## 2 - Lancer le projet

Commencez par rejoindre le dossier du projet :
```bash 
$ cd data_engineering_e4_project/
```
Une fois dedans, afficher le contenu grâce à la commande :
```bash 
$ ls
```
Vous devriez normalement voir cela :
<br><br>
![ls project](img/ls-project.png)
<br><br>
Une fois que vous êtes bien dans ce répertoire, vérifiez que votre application DockerDesktop 
est en fonctionnement (application sur la droite de l'image).
<br><br>
![taskbar](img/taskbar.png)
<br><br>
Enfin, pour lancer le projet, il suffit de rentrer la commande suivante dans le GitBash.
```bash 
$ docker-compose up -d
```

Une fois cela fait, vous devriez voir apparaître des lignes dans votre Bash. Ces dernières ne 
seront pas forcément identiques à celles de l'image ci-dessous si c'est votre première 
installation du projet, cela ne change rien. 
<br><br>
![docker-compose up -d](img/docker-compose-up-d.png)
<br><br>
Veuillez attendre jusqu'à ce que vous voyiez un groupe de conteneurs apparaître dans votre 
application DockerDesktop, cela peut prendre plusieurs minutes selon votre connexion internet.<br>
Il y a 4 services (4 conteneurs distincts ici) dans ce groupe de conteneurs, le service 
'api_web' ne passera au vert que lorsque 'scraping' sera terminé.

###### DockerDesktop lorsque le groupe de conteneurs vient d'être créé
![desktop1](img/desktop1.png)
###### DockerDesktop une fois 'scraping' terminé correctement
![desktop2](img/desktop2.png)

Veillez à ne pas arrêter les services pour le bon fonctionnement de l'application Web Flask.<br>
Une fois le service 'api_web' en vert, vous pouvez cliquer sur le port souligné en bleu 
*'5000 :5000'* (voir image ci-dessus) ou bien cliquer sur ce
<a href="http://localhost:5000">lien</a>.

## 3 - Utiliser Flask

Lorsque vous ouvrez le lien, vous arrivez sur la page d'accueil, c'est une utilisation 
classique de site Web :
- Une barre de navigation est disponible en haut de la page. 
- En bas de page se trouve un footer avec des informations.
- Concernant le contenu de chaque page, vous trouverez plus de détails sur comment utiliser et 
  comprendre nos pages ci-dessous.

###### Page d'accueil du service Web
![accueil](img/web_accueil.png)

Vous y trouverez quelques informations concernant le projet et le site. 

###### Page de visualisation de la base de données
![db1](img/db1.png)

Ici, vous trouverez tous les films que nous récupérons et toutes les informations relatives à 
ces derniers. Vous pouvez ajuster la recherche grâce à des filtres et les trier par ordre 
croissant et décroissant.

###### Page de visualisation de la base de données (pagination)
![db2](img/db2.png)

Comme vous pouvez le voir, afin de rendre tout cela visible, nous avons bloqué à 30 le nombre de 
films par page, cela implique donc un système de pages ! Vous pouvez naviguer librement 
entre les différentes pages grâce aux boutons (+/- 1 page) ou grâce à un sélecteur pour choisir 
n'importe quelle page disponible.

###### Page de visualisation géographique (carte)
![carte](img/carte.png)

Ici, vous pouvez retrouver le nombre de films par pays dans le top 1000 de manière visuelle, avec 
une légende colorée et une courte analyse en dessous de la carte. Vous pouvez bien entendu vous 
déplacer et utiliser les outils de zoom sur la carte.

###### Page d'analyses
![carte](img/analyse1.png)

Sur cette page, vous retrouverez différentes analyses appuyées par des graphiques.
<br><br>
### <span style="color : dodgerblue">Bonne exploration sur notre application Web٩(^ᴗ^)۶</span>

# GUIDE DU DÉVELOPPEUR

Dans un premier temps, nous rappelons que nous avons codé en anglais pour que cela soit 
compréhensible de tous.

## 1 - Structure logique du projet

###### Arbre du projet




