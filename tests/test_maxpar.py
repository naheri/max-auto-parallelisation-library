
# tests/test_maxpar.py
import max_auto_parallelisation_library.maxpar as maxpar
import time
import threading
import pytest
from datetime import datetime
from max_auto_parallelisation_library.maxpar import Task, runT1, runT2, runTsomme, TaskSystem
from max_auto_parallelisation_library.validators import TaskSystemValidationError




def test_task_initialization():

    """initialization task test"""

    task = Task(name="TestTask", reads=["A"], writes=["B"], run=None)
    assert task.name == "TestTask"
    assert task.reads == ["A"]
    assert task.writes == ["B"]
    assert task.run is None

def test_task_system_initialization():

    """task system initialization test"""

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
def test_validation_empty_tasks():
    """
    Tests the validation of an empty task system.
    """
    with pytest.raises(TaskSystemValidationError, match="Task list CANNOT be empty"):
        TaskSystem(tasks=[], precedence={"T1": []})

def test_validation_duplicate_task_names():
    """
    Tests the validation of a task system with duplicate task names.
    """
    tasks = [
        Task(name="T1", reads=["A"], writes=["B"], run=None),
        Task(name="T1", reads=["C"], writes=["D"], run=None)
    ]
    with pytest.raises(TaskSystemValidationError, match="Duplicated tasks name detected: T1"):
        TaskSystem(tasks=tasks, precedence={"T1": []})

def test_validation_invalid_precedence():
    """
    Tests the validation of a task system with invalid precedence.
    """
    tasks = [
        Task(name="T1", reads=["A"], writes=["B"], run=None)
    ]
    precedence = {
        "T1": ["T2"]  # T2 doesn't exist, it should raise an error
    }
    '''
    The error raised comes from the fact that T2 is not in the tasks list. 
    Though it tries to access it in the precedence dictionary.
    Put this function in comment to not see the error.
    '''
    with pytest.raises(TaskSystemValidationError, match="Dépendances invalides.*T2"):
        TaskSystem(tasks=tasks, precedence=precedence)

def test_validation_cycle_detection():
    """
    Tests the cycle detection in the precedence graph.
    """
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
    with pytest.raises(TaskSystemValidationError, match="Detected cycle in precedence graph"):
        TaskSystem(tasks=tasks, precedence=precedence)

def test_validation_missing_task_in_precedence():
    """
    Tests the validation of a task system with missing tasks in the precedence graph.
    """
    tasks = [
        Task(name="T1", reads=["A"], writes=["B"], run=None),
        Task(name="T2", reads=["B"], writes=["C"], run=None)
    ]
    precedence = {
        "T1": []
        # T2 is missing in the precedence graph
    }
    with pytest.raises(TaskSystemValidationError, match="Missing tasks in precedence graph: T2"):
        TaskSystem(tasks=tasks, precedence=precedence)

def test_validation_valid_system():
    """
    Tests that a valid task system passes validation without raising an error.
    """
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
        pytest.fail("Validation failed for a valid task system")
def test_task_execution():
    """Function to test the execution of tasks in a task system."""
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

    """getAllDependencies() test"""

    t1 = Task(name="T1", writes=["X"], run=runT1)
    t2 = Task(name="T2", writes=["Y"], run=runT2)
    tSomme = Task(name="somme", reads=["X", "Y"], writes=["Z"], run=runTsomme)

    precedence = {
        "somme": ["T1", "T2"],
        "T1": [],
        "T2": ["T1"]
    }

    s1 = TaskSystem(tasks=[t1, t2, tSomme], precedence=precedence)


    dependencies = s1.getAllDependencies("somme")
    assert set(dependencies) == {"T1", "T2"}

    dependencies = s1.getAllDependencies("T1")
    assert not set(dependencies)

    dependencies = s1.getAllDependencies("T2")
    assert set(dependencies) == {"T1"}
    

