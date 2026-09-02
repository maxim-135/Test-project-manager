from typing import Dict, Any, List, Optional, Set
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class DAGService:
    """Service for Directed Acyclic Graph operations."""
    
    def __init__(self):
        self.graph: Dict[str, Set[str]] = defaultdict(set)
        self.in_degree: Dict[str, int] = defaultdict(int)
    
    def add_node(self, node_id: str) -> None:
        """Add a node to the DAG."""
        if node_id not in self.in_degree:
            self.in_degree[node_id] = 0
            self.graph[node_id] = set()
    
    def add_edge(self, from_node: str, to_node: str) -> None:
        """Add a directed edge between nodes."""
        self.add_node(from_node)
        self.add_node(to_node)
        self.graph[from_node].add(to_node)
        self.in_degree[to_node] += 1
    
    def topological_sort(self) -> List[str]:
        """Return nodes in topological order (Kahn's algorithm)."""
        in_degree_copy = self.in_degree.copy()
        queue = [node for node, degree in in_degree_copy.items() if degree == 0]
        result = []
        
        while queue:
            node = queue.pop(0)
            result.append(node)
            for neighbor in self.graph[node]:
                in_degree_copy[neighbor] -= 1
                if in_degree_copy[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(result) != len(self.graph):
            raise ValueError("Graph contains a cycle!")
        
        return result
    
    def get_dependencies(self, node_id: str) -> List[str]:
        """Get all dependencies of a node."""
        return list(self.graph.get(node_id, set()))
    
    def has_cycle(self) -> bool:
        """Check if the graph contains a cycle."""
        try:
            self.topological_sort()
            return False
        except ValueError:
            return True
