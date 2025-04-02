# Max Auto Parallelisation

An intelligent Python library for automatic task parallelization with dependency management and performance optimization.

![Task System Example]('/Users/naher/Downloads/screens_CleanShotX/CleanShot 2025-04-02 at 19.15.28@2x.png')

## 🎯 Overview

Max Auto Parallelisation helps you optimize task execution by automatically identifying and managing parallel execution opportunities while respecting task dependencies.

### Key Features
- Automatic parallelization detection
- Dependency validation and cycle detection
- Performance measurement and optimization
- Visual task graph generation
- Interactive task system creation

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/max_auto_parallelisation.git
cd max_auto_parallelisation

# Install dependencies
pip install -r requirements.txt
```

## 📋 Requirements
- Python 3.7+
- graphviz (optional, for visualization)
- pytest (for testing)

## 💡 Usage

### Interactive Task Creation
```bash
python max_auto_parallelisation_library/input.py
```

### Programmatic Usage
```python
from max_auto_parallelisation_library.maxpar import Task, TaskSystem

# Define tasks
task1 = Task(name="T1", reads=["A"], writes=["B"], run=lambda: print("Task 1"))
task2 = Task(name="T2", reads=["B"], writes=["C"], run=lambda: print("Task 2"))

# Define dependencies
precedence = {
    "T1": [],
    "T2": ["T1"]
}

# Create and run system
system = TaskSystem(tasks=[task1, task2], precedence=precedence)
system.run()
```

## 🧪 Testing

The project includes comprehensive tests. To run them:

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest -v tests/

# Run specific test file
pytest tests/test_maxpar.py -v

# Run with coverage report
pytest --cov=max_auto_parallelisation_library tests/
```

### Test Output Example
```
============================= test session starts ==============================
collecting ... collected 8 items

tests/test_maxpar.py::test_task_initialization PASSED                  [ 12%]
tests/test_maxpar.py::test_task_system_initialization PASSED          [ 25%]
...
```

## 📊 Performance Analysis

The library includes built-in performance analysis:
```python
results = system.parCost(num_runs=3, warmup_runs=1)
print(f"Speedup achieved: {results['speedup']}x")
```

![Performance Comparison](docs/images/performance.png)

## 🔍 Use Cases

### 1. Data Processing Pipelines
```python
# Example: ETL Pipeline
extract_task = Task(name="extract", writes=["raw_data"])
transform_task = Task(name="transform", reads=["raw_data"], writes=["processed_data"])
load_task = Task(name="load", reads=["processed_data"])
```

### 2. Build Systems
- Compiling multiple source files
- Asset generation
- Documentation building

### 3. Scientific Computing
- Matrix operations
- Image processing
- Simulation calculations

## 🛠 Contributing

1. Fork the repository
2. Create your feature branch
3. Run tests before committing:
```bash
pytest tests/ -v
```
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

- Report issues on GitHub
- Join our community discussions
- Check documentation for detailed API reference

## 🌟 Acknowledgments

- Built with Python's concurrent.futures
- Visualization powered by graphviz
- Testing framework: pytest

---

**Note**: Remember to replace images paths with actual screenshots from your test runs and system visualizations.