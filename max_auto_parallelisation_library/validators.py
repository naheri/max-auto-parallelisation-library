class TaskSystemValidationError(Exception):
    """Exception personnalisée pour les erreurs de validation du système de tâches."""
    pass

class TaskSystemValidator:
    """Validateur pour les systèmes de tâches.
    
    Cette classe fournit des méthodes de validation pour vérifier l'intégrité
    et la cohérence d'un système de tâches avant sa construction.
    """
    
    @staticmethod
    def validate_system(tasks, precedence):
        """Valide l'ensemble du système de tâches.
        
        Args:
            tasks (list[Task]): Liste des tâches à valider
            precedence (dict): Dictionnaire des relations de précédence
            
        Raises:
            TaskSystemValidationError: Si une des validations échoue
        """
        errors = []
        
        try:
            TaskSystemValidator._validate_tasks(tasks)
        except TaskSystemValidationError as e:
            errors.append(str(e))
            
        try:
            TaskSystemValidator._validate_precedence_graph(tasks, precedence)
        except TaskSystemValidationError as e:
            errors.append(str(e))
            
        try:
            TaskSystemValidator._check_cycles(precedence)
        except TaskSystemValidationError as e:
            errors.append(str(e))
            
        if errors:
            raise TaskSystemValidationError(
                "Validation du système de tâches échouée:\n" + 
                "\n".join(f"- {error}" for error in errors)
            )

    @staticmethod
    def _validate_tasks(tasks):
        """Valide la liste des tâches.
        
        Vérifie les doublons et la validité des attributs de chaque tâche.
        """
        if not tasks:
            raise TaskSystemValidationError("La liste des tâches ne peut pas être vide")
            

        task_names = [task.name for task in tasks]
        duplicates = {name for name in task_names if task_names.count(name) > 1}
        if duplicates:
            raise TaskSystemValidationError(
                f"Noms de tâches dupliqués détectés: {', '.join(duplicates)}"
            )
            
        # verification of task attributes
        for task in tasks:
            if not task.name:
                raise TaskSystemValidationError("Une tâche doit avoir un nom")
                
            if not isinstance(task.reads, list):
                raise TaskSystemValidationError(
                    f"Les lectures de la tâche {task.name} doivent être une liste"
                )
                
            if not isinstance(task.writes, list):
                raise TaskSystemValidationError(
                    f"Les écritures de la tâche {task.name} doivent être une liste"
                )

    @staticmethod
    def _validate_precedence_graph(tasks, precedence):
        """Valide le graphe de précédence.
        
        Vérifie la cohérence entre les tâches et le graphe de précédence.
        """
        task_names = {task.name for task in tasks}
        
        missing_in_precedence = task_names - set(precedence.keys())
        if missing_in_precedence:
            raise TaskSystemValidationError(
                f"Tâches manquantes dans le graphe de précédence: {', '.join(missing_in_precedence)}"
            )
            
        for task_name, deps in precedence.items():
            if task_name not in task_names:
                raise TaskSystemValidationError(
                    f"Tâche inconnue dans le graphe de précédence: {task_name}"
                )
                
            invalid_deps = set(deps) - task_names
            if invalid_deps:
                raise TaskSystemValidationError(
                    f"Dépendances invalides pour la tâche {task_name}: {', '.join(invalid_deps)}"
                )

    @staticmethod
    def _check_cycles(precedence):
        """
        Detect cycles in the precedence graph using a depth-first search (DFS) approach.
        """
        visited = set()
        temp_visited = set()

        def detect_cycle(node):
            if node in temp_visited:
                cycle_path = [node]
                raise TaskSystemValidationError(
                    f"Cycle détecté dans le graphe de précédence: {' -> '.join(cycle_path)}"
                )
                
            if node not in visited:
                temp_visited.add(node)
                for neighbor in precedence[node]:
                    detect_cycle(neighbor)
                temp_visited.remove(node)
                visited.add(node)
                
        for node in precedence:
            if node not in visited:
                detect_cycle(node)