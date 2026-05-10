def schedule_tasks(tasks, dependencies):
    """
    Computes a valid execution order for tasks with dependencies.
    
    Args:
        tasks: list[str] - List of unique task names
        dependencies: list[tuple[str, str]] - Dependency pairs (before_task, after_task)
    
    Returns:
        list[str] - A valid ordering of all tasks where dependencies are satisfied
    
    Raises:
        TypeError: If tasks or dependencies are not lists, or if task names are not strings,
                   or if dependencies are not tuples of two strings
        ValueError: If duplicate task names exist, if dependencies reference unknown tasks,
                    or if circular dependencies exist
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
        raise ValueError("Duplicate task names found")
    
    # Validate dependencies format and content
    for dep in dependencies:
        if not isinstance(dep, tuple) or len(dep) != 2:
            raise TypeError("Dependency must be a tuple of two elements")
        if not isinstance(dep[0], str) or not isinstance(dep[1], str):
            raise TypeError("Dependency must be a pair of strings")
    
    # Convert tasks to set for O(1) lookup
    task_set = set(tasks)
    
    # Validate all dependencies reference known tasks
    for before_task, after_task in dependencies:
        if before_task not in task_set:
            raise ValueError(f"Dependency references unknown task: {before_task}")
        if after_task not in task_set:
            raise ValueError(f"Dependency references unknown task: {after_task}")
    
    # Handle empty case
    if not tasks:
        return []
    
    # Build adjacency list and in-degree count
    graph = {task: [] for task in tasks}
    in_degree = {task: 0 for task in tasks}
    
    for before_task, after_task in dependencies:
        # Check for self-referential dependency
        if before_task == after_task:
            raise ValueError(f"Circular dependency: task cannot depend on itself")
        
        graph[before_task].append(after_task)
        in_degree[after_task] += 1
    
    # Kahn's algorithm with lexicographic ordering (largest first)
    # Use a list and sort to maintain deterministic lexicographic order
    available = sorted([task for task in tasks if in_degree[task] == 0], reverse=True)
    result = []
    
    while available:
        # Select lexicographically largest available task
        current = available.pop(0)
        result.append(current)
        
        # Process neighbors
        neighbors = []
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                neighbors.append(neighbor)
        
        # Add newly available tasks and maintain sorted order
        available.extend(neighbors)
        available.sort(reverse=True)
    
    # Check for cycles: if not all tasks were processed, there's a cycle
    if len(result) != len(tasks):
        raise ValueError("Circular dependency detected")
    
    return result
