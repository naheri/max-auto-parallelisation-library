class Task:
    def __init__(self, name="", reads=None, writes=None, run=None):
        self.name = name
        self.reads = reads if reads is not None else []
        self.writes = writes if writes is not None else []
        self.run = run

X = None
Y = None
Z = None

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
        """
        Task system constructor
        """
        self.tasks = tasks
        self.task_map = {task.name : task for task in tasks} # associe chaque nom de tâche à une tâche
        self.precedence = precedence.copy() # sinon ça modifie le dictionnaire original aussi

        