def test_create_max_parallel_system():
    """
    Test the create_max_parallel_system function with a set of tasks
    """
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
    
    initial_system = TaskSystem(tasks=tasks, precedence=precedence)
    # draw the initial system
    initial_system.draw("task_system_initial")
    max_parallel_system = initial_system.create_max_parallel_system()
    # draw the max parallel system
    max_parallel_system.draw("task_system_max_parallel")
    actual_precedence_max = {task: set(deps) for task, deps in max_parallel_system.precedence.items()}
    
    assert actual_precedence_max == expected_precedence_max


def test_sequential_execution():
    """
        runSeq() test, we use datetime.now() instead of timeit
          because we use the functions one time only
    """

    execution_times = {}

    global A, B, C, D, E

    def run1():
        global A, B, C
        start = datetime.now()
        time.sleep(0.1) 
        C = A + B
        execution_times["1"] = datetime.now() - start
        print(f"[SEQ] Task 1 executed: C = A + B = {C}")
        print(f"A : {A}, B : {B}, C : {C}, D : {D}, E : {E}")

    def run2():
        global A, D
        start = datetime.now()
        time.sleep(0.1)  
        D = A * 2
        execution_times["2"] = datetime.now() - start
        print(f"[SEQ] Task 2 executed: D = A * 2 = {D}")
        print(f"A : {A}, B : {B}, C : {C}, D : {D}, E : {E}")

    def run3():
        global C, D, A
        start = datetime.now()
        time.sleep(0.1)  
        A = C + D if C is not None and D is not None else 0
        execution_times["3"] = datetime.now() - start
        print(f"[SEQ] Task 3 executed: A = C + D = {A}")
        print(f"A : {A}, B : {B}, C : {C}, D : {D}, E : {E}")

    def run4():
        global C, D, E
        start = datetime.now()
        time.sleep(0.1) 
        E = C - D if C is not None and D is not None else 0
        execution_times["4"] = datetime.now() - start
        print(f"[SEQ] Task 4 executed: E = C - D = {E}")
        print(f"A : {A}, B : {B}, C : {C}, D : {D}, E : {E}")

    def run5():
        global D, B
        start = datetime.now()
        time.sleep(0.1)  
        B = D // 2 if D is not None else 0
        execution_times["5"] = datetime.now() - start
        print(f"[SEQ] Task 5 executed: B = D // 2 = {B}")
        print(f"A : {A}, B : {B}, C : {C}, D : {D}, E : {E}")

    def run6():
        global E
        start = datetime.now()
        time.sleep(0.1)  
        E = E * 2 if E is not None else 0
        execution_times["6"] = datetime.now() - start
        print(f"[SEQ] Task 6 executed: E = E * 2 = {E}")
        print(f"A : {A}, B : {B}, C : {C}, D : {D}, E : {E}")

    def run7():
        global A, B, D
        start = datetime.now()
        time.sleep(0.1)  
        if A is not None and B is not None and D is not None:
            D = A + B + D
        else:
            A_val = A if A is not None else 0
            B_val = B if B is not None else 0
            D_val = D if D is not None else 0
            D = A_val + B_val + D_val
        execution_times["7"] = datetime.now() - start
        print(f"[SEQ] Task 7 executed: D = A + B + D = {D}")
        print(f"A : {A}, B : {B}, C : {C}, D : {D}, E : {E}")

    def run8():
        global A, C, E
        start = datetime.now()
        time.sleep(0.1)  
        if A is not None and C is not None:
            E = (A * C) // E if E != 0 else A * C
        else:
            E = 0  
        execution_times["8"] = datetime.now() - start
        print(f"[SEQ] Task 8 executed: E = (A * C) // E = {E}")
        print(f"A : {A}, B : {B}, C : {C}, D : {D}, E : {E}")


    A = 10
    B = 20
    C = None
    D = None
    E = None

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

    system = TaskSystem(tasks=tasks, precedence=precedence)

    print("Task system for sequential execution:")
    for task, deps in precedence.items():
        print(f"  {task} depends on: {deps}")


    print("\n=== SEQUENTIAL EXECUTION RESULTS ===")
    start_time = time.time()
    system.runSeq()
    total_time = time.time() - start_time

    print("\n=== SEQUENTIAL EXECUTION RESULTS ===")
    print(f"A = {A}, B = {B}, C = {C}, D = {D}, E = {E}")
    print(f"Total time: {total_time:.4f} seconds")

    assert C == 30, "C devrait être égal à A + B = 10 + 20 = 30"
    assert D is not None, "D should not be None after execution"
    assert E is not None, "E should not be None after execution"

    print("\nExecution time per task:")
    for task_name, duration in execution_times.items():
        print(f"  Task {task_name}: {duration.total_seconds():.4f} seconds")

