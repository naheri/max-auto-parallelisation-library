class Task:
    def __init__(self, name="", reads=None, writes=None, run=None):
        self.name = name
        self.reads = reads if reads is not None else []
        self.writes = writes if writes is not None else []
        self.run = run

# Variables globales
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
        self.tasks = tasks
        self.task_map = {task.name: task for task in tasks}
        self.precedence = precedence.copy()
        self.validate_inputs()

    def validate_inputs(self):
        print("=== Validation des entrées ===")
        # 1. Vérification des doublons dans les noms de tâches
        names = [task.name for task in self.tasks]
        if len(names) != len(set(names)):
            duplicates = [name for name in set(names) if names.count(name) > 1]
            print("Duplication détectée :", duplicates)
            raise ValueError(f"Des noms de tâches dupliqués ont été détectés : {duplicates}")
        else:
            print("Aucun doublon détecté dans les noms des tâches.")


        # 2. Vérification que les clés du dictionnaire de précédence correspondent à des tâches existantes
        task_names = set(names)
        for key, deps in self.precedence.items():
            if key not in task_names:
                print(f"Erreur : La tâche '{key}' du dictionnaire de précédence n'existe pas dans la liste des tâches.")
                raise ValueError(f"Le dictionnaire de précédence contient la tâche '{key}' qui n'existe pas dans la liste des tâches.")
            for dep in deps:
                if dep not in task_names:
                    print(f"Erreur : La tâche '{key}' dépend de '{dep}', qui n'existe pas.")
                    raise ValueError(f"La tâche '{key}' dépend de '{dep}', mais cette tâche n'existe pas.")
        print("Les clés et dépendances du dictionnaire de précédence sont valides.")


        # 3. Vérification de l'absence de cycles dans le graphe de précédence
        try:
            self._validate_no_cycles()
            print("Aucun cycle détecté dans le graphe de précédence. Le système est cohérent (acyclique).")
        except ValueError as e:
            print("Cycle détecté :", e)
            raise

    def _validate_no_cycles(self):
        visited = set()
        rec_stack = set()

        def dfs(task_name):
            visited.add(task_name)
            rec_stack.add(task_name)
            for dep in self.precedence.get(task_name, []):
                if dep not in visited:
                    dfs(dep)
                elif dep in rec_stack:
                    raise ValueError(f"Cycle détecté dans les précédences impliquant la tâche '{dep}'")
            rec_stack.remove(task_name)

        for task in self.tasks:
            if task.name not in visited:
                dfs(task.name)