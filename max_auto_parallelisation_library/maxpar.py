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

# propositions ma solution pour 2.7 

def parCost(self, num_runs=5, warmup_runs=2, verbose=True):
    """
    Compare le temps d'exécution séquentiel (runSeq()) et parallèle (run())
    en utilisant le module timeit pour une mesure précise.
    
    Args:
        num_runs (int): nombre de répétitions pour la mesure.
        warmup_runs (int): nombre d'exécutions préliminaires pour stabiliser l'exécution.
        verbose (bool): si True, affiche les résultats détaillés.
        
    Returns:
        dict: contenant le temps moyen séquentiel, parallèle et le speedup.
    """
    import timeit

    # Phase de réchauffement : exécuter plusieurs fois pour préparer les caches
    for _ in range(warmup_runs):
        self.runSeq()
        self.run()

    # Mesurer le temps total pour num_runs exécutions en mode séquentiel
    
    seq_total_time = timeit.timeit(self.runSeq, number=num_runs)
    
    # Mesurer le temps total pour num_runs exécutions en mode parallèle
    par_total_time = timeit.timeit(self.run, number=num_runs)
    
    # Calcul des moyennes
    avg_seq = seq_total_time / num_runs
    avg_par = par_total_time / num_runs
    # Calcul du speedup
    speedup = avg_seq / avg_par if avg_par > 0 else float('inf')
    
    if verbose:
        print("\n===== RÉSULTATS (Alternative timeit) =====")
        print(f"Temps moyen séquentiel: {avg_seq:.6f} secondes")
        print(f"Temps moyen parallèle:    {avg_par:.6f} secondes")
        print(f"Speedup: {speedup:.2f}x")
    
    return {
        "sequential_mean_time": avg_seq,
        "parallel_mean_time": avg_par,
        "speedup": speedup


# 2.6 solutions 


        def tester_determinisme(self, dico_globaux, cles=["X", "Y", "Z"], nb_exec=5):
        """
        Teste si le système de tâches est déterministe en l'exécutant plusieurs fois
        avec le même état initial pour les variables globales spécifiées.
        
        Args:
            dico_globaux (dict): Le dictionnaire des variables globales (ex. obtenu avec globals()).
            cles (list): Liste des noms de variables à tester (ex. ["X", "Y", "Z"]).
            nb_exec (int): Nombre d'exécutions à réaliser.
        
        Returns:
            bool: True si toutes les exécutions donnent exactement le même état final pour les variables testées,
                  False sinon.
        """
        # Sauvegarder l'état initial des variables à tester
        # On crée un dictionnaire 'etat_initial' avec pour chaque clé la valeur actuelle dans dico_globaux
        etat_initial = {cle: dico_globaux.get(cle) for cle in cles}

        # Initialiser une liste pour stocker l'état final obtenu après chaque exécution
        etats_obtenus = []

        # Boucle pour exécuter le système nb_exec fois
        for i in range(nb_exec):
            # Réinitialiser les variables globales à leur état initial
            # Pour chaque clé (par exemple "X", "Y", "Z") on remet la valeur enregistrée dans etat_initial
            for cle, valeur in etat_initial.items():
                dico_globaux[cle] = valeur  # Réinitialisation

            # Exécuter le système de tâches
            # Ici, on utilise self.run() pour exécuter le système en mode parallèle
            self.run()

            # Après l'exécution, on récupère l'état final des variables testées dans un nouveau dictionnaire
            etat_courant = {cle: dico_globaux.get(cle) for cle in cles}
            # Ajouter cet état à la liste des états obtenus
            etats_obtenus.append(etat_courant)

            # Détail de la boucle :
            # - La boucle 'for i in range(nb_exec)' répète l'exécution du système nb_exec fois.
            # - Avant chaque exécution, on réinitialise les variables globales (X, Y, Z) à leurs valeurs initiales.
            # - Après l'exécution, on capture les valeurs finales de ces variables et on les stocke dans la liste 'etats_obtenus'.

        # Comparer tous les états obtenus pour vérifier que tous sont identiques
        # La fonction all() retourne True si chaque état dans 'etats_obtenus' est égal au premier état obtenu
        deterministe = all(etat == etats_obtenus[0] for etat in etats_obtenus)

        # Retourner le résultat du test : True si le système est déterministe, False sinon
        return deterministe


    }


# derniére versionnnnnnnnnnnnnnnnn



def detTestRnd(self, dico_globaux, cles=["X"], nb_exec=5):
        """
        Teste le déterminisme du système en l'exécutant nb_exec fois avec le même état initial
        pour les variables globales spécifiées.
        
        Args:
            dico_globaux (dict): Le dictionnaire des variables globales (ex. obtenu avec globals()).
            cles (list): Liste des noms des variables globales à tester (par exemple ["X"]).
            nb_exec (int): Nombre d'exécutions à réaliser.
        
        Returns:
            bool: True si toutes les exécutions produisent exactement le même état final pour les variables testées,
                  False sinon.
        """
        # Sauvegarder l'état initial des variables à tester
        etat_initial = {cle: dico_globaux.get(cle) for cle in cles}
        etats_final = []  # Liste pour stocker l'état final après chaque exécution
        
        # Boucle : on exécute le système nb_exec fois
        for i in range(nb_exec):
            # Réinitialiser les variables globales à leur état initial
            for cle, valeur in etat_initial.items():
                dico_globaux[cle] = valeur
            # Exécuter le système de tâches (ici en mode parallèle)
            self.run()
            # Capturer l'état final des variables spécifiées
            etat_courant = {cle: dico_globaux.get(cle) for cle in cles}
            etats_final.append(etat_courant)
        
        # Comparer tous les états finaux : si tous sont identiques, le système est déterministe
        deterministe = all(etat == etats_final[0] for etat in etats_final)
        return deterministe