def test_parallel_execution():
    """
    Tests run() function to check that it correctly executes tasks in parallel
      according to the maximum parallelism system.
    """
    
    # Store execution times
    execution_times = {}
    execution_start_times = {}
    execution_end_times = {}

    # State variables dictionary to be shared between tasks
    state = {
        'A': 10,
        'B': 15,
        'C': None,
        'D': None,
        'E': None
    }

    # Mutex (semaphore) to protect shared state
    state_mutex = threading.Lock()

    # Simulate realistic tasks execution with a delay and record execution time
    def run1():
        execution_start_times["1"] = datetime.now()
        time.sleep(0.1)  

        with state_mutex:
            local_state = state.copy()
            local_state['C'] = local_state['A'] + local_state['B']
            state.update(local_state)
            print(f"[PAR] Task 1 executed: C = A + B = {state['C']}")

        execution_end_times["1"] = datetime.now()
        execution_times["1"] = execution_end_times["1"] - execution_start_times["1"]

    def run2():
        execution_start_times["2"] = datetime.now()
        time.sleep(0.1)  

        with state_mutex:
            local_state = state.copy()
            local_state['D'] = local_state['A'] * 2
            state.update(local_state)
            print(f"[PAR] Task 2 executed: D = A * 2 = {state['D']}")

        execution_end_times["2"] = datetime.now()
        execution_times["2"] = execution_end_times["2"] - execution_start_times["2"]

    def run3():
        execution_start_times["3"] = datetime.now()
        time.sleep(0.1)  

        with state_mutex:
            local_state = state.copy()
            # Vérifier que C et D ne sont pas None
            if local_state['C'] is not None and local_state['D'] is not None:
                local_state['A'] = local_state['C'] + local_state['D']
            else:
                local_state['A'] = 0 
            state.update(local_state)
            print(f"[PAR] Task 3 executed: A = C + D = {state['A']}")

        execution_end_times["3"] = datetime.now()
        execution_times["3"] = execution_end_times["3"] - execution_start_times["3"]

    def run4():
        execution_start_times["4"] = datetime.now()
        time.sleep(0.1)  

        with state_mutex:
            local_state = state.copy()
            if local_state['C'] is not None and local_state['D'] is not None:
                local_state['E'] = local_state['C'] - local_state['D']
            else:
                local_state['E'] = 0  
            state.update(local_state)
            print(f"[PAR] Task 4 executed: E = C - D = {state['E']}")

        execution_end_times["4"] = datetime.now()
        execution_times["4"] = execution_end_times["4"] - execution_start_times["4"]

    def run5():
        execution_start_times["5"] = datetime.now()
        time.sleep(0.1)  

        with state_mutex:
            local_state = state.copy()
            local_state['B'] = local_state['D'] // 2 if local_state['D'] is not None else 0
            state.update(local_state)
            print(f"[PAR] Task 5 executed: B = D // 2 = {state['B']}")

        execution_end_times["5"] = datetime.now()
        execution_times["5"] = execution_end_times["5"] - execution_start_times["5"]

    def run6():
        execution_start_times["6"] = datetime.now()
        time.sleep(0.1)  

        with state_mutex:
            local_state = state.copy()
            local_state['E'] = local_state['E'] * 2 if local_state['E'] is not None else 0
            state.update(local_state)
            print(f"[PAR] Task 6 executed: E = E * 2 = {state['E']}")

        execution_end_times["6"] = datetime.now()
        execution_times["6"] = execution_end_times["6"] - execution_start_times["6"]

    def run7():
        execution_start_times["7"] = datetime.now()
        time.sleep(0.1)  

        with state_mutex:
            local_state = state.copy()

            if local_state['A'] is not None and local_state['B'] is not None and local_state['D'] is not None:
                local_state['D'] = local_state['A'] + local_state['B'] + local_state['D']
            else:
                # if certain values are None, use 0 as default
                A_val = local_state['A'] if local_state['A'] is not None else 0
                B_val = local_state['B'] if local_state['B'] is not None else 0
                D_val = local_state['D'] if local_state['D'] is not None else 0
                local_state['D'] = A_val + B_val + D_val
            state.update(local_state)
            print(f"[PAR] Task 7 executed: D = A + B + D = {state['D']}")

        execution_end_times["7"] = datetime.now()
        execution_times["7"] = execution_end_times["7"] - execution_start_times["7"]

    def run8():
        execution_start_times["8"] = datetime.now()
        time.sleep(0.1)  

        with state_mutex:
            local_state = state.copy()
            if local_state['A'] is not None and local_state['C'] is not None:
                E_val = local_state['E'] if local_state['E'] is not None else 0
                local_state['E'] = (local_state['A'] * local_state['C']) // E_val if E_val != 0 else local_state['A'] * local_state['C']
            else:
                local_state['E'] = 0 
            state.update(local_state)
            print(f"[PAR] Task 8 executed: E = (A * C) // E = {state['E']}")

        execution_end_times["8"] = datetime.now()
        execution_times["8"] = execution_end_times["8"] - execution_start_times["8"]

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

    initial_system = TaskSystem(tasks=tasks, precedence=precedence)

    max_parallel_system = initial_system.create_max_parallel_system()
    # convert lists to sets for printing
    max_precedence = {task: set(deps) for task, deps in max_parallel_system.precedence.items()}

    print("Maxmal parallelism system:")
    for task, deps in max_precedence.items():
        print(f"  {task} depends on: {deps}")

    if hasattr(max_parallel_system, '_compute_execution_levels'):
        execution_levels = max_parallel_system._compute_execution_levels()
        print("\n=== EXECUTION LEVELS (PARALLEL) ===")
        for i, level in enumerate(execution_levels):
            print(f"Level {i+1}: {level}")

    # Suivre l'ordre d'exécution
    execution_order = []
    execution_mutex = threading.Lock()  # sémaphore

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

    # replace origin function with tracking function
    for task in tasks:
        original_task_run[task.name] = task.run
        task_obj = max_parallel_system.task_map.get(task.name)
        if task_obj:
            task_obj.run = create_tracking_function(task.name, original_task_run[task.name])

    print("\n=== PARALLEL EXECUTION ===")
    start_time = time.time()
    max_parallel_system.run()
    total_time = time.time() - start_time

    print("\n=== OBSERVED EXECUTION ORDER (PARALLEL) ===")
    for i, task_name in enumerate(execution_order):
        print(f"{i+1}. Tâche {task_name}")


    print("\n=== PARALLEL EXECUTION RESULTS ===")
    print(f"A = {state['A']}, B = {state['B']}, C = {state['C']}, D = {state['D']}, E = {state['E']}")
    print(f"Total time: {total_time:.4f} seconds")


    assert state['C'] == 25, f"C should be 25, but was {state['C']}"
    assert state['D'] is not None, "D should not be None after execution"
    assert state['E'] is not None, "E should not be None after execution"

    # execution time
    print("\nExecution time per task :")
    for task_name, duration in execution_times.items():
        print(f"  Task {task_name}: {duration.total_seconds():.4f} seconds")

    print("\nParallelism analysis:")
    parallel_tasks = []

    for i in range(1, 9):
        for j in range(i+1, 9):
            task_i = str(i)
            task_j = str(j)

            # verify if tasks were executed in parallel
            if task_i in execution_start_times and task_j in execution_start_times:
                start_i = execution_start_times[task_i]
                end_i = execution_end_times[task_i]
                start_j = execution_start_times[task_j]
                end_j = execution_end_times[task_j]

                if (start_i <= end_j and start_j <= end_i):
                    parallel_tasks.append((task_i, task_j))
                    print(f"  Tasks {task_i} and {task_j} were executed in parallel !")


    assert parallel_tasks, "No tasks were executed in parallel !"
