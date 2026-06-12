# Traveling Salesperson Problem — Simulated Annealing

This module solves TSP instances using:

- **Brute‑Force Search** (optimal but exponential)
- **Simulated Annealing** (fast, probabilistic)

The SA implementation includes:
- 2‑Opt inversion neighbor generation  
- Inner loop for thermal equilibrium  
- Geometric cooling schedule: Tₖ = T₀ × αᵏ  
- Stability testing across 10 runs  

---

## 🚀 Features

- Reads TSP datasets from text files  
- Computes Euclidean distances  
- Tracks temperature, cost, and random‑walk events  
- Generates all required plots for TSP4  

---

## ▶️ Run

**"python TSP_Titagwan_Bradley.py"**

---

## 📄 Notes

- SA consistently reaches the optimal solution for all provided datasets.  
- Brute‑force becomes infeasible at 12 cities (factorial growth).  
