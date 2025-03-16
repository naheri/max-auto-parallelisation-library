# Librairie en Python pour automatiser la parallélisation maximale de systèmes de tâches.

Maxpar - Parallélisation Maximale Automatique
Description
Maxpar est une bibliothèque Python permettant l'automatisation de la parallélisation maximale de systèmes de tâches. Cette bibliothèque offre des outils pour définir des tâches qui interagissent à travers un ensemble de variables partagées, et permet d'optimiser leur exécution parallèle tout en respectant les contraintes de dépendance.
Fonctionnalités

Définition de tâches avec leurs domaines de lecture et d'écriture
Construction automatique d'un système de tâches à parallélisme maximal
Exécution séquentielle respectant les contraintes de précédence
Exécution parallèle optimisée
Affichage graphique du système de tâches
Test randomisé de déterminisme
Analyse comparative des performances entre exécution séquentielle et parallèle

Installation
bashCopier# Clonez le dépôt
git clone https://github.com/username/maxpar.git
cd maxpar

# Installez les dépendances (si nécessaire)
pip install -r requirements.txt
Utilisation
Création de tâches
pythonCopierfrom maxpar import Task

# Définition des variables globales
X = None
Y = None
Z = None

# Définition des fonctions de tâches
def runT1():
    global X
    X = 1

def runT2():
    global Y
    Y = 2

def runTsomme():
    global X, Y, Z
    Z = X + Y

# Création des objets Task
t1 = Task()
t1.name = "T1"
t1.writes = ["X"]
t1.run = runT1

t2 = Task()
t2.name = "T2"
t2.writes = ["Y"]
t2.run = runT2

tSomme = Task()
tSomme.name = "somme"
tSomme.reads = ["X", "Y"]
tSomme.writes = ["Z"]
tSomme.run = runTsomme
Création d'un système de tâches
pythonCopierfrom maxpar import TaskSystem

# Création du système avec des contraintes de précédence
system = TaskSystem([t1, t2, tSomme], {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"]})
Exécution du système
pythonCopier# Exécution séquentielle
system.runSeq()

# Exécution parallèle
system.run()

# Affichage des résultats
print(X, Y, Z)
Analyse et visualisation
pythonCopier# Affichage des dépendances pour une tâche
dependencies = system.getDependencies("somme")
print(dependencies)

# Affichage graphique du système
system.draw()

# Test randomisé de déterminisme
system.detTestRnd()

# Analyse du coût de parallélisation
system.parCost()
Architecture
La bibliothèque est organisée autour de deux classes principales :

Task : Représente une tâche individuelle avec ses domaines de lecture/écriture
TaskSystem : Gère un ensemble de tâches et leurs relations de précédence

Algorithme de parallélisation
L'algorithme de parallélisation maximale utilise les conditions de Bernstein pour déterminer quelles tâches peuvent être exécutées en parallèle sans affecter le résultat final. Deux tâches peuvent être exécutées en parallèle si et seulement si :

Le domaine d'écriture de la première tâche est disjoint du domaine de lecture de la seconde
Le domaine d'écriture de la seconde tâche est disjoint du domaine de lecture de la première
Les domaines d'écriture des deux tâches sont disjoints

Limitations et avertissements

L'utilisation de variables globales est généralement déconseillée en programmation, mais elle est utilisée ici pour simuler des ressources partagées en accès concurrent.
La fiabilité de l'analyse de parallélisation dépend de la déclaration correcte des domaines de lecture et d'écriture des tâches.

Licence
Ce projet est distribué sous la licence MIT.
Contributeurs
Ce projet a été développé dans le cadre du cours de Systèmes d'Exploitation à l'Université d'Évry.