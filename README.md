# The Torchbearer

**Student Name:** Ryan Desrosiers
**Student ID:** 130096873
**Course:** CS 460 – Algorithms | Spring 2026

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  A single shortest path would only give the shortest path from S to all the different dungeon locations, but we need the path that visits multiple nodes in the shortest overall path. 

- **What decision remains after all inter-location costs are known:**
  Once the shortest path between any and all two nodes is calculated, the order in which we need to visit them must still be decided. 

- **Why this requires a search over orders (one sentence):**
  Since there will be many different combinations of orders (shortest path to different nodes combined), a search over the many different orders is needed.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source |
|---|---|
| Start Node | This is a source because the algorithm will start here|
| Dungeon/Relic Node | Since we need to visit multiple dungeons sequentially, each visited node might become a source node for the remaining part of the path. |

### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | Dictionary |
| What the keys represent | The keys represent the nodes |
| What the values represent |A dictionary as well|
| Lookup time complexity | O(1) because it uses hashing to store the values|
| Why O(1) lookup is possible |Because it uses hashing, the key leads directly to the value| 

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** The dijkstra algorithm is run for every source node (spawn + end point + relics). 
- **Cost per run:** Dijkstra relaxes all the edges in a graph, and since we used a heap, those actions cost about log(v) work. 
- **Total complexity:** The total work is O(S*ELogV). 
- **Justification (one line):** Dijkstra will be run from every source node. So, the total complexity is the number of source nodes (S) times the cost per run of dijkstra which is (ELogV) --> S * ELogV = (S*ELogV). 

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means


- **For nodes already finalized (in S):**
  For every finalized node, the distance stored for it is the shortest distance from the source to that node. 

- **For nodes not yet finalized (not in S):**
  For every node that is not yet finalized, the distance stored for it is the shortest current known path from the sourde to that node. 

### Part 3b: Why Each Phase Holds


- **Initialization : why the invariant holds before iteration 1:**
 The invariant holds before iteration 1 because before the first iteration, none of the paths to other nodes are discovered yet. Since no paths are known, the distance for every node but the source node is set to infinity (marking unreachable for now). Then the distance to the source node, is the distance to itself which is zero. 

- **Maintenance : why finalizing the min-dist node is always correct:**
 The min-dist node is always correct because a priority queue is used, which means the shortest distance from all known unfinalized distances is extracted. Since another path to this node would only be found through future unknown paths, and there are only nonnegative edge weights, another path would only be more expensive. 

- **Termination : what the invariant guarantees when the algorithm ends:**
  When the algorithm ends that means all reachable node have been finalized. Since every finalized node has the minimum possible distance stored, and every node is finalized, every path known is the shortest possible path from the source to the node. 

### Part 3c: Why This Matters for the Route Planner

Since we precompute and the store the shortest distances between certain nodes, the correct route must be calculated using those true shortest distances. 

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode: The failure mode happens when the closest relic chosen by a greedy decision does not lead to the optimal global path. 
- **Counter-example setup:** For a counter example, consider the following graph: (A->B: 1), (A->C: 2), (C->B: 2), (B->C: 4), (C->D: 1), (B->D: 1). Suppose the relics are at B and C, and the start and end nodes are A and D respectively. 
- **What greedy picks:** The greedy choice would be the closest possible relic which would be the relic at B. 
- **What optimal picks:** The optimal choice would be going to the relic C first. 
- **Why greedy loses:** The path that greedy would choose is: (A->B->C->D which costs 6), whereas the optimal is: (A->C->B->D: which costs 5). 

### What the Algorithm Must Explore

The algorithm must explore different orders of visiting relics using the precomputed shortest distances. 

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_loc | Node | This node keeps track of where the algorithm is currently. |
| Relics already collected | relics_visited_order | List | Keeps a list of relics that already have been visited. |
| Fuel cost so far | cost_so_far | int | Keeps track of fuel used up until current location |

### Part 5b: Data Structure for Visited Relics

| Property | Your answer |
|---|---|
| Data structure chosen | List |
| Operation: check if relic already collected | Time complexity: O(n) |
| Operation: mark a relic as collected | Time complexity: O(n) |
| Operation: unmark a relic (backtrack) | Time complexity: O(n)|
| Why this structure fits | A list is used to keep track of the order they were visited. |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** The worst case would be k! permutations. 
- **Why:** Since you are exploring all possible orders/permutations of k relics, with no pruning the number is k factorial. 

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking


- **What is tracked:** The current cost of the path that has been found. 
- **When it is used:** After the algorithm finishes a valid path, it is compared to the running minimum. 
- **What it allows the algorithm to skip:** It allows the algorithm to skip some orders that are already worse than the current minimum and therefore could not be the best solution. 

### Part 6b: Lower Bound Estimation


- **What information is available at the current state:** During recursion we must know the current node it's at, a list of relics that we have visited so far, a list of relics that still need to be visited, and the current cost of the path. 
- **What the lower bound accounts for:** The lower bound acts as an estimate of what the minimum possible total cost of the current path could be using the precomputed distances that are laid out for the remaining path. 
- **Why it never overestimates:** The lower bound is always assumes an optimal route path from there on out, therefore it assumes a best-case scenario so it will never overestimate a path cost.  
### Part 6c: Pruning Correctness


- Pruning is always safe here because the lower bound is always an under-estimate. Since it is an optimistic estimate, it will never prune a valid solution by mistake (only those that are unnecessary to compute and will not possibly beat the current minimum). 

---

## References

> Bullet list. If none beyond lecture notes, write that.

- Lecture Notes
