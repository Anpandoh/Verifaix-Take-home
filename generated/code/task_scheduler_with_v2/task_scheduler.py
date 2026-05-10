def schedule_tasks(tasks, dependencies):
    """
    Computes a valid execution order for tasks with dependencies.
    
    Args:
        tasks: list[str] - List of unique task names
        dependencies: list[tuple[str, str]] - Dependency pairs (before_task, after_task)
    
    Returns:
        list[str] - A valid ordering of all tasks respecting dependencies,
                   with lexicographically largest tasks selected first when available.
    
    Raises:
        TypeError: If tasks or dependencies are not lists, or if task names are not strings,
                  or if dependencies are not pairs of strings.
        ValueError: If duplicate task names exist, if dependencies refer to unknown tasks,
                   or if circular dependencies exist.
    """
    # Type validation
    if not isinstance(tasks, list):
        raise TypeError("tasks must be a list")
    if not isinstance(dependencies, list):
        raise TypeError("dependencies must be a list")
    
    # Validate task names are strings
    for task in tasks:
        if not isinstance(task, str):
            raise TypeError("Task name must be a string")
    
    # Check for duplicate task names
    if len(tasks) != len(set(tasks)):
        raise ValueError("Duplicate task names")
    
    # Validate dependencies are pairs of strings
    for dep in dependencies:
        if not isinstance(dep, (tuple, list)) or len(dep) != 2:
            raise TypeError("Dependency must be a pair of strings")
        if not isinstance(dep[0], str) or not isinstance(dep[1], str):
            raise TypeError("Dependency must be a pair of strings")
    
    # Handle empty case
    if not tasks:
        return []
    
    task_set = set(tasks)
    
    # Check that all dependencies refer to known tasks
    for before_task, after_task in dependencies:
        if before_task not in task_set:
            raise ValueError("Dependency refers to unknown task")
        if after_task not in task_set:
            raise ValueError("Dependency refers to unknown task")
    
    # Build adjacency list and in-degree count
    graph = {task: [] for task in tasks}
    in_degree = {task: 0 for task in tasks}
    
    for before_task, after_task in dependencies:
        graph[before_task].append(after_task)
        in_degree[after_task] += 1
    
    # Detect circular dependencies using DFS
    def has_cycle():
        visited = set()
        rec_stack = set()
        
        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for task in tasks:
            if task not in visited:
                if dfs(task):
                    return True
        return False
    
    if has_cycle():
        raise ValueError("Circular dependency exists")
    
    # Topological sort using Kahn's algorithm with lexicographic ordering
    # Use a list and sort to maintain lexicographically largest-first ordering
    available = [task for task in tasks if in_degree[task] == 0]
    available.sort(reverse=True)  # Sort in descending order for lexicographic largest-first
    
    result = []
    
    while available:
        # Pick the lexicographically largest available task
        current = available.pop(0)
        result.append(current)
        
        # Process neighbors
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                available.append(neighbor)
                available.sort(reverse=True)  # Maintain sorted order
    
    return result
