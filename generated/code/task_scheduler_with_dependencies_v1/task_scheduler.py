def schedule_tasks(tasks, dependencies):
    """
    Computes a valid execution order for tasks with dependencies.
    
    Args:
        tasks: list[str] - List of unique task names
        dependencies: list[tuple[str, str]] - Dependency pairs (before_task, after_task)
    
    Returns:
        list[str] - A valid ordering of all tasks respecting dependencies
    
    Raises:
        TypeError: If tasks or dependencies are not lists, or if task names are not strings,
                   or if dependencies are not pairs of strings
        ValueError: If duplicate task names exist, if dependencies reference unknown tasks,
                    if circular dependencies exist, or if self-referential dependencies exist
    """
    # Type validation for tasks parameter
    if not isinstance(tasks, list):
        raise TypeError("tasks must be a list")
    
    # Type validation for dependencies parameter
    if not isinstance(dependencies, list):
        raise TypeError("dependencies must be a list")
    
    # Type validation for task names
    for task in tasks:
        if not isinstance(task, str):
            raise TypeError("Task name must be a string")
    
    # Check for duplicate task names
    if len(tasks) != len(set(tasks)):
        raise ValueError("Duplicate task names")
    
    # Type validation for dependencies and check for unknown tasks
    task_set = set(tasks)
    for dep in dependencies:
        if not isinstance(dep, tuple) or len(dep) != 2:
            raise TypeError("Dependency must be a pair of strings")
        before_task, after_task = dep
        if not isinstance(before_task, str) or not isinstance(after_task, str):
            raise TypeError("Dependency must be a pair of strings")
        if before_task not in task_set:
            raise ValueError("Dependency refers to unknown task")
        if after_task not in task_set:
            raise ValueError("Dependency refers to unknown task")
        if before_task == after_task:
            raise ValueError("Circular dependency exists")
    
    # Handle empty input
    if not tasks:
        return []
    
    # Build adjacency list and in-degree count
    graph = {task: [] for task in tasks}
    in_degree = {task: 0 for task in tasks}
    
    for before_task, after_task in dependencies:
        graph[before_task].append(after_task)
        in_degree[after_task] += 1
    
    # Detect circular dependencies using Kahn's algorithm
    queue = [task for task in tasks if in_degree[task] == 0]
    queue.sort()  # Start with lexicographically smallest
    
    result = []
    in_degree_copy = in_degree.copy()
    
    while queue:
        # Always pick the lexicographically smallest available task
        queue.sort()
        current = queue.pop(0)
        result.append(current)
        
        for neighbor in graph[current]:
            in_degree_copy[neighbor] -= 1
            if in_degree_copy[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all tasks were processed (no circular dependency)
    if len(result) != len(tasks):
        raise ValueError("Circular dependency exists")
    
    return result
