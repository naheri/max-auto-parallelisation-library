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
        self.tasks = tasks
        self.task_map = {task.name: task for task in tasks}
        self.precedence = precedence.copy()
        self.validate_inputs()


    def validate_inputs(self):
        # 1. Vérification des doublons dans les noms de tâches
        names = [task.name for task in self.tasks]

        if len(names) != len(set(names)):
            duplicates = [name for name in set(names) if names.count(name) > 1]
            raise ValueError(f"Des noms de tâches dupliqués ont été détectés : {duplicates}")


        # 2. Vérification que les clés du dictionnaire de précédence correspondent à des tâches existantes
        task_names = set(names)
        for key, deps in self.precedence.items():
            if key not in task_names:
                raise ValueError(f" la tâche '{key}' n'existe pas dans la liste des tâches.")
            for dep in deps:
                if dep not in task_names:
                    raise ValueError(f"La tâche '{key}' dépend de '{dep}', mais cette tâche n'existe pas.")


        # 3. Vérification de l'absence de cycles dans le graphe de précédence
        self._validate_no_cycles()

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
            rec_stack.remove(task_name) # supprimer dernier chemin étudié

        for task in self.tasks:
            if task.name not in visited:
                dfs(task.name)




# premiére solution : 
    def draw(self):
        import networkx as nx
        import matplotlib.pyplot as plt

        # Créer un graphe 
        G = nx.DiGraph()

        # Ajouter tous les nœuds correspondant aux tâches
        for task in self.tasks:
            G.add_node(task.name)  

        # Ajouter les arêtes en se basant sur le dictionnaire de précédence
        for task_name, dependencies in self.precedence.items():
            for dep in dependencies:
                G.add_edge(dep, task_name)

        # Calculer les positions des nœuds pour un affichage clair
        pos = nx.spring_layout(G)  
        nx.draw(G, pos,
                with_labels=True,       
                node_color="lightblue",  
                node_size=2000,          
                arrowstyle="-|>",         
                arrowsize=20)             

        plt.title("Graphe de précédence du système de parallélisme maximal")
        plt.show()


# 2 éme solution recomandé simple et facile de walid : 

""" 
    def draw(self):
        
        Affiche graphiquement le graphe de précédence du système de tâches en utilisant Graphviz.
        Chaque nœud représente une tâche et chaque arête indique qu'une tâche doit être exécutée avant une autre.
        
        from graphviz import Digraph
                dot = Digraph(comment='Graphe de précédence du système de parallélisme maximal')
        

        for task in self.tasks:
            dot.node(task.name, task.name)
        
        for task_name, dependencies in self.precedence.items():
            for dep in dependencies:
                # Ajouter une arête allant de la tâche de dépendance (dep) vers la tâche courante (task_name)
                dot.edge(dep, task_name)
        dot.view()
        """