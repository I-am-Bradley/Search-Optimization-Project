# Magic Square — A\* Search & UCS

This module solves a 3×3 Magic Square using:

- **Uniform Cost Search (UCS)**
- **A\* Search with Manhattan Distance ÷ 2 (admissible)**
- **A\* Search with Misplaced Tiles (non‑admissible)**

The program compares all three in terms of:
- Nodes expanded  
- Execution time  
- Path cost  

---

## 🚀 Features

- Generates random 3×3 states  
- Computes successors via adjacent swaps  
- Implements two heuristics  
- Produces comparison plots  
- Includes a 10‑run evaluation for statistical reliability  

---

## ▶️ Run

**"python MS_Titagwan_Bradley.py"**


---

## 📄 Notes

- Manhattan Distance ÷ 2 is admissible because one swap moves two tiles.  
- Misplaced Tiles is not admissible and may return sub‑optimal paths.  
