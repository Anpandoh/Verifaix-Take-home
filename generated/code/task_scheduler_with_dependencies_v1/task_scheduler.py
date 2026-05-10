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
                   dependency pairs are not properly typed
        ValueError: If duplicate tasks exist, unknown tasks in dependencies,
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
    
    # Validate dependencies are tuples of strings
    for dep in dependencies:
        if not isinstance(dep, tuple) or len(dep) != 2:
            raise TypeError("Dependency must be a tuple of two elements")
        if not isinstance(dep[0], str) or not isinstance(dep[1], str):
            raise TypeError("Dependency must be a pair of strings")
    
    # Check for duplicate task names
    if len(tasks) != len(set(tasks)):
        raise ValueError("Duplicate task names found")
    
    # Handle empty case
    if not tasks:
        return []
    
    task_set = set(tasks)
    
    # Validate all dependencies reference known tasks
    for before, after in dependencies:
        if before not in task_set:
            raise ValueError(f"Unknown task in dependency: {before}")
        if after not in task_set:
            raise ValueError(f"Unknown task in dependency: {after}")
    
    # Check for self-referential dependencies
    for before, after in dependencies:
        if before == after:
            raise ValueError(f"Task cannot depend on itself: {before}")
    
    # Build adjacency list and in-degree count
    graph = {task: [] for task in tasks}
    in_degree = {task: 0 for task in tasks}
    
    # Process dependencies (avoid duplicates by using set)
    seen_deps = set()
    for before, after in dependencies:
        if (before, after) not in seen_deps:
            graph[before].append(after)
            in_degree[after] += 1
            seen_deps.add((before, after))
    
    # Kahn's algorithm with lexicographic ordering
    queue = sorted([task for task in tasks if in_degree[task] == 0])
    result = []
    
    while queue:
        # Always pick lexicographically smallest available task
        current = queue.pop(0)
        result.append(current)
        
        # Process neighbors
        neighbors = []
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                neighbors.append(neighbor)
        
        # Add new available tasks in sorted order
        queue.extend(neighbors)
        queue.sort()
    
    # Check for cycles
    if len(result) != len(tasks):
        raise ValueError("Circular dependency detected")
    
    return result
