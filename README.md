# Search & Optimization Algorithms

## 🧭 Project Overview

### Title:
### Search & Optimization Algorithms

### Purpose

This repository contains three Artificial Intelligence projects implementing classical search and optimization algorithms. The projects explore heuristic search, metaheuristic optimization, and evolutionary computation by solving the Magic Square, Traveling Salesperson Problem (TSP), and 3-SAT Constraint Satisfaction Problem. Each implementation includes source code, datasets, visualizations, and an analytical report comparing algorithm performance.

### Audience

- Artificial Intelligence Students
- Computer Science Students
- Researchers
- Software Engineers
- Machine Learning Enthusiasts

---

# 🧱 Project Scope

## Project 1: Magic Square Search

Implements informed and uninformed search algorithms to solve the Magic Square problem while comparing search efficiency and heuristic performance.

### Components

- Uniform Cost Search (UCS)
- A* Search Engine
- Heuristic Evaluation
- Performance Analysis

### Techniques

- Uniform Cost Search
- A* Search
- Manhattan Distance Heuristic
- Misplaced Tiles Heuristic

---

## Project 2: Traveling Salesperson Problem

Applies Simulated Annealing to optimize travel routes while exploring the effects of cooling schedules and neighborhood generation.

### Components

- TSP Solver
- Neighbor Generator
- Cooling Scheduler
- Performance Visualization

### Techniques

- Simulated Annealing
- 2-Opt Neighborhood Search
- Geometric Cooling
- Equilibrium Inner Loop

---

## Project 3: 3-SAT Constraint Satisfaction

Uses a Genetic Algorithm to solve Boolean satisfiability problems through evolutionary optimization.

### Components

- Population Initialization
- Fitness Evaluation
- Selection
- Crossover
- Mutation
- Elitism

### Techniques

- Genetic Algorithm
- Tournament Selection
- One-Point & Two-Point Crossover
- Mutation
- Elitism
- Adaptive Evolution

---

# 📂 Repository Structure

```text
Search_Optimization_Algorithms/
│
├── Datasets/
│   ├── 3SAT_100_100.txt
│   ├── 3SAT_100_500.txt
│   ├── 3SAT_24_100.txt
│   ├── 3SAT_4_6.txt
│   ├── 3SAT_generator.py
│   ├── TSP1.txt
│   ├── TSP2.txt
│   ├── TSP3.txt
│   └── TSP4.txt
│
├── MagicSquare_AStar/
│   ├── MS_Titagwan_Bradley.py
│   ├── README.md
│
└── Report/
│   └── Project_Report.pdf
│   
├── SAT_GeneticAlgorithm/
│   ├── 3SAT_Titagwan_Bradley.py
│   └── README.md
│   
├── TSP_SimulatedAnnealing/
│   ├──README.md
│   └── TSP_Titagwan_Bradley.py
│
└── README.md
```

---

# 🤖 Algorithms Included

| Project | Algorithm | Purpose |
|---------|-----------|----------|
| Magic Square | Uniform Cost Search (UCS) | Finds the optimal solution using uninformed search |
| Magic Square | A* Search | Uses heuristic-guided search to improve efficiency |
| TSP | Simulated Annealing | Optimizes travel routes using probabilistic hill climbing |
| 3-SAT | Genetic Algorithm | Evolves candidate solutions to maximize satisfied clauses |

---

# 📊 Results Summary

## Magic Square

- Compared Uniform Cost Search and A* Search.
- Evaluated Manhattan Distance and Misplaced Tiles heuristics.
- Analyzed search efficiency and heuristic effectiveness.

## Traveling Salesperson Problem

- Implemented Simulated Annealing using 2-Opt neighbor generation.
- Evaluated the effects of geometric cooling on solution quality.
- Generated plots illustrating optimization performance over time.

## 3-SAT Constraint Satisfaction

- Solved Boolean satisfiability using a Genetic Algorithm.
- Compared crossover and mutation strategies.
- Evaluated convergence behavior and adaptive optimization techniques.

---

# 🚀 How to Run

Each project is self-contained and can be executed independently.

```bash
python <filename>.py
```

### Dependencies

Install the required Python packages:

```bash
pip install numpy matplotlib
```

The project also uses standard Python libraries:

- heapq
- time
- os

---

# 💻 Skills Demonstrated

- Artificial Intelligence
- Search Algorithms
- Heuristic Search
- A* Search
- Uniform Cost Search
- Simulated Annealing
- Genetic Algorithms
- Evolutionary Computation
- Constraint Satisfaction Problems
- Metaheuristic Optimization
- Algorithm Analysis
- Performance Benchmarking
- Data Visualization
- Python
- NumPy
- Matplotlib

---

# 📈 Future Improvements

- Implement additional heuristic search algorithms
- Compare Simulated Annealing with Hill Climbing and Tabu Search
- Add Parallel Genetic Algorithms
- Benchmark against modern optimization libraries
- Expand datasets for large-scale experimentation

---

# 📄 Documentation

The repository includes:

- Source Code
- Input Datasets
- Performance Plots
- Analytical Report

The complete project report can be found in:

```
Report/Project_Report.pdf
```

---

# 📬 Author

**Bradley Titagwan**

Version: v1.0
