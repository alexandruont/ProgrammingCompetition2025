# Graph Treasure Hunt Optimizer (DFS + Pruning + Heuristics)

This project implements an optimized **Depth-First Search** algorithm enhanced with **Branch and Bound** techniques and **heuristic sorting** to find the **cyclic path with the maximum score** in a graph where each edge contains a number of collectable artifacts.


---

## Optimizations

- **Depth-First Search** to explore all cyclic paths from every valid starting node
- **Pruning** based on upper bound score estimation (Branch and Bound)
- **Heuristic neighbor sorting** to prioritize valuable paths
- **Backtracking** to revert and explore alternatives efficiently

---

## Problem Description

Given:
- A **graph** where nodes represent rooms and edges (tunnels) contain a number of **artifacts**
- A **visit limit** per room
- Goal: Start in any room and return to it, collecting the **maximum number of artifacts** without exceeding visit limits or reusing tunnel artifacts

---

