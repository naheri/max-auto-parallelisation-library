
# tests/test_maxpar.py
from max_auto_parallelisation_library.maxpar import Task, runT1, runT2, runTsomme, TaskSystem
from max_auto_parallelisation_library.validators import TaskSystemValidationError, TaskSystemValidator
import max_auto_parallelisation_library.maxpar as maxpar
import pytest


def test_task_initialization():
    """Test de l'initialisation d'une tâche."""
    task = Task(name="TestTask", reads=["A"], writes=["B"], run=None)
    assert task.name == "TestTask"
    assert task.reads == ["A"]
    assert task.writes == ["B"]
    assert task.run is None

def test_task_system_initialization():
    """Test de l'initialisation du système de tâches."""
    t1 = Task(name="T1", writes=["X"], run=runT1)
    t2 = Task(name="T1", writes=["Y"], run=runT2)
    tSomme = Task(name="somme", reads=["X", "Y"], writes=["Z"], run=runTsomme)
    
    precedence = {
        "T1": [],
        "T2": [],
        "somme": ["T1", "T2"]
    }
    
    s1 = TaskSystem(tasks=[t1, t2, tSomme], precedence=precedence)
    
    assert s1.tasks == [t1, t2, tSomme]
    assert s1.precedence == precedence
def test_validation_empty_tasks():
    """Test la validation avec une liste de tâches vide"""
    with pytest.raises(TaskSystemValidationError, match="La liste des tâches ne peut pas être vide"):
        TaskSystem(tasks=[], precedence={"T1": []})

def test_validation_duplicate_task_names():
    """Test la validation avec des noms de tâches dupliqués"""
    tasks = [
        Task(name="T1", reads=["A"], writes=["B"], run=None),
        Task(name="T1", reads=["C"], writes=["D"], run=None)
    ]
    with pytest.raises(TaskSystemValidationError, match="Noms de tâches dupliqués détectés: T1"):
        TaskSystem(tasks=tasks, precedence={"T1": []})

def test_validation_invalid_precedence():
    """Test la validation avec des dépendances invalides"""
    tasks = [
        Task(name="T1", reads=["A"], writes=["B"], run=None)
    ]
    precedence = {
        "T1": ["T2"]  # T2 n'existe pas
    }
    with pytest.raises(TaskSystemValidationError, match="Dépendances invalides.*T2"):
        TaskSystem(tasks=tasks, precedence=precedence)

def test_validation_cycle_detection():
    """Test la détection de cycles dans le graphe de précédence"""
    tasks = [
        Task(name="T1", reads=["A"], writes=["B"], run=None),
        Task(name="T2", reads=["B"], writes=["C"], run=None),
        Task(name="T3", reads=["C"], writes=["A"], run=None)
    ]
    precedence = {
        "T1": ["T3"],
        "T2": ["T1"],
        "T3": ["T2"]
    }
    with pytest.raises(TaskSystemValidationError, match="Cycle détecté"):
        TaskSystem(tasks=tasks, precedence=precedence)

def test_validation_missing_task_in_precedence():
    """Test la validation quand une tâche est manquante dans le graphe de précédence"""
    tasks = [
        Task(name="T1", reads=["A"], writes=["B"], run=None),
        Task(name="T2", reads=["B"], writes=["C"], run=None)
    ]
    precedence = {
        "T1": []
        # T2 manque dans le graphe de précédence
    }
    with pytest.raises(TaskSystemValidationError, match="Tâches manquantes dans le graphe de précédence: T2"):
        TaskSystem(tasks=tasks, precedence=precedence)

def test_validation_valid_system():
    """Test qu'un système valide passe la validation"""
    tasks = [
        Task(name="T1", reads=["A"], writes=["B"], run=None),
        Task(name="T2", reads=["B"], writes=["C"], run=None)
    ]
    precedence = {
        "T1": [],
        "T2": ["T1"]
    }
    try:
        TaskSystem(tasks=tasks, precedence=precedence)
    except TaskSystemValidationError:
        pytest.fail("La validation a échoué pour un système valide")
