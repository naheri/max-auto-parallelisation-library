class Task:
    def __init__(self, name="", reads=None, writes=None, run=None):
        self.name = name
        self.reads = reads if reads is not None else []
        self.writes = writes if writes is not None else []
        self.run = run

X = None
Y = None
Z = None

def runT1():
    global X  
    X = 1

def runT2():
    global Y  
    Y = 2

def runTsomme():
    global X, Y, Z  
    Z = X + Y


class TaskSystem:
    def __init__(self, tasks, precedence):
        """
        Task system constructor
        """
        self.tasks = tasks
        self.task_map = {task.name : task for task in tasks} # associe chaque nom de tâche à une tâche
        self.precedence = precedence.copy() # sinon ça modifie le dictionnaire original aussi



class TaskSystem:
    def __init__(self, tasks, precedence):
        """
        Initialise le système de tâches avec :
        """
        self.tasks = {task.name: task for task in tasks}
        self.precedence = precedence.copy()

    def getDependencies(self, nomTache):
        """
        Récupère la liste des noms des tâches qui doivent s'exécuter avant `nomTache`
        """
        if nomTache not in self.precedence:
            return []  # Si la tâche n'a pas de dépendances, renvoyer une liste vide

        res = set()  # Utiliser un `set` pour éviter les doublons

        def recdep(name):
            """ Fonction récursive pour parcourir toutes les dépendances d'une tâche attention direct et indirect """
            for dep in self.precedence.get(name, []):
                if dep not in res:
                    res.add(dep)
                    recdep(dep)

        recdep(nomTache)
        return list(res)  # Retourner la liste des dépendances

        
