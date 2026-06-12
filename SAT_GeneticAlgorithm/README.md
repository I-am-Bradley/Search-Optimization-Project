# 3‑SAT Solver — Genetic Algorithm

This module solves CNF‑formatted 3‑SAT problems using a Genetic Algorithm with:

- Tournament selection  
- Single‑point, two‑point, and uniform crossover  
- Mutation with stagnation‑based adaptation  
- Elitism to preserve top individuals  

---

## 🚀 Features

- Reads SAT clauses from text files  
- Tracks max/avg/min fitness per generation  
- Generates required fitness‑evolution plots  
- Scales to 100‑variable SAT instances  

---

## ▶️ Run

**"python 3SAT_Titagwan_Bradley.py"**

---

## 📄 Notes

- 3SAT_100_100 is under‑constrained and easily solved.  
- 3SAT_100_500 is over‑constrained; best result is 495/500.  
