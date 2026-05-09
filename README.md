# The Torchbearer

**Student Name:** Ryan Desrosiers
**Student ID:** 130096873
**Course:** CS 460 – Algorithms | Spring 2026

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  A single shortest path would only give the shortest path from S to all the different dungeon locations. But we need the path that visits multiple nodes in the shortest overall path. 

- **What decision remains after all inter-location costs are known:**
  Once the shortest path between any and all two nodes is calculated, the order between the multiple nodes that we need to visit must still be decided. 

- **Why this requires a search over orders (one sentence):**
  Since there will be many different combinations of orders (shortest path to different nodes combined), a search over the many different orders is needed.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source |
|---|---|
| Start Node |This is a source because the algorithm will start here|
| Dunegon Node |Since we need to visit multiple dungeons sequentially, one dungeon may become a start node in the path to another. |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property | Your answer |
|---|---|
| Data structure name |Dictionary |
| What the keys represent |The keys represent the nodes |
| What the values represent |The values are an adjacency list with each item being the tuple (node, distance)|
| Lookup time complexity | O(1) because it uses hashing to store the values|
| Why O(1) lookup is possible |Because it uses hashing, the key leads directly to the value| 

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** The dijkstra algorithm is run for every source node. 
- **Cost per run:** _your answer_
- **Total complexity:** _your answer_
- **Justification (one line):** _your answer_

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  For every finalized node, the distance stored for it is the shortest distance from the source to that node. 

- **For nodes not yet finalized (not in S):**
  For every node that is not yet finalized, the distance stored for it is the shortest current known path from the sourde to that node. 

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
 The invariant holds before iteration 1 because before the first iteration, none of the paths to other nodes are discovered yet. Since no paths are known, the distance for every node but the source node is set to infinity (marking unreachable for now). Then the distance to the source node, is the distance to itself which is zero. 

- **Maintenance : why finalizing the min-dist node is always correct:**
 The min-dist node is always correct because since a priority queue is used, that was the shortest distance from all known unfinalized distances in the priority queue. Since another path to this node would only be found through future unknown paths, that would only add cost later and therefore not be the minimum. *************** change this explanation later ***** 

- **Termination : what the invariant guarantees when the algorithm ends:**
  When the algorithm ends that means all reachable node have been finalized. Since every finalized node has the current possible distance stored, and every node is finalized, every path known is the shortest possible path from the source to the node. 

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

The shortest possible distances from the source to every node are necessary pieces of information for the torchbearer to have to be able to visit all the relics and find the shortest path to the end. 

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode: The failure mode happens when the closest relic chosen by a greedy decision does not lead to the optimal global path. 
- **Counter-example setup:** For a counter example, consider the following graph: (A->B: 1), (A->C: 2), (C->B: 2), (B->C: 4), (C->D: 1), (B->D: 1). Suppose the relics are at B and C, and the start and end nodes are A and D respectively. 
- **What greedy picks:** The greedy choice would be the closest possible relic which would be the relic at B. 
- **What optimal picks:** The optimal choice would be going to the relic C first. 
- **Why greedy loses:** The path that greedy would choose is: (A->B->C->D which costs 6), whereas the optimal is: (A->C->B->D: which costs 5). 

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- _Your answer here._

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current | node? | |
| Relics already collected | collected | List | |
| Fuel cost so far | costFuel | int | Keeps track of fuel used so far |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | Set?|
| Operation: check if relic already collected | Time complexity: O(1)? |
| Operation: mark a relic as collected | Time complexity: O(1)? |
| Operation: unmark a relic (backtrack) | Time complexity: O(1)?|
| Why this structure fits | |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _Your answer (in terms of k)._
- **Why:** _One-line justification._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