def test_draw_method():
    """Tests the visualization of task system."""
    import os
    from pathlib import Path
    
    # Define expected image path
    image_path = Path("/Users/naher/Documents/max_auto_parallelisation/images/task_system")
    
    # Create a simple task system
    t1 = Task(name="T1", writes=["X"], run=runT1)
    t2 = Task(name="T2", writes=["Y"], run=runT2)
    t_somme = Task(name="somme", reads=["X", "Y"], writes=["Z"], run=runTsomme)
    
    tasks = [t1, t2, t_somme]
    precedence = {
        "T1": [],
        "T2": [],
        "somme": ["T1", "T2"]
    }
    
    system = TaskSystem(tasks=tasks, precedence=precedence)
    
    try:
        output_path = system.draw()
        
        if not output_path:
            pytest.skip("Test skipped: graphviz is not installed")
        
        # Verify file exists and has content
        assert os.path.exists(output_path), f"File {output_path} was not created"
        assert os.path.getsize(output_path) > 0, f"File {output_path} is empty"
        
        print(f"Graph image generated successfully at: {output_path}")
        
    except ImportError:
        pytest.skip("Test skipped: graphviz is not installed")

def test_parcost_performance():
    """
    Compare exection time between a parallelizable system and a sequential system.
    """
    
    global A, B, C, D, E
    A = 10
    B = 20
    C = None
    D = None
    E = None

    # Simulate realistic tasks execution with a delay
    def task_with_delay(delay=0.01):
        def run_task():
            time.sleep(delay)  
            return True
        return run_task

    def run1():
        global A, B, C
        time.sleep(0.02)
        C = A + B

    def run2():
        global A, D
        time.sleep(0.02)
        D = A * 2

    def run3():
        global C, D, A
        time.sleep(0.02)
        A = C + D if C is not None and D is not None else 0

    def run4():
        global C, D, E
        time.sleep(0.02) 
        E = C - D if C is not None and D is not None else 0

    # Parallel
    tasks_parallel = [
        Task(name="T1", reads=["A", "B"], writes=["C"], run=run1),
        Task(name="T2", reads=["A"], writes=["D"], run=run2),  
        Task(name="T3", reads=["C", "D"], writes=["A"], run=run3),
        Task(name="T4", reads=["C", "D"], writes=["E"], run=run4) 
    ]

    precedence_parallel = {
        "T1": [],
        "T2": [],
        "T3": ["T1", "T2"],
        "T4": ["T1", "T2"]
    }

    # Sequential
    tasks_sequential = [
        Task(name="T1", reads=["A", "B"], writes=["C"], run=run1),
        Task(name="T2", reads=["C"], writes=["D"], run=run2),     
        Task(name="T3", reads=["D"], writes=["A"], run=run3),      
        Task(name="T4", reads=["A"], writes=["E"], run=run4)       
    ]

    precedence_sequential = {
        "T1": [],
        "T2": ["T1"],
        "T3": ["T2"],
        "T4": ["T3"]
    }


    system_parallel = TaskSystem(tasks=tasks_parallel, precedence=precedence_parallel)
    system_sequential = TaskSystem(tasks=tasks_sequential, precedence=precedence_sequential)

    print("\n===== TEST WITH PARALLELIZED SYSTEM =====")
    results_parallel = system_parallel.parCost(num_runs=3, warmup_runs=1, verbose=True)

    print("\n===== TEST WITH SEQUENTIAL SYSTEM =====")
    results_sequential = system_sequential.parCost(num_runs=3, warmup_runs=1, verbose=True)

