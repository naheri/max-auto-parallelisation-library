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




class Task:
    def __init__(self, name="", reads=None, writes=None, run=None):
        self.name = name
        self.reads = reads if reads is not None else []
        self.writes = writes if writes is not None else []
        self.run = run

class TaskSystem:
    def __init__(self, tasks, precedence):
        self.tasks = tasks
        self.task_map = {task.name: task for task in tasks}
        self.precedence = precedence.copy()

    def getAllDependencies(self, task_name):
        """
        Retourne toutes les dépendances d'une tâche (directes et transitives).
        
        Args:
            task_name: Le nom de la tâche pour laquelle on veut obtenir les dépendances.
            
        Returns:
            Un ensemble contenant les noms de toutes les tâches dont dépend la tâche donnée.
        """
        all_deps = set()
        
        def collect_deps(name):
            direct_deps = self.precedence.get(name, [])
            for dep in direct_deps:
                if dep not in all_deps:
                    all_deps.add(dep)
                    collect_deps(dep)
        
        collect_deps(task_name)
        return all_deps

    def create_max_parallel_system(self):
        """
        Construit un système de tâches équivalent avec un parallélisme maximal.
        Applique les conditions de Bernstein pour déterminer les dépendances nécessaires.
        
        Returns:
            Un nouveau TaskSystem avec un parallélisme maximal.
        """
        # Créer un nouveau dictionnaire de précédence pour le système maximal
        # Initialiser avec des ensembles vides pour chaque tâche
        max_precedence = {task.name: set() for task in self.tasks}
        
        # Créer un graphe des relations de dépendance basées sur les conditions de Bernstein
        # Pour chaque paire de tâches
        for i, task_i in enumerate(self.tasks):
            for j, task_j in enumerate(self.tasks):
                if i != j:  # Ne pas comparer une tâche avec elle-même
                    # Appliquer les conditions de Bernstein
                    reads_i = set(task_i.reads)
                    writes_i = set(task_i.writes)
                    reads_j = set(task_j.reads)
                    writes_j = set(task_j.writes)
                    
                    # Condition 1: Li ∩ Ej ≠ ∅ (Lecture de i et Écriture de j)
                    condition1 = any(r in writes_j for r in reads_i)
                    
                    # Condition 2: Lj ∩ Ei ≠ ∅ (Lecture de j et Écriture de i)
                    condition2 = any(r in writes_i for r in reads_j)
                    
                    # Condition 3: Ei ∩ Ej ≠ ∅ (Écriture de i et Écriture de j)
                    condition3 = any(w in writes_j for w in writes_i)
                    
                    # Si l'une des conditions est remplie, il y a un conflit potentiel
                    conflict = condition1 or condition2 or condition3
                    
                    if conflict:
                        # Vérifier s'il existe un chemin de j vers i dans le graphe de précédence original
                        original_deps = self.getAllDependencies(task_j.name)
                        if task_i.name in original_deps:
                            # j dépend déjà de i, donc dans le système max, tj doit toujours dépendre de ti
                            max_precedence[task_j.name].add(task_i.name)
        
        # Éliminer les arcs redondants
        self._eliminate_redundant_edges(max_precedence)
        
        # Créer et retourner un nouveau système de tâches avec le parallélisme maximal
        max_system = TaskSystem(tasks=self.tasks.copy(), 
                              precedence={k: list(v) for k, v in max_precedence.items()})
        return max_system

    def _eliminate_redundant_edges(self, precedence):
        """
        Élimine les arcs redondants du graphe de précédence.
        Un arc est redondant s'il existe un chemin alternatif entre les mêmes nœuds.
        
        Args:
            precedence: Le graphe de précédence sous forme de dictionnaire {tâche: ensemble_de_dépendances}.
        """
        for task_name, deps in precedence.items():
            redundant = set()
            for dep in deps:

                transitive_deps = set()
                deps_copy = deps.copy()  
                deps_copy.remove(dep)  
                

                for other_dep in deps_copy:
                    # Si other_dep dépend de dep, alors l'arc direct task_name -> dep est redondant
                    if dep in precedence.get(other_dep, set()):
                        redundant.add(dep)
                        break
                    
                    if self._is_transitively_dependent(other_dep, dep, precedence):
                        redundant.add(dep)
                        break
            
            deps.difference_update(redundant)

    def _is_transitively_dependent(self, start, target, precedence):
        """
        Vérifie si target est accessible depuis start via des dépendances transitives.
        
        Args:
            start: Le nom de la tâche de départ.
            target: Le nom de la tâche cible.
            precedence: Le graphe de précédence sous forme de dictionnaire.
            
        Returns:
            True si target est accessible depuis start, False sinon.
        """
        # Utiliser BFS pour trouver un chemin
        visited = set()
        queue = [start]
        
        while queue:
            current = queue.pop(0)
            
            if current == target:
                return True
            
            if current not in visited:
                visited.add(current)
                for next_task in precedence.get(current, set()):
                    if next_task not in visited:
                        queue.append(next_task)
        
        return False

    def runSeq(self):
        """
        Exécuter les tâches du système de façon séquentielle en respectant l'ordre imposé par la relation de précédence.
        Utilise un tri topologique pour déterminer l'ordre d'exécution.
        """
        visited = set()
        temp_visited = set()
        order = []
        
        def visit(node):
            if node in temp_visited:
                raise ValueError(f"Cycle détecté dans le graphe de précédence impliquant {node}")
            if node not in visited:
                temp_visited.add(node)
                for neighbor in self.precedence.get(node, []):
                    visit(neighbor)
                temp_visited.remove(node)
                visited.add(node)
                order.append(node)
        
        for task_name in self.precedence:
            if task_name not in visited:
                visit(task_name)
        
        # Inverser l'ordre 
        execution_order = list(reversed(order))
        
        for task_name in execution_order:
            task = self.task_map.get(task_name)
            if task and task.run:
                task.run()

    def run(self):
        """
        Exécuter les tâches du système en parallélisant celles qui peuvent être parallélisées 
        selon la spécification du parallélisme maximal.
        Utilise la bibliothèque concurrent.futures pour la parallélisation.
        """
        import concurrent.futures
        
        # Effectuer un tri topologique pour déterminer les niveaux d'exécution
        # Chaque niveau contient des tâches qui peuvent être exécutées en parallèle
        levels = self._compute_execution_levels()
        
        # Exécuter chaque niveau en parallèle
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for level in levels:
                futures = []
                for task_name in level:
                    task = self.task_map.get(task_name)
                    if task and task.run:
                        future = executor.submit(task.run)
                        futures.append(future)
                
                # Attendre que toutes les tâches du niveau soient terminées avant de passer au niveau suivant
                for future in futures:
                    future.result()  # Cela bloquera jusqu'à ce que la tâche soit terminée

    def _compute_execution_levels(self):
        """
        Calcule les niveaux d'exécution pour les tâches.
        Chaque niveau contient des tâches qui peuvent être exécutées en parallèle.
        
        Returns:
            Une liste de listes, où chaque sous-liste contient les noms des tâches d'un niveau.
        """
        # Copier le graphe de précédence pour ne pas le modifier
        remaining_deps = {}
        for task_name, deps in self.precedence.items():
            remaining_deps[task_name] = len(deps)
        
        # Garder une trace des tâches qui sont prêtes à être exécutées
        # (aucune dépendance ou toutes les dépendances sont satisfaites)
        ready_tasks = set()
        for task_name in self.precedence:
            if remaining_deps[task_name] == 0:
                ready_tasks.add(task_name)
        
        # Calculer les niveaux d'exécution
        levels = []
        while ready_tasks:
            # Ce niveau contient toutes les tâches prêtes à être exécutées
            current_level = list(ready_tasks)
            levels.append(current_level)
            ready_tasks.clear()
            
            # Mettre à jour les dépendances restantes pour les tâches futures
            for completed_task in current_level:
                # Parcourir toutes les tâches pour trouver celles qui dépendent de completed_task
                for task_name, deps in self.precedence.items():
                    if completed_task in deps and remaining_deps[task_name] > 0:
                        remaining_deps[task_name] -= 1
                        # Si toutes les dépendances sont satisfaites, la tâche est prête
                        if remaining_deps[task_name] == 0:
                            ready_tasks.add(task_name)
        
        return levels

    