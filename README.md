# Max Auto Parallelisation Library 🧠⚙️

A Python library for **automated maximum parallelization** of task systems — designed to simplify concurrent programming and optimize execution time.

![Task Graph Example](images/task_system_max_parallel.png)

## 🔍 Overview

This library enables:
- ⚡ Automatic detection and elimination of unnecessary dependencies
- 🚀 Maximized parallel task execution
- 🔐 Thread-safe and deterministic execution
- 📊 Benchmarking and performance analysis
- 🧩 Graph visualization of task dependencies

## 📦 Installation

```bash
pip install max_auto_parallelisation_library
# or install dependencies manually
pip install -r requirements.txt
🚀 Quick Start
python
Copier
Modifier
from max_auto_parallelisation_library import Task, TaskSystem

tasks = [
    Task("T1", writes=["X"], run=lambda: print("T1")),
    Task("T2", reads=["X"], writes=["Y"], run=lambda: print("T2")),
    Task("T3", reads=["Y"], run=lambda: print("T3"))
]

precedence = {
    "T1": [],
    "T2": ["T1"],
    "T3": ["T2"]
}

system = TaskSystem(tasks, precedence)
system.run()  # Or system.runSeq()
✨ Key Features
✅ Maximal Parallelism with automatic graph optimization

🔄 Sequential and Parallel Execution

📈 Execution Cost Analysis with parCost()

🔬 Determinism Testing with detTestRnd()

🎯 Graph Visualization (requires Graphviz)

🧪 Use Cases
Data processing pipelines

Scientific computations

Build systems automation

👨‍💻 Developers
AHAMADA Naheri

GHALEM Oualid

Special thanks to Sergiu Ivanov (Université d'Évry).


📝 License
MIT License — see LICENSE

📚 Citation
bibtex
Copier
Modifier
@software{max_auto_parallelisation,
  author = {AHAMADA, Naheri and GHALEM, Oualid},
  title = {Max Auto Parallelisation Library},
  year = {2025},
  url = {https://github.com/naheri/max-auto-parallelisation-library}
}