def test_task_execution():
    """Test que les tâches exécutent bien leur fonction."""
    maxpar.X = None
    maxpar.Y = None
    maxpar.Z = None
    
    t1 = Task(name="T1", writes=["X"], run=runT1)
    t2 = Task(name="T2", writes=["Y"], run=runT2)
    tSomme = Task(name="somme", reads=["X", "Y"], writes=["Z"], run=runTsomme)
    
    t1.run()
    assert maxpar.X == 1  
    t2.run()
    assert maxpar.Y == 2  
    tSomme.run()
    assert maxpar.Z == 3  

def test_task_system_get_all_dependencies():
    """Test de la fonction getAllDependencies."""
    t1 = Task(name="T1", writes=["X"], run=runT1)
    t2 = Task(name="T2", writes=["Y"], run=runT2)
    tSomme = Task(name="somme", reads=["X", "Y"], writes=["Z"], run=runTsomme)
    
    precedence = {
        "somme": ["T1", "T2"],
        "T1": [],
        "T2": ["T1"]
    }
    
    s1 = TaskSystem(tasks=[t1, t2, tSomme], precedence=precedence)
    
    # Test des dépendances pour la tâche "somme"
    dependencies = s1.getAllDependencies("somme")
    assert set(dependencies) == {"T1", "T2"}
    
    # Test des dépendances pour la tâche "T1"
    dependencies = s1.getAllDependencies("T1")
    assert set(dependencies) == set()
    
    # Test des dépendances pour la tâche "T2"
    dependencies = s1.getAllDependencies("T2")
    assert set(dependencies) == {"T1"}
    
def test_task_system_complex_dependencies():
    """Test des dépendances complexes avec transitivité."""
    precedence = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["E"],
        "D": [],
        "E": []
    }
    
    s1 = TaskSystem(tasks=[], precedence=precedence)
    
    # Test des dépendances pour la tâche "A"
    dependencies = s1.getAllDependencies("A")
    assert set(dependencies) == {"B", "C", "D", "E"}
    
    # Test des dépendances pour la tâche "B"
    dependencies = s1.getAllDependencies("B")
    assert set(dependencies) == {"D"}
    
    # Test des dépendances pour la tâche "C"
    dependencies = s1.getAllDependencies("C")
    assert set(dependencies) == {"E"}
    
    # Test des dépendances pour la tâche "D"
    dependencies = s1.getAllDependencies("D")
    assert set(dependencies) == set()
    
    # Test des dépendances pour la tâche "E"
    dependencies = s1.getAllDependencies("E")
    assert set(dependencies) == set()


def test_create_max_parallel_system():
    """
    Teste la fonction maxpar.create_max_parallel_system avec un ensemble de tâches
    et vérifie que le résultat correspond au parallélisme maximal attendu.
    """
    # Créer les tâches
    tasks = [
        Task(name="1", reads=["A", "B"], writes=["C"], run=None),
        Task(name="2", reads=["A"], writes=["D"], run=None),
        Task(name="3", reads=["C", "D"], writes=["A"], run=None),
        Task(name="4", reads=["C", "D"], writes=["E"], run=None),
        Task(name="5", reads=["D"], writes=["B"], run=None),
        Task(name="6", reads=["E"], writes=["E"], run=None),
        Task(name="7", reads=["A", "B", "D"], writes=["D"], run=None),
        Task(name="8", reads=["A", "C"], writes=["E"], run=None)
    ]
    
    # Définir les dépendances initiales
    precedence = {
        "1": [],
        "2": ["1"],
        "3": ["2"],
        "4": ["2"],
        "5": ["3", "4"],
        "6": ["4"],
        "7": ["5", "6"],
        "8": ["7"]
    }
    
    # Résultat attendu après maximisation du parallélisme
    expected_precedence_max = {
        "1": set(),
        "2": set(),
        "3": {"1", "2"},
        "4": {"1", "2"},
        "5": {"2", "1"},
        "6": {"4"},
        "7": {"3", "5", "4"},
        "8": {"3", "6"}
    }
    
    # Créer le système initial
    initial_system = TaskSystem(tasks=tasks, precedence=precedence)
    
    # Générer le système à parallélisme maximal
    max_parallel_system = initial_system.create_max_parallel_system()
    
    # Convertir les listes de dépendances en ensembles pour la comparaison
    actual_precedence_max = {task: set(deps) for task, deps in max_parallel_system.precedence.items()}
    
    # Vérifier que le résultat correspond à l'attendu
    assert actual_precedence_max == expected_precedence_max
