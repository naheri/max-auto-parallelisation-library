import concurrent.futures
from max_auto_parallelisation_library.validators import TaskSystemValidationError, TaskSystemValidator
import timeit
import graphviz
from pathlib import Path
  
class Task:
    def __init__(self, name="", reads=None, writes=None, run=None):
        self.name = name
        self.reads = reads if reads is not None else []
        self.writes = writes if writes is not None else []
        self.run = run

X = None
Y = None
Z = None
# tests
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
        TaskSystemValidator.validate_system(tasks, precedence) # verification of the system at each creation of a system
        self.tasks = tasks
        self.task_map = {task.name: task for task in tasks}
        self.precedence = precedence.copy()

    def getAllDependencies(self, task_name):
        """
        Returns all dependencies of a task (direct and transitive).
    
        Args:
            task_name: The name of the task for which to get dependencies.
            
        Returns:
            A set containing the names of all tasks on which the given task depends.
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
        Builds an equivalent task system with maximum parallelism.
        Applies Bernstein's conditions to determine necessary dependencies.
        
        Returns:
            A new TaskSystem with maximum parallelism.
        """
        max_precedence = {task.name: set() for task in self.tasks}

        # Apply Bernstein's conditions to each pair of tasks
        for i, task_i in enumerate(self.tasks):
            for j, task_j in enumerate(self.tasks):
                if i != j:
                    reads_i = set(task_i.reads)
                    writes_i = set(task_i.writes)
                    reads_j = set(task_j.reads)
                    writes_j = set(task_j.writes)

                    condition1 = any(r in writes_j for r in reads_i)
                    condition2 = any(r in writes_i for r in reads_j)
                    condition3 = any(w in writes_j for w in writes_i)

                    conflict = condition1 or condition2 or condition3
                    # if there is a conflict, add the dependency
                    if conflict:
                        original_deps = self.getAllDependencies(task_j.name)
                        if task_i.name in original_deps:
                            max_precedence[task_j.name].add(task_i.name)

        self._eliminate_redundant_edges(max_precedence)
        return TaskSystem(
            tasks=self.tasks.copy(),
            precedence={k: list(v) for k, v in max_precedence.items()},
        )

    def _eliminate_redundant_edges(self, precedence):
        """
        Eliminates redundant edges from the precedence graph.
        An edge is redundant if there is an alternative path between the same nodes.
        
        Args:
            precedence: The precedence graph as a dictionary {task: set_of_dependencies}.
        """
        for task_name, deps in precedence.items():
            redundant = set()
            for dep in deps:
                deps_copy = deps.copy()  
                deps_copy.remove(dep)  

                for other_dep in deps_copy:
                    if dep in precedence.get(other_dep, set()):
                        redundant.add(dep)
                        break
                    
                    if self._is_transitively_dependent(other_dep, dep, precedence):
                        redundant.add(dep)
                        break
            
            deps.difference_update(redundant)

    def _is_transitively_dependent(self, start, target, precedence):
        """
        Checks if target is reachable from start via transitive dependencies using BFS.
        
        Args:
            start: The name of the starting task.
            target: The name of the target task.
            precedence: The precedence graph as a dictionary.
            
        Returns:
            True if target is reachable from start, False otherwise.
        """
        visited = set()
        queue = [start]
        # BFS to find if target is reachable from start
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

    def _compute_execution_levels(self):
        """
        Calculate levels of tasks.
        Each level contains tasks that can be executed in parallel.
        
        Returns:
            A list of lists, where each sublist contains the names of tasks in a level.
        """
        # Count the number of dependencies for each task
        remaining_deps = {}
        for task_name, deps in self.precedence.items():
            remaining_deps[task_name] = len(deps)
        # Find tasks with no dependencies
        ready_tasks = set()
        for task_name in self.precedence:
            if remaining_deps[task_name] == 0:
                ready_tasks.add(task_name)
        
        levels = []
        while ready_tasks:
            current_level = list(ready_tasks)
            levels.append(current_level)
            ready_tasks.clear()
            '''for each task, find tasks that depend on it, decrease their dependency count, 
            if count is 0, add to ready_tasks'''
            for completed_task in current_level:
                for task_name, deps in self.precedence.items():
                    if completed_task in deps and remaining_deps[task_name] > 0:
                        remaining_deps[task_name] -= 1
                        if remaining_deps[task_name] == 0:
                            ready_tasks.add(task_name)
        
        return levels

    def runSeq(self):
        """
        Executes tasks level by level (sequential between levels),
        but parallelizes tasks that are at the same level.
        """
        levels = self._compute_execution_levels()
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for level in levels:
                futures = []
                for task_name in level:
                    task = self.task_map.get(task_name)
                    if task and task.run:
                        future = executor.submit(task.run)
                        futures.append(future)
                
                for future in futures:
                    future.result()

    def run(self):
        """
        First applies the maximum parallelism algorithm, then executes the tasks
        by parallelizing those that can be according to this maximum parallelism system.
        """
        max_parallel_system = self.create_max_parallel_system()
        
        levels = max_parallel_system._compute_execution_levels()
        # Execute the tasks level by level (sequential between levels)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for level in levels:
                futures = []
                for task_name in level:
                    task = self.task_map.get(task_name)
                    if task and task.run:
                        future = executor.submit(task.run)
                        futures.append(future)
                
                for future in futures:
                    future.result()

    def draw(self, filename="task_system", format="png"):
        """Generates a graphical representation of the task system.
        
        Args:
            filename (str): Path where to save the output file
            format (str): Output format (png, pdf, etc.)
            
        Returns:
            str: Path to the generated file or None if graphviz is not installed
        """
    
        images_dir = Path("/Users/naher/Documents/max_auto_parallelisation/images")
        images_dir.mkdir(parents=True, exist_ok=True)
        
        dot = graphviz.Digraph(comment='Task System')
        
        # Add nodes
        for task in self.tasks:
            label = f"{task.name}"
            dot.node(task.name, label)
        
        # Add edges
        for task, deps in self.precedence.items():
            for dep in deps:
                dot.edge(dep, task)
        
        full_path = images_dir / filename
        
        output_path = dot.render(filename=str(full_path), format=format, cleanup=True)
        
        print(f"Graph generated at: {output_path}")
        return output_path
    def parCost(self, num_runs=5, warmup_runs=2, verbose=True):
        '''
        Compares sequential and parallel execution times of the task system.
        Returns execution times and speedup metrics.
        '''

        # warmup_runs to prepare the cache (good practice)
        for _ in range(warmup_runs):
            self.runSeq()
            self.run()
        
        seq_total_time = timeit.timeit(self.runSeq, number=num_runs)
        par_total_time = timeit.timeit(self.run, number=num_runs)
        
        # calculation of the average time
        avg_seq = seq_total_time / num_runs
        avg_par = par_total_time / num_runs
        
        # calculate speedup
        speedup = avg_seq / avg_par if avg_par > 0 else float('inf')
        
        if verbose:
            print("\n===== PERFORMANCE ANALYSIS =====")
            print(f"Mean execution time (SEQ): {avg_seq:.6f} seconds")
            print(f"Mean execution time (PAR): {avg_par:.6f} seconds")
            print(f"Speedup: {speedup:.2f}x")
            if speedup > 1:
                print(f"Performance improvement: {((speedup - 1) * 100):.1f}%")
        
        return {
            "sequential_mean_time": avg_seq,
            "parallel_mean_time": avg_par,
            "speedup": speedup,
            "improvement_percentage": ((speedup - 1) * 100) if speedup > 1 else 0
        }
