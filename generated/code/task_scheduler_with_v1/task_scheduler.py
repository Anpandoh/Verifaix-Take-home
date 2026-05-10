def schedule_tasks(tasks, dependencies):
    """
    Computes a valid execution order for tasks with dependencies.
    
    Args:
        tasks: list[str] - List of unique task names
        dependencies: list[tuple[str, str]] - Dependency pairs (before_task, after_task)
    
    Returns:
        list[str] - A valid ordering of all tasks respecting dependencies
    
    Raises:
        TypeError: If tasks or dependencies are not lists, or if task names or
                   dependency pairs are not strings/string pairs
        ValueError: If duplicate tasks exist, dependencies reference unknown tasks,
                    or circular dependencies exist
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
        before_task, after_task = dep
        if not isinstance(before_task, str) or not isinstance(after_task, str):
            raise TypeError("Dependency must be a pair of strings")
    
    # Handle empty input
    if not tasks:
        return []
    
    # Create task set for validation
    task_set = set(tasks)
    
    # Validate all dependencies reference known tasks
    for before_task, after_task in dependencies:
        if before_task not in task_set:
            raise ValueError(f"Dependency references unknown task: {before_task}")
        if after_task not in task_set:
            raise ValueError(f"Dependency references unknown task: {after_task}")
    
    # Build adjacency list and in-degree count
    graph = {task: [] for task in tasks}
    in_degree = {task: 0 for task in tasks}
    
    for before_task, after_task in dependencies:
        graph[before_task].append(after_task)
        in_degree[after_task] += 1
    
    # Detect circular dependencies using Kahn's algorithm
    # Start with tasks that have no dependencies
    queue = sorted([task for task in tasks if in_degree[task] == 0])
    result = []
    temp_in_degree = in_degree.copy()
    
    while queue:
        # Always pick lexicographically smallest available task
        queue.sort()
        current = queue.pop(0)
        result.append(current)
        
        # Process neighbors
        for neighbor in graph[current]:
            temp_in_degree[neighbor] -= 1
            if temp_in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If we couldn't process all tasks, there's a cycle
    if len(result) != len(tasks):
        raise ValueError("Circular dependency detected")
    
    return result