def test_sequential_execution():
        """
        Teste la fonction runSeq() pour vérifier qu'elle exécute 
        correctement les tâches selon leurs dépendances.
        """
        import time
        from datetime import datetime
        
        # Variables globales pour stocker les temps d'exécution
        execution_times = {}
        
        # Variables globales pour les données manipulées par les tâches
        global A, B, C, D, E
        
        # Définir des fonctions de tâches qui simulent une charge de travail
        # et enregistrent leur temps d'exécution
        def run1():
            global A, B, C
            start = datetime.now()
            time.sleep(0.1)  # Simulation d'un traitement
            C = A + B
            execution_times["1"] = datetime.now() - start
            print(f"[SEQ] Tâche 1 exécutée: C = A + B = {C}")
            print(f"A : {A}, B : {B}, C : {C}, D : {D}, E : {E}")
        
        def run2():
            global A, D
            start = datetime.now()
            time.sleep(0.1)  # Simulation d'un traitement
            D = A * 2
            execution_times["2"] = datetime.now() - start
            print(f"[SEQ] Tâche 2 exécutée: D = A * 2 = {D}")
            print(f"A : {A}, B : {B}, C : {C}, D : {D}, E : {E}")
        
        def run3():
            global C, D, A
            start = datetime.now()
            time.sleep(0.1)  # Simulation d'un traitement
            # Vérifier que C et D ne sont pas None
            if C is not None and D is not None:
                A = C + D
            else:
                A = 0  # Valeur par défaut
            execution_times["3"] = datetime.now() - start
            print(f"[SEQ] Tâche 3 exécutée: A = C + D = {A}")
            print(f"A : {A}, B : {B}, C : {C}, D : {D}, E : {E}")
        
        def run4():
            global C, D, E
            start = datetime.now()
            time.sleep(0.1)  # Simulation d'un traitement
            # Vérifier que C et D ne sont pas None
            if C is not None and D is not None:
                E = C - D
            else:
                E = 0  # Valeur par défaut
            execution_times["4"] = datetime.now() - start
            print(f"[SEQ] Tâche 4 exécutée: E = C - D = {E}")
            print(f"A : {A}, B : {B}, C : {C}, D : {D}, E : {E}")
        
        def run5():
            global D, B
            start = datetime.now()
            time.sleep(0.1)  # Simulation d'un traitement
            # Vérifier que D n'est pas None
            if D is not None:
                B = D // 2
            else:
                B = 0  # Valeur par défaut
            execution_times["5"] = datetime.now() - start
            print(f"[SEQ] Tâche 5 exécutée: B = D // 2 = {B}")
            print(f"A : {A}, B : {B}, C : {C}, D : {D}, E : {E}")
        
        def run6():
            global E
            start = datetime.now()
            time.sleep(0.1)  # Simulation d'un traitement
            # Vérifier que E n'est pas None
            if E is not None:
                E = E * 2
            else:
                E = 0  # Valeur par défaut
            execution_times["6"] = datetime.now() - start
            print(f"[SEQ] Tâche 6 exécutée: E = E * 2 = {E}")
            print(f"A : {A}, B : {B}, C : {C}, D : {D}, E : {E}")
        
        def run7():
            global A, B, D
            start = datetime.now()
            time.sleep(0.1)  # Simulation d'un traitement
            # Vérifier que A, B et D ne sont pas None
            if A is not None and B is not None and D is not None:
                D = A + B + D
            else:
                # Si certaines variables sont None, utiliser 0 à leur place
                A_val = A if A is not None else 0
                B_val = B if B is not None else 0
                D_val = D if D is not None else 0
                D = A_val + B_val + D_val
            execution_times["7"] = datetime.now() - start
            print(f"[SEQ] Tâche 7 exécutée: D = A + B + D = {D}")
            print(f"A : {A}, B : {B}, C : {C}, D : {D}, E : {E}")
        
        def run8():
            global A, C, E
            start = datetime.now()
            time.sleep(0.1)  # Simulation d'un traitement
            # Vérifier que A et C ne sont pas None avant de faire la multiplication
            if A is not None and C is not None:
                E = (A * C) // E if E != 0 else A * C
            else:
                E = 0  # Valeur par défaut si A ou C est None
            execution_times["8"] = datetime.now() - start
            print(f"[SEQ] Tâche 8 exécutée: E = (A * C) // E = {E}")
            print(f"A : {A}, B : {B}, C : {C}, D : {D}, E : {E}")
        
        # Initialiser les valeurs
        A = 10
        B = 20
        C = None
        D = None
        E = None
        
        # Définir les tâches
        tasks = [
            Task(name="1", reads=["A", "B"], writes=["C"], run=run1),
            Task(name="2", reads=["A"], writes=["D"], run=run2),
            Task(name="3", reads=["C", "D"], writes=["A"], run=run3),
            Task(name="4", reads=["C", "D"], writes=["E"], run=run4),
            Task(name="5", reads=["D"], writes=["B"], run=run5),
            Task(name="6", reads=["E"], writes=["E"], run=run6),
            Task(name="7", reads=["A", "B", "D"], writes=["D"], run=run7),
            Task(name="8", reads=["A", "C"], writes=["E"], run=run8)
        ]
        
        # Définir les dépendances
        precedence = {
            "1": [],
            "2": ["1"],
            "3": ["2"],
            "4": ["2"],
            "5": ["3", "4"],
            "6": ["4"],
            "7": ["5", "6"],
            "8": ["7"]
        }
        
        # Créer le système
        system = TaskSystem(tasks=tasks, precedence=precedence)
        
        # Afficher les dépendances
        print("Système de tâches pour l'exécution séquentielle:")
        for task, deps in precedence.items():
            print(f"  {task} dépend de: {deps}")
        
        # Exécution séquentielle
        print("\n=== EXÉCUTION SÉQUENTIELLE ===")
        start_time = time.time()
        system.runSeq()
        total_time = time.time() - start_time
        
        # Afficher les résultats
        print("\n=== RÉSULTATS DE L'EXÉCUTION SÉQUENTIELLE ===")
        print(f"A = {A}, B = {B}, C = {C}, D = {D}, E = {E}")
        print(f"Temps total: {total_time:.4f} secondes")
        
        # Vérifier les valeurs attendues après l'exécution
        assert C == 30, "C devrait être égal à A + B = 10 + 20 = 30"
        assert D is not None, "D ne devrait pas être None après l'exécution"
        assert E is not None, "E ne devrait pas être None après l'exécution"
        
        print("\nTemps d'exécution par tâche:")
        for task_name, duration in execution_times.items():
            print(f"  Tâche {task_name}: {duration.total_seconds():.4f} secondes")

