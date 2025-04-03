Max Auto Parallelisation Library

An intelligent Python library for automatic task parallelization with dependency management and performance optimization.



Overview

Max Auto Parallelisation Library automatically optimizes task execution by:

Detecting and removing redundant dependencies

Maximizing parallel execution opportunities

Ensuring thread-safe execution

Providing real-time performance metrics

Installation

pip install max_auto_parallelisation_library

Then install additional dependencies:

pip install -r requirements.txt

Quick Start

from max_auto_parallelisation_library import Task, TaskSystem

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

# Create and run system
system = TaskSystem(tasks=tasks, precedence=precedence)
system.run()  # Executes tasks in parallel where possible

Key Features
