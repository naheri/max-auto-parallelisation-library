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
        Initialise le système de tâches et effectue les validations.
        """
        self._validate_tasks(tasks, precedence)

        # Stocker les tâches sous forme de dictionnaire {nom: tâche}
        self.tasks = {task.name: task for task in tasks}
        self.precedence = precedence.copy()

    def _validate_tasks(self, tasks, precedence):
        """
        Vérifie :
        - Pas de noms de tâches en double
        - Toutes les dépendances existent
        - Absence de cycle dans le graphe de précédence
        """
        temp = set()


        # 1️⃣ Vérifier les doublons de tâches
        for task in tasks:
            if task.name in temp:
                print(f"🚨 ERREUR : La tâche '{task.name}' est dupliquée !")
                raise ValueError(f"🚨 Erreur : La tâche '{task.name}' est doublée !!!")
            temp.add(task.name)

        # 2️⃣ Vérifier les dépendances inexistantes
        for task_name, dependencies in precedence.items():
            for dep in dependencies:
                if dep not in temp:
                    raise ValueError(f"🚨 Erreur : La tâche '{dep}' n'existe pas dans la liste des tâches !!!")

    

        
