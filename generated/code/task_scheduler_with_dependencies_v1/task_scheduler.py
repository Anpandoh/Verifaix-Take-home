def schedule_tasks(tasks, dependencies):
    """
    Computes a valid execution order for tasks with dependencies.
    
    Args:
        tasks: list[str] - List of unique task names
        dependencies: list[tuple[str, str]] - Dependency pairs (before_task, after_task)
    
    Returns:
        list[str] - A valid ordering of all tasks respecting dependencies
    
    Raises:
        TypeError: If tasks or dependencies are not lists, or contain invalid types
        ValueError: If duplicate tasks, unknown tasks in dependencies, or circular dependencies exist
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
    
    # Check for duplicate tasks
    if len(tasks) != len(set(tasks)):
        raise ValueError("Duplicate task names found")
    
    # Validate dependencies format
    for dep in dependencies:
        if not isinstance(dep, tuple) or len(dep) != 2:
            raise TypeError("Dependency must be a pair of strings")
        if not isinstance(dep[0], str) or not isinstance(dep[1], str):
            raise TypeError("Dependency must be a pair of strings")
    
    # Handle empty case
    if not tasks:
        return []
    
    # Create task set for validation
    task_set = set(tasks)
    
    # Validate all dependencies reference known tasks
    for before_task, after_task in dependencies:
        if before_task not in task_set:
            raise ValueError(f"Dependency refers to unknown task: {before_task}")
        if after_task not in task_set:
            raise ValueError(f"Dependency refers to unknown task: {after_task}")
    
    # Build adjacency list and in-degree count
    graph = {task: [] for task in tasks}
    in_degree = {task: 0 for task in tasks}
    
    for before_task, after_task in dependencies:
        if before_task == after_task:
            raise ValueError(f"Circular dependency exists: task cannot depend on itself")
        graph[before_task].append(after_task)
        in_degree[after_task] += 1
    
    # Kahn's algorithm with lexicographic ordering
    # Start with tasks that have no dependencies
    available = sorted([task for task in tasks if in_degree[task] == 0])
    result = []
    
    while available:
        # Pick lexicographically smallest available task
        current = available.pop(0)
        result.append(current)
        
        # Process all tasks that depend on current
        for dependent in sorted(graph[current]):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                # Insert in sorted position to maintain lexicographic order
                available.append(dependent)
                available.sort()
    
    # Check for cycles: if we didn't process all tasks, there's a cycle
    if len(result) != len(tasks):
        raise ValueError("Circular dependency exists")
    
    return result
