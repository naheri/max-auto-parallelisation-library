
# tests/test_maxpar.py
from max_auto_parallelisation_library.maxpar import Task, runT1, runT2, runTsomme, TaskSystem

import max_auto_parallelisation_library.maxpar as maxpar


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
    t2 = Task(name="T2", writes=["Y"], run=runT2)
    tSomme = Task(name="somme", reads=["X", "Y"], writes=["Z"], run=runTsomme)
    
    precedence = {
        "T1": [],
        "T2": [],
        "somme": ["T1", "T2"]
    }
    
    s1 = TaskSystem(tasks=[t1, t2, tSomme], precedence=precedence)
    
    assert s1.tasks == [t1, t2, tSomme]
    assert s1.precedence == precedence

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