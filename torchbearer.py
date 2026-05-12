"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Ryan Desrosiers 
Student ID:   130096873

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    a1 = "A single shortest path would only give the shortest path from S to all the different dungeon locations, but we need the path that visits multiple nodes in the shortest overall path." 
    b1 = "Once the shortest path between any and all two nodes is calculated, the order in which we need to visit them must still be decided."
    c1 = "Since there will be many different combinations of orders (shortest path to different nodes combined), a search over the many different orders is needed."
    return a1 + b1 + c1


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    TODO
    """
    answer = set() # set for no duplicates then make into list 
    answer.add(spawn)
    for relic in relics: 
        answer.add(relic)
    answer.add(exit_node)
    answer = list(answer)
    return answer


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    TODO
    """
    distances = {}
    visited = set()
    for node in graph:
        distances[node] = float('inf')
    distances[source] = 0
    prq = []
    heapq.heappush(prq, (0, source)) # init priority queue with source node 
    while prq: 
        # check neighbors to relax edges? 
        current = heapq.heappop(prq)  
        node = current[1]
        distance = current[0]
        if node in visited: 
            continue 
        visited.add(node)
        for neighbor, cost in graph[node]:
            if distance + cost < distances[neighbor]:
                distances[neighbor] = distance + cost
                heapq.heappush(prq, (distance + cost, neighbor))
    return distances 


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    TODO
    """
    shortest_paths = {}
    nodes = select_sources(spawn, relics, exit_node)
    for node in nodes: 
        shortest_paths[node] = run_dijkstra(graph, node)
    return shortest_paths


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    TODO
    """
    a3 = """ Part 3a: What the Invariant Means
For nodes already finalized (in S): For every finalized node, the distance stored for it is the shortest distance from the source to that node.
For nodes not yet finalized (not in S): For every node that is not yet finalized, the distance stored for it is the shortest current known path from the sourde to that node."""
    b3 = """Part 3b: Why Each Phase Holds
Initialization : why the invariant holds before iteration 1: The invariant holds before iteration 1 because before the first iteration, none of the paths to other nodes are discovered yet. Since no paths are known, the distance for every node but the source node is set to infinity (marking unreachable for now). Then the distance to the source node, is the distance to itself which is zero.

Maintenance : why finalizing the min-dist node is always correct: The min-dist node is always correct because a priority queue is used, which means the shortest distance from all known unfinalized distances is extracted. Since another path to this node would only be found through future unknown paths, and there are only nonnegative edge weights, another path would only be more expensive.

Termination : what the invariant guarantees when the algorithm ends: When the algorithm ends that means all reachable node have been finalized. Since every finalized node has the minimum possible distance stored, and every node is finalized, every path known is the shortest possible path from the source to the node.

"""
    c3 = """Part 3c: Why This Matters for the Route Planner
Since we precompute and the store the shortest distances between certain nodes, the correct route must be calculated using those true shortest distances."""
    return a3 + b3 + c3 


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    TODO
    """
    part4 = """Why Greedy Fails
**The failure mode: The failure mode happens when the closest relic chosen by a greedy decision does not lead to the optimal global path.
Counter-example setup: For a counter example, consider the following graph: (A->B: 1), (A->C: 2), (C->B: 2), (B->C: 4), (C->D: 1), (B->D: 1). Suppose the relics are at B and C, and the start and end nodes are A and D respectively.
What greedy picks: The greedy choice would be the closest possible relic which would be the relic at B.
What optimal picks: The optimal choice would be going to the relic C first.
Why greedy loses: The path that greedy would choose is: (A->B->C->D which costs 6), whereas the optimal is: (A->C->B->D: which costs 5).
What the Algorithm Must Explore
The algorithm must explore different orders of visiting relics using the precomputed shortest distances.

    """
    return part4


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    

    TODO
    """
    collected = []
    cost = 0
    best_solution_sofar = [float('inf'), []] # best cost of path so far - 0, empty list for best path of nodes 
    _explore(dist_table, spawn, relics, collected, cost, exit_node, best_solution_sofar)
    return (best_solution_sofar[0], best_solution_sofar[1]) 


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    TODO
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    if (not relics_remaining): # means no more relics remaining 
        final_cost = cost_so_far + dist_table[current_loc][exit_node]
        if (final_cost < best[0]):
            best[0] = final_cost
            best[1] = relics_visited_order.copy()
        return
    if (cost_so_far >= best[0]): # stop work rn for paths with no possibility of beating current min 
        return # means were already at or past the current minimum (so this answer will never be more optimal)
    for relic in relics_remaining:
        total_cost = cost_so_far + dist_table[current_loc][relic]
        new_order = relics_visited_order + [relic]
        remaining_now = [x for x in relics_remaining if x != relic]
        _explore(dist_table, relic, remaining_now, new_order, total_cost, exit_node, best)



# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
