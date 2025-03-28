import pytest
from max_auto_parallelisation_library.maxpar import Task, TaskSystem, runT1, runT2, runTsomme
import max_auto_parallelisation_library.maxpar as maxpar

def test_task_initialization():
    """Test que la classe Task s'initialise correctement."""
    task = Task(name="TestTask", reads=["A"], writes=["B"], run=None)
    assert task.name == "TestTask"
    assert task.reads == ["A"]
    assert task.writes == ["B"]
    assert task.run is None

def test_task_execution():
    """Test que les tâches exécutent correctement leurs fonctions et modifient les variables globales."""
    # Réinitialisation des variables globales
    maxpar.X = None
    maxpar.Y = None
    maxpar.Z = None

    t1 = Task(name="T1", writes=["X"], run=runT1)
    t2 = Task(name="T2", writes=["Y"], run=runT2)
    tSomme = Task(name="somme", reads=["X", "Y"], writes=["Z"], run=runTsomme)

    # Exécution des tâches en séquence
    t1.run()
    assert maxpar.X == 1, "Erreur : T1 doit mettre X à 1"
    t2.run()
    assert maxpar.Y == 2, "Erreur : T2 doit mettre Y à 2"
    tSomme.run()
    assert maxpar.Z == 3, "Erreur : somme doit donner Z = 3 (1 + 2)"

def test_duplicate_task_error():
    """Test si une erreur est levée lorsqu'une tâche est dupliquée."""
    # Création d'un doublon : "T1" apparaît deux fois.
    t1 = Task("T1")
    t2 = Task("T2")
    t3 = Task("T1")  # Doublon de nom "T1"
    tasks = [t1, t2, t3]
    precedence = {"T2": ["T1"]}

    with pytest.raises(ValueError, match="Des noms de tâches dupliqués"):
        TaskSystem(tasks, precedence)

def test_missing_dependency_error():
    """Test si une erreur est levée lorsqu'une tâche dépend d'une tâche inexistante."""
    t1 = Task("T1")
    t2 = Task("T2")
    tasks = [t1, t2]
    # Ici, "T3" est mentionné dans le dictionnaire alors qu'elle n'existe pas
    precedence = {"T2": ["T1"], "T3": ["T4"]}
    
    with pytest.raises(ValueError, match="n'existe pas"):
        TaskSystem(tasks, precedence)

def test_cycle_detection():
    """Test si une erreur est levée lorsqu'un cycle est détecté dans le graphe de précédence."""
    t1 = Task("T1")
    t2 = Task("T2")
    t3 = Task("T3")
    tasks = [t1, t2, t3]
    # Création d'un cycle : T1 -> T2, T2 -> T3, T3 -> T1
    precedence = {
        "T1": ["T2"],
        "T2": ["T3"],
        "T3": ["T1"]
    }
    with pytest.raises(ValueError, match="Cycle détecté dans les précédences"):
        TaskSystem(tasks, precedence)

def test_valid_task_system():
    """Test si un système de tâches valide est bien créé sans erreur."""
    t1 = Task("T1")
    t2 = Task("T2")
    t3 = Task("T3")
    tasks = [t1, t2, t3]
    # Dictionnaire de précédence valide : T2 dépend de T1 et T3 dépend de T2
    precedence = {"T2": ["T1"], "T3": ["T2"]}
    try:
        _ = TaskSystem(tasks, precedence)
    except ValueError as e:
        pytest.fail(f"La création d'un système de tâches valide a levé une erreur inattendue : {e}")

if __name__ == "__main__":
    pytest.main()