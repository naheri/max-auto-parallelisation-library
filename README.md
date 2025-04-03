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
or install all dependencies:
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


