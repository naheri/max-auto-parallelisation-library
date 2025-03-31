# tests/test_maxpar.py
from max_auto_parallelisation_library.maxpar import Task, TaskSystem, runT1, runT2, runTsomme
import max_auto_parallelisation_library.maxpar as maxpar
import pytest

def test_task_initialization():
    """Test que la classe Task s'initialise correctement"""
    task = Task(name="TestTask", reads=["A"], writes=["B"], run=None)
    assert task.name == "TestTask"
    assert task.reads == ["A"]
    assert task.writes == ["B"]
    assert task.run is None


def test_task_execution():
    """Test que les tâches exécutent bien leur fonction"""
    # Réinitialisation des variables globales
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

def test_duplicate_task_error():
    """Test si une erreur est levée lorsqu'une tâche est dupliquée."""
    t1 = Task("T1")
    t2 = Task("T2")
    t3 = Task("T1")  # Doublon

    tasks = [t1, t2, t3]
    precedence = {"T2": ["T1"]}
    
    # On s'attend à ce que l'initialisation du système lève une ValueError pour les doublons
    with pytest.raises(ValueError, match="Des noms de tâches dupliqués"):
        TaskSystem(tasks, precedence)

def test_missing_dependency_error():
    """Test si une erreur est levée lorsqu'une tâche dépend d'une tâche inexistante."""
    t1 = Task("T1")
    t2 = Task("T2")

    tasks = [t1, t2]
    # Ici, le dictionnaire mentionne "T3" qui n'existe pas, et "T3" dépend de "T4"
    precedence = {"T2": ["T1"], "T3": ["T4"]}
    
    with pytest.raises(ValueError, match="n'existe pas"):
        TaskSystem(tasks, precedence)

def test_valid_task_system():
    """Test si un système de tâches valide est bien créé sans erreur."""
    t1 = Task("T1")
    t2 = Task("T2")
    tSomme = Task("somme")

    tasks = [t1, t2, tSomme]
    precedence = {"T2": ["T1"], "somme": ["T1", "T2"]}
    
    try:
        _ = TaskSystem(tasks, precedence)
    except ValueError:
        pytest.fail("La création d'un système de tâches valide a levé une erreur inattendue.")

def test_draw():
    """
    Test que la méthode draw() s'exécute sans erreur.
    Ce test crée un système de tâches simple et appelle draw().
    """
    t1 = Task("T1")
    t2 = Task("T2")
    t3 = Task("T3")
    t4 = Task("T4")
    t5 = Task("T5")


    tasks = [t1, t2, t3, t4, t5]
    precedence = {"T2": ["T1"], "T3": ["T2"], "T4": ["T2","T3"], "T5": ["T4"]}
    
    system = TaskSystem(tasks, precedence)
    
    try:
        system.draw()
    except Exception as e:
        pytest.fail(f"La méthode draw() a levé une exception inattendue : {e}")


# test de solution de 2.7 
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
            print("\n===== RÉSULTATS (timeit) =====")
            print(f"Temps moyen séquentiel: {avg_seq:.6f} secondes")
            print(f"Temps moyen parallèle:    {avg_par:.6f} secondes")
            print(f"Speedup: {speedup:.2f}x")

        return {
            "sequential_mean_time": avg_seq,
            "parallel_mean_time": avg_par,
            "speedup": speedup
        }



# test de fonction 2.6 
def test_detTestRnd():
    """
    Teste la méthode detTestRnd() pour vérifier que le système de tâches est déterministe.
    Pour ce test, aucune tâche ne modifie les variables globales, donc l'état initial doit rester inchangé.
    """
    # Déclaration et initialisation des variables globales
    global X, Y, Z
    X = 0
    Y = 0
    Z = 0

    # Fonction dummy qui ne fait rien (les variables globales ne seront pas modifiées)
    def fonction_inutile():
        pass

    # Création de deux tâches simples utilisant la fonction dummy
    t1 = Task(name="T1", run=fonction_inutile)
    t2 = Task(name="T2", run=fonction_inutile)
    
    # Définition d'une dépendance simple : T2 dépend de T1
    tasks = [t1, t2]
    precedence = {"T1": [], "T2": ["T1"]}
    
    # Création du système de tâches
    systeme = TaskSystem(tasks=tasks, precedence=precedence)
    
    # Appeler la méthode detTestRnd en passant globals(), la liste des variables à tester et le nombre d'exécutions
    resultat = systeme.detTestRnd(globals(), cles=["X", "Y", "Z"], nb_exec=5)
    
    # Afficher le résultat dans le terminal
    print("\nSystème déterministe :", resultat)
    
    # Comme aucune tâche ne modifie X, Y, Z, le système doit être déterministe (résultat True)
    assert resultat, "Le système devrait être déterministe pour ce jeu de valeurs initiales.







if __name__ == "__main__":
    pytest.main()
