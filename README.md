# ⚙️ Max Auto Parallelisation Library

An intelligent Python library for automatic task parallelization with dependency management and performance optimization.

![Task System Example](images/task_system_max_parallel.png)

---

## 📘 Overview

**Max Auto Parallelisation Library** helps optimize task execution by:
- 🔍 Detecting and removing redundant dependencies
- 🧵 Enabling maximum parallel execution
- 🔐 Ensuring thread-safe execution
- 📊 Providing real-time performance metrics

---

## 🚀 Installation

```bash
pip install max_auto_parallelisation_library
or to install all dependencies:

bash
Copier
Modifier
pip install -r requirements.txt
🧪 Quick Start
python
Copier
Modifier
from max_auto_parallelisation_library import Task, TaskSystem

def load_data():
    pass

def process_data():
    pass

def analyze_data():
    pass

# Define tasks
tasks = [
    Task("data_load", writes=["raw_data"], run=load_data),
    Task("process", reads=["raw_data"], writes=["processed"], run=process_data),
    Task("analyze", reads=["processed"], writes=["results"], run=analyze_data)
]

# Define dependencies
precedence = {
    "data_load": [],
    "process": ["data_load"],
    "analyze": ["process"]
}

# Create and run the task system
system = TaskSystem(tasks=tasks, precedence=precedence)
system.run()
🛠️ Features
1. Automatic Dependency Optimization
Detects and removes unnecessary dependencies

Constructs a maximal parallelism task graph

2. Thread-Safe Execution
Prevents race conditions

Ensures safe resource access

3. Performance Analysis
python
Copier
Modifier
results = system.parCost(num_runs=5, warmup_runs=2)
print(f"Speedup: {results['speedup']}x")
4. Visual Task Graph Generation
python
Copier
Modifier
system.draw("task_system")  # Requires Graphviz installed
🔍 Use Cases
✔️ Data Pipelines
python
Copier
Modifier
Task("extract", writes=["raw"]),
Task("clean", reads=["raw"], writes=["clean"]),
Task("transform", reads=["clean"], writes=["final"]),
Task("load", reads=["final"], writes=["db"])
✔️ Scientific Simulations
python
Copier
Modifier
Task("simulate", writes=["results"]),
Task("analyze", reads=["results"], writes=["summary"])
✔️ Build Systems
python
Copier
Modifier
Task("compile", writes=["bin"]),
Task("test", reads=["bin"]),
Task("deploy", reads=["bin"])
📚 API Reference
Task Class
python
Copier
Modifier
Task(
    name: str,
    reads: List[str] = [],
    writes: List[str] = [],
    run: Callable = None
)
TaskSystem Class
python
Copier
Modifier
TaskSystem(
    tasks: List[Task],
    precedence: Dict[str, List[str]]
)
⏱️ Performance Tips
Use parCost() to compare sequential vs parallel speed

Prefer balanced task granularity

Avoid unnecessary interdependencies

👨‍💻 Contributing
Fork the repository

Create a new branch

Install dev dependencies

bash
Copier
Modifier
pip install -e ".[dev]"
Run tests

bash
Copier
Modifier
pytest tests/ -v
Submit a Pull Request 🚀

📄 License
MIT License – see LICENSE for more.

👥 Authors
AHAMADA Naheri

GHALEM Oualid

Special thanks to our professor Sergiu IVANOV
Université d'Évry / Université Paris-Saclay

📖 Citation
bibtex
Copier
Modifier
@software{max_auto_parallelisation,
  author = {AHAMADA, Naheri and GHALEM, Oualid},
  title = {Max Auto Parallelisation Library},
  year = {2025},
  url = {https://github.com/Oualidu/max-auto-parallelisation-library}
}
