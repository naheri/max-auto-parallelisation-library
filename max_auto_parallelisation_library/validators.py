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
        """
        Validate the task system.
        Args:
            tasks (list[Task]): List of tasks to validate
            precedence (dict): Precedence graph where keys are task names and values are lists of dependencies
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
                "Validation of task system => FAILED:\n" + 
                "\n".join(f"- {error}" for error in errors)
            )

    @staticmethod
    def _validate_tasks(tasks):
        """
        Validate the list of tasks.
        Args:
            tasks (list[Task]): List of tasks to validate
        """
        if not tasks:
            raise TaskSystemValidationError("Task list CANNOT be empty")
            

        task_names = [task.name for task in tasks]
        duplicates = {name for name in task_names if task_names.count(name) > 1}
        if duplicates:
            raise TaskSystemValidationError(
                f"Duplicated tasks name detected: {', '.join(duplicates)}"
            )
            
        # verification of task attributes
        for task in tasks:
            if not task.name:
                raise TaskSystemValidationError("Each task MUST have a name")
                
            if not isinstance(task.reads, list):
                raise TaskSystemValidationError(
                    f"reading domain of {task.name} should be a list"
                )
                
            if not isinstance(task.writes, list):
                raise TaskSystemValidationError(
                    f"write domain of {task.name} should be a list"
                )

    @staticmethod
    def _validate_precedence_graph(tasks, precedence):
        """      Check the consistency of the precedence graph and tasks.
        Args:
            tasks (list[Task]): List of tasks to validate
            precedence (dict): Precedence graph where keys are task names and values are lists of dependencies
        """
        task_names = {task.name for task in tasks}
        
        missing_in_precedence = task_names - set(precedence.keys())
        if missing_in_precedence:
            raise TaskSystemValidationError(
                f"Missing tasks in precedence graph: {', '.join(missing_in_precedence)}"
            )
            
        for task_name, deps in precedence.items():
            if task_name not in task_names:
                raise TaskSystemValidationError(
                    f"Unknown task in precedence graph : {task_name}"
                )
                
            invalid_deps = set(deps) - task_names
            if invalid_deps:
                raise TaskSystemValidationError(
                    f"Invalid dependencies for {task_name}: {', '.join(invalid_deps)}"
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
                    f"Detected cycle in precedence graph: {' -> '.join(cycle_path)}"
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