import networkx as nx

from typing import Any

class Orchestrator:
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def add_task(self, task_func, task_name, depends_on=None):
        """
        Adds a task to the DAG. 
        
        Args:
        - task_func: the function to run
        - task_name: the name of the task
        - depends_on: a list of task names that this task depends on
        """
        self.graph.add_node(task_name, func=task_func)
        
        if depends_on is not None:
            for parent_task in depends_on:
                self.graph.add_edge(parent_task, task_name)
    
    def run(self, input: Any):
        """
        Runs all tasks in the DAG in topological order.
        """
        for task_name in nx.topological_sort(self.graph):
            task_func = self.graph.nodes[task_name]['func']
            res = task_func()
