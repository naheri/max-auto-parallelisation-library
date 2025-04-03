# Max Auto Parallelisation Library 🧠⚙️

A Python library for **automated maximum parallelization** of task systems — designed to simplify concurrent programming and optimize execution time.

<p align="center">
  <img src="images/task_system_max_parallel.png" width="70%" alt="Task System Example">
</p>
![alt tag](https://private-user-images.githubusercontent.com/203723579/429864920-a40b358c-1538-427a-879e-c711387eda34.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDM2NzEyMjMsIm5iZiI6MTc0MzY3MDkyMywicGF0aCI6Ii8yMDM3MjM1NzkvNDI5ODY0OTIwLWE0MGIzNThjLTE1MzgtNDI3YS04NzllLWM3MTEzODdlZGEzNC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNDAzJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDQwM1QwOTAyMDNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT03ODQwYTdjOThlOTQ0ZGNjNTZlNzQyYzY3YmY2YjgxZWY1YWZjYWIwZjhlNDIzOTkxZTc1YWZjYTkwMjgzYzA2JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.-B8SDX-OwZxu1vE0hYZPEaE9CtDu1ASxqO9hd-MGYa8)
---


## 🔍 Overview

This library enables:

- ⚡ Automatic detection and elimination of unnecessary dependencies
- 🚀 Maximized parallel task execution
- 🔐 Thread-safe and deterministic execution
- 📊 Benchmarking and performance analysis
- 🧩 Graph visualization of task dependencies

---

## 📦 Installation

```bash
pip install max_auto_parallelisation_library
# Or install required dependencies
pip install -r requirements.txt
```

---

## 🚀 Quick Start

```python
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
```

---

## ✨ Key Features

### ✅ Maximal Parallelism
- Removes redundant dependencies
- Optimizes execution order for concurrency

### 🔄 Execution Modes
- `runSeq()`: Sequential execution
- `run()`: Parallel execution (with thread-safety)

### 📈 Performance Analysis

```python
results = system.parCost(num_runs=5, warmup_runs=2)
print(f"Speedup: {results['speedup']}x")
print(f"Improvement: {results['improvement_percentage']}%")
```

### 🔬 Determinism Test

```python
is_deterministic = system.detTestRnd(globals(), cles=["X", "Y", "Z"])
print("Deterministic?", is_deterministic)
```

### 🔹 Visual Task Graph

```python
system.draw("task_system")  # Requires Graphviz
```

---

## 🧪 Use Cases

### Data Pipelines
```python
tasks = [
    Task("extract", writes=["raw"]),
    Task("clean", reads=["raw"], writes=["clean"]),
    Task("transform", reads=["clean"], writes=["data"]),
    Task("load", reads=["data"])
]
```

### Scientific Workflows
```python
tasks = [
    Task("calc1", reads=["A"], writes=["C"]),
    Task("calc2", reads=["B"], writes=["D"]),
    Task("merge", reads=["C", "D"], writes=["result"])
]
```

### Build Systems
```python
tasks = [
    Task("compile_A", writes=["build/A"]),
    Task("compile_B", writes=["build/B"]),
    Task("test", reads=["build/A", "build/B"]),
    Task("deploy", reads=["build/A", "build/B"])
]
```

---

## 📂 API Reference

### `Task`
```python
Task(
    name: str,
    reads: List[str] = [],
    writes: List[str] = [],
    run: Callable = None
)
```

### `TaskSystem`
```python
TaskSystem(
    tasks: List[Task],
    precedence: Dict[str, List[str]]
)
```

---

## 🚀 Performance Tips

- Measure gains with `parCost()`
- Keep tasks reasonably coarse
- Avoid excessive overhead with tiny tasks

---

## ✨ Contributing

1. Fork the repo
2. Create your branch
3. Install dev dependencies:
```bash
pip install -e ".[dev]"
```
4. Run tests:
```bash
pytest tests/ -v
```
5. Open a pull request

---

## 📄 License
MIT License — see [LICENSE](LICENSE)

---

## 👨‍💼 Authors
- AHAMADA Naheri
- GHALEM Oualid

With thanks to **Sergiu Ivanov** — Université d'Évry

---

## 📖 Citation

```bibtex
@software{max_auto_parallelisation,
  author = {AHAMADA, Naheri and GHALEM, Oualid},
  title = {Max Auto Parallelisation Library},
  year = {2025},
  url = {https://github.com/naheri/max-auto-parallelisation-library}
}
```

