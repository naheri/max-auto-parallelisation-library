from max_auto_parallelisation_library.maxpar import Task, TaskSystem
import sys

def get_valid_input(prompt, validator=None, error_msg=None):
    """
    Utility function to get validated input from user.
    """
    while True:
        try:
            user_input = input(prompt).strip()
            if validator and not validator(user_input):
                raise ValueError(error_msg if error_msg else "Invalid input")
            return user_input
        except ValueError as e:
            print(f"Error: {e}")

def get_task_info():
    """
    Get task information from user input.
    """
    print("\n=== New Task Creation ===")
    
    # Get task name
    name = get_valid_input(
        "Enter task name: ",
        lambda x: x and x.isalnum(),
        "Task name must be alphanumeric and non-empty"
    )
    
    reads = []
    while True:
        read = input("Enter a read variable (or press Enter to finish): ").strip()
        if not read:
            break
        reads.append(read)
    
    writes = []
    while True:
        write = input("Enter a write variable (or press Enter to finish): ").strip()
        if not write:
            break
        writes.append(write)
    
    def task_function():
        print(f"Executing task {name}")
    
    return Task(name=name, reads=reads, writes=writes, run=task_function)

def create_task_system():
    """Create a task system interactively."""
    tasks = []
    precedence = {}
    
    print("=== Task System Creation ===")
    
    while True:
        choice = get_valid_input(
            "\nDo you want to add a task? (y/n): ",
            lambda x: x.lower() in ['y', 'n'],
            "Please enter 'y' or 'n'"
        )
        
        if choice.lower() == 'n':
            if not tasks:
                print("Error: Task system must have at least one task")
                continue
            break
        
        task = get_task_info()
        tasks.append(task)
        precedence[task.name] = []
    
    print("\n=== Define Task Dependencies ===")
    task_names = [task.name for task in tasks]
    
    for task in tasks:
        print(f"\nFor task {task.name}:")
        while True:
            dep = input("Enter a dependency (or press Enter to finish): ").strip()
            if not dep:
                break
            if dep not in task_names:
                print(f"Error: Task {dep} does not exist")
                continue
            if dep == task.name:
                print("Error: A task cannot depend on itself")
                continue
            precedence[task.name].append(dep)
    
    return TaskSystem(tasks=tasks, precedence=precedence)

def main():
    """Main function to run the interactive task system creation."""
    try:
        print("Welcome to Task System Creator!")
        system = create_task_system()
        
        print("\n=== Created Task System ===")
        print("Tasks:")
        for task in system.tasks:
            print(f"- {task.name}")
            print(f"  Reads: {task.reads}")
            print(f"  Writes: {task.writes}")
        
        print("\nDependencies:")
        for task, deps in system.precedence.items():
            print(f"- {task} depends on: {deps if deps else 'none'}")
        
        try:
            system.draw("task_system")
            print("\nTask system graph has been generated as 'task_system.png'")
        except Exception as e:
            print(f"\nCould not generate graph: {e}")
        
        choice = get_valid_input(
            "\nDo you want to run the system? (y/n): ",
            lambda x: x.lower() in ['y', 'n'],
            "Please enter 'y' or 'n'"
        )
        
        if choice.lower() == 'y':
            print("\nRunning task system...")
            system.run()
            print("Task system execution completed")
            

            print("\nAnalyzing performance...")
            results = system.parCost(num_runs=3, warmup_runs=1)
            print(f"Speedup achieved: {results['speedup']:.2f}x")
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()