def test_parallel_execution():
    """
    Teste la fonction run() pour vérifier qu'elle exécute 
    correctement les tâches en parallèle selon le système de parallélisme maximal.
    """
    import time
    import threading
    from datetime import datetime
    
    # Dictionnaire pour stocker les temps d'exécution
    execution_times = {}
    execution_start_times = {}
    execution_end_times = {}
    
    # Dictionnaire d'état qui remplacera les variables globales
    state = {
        'A': 10,
        'B': 15,
        'C': None,
        'D': None,
        'E': None
    }
    
    # Mutex pour protéger l'accès au dictionnaire d'état
    state_mutex = threading.Lock()
    
    # Définir des fonctions de tâches qui simulent une charge de travail
    # et enregistrent leur temps d'exécution
    def run1():
        execution_start_times["1"] = datetime.now()
        time.sleep(0.1)  # Simulation d'un traitement
        
        with state_mutex:
            local_state = state.copy()
            local_state['C'] = local_state['A'] + local_state['B']
            state.update(local_state)
            print(f"[PAR] Tâche 1 exécutée: C = A + B = {state['C']}")
        
        execution_end_times["1"] = datetime.now()
        execution_times["1"] = execution_end_times["1"] - execution_start_times["1"]
    
    def run2():
        execution_start_times["2"] = datetime.now()
        time.sleep(0.1)  # Simulation d'un traitement
        
        with state_mutex:
            local_state = state.copy()
            local_state['D'] = local_state['A'] * 2
            state.update(local_state)
            print(f"[PAR] Tâche 2 exécutée: D = A * 2 = {state['D']}")
        
        execution_end_times["2"] = datetime.now()
        execution_times["2"] = execution_end_times["2"] - execution_start_times["2"]
    
    def run3():
        execution_start_times["3"] = datetime.now()
        time.sleep(0.1)  # Simulation d'un traitement
        
        with state_mutex:
            local_state = state.copy()
            # Vérifier que C et D ne sont pas None
            if local_state['C'] is not None and local_state['D'] is not None:
                local_state['A'] = local_state['C'] + local_state['D']
            else:
                local_state['A'] = 0  # Valeur par défaut
            state.update(local_state)
            print(f"[PAR] Tâche 3 exécutée: A = C + D = {state['A']}")
        
        execution_end_times["3"] = datetime.now()
        execution_times["3"] = execution_end_times["3"] - execution_start_times["3"]
    
    def run4():
        execution_start_times["4"] = datetime.now()
        time.sleep(0.1)  # Simulation d'un traitement
        
        with state_mutex:
            local_state = state.copy()
            # Vérifier que C et D ne sont pas None
            if local_state['C'] is not None and local_state['D'] is not None:
                local_state['E'] = local_state['C'] - local_state['D']
            else:
                local_state['E'] = 0  # Valeur par défaut
            state.update(local_state)
            print(f"[PAR] Tâche 4 exécutée: E = C - D = {state['E']}")
        
        execution_end_times["4"] = datetime.now()
        execution_times["4"] = execution_end_times["4"] - execution_start_times["4"]
    
    def run5():
        execution_start_times["5"] = datetime.now()
        time.sleep(0.1)  # Simulation d'un traitement
        
        with state_mutex:
            local_state = state.copy()
            # Vérifier que D n'est pas None
            if local_state['D'] is not None:
                local_state['B'] = local_state['D'] // 2
            else:
                local_state['B'] = 0  # Valeur par défaut
            state.update(local_state)
            print(f"[PAR] Tâche 5 exécutée: B = D // 2 = {state['B']}")
        
        execution_end_times["5"] = datetime.now()
        execution_times["5"] = execution_end_times["5"] - execution_start_times["5"]
    
    def run6():
        execution_start_times["6"] = datetime.now()
        time.sleep(0.1)  # Simulation d'un traitement
        
        with state_mutex:
            local_state = state.copy()
            # Vérifier que E n'est pas None
            if local_state['E'] is not None:
                local_state['E'] = local_state['E'] * 2
            else:
                local_state['E'] = 0  # Valeur par défaut
            state.update(local_state)
            print(f"[PAR] Tâche 6 exécutée: E = E * 2 = {state['E']}")
        
        execution_end_times["6"] = datetime.now()
        execution_times["6"] = execution_end_times["6"] - execution_start_times["6"]
    
    def run7():
        execution_start_times["7"] = datetime.now()
        time.sleep(0.1)  # Simulation d'un traitement
        
        with state_mutex:
            local_state = state.copy()
            # Vérifier que A, B et D ne sont pas None
            if local_state['A'] is not None and local_state['B'] is not None and local_state['D'] is not None:
                local_state['D'] = local_state['A'] + local_state['B'] + local_state['D']
            else:
                # Si certaines variables sont None, utiliser 0 à leur place
                A_val = local_state['A'] if local_state['A'] is not None else 0
                B_val = local_state['B'] if local_state['B'] is not None else 0
                D_val = local_state['D'] if local_state['D'] is not None else 0
                local_state['D'] = A_val + B_val + D_val
            state.update(local_state)
            print(f"[PAR] Tâche 7 exécutée: D = A + B + D = {state['D']}")
        
        execution_end_times["7"] = datetime.now()
        execution_times["7"] = execution_end_times["7"] - execution_start_times["7"]
    
    def run8():
        execution_start_times["8"] = datetime.now()
        time.sleep(0.1)  # Simulation d'un traitement
        
        with state_mutex:
            local_state = state.copy()
            # Vérifier que A et C ne sont pas None avant de faire la multiplication
            if local_state['A'] is not None and local_state['C'] is not None:
                E_val = local_state['E'] if local_state['E'] is not None else 0
                local_state['E'] = (local_state['A'] * local_state['C']) // E_val if E_val != 0 else local_state['A'] * local_state['C']
            else:
                local_state['E'] = 0  # Valeur par défaut si A ou C est None
            state.update(local_state)
            print(f"[PAR] Tâche 8 exécutée: E = (A * C) // E = {state['E']}")
        
        execution_end_times["8"] = datetime.now()
        execution_times["8"] = execution_end_times["8"] - execution_start_times["8"]
    
    # Définir les tâches
    tasks = [
        Task(name="1", reads=["A", "B"], writes=["C"], run=run1),
        Task(name="2", reads=["A"], writes=["D"], run=run2),
        Task(name="3", reads=["C", "D"], writes=["A"], run=run3),
        Task(name="4", reads=["C", "D"], writes=["E"], run=run4),
        Task(name="5", reads=["D"], writes=["B"], run=run5),
        Task(name="6", reads=["E"], writes=["E"], run=run6),
        Task(name="7", reads=["A", "B", "D"], writes=["D"], run=run7),
        Task(name="8", reads=["A", "C"], writes=["E"], run=run8)
    ]
    
    # Définir les dépendances
    precedence = {
        "1": [],
        "2": ["1"],
        "3": ["2"],
        "4": ["2"],
        "5": ["3", "4"],
        "6": ["4"],
        "7": ["5", "6"],
        "8": ["7"]
    }
    
    # Créer le système initial
    initial_system = TaskSystem(tasks=tasks, precedence=precedence)
    
    # Générer le système à parallélisme maximal
    max_parallel_system = initial_system.create_max_parallel_system()
    
    # Convertir les listes de dépendances en ensembles pour l'affichage
    max_precedence = {task: set(deps) for task, deps in max_parallel_system.precedence.items()}
    
    # Afficher les dépendances du système à parallélisme maximal
    print("Système avec parallélisme maximal:")
    for task, deps in max_precedence.items():
        print(f"  {task} dépend de: {deps}")
    
    # Calculer et afficher les niveaux d'exécution théoriques
    if hasattr(max_parallel_system, '_compute_execution_levels'):
        execution_levels = max_parallel_system._compute_execution_levels()
        print("\n=== NIVEAUX D'EXÉCUTION THÉORIQUES (PARALLÈLE) ===")
        for i, level in enumerate(execution_levels):
            print(f"Niveau {i+1}: {level}")
    
    # Suivre l'ordre d'exécution
    execution_order = []
    execution_mutex = threading.Lock()  # Pour éviter les problèmes de concurrence
    
    # Remplacer temporairement les fonctions run pour suivre l'ordre d'exécution
    original_task_run = {}
    
    # Fonction de création d'une fonction de suivi pour chaque tâche
    def create_tracking_function(task_name, original_function):
        def tracking_function():
            result = original_function()
            with execution_mutex:
                execution_order.append(task_name)
            return result
        return tracking_function
    
    # Remplacer les fonctions d'origine par nos fonctions de suivi
    for task in tasks:
        original_task_run[task.name] = task.run
        task_obj = max_parallel_system.task_map.get(task.name)
        if task_obj:
            task_obj.run = create_tracking_function(task.name, original_task_run[task.name])
    
    # Exécution parallèle
    print("\n=== EXÉCUTION PARALLÈLE ===")
    start_time = time.time()
    max_parallel_system.run()
    total_time = time.time() - start_time
    
    # Afficher l'ordre d'exécution observé
    # Remarque: cet ordre peut varier en raison de la nature des exécutions parallèles
    print("\n=== ORDRE D'EXÉCUTION OBSERVÉ (PARALLÈLE) ===")
    for i, task_name in enumerate(execution_order):
        print(f"{i+1}. Tâche {task_name}")
    
    # Afficher les résultats
    print("\n=== RÉSULTATS DE L'EXÉCUTION PARALLÈLE ===")
    print(f"A = {state['A']}, B = {state['B']}, C = {state['C']}, D = {state['D']}, E = {state['E']}")
    print(f"Temps total: {total_time:.4f} secondes")
    
    # Vérifier les valeurs attendues après l'exécution
    assert state['C'] == 25, f"C devrait être égal à A + B = 10 + 15 = 25, mais était {state['C']}"
    assert state['D'] is not None, "D ne devrait pas être None après l'exécution"
    assert state['E'] is not None, "E ne devrait pas être None après l'exécution"
    
    # Analyser le parallélisme
    print("\nTemps d'exécution par tâche:")
    for task_name, duration in execution_times.items():
        print(f"  Tâche {task_name}: {duration.total_seconds():.4f} secondes")
    
    # Vérifier le parallélisme
    # On vérifie si certaines tâches se sont exécutées en parallèle en comparant leurs intervalles d'exécution
    print("\nAnalyse du parallélisme:")
    parallel_tasks = []
    
    for i in range(1, 9):
        for j in range(i+1, 9):
            task_i = str(i)
            task_j = str(j)
            
            # Si les deux tâches ont été exécutées
            if task_i in execution_start_times and task_j in execution_start_times:
                # Vérifier si les intervalles d'exécution se chevauchent
                start_i = execution_start_times[task_i]
                end_i = execution_end_times[task_i]
                start_j = execution_start_times[task_j]
                end_j = execution_end_times[task_j]
                
                if (start_i <= end_j and start_j <= end_i):
                    parallel_tasks.append((task_i, task_j))
                    print(f"  Les tâches {task_i} et {task_j} se sont exécutées en parallèle!")
    
    # Vérifier qu'il y a eu du parallélisme
    assert len(parallel_tasks) > 0, "Aucune tâche ne s'est exécutée en parallèle!"
    

