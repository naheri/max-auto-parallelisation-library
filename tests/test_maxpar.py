# tests/test_maxpar.py
from max_auto_parallelisation_library.maxpar import Task, runT1, runT2, runTsomme
import max_auto_parallelisation_library.maxpar as maxpar

def test_task_initialization():

    """Test que la classe Task s'initialise correctement"""

    task = Task(name="TestTask", reads=["A"], writes=["B"], run=None)
    assert task.name == "TestTask"
    assert task.reads == ["A"]
    assert task.writes == ["B"]
    assert task.run is None

def test_task_execution():

    """Test que les tâches exécutent bien leur fonction"""

    maxpar.X = None
    maxpar.Y = None
    maxpar.Z = None
    
    t1 = Task(name="T1", writes=["X"], run=runT1)
    t2 = Task(name="T2", writes=["Y"], run=runT2)
    tSomme = Task(name="somme", reads=["X", "Y"], writes=["Z"], run=runTsomme)
    
    # Exécuter les tâches
    t1.run()
    assert maxpar.X == 1  # Vérifie que X a été mis à jour
    t2.run()
    assert maxpar.Y == 2  # Vérifie que Y a été mis à jour
    tSomme.run()
    assert maxpar.Z == 3  # Vérifie que Z = X + Y