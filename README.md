Max Auto Parallelisation Library

An intelligent Python library for automatic task parallelization with dependency management and performance optimization.



🔍 Overview

Max Auto Parallelisation Library helps you optimize task execution by:

✅ Detecting and removing redundant dependencies

⏳ Maximizing parallel execution opportunities

⚖️ Ensuring thread-safe execution

⌛ Providing real-time performance metrics

⚡ Installation

pip install max_auto_parallelisation_library

Or install all dependencies:

pip install -r requirements.txt

✨ Quick Start

from max_auto_parallelisation_library import Task, TaskSystem

def load_data():
    # code to load data
    pass

def process_data():
    # code to process data
    pass

def analyze_data():
    # code to analyze data
    pass

tasks = [
    Task("data_load", writes=["raw_data"], run=load_data),
    Task("process", reads=["raw_data"], writes=["processed"], run=process_data),
    Task("analyze", reads=["processed"], writes=["results"], run=analyze_data)
]

precedence = {
    "data_load": [],
    "process": ["data_load"],
    "analyze": ["process"]
}

system = TaskSystem(tasks=tasks, precedence=precedence)
system.run()

📊 Key Features

🔄 Automatic Dependency Optimization

Identifies unnecessary task constraints

Builds maximum parallelism safely

Validates user-specified graphs

🔑 Thread-Safe Execution

Prevents race conditions

Uses shared resource protection

Reliable under concurrency

⏲️ Performance Analysis

results = system.parCost(num_runs=5, warmup_runs=2)
print(f"Speedup: {results['speedup']}x")
print(f"Improvement: {results['improvement_percentage']}%")

🎭 Visual Graph Drawing

system.draw("task_system")  # requires Graphviz

📂 Use Cases

Data Engineering Pipelines

Task("extract", writes=["raw"]),
Task("clean", reads=["raw"], writes=["cleaned"]),
Task("transform", reads=["cleaned"], writes=["transformed"]),
Task("load", reads=["transformed"], writes=["db"])

Scientific Computing

Task("A_x_B", reads=["A", "B"], writes=["AB"]),
Task("B_x_D", reads=["B", "D"], writes=["BD"]),
Task("combine", reads=["AB", "BD"], writes=["Result"])

Build & Deploy

Task("compile_frontend", writes=["dist/frontend"]),
Task("compile_backend", writes=["dist/backend"]),
Task("test", reads=["dist/frontend", "dist/backend"]),
Task("deploy", reads=["dist/frontend", "dist/backend"])

🔍 API Reference

Task Class

Task(
  name: str,
  reads: List[str] = [],
  writes: List[str] = [],
  run: Callable = None
)

TaskSystem Class

TaskSystem(
  tasks: List[Task],
  precedence: Dict[str, List[str]]
)

⏱ Performance Considerations

Use parCost() to evaluate benefits of parallel execution

Balance between too many fine-grained tasks and coarse ones

Consider I/O vs CPU-bound operations

♻️ Contributing

Fork this repo

Create a branch: git checkout -b feature-name

Install dev dependencies:

pip install -e ".[dev]"

Run tests:

pytest tests/ -v

Submit a PR 📈

📃 License

MIT License. See LICENSE.

👤 Authors

AHAMADA Naheri

GHALEM Oualid

Thanks to our teacher Sergiu Ivanov (Université d'Évry) 🎓

📄 Citation

@software{max_auto_parallelisation,
  author = {AHAMADA, Naheri and GHALEM, Oualid},
  title = {Max Auto Parallelisation Library},
  year = {2025},
  url = {https://github.com/Oualidu/max-auto-parallelisation-library}
}