'''def test_max_parallelism_system():
    """Test de la construction du système de tâches avec parallélisme maximal."""
    # Définir les tâches (sans fonctions run pour simplifier)
    tasks = [
        Task(name="1", reads=["A","B"], writes=["C"], run=None),
        Task(name="2", reads=["A"], writes=["D"], run=None),
        Task(name="3", reads=["C","D"], writes=["A"], run=None),
        Task(name="4", reads=["C","D"], writes=["E"], run=None),
        Task(name="5", reads=["D"], writes=["B"], run=None),
        Task(name="6", reads=["E"], writes=["E"], run=None),
        Task(name="7", reads=["A","B","D"], writes=["D"], run=None),
        Task(name="8", reads=["A","C"], writes=["E"], run=None)
    ]
    
    # Définir les dépendances initiales
    precedence = {
        "1": [],
        "2": ["1"],
        "3": ["2"],
        "4": ["2"],
        "5": ["3","4"],
        "6": ["4"],
        "7": ["5", "6"],
        "8": ["7"]
    }
    
    # Créer le système de tâches initial
    system = TaskSystem(tasks=tasks, precedence=precedence)
    
    # Construire le système de tâches avec parallélisme maximal
    smax_system = system.create_max_parallel_system()
    
    # Définir le résultat attendu
    expected_precedence_max = {
        "1": set(),
        "2": set(),
        "3": {"1", "2"},
        "4": {"1", "2"},
        "5": {"2", "1"},
        "6": {"4"},
        "7": {"3","5","4"},
        "8": {"3","6"}
    }
    
    # Conversion des listes en sets pour la comparaison
    actual_precedence_max = {task: set(deps) for task, deps in smax_system.precedence.items()}
    
    # Afficher les résultats pour vérification
    print("Précédence initiale :")
    print(precedence)
    print("\nPrécédence maximale calculée :")
    print(actual_precedence_max)
    print("\nPrécédence maximale attendue :")
    print(expected_precedence_max)
    
    # Vérifier que le résultat est correct
    assert actual_precedence_max == expected_precedence_max'''
