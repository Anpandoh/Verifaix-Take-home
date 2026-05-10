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
        raise TypeError("tasks is not a list")
    if not isinstance(dependencies, list):
        raise TypeError("dependencies is not a list")
    
    # Validate task names are strings
    for task in tasks:
        if not isinstance(task, str):
            raise TypeError("Task name is not a string")
    
    # Check for duplicate task names
    if len(tasks) != len(set(tasks)):
        raise ValueError("Duplicate task names")
    
    # Validate dependency format
    for dep in dependencies:
        if not isinstance(dep, tuple) or len(dep) != 2:
            raise TypeError("Dependency is not a pair of strings")
        if not isinstance(dep[0], str) or not isinstance(dep[1], str):
            raise TypeError("Dependency is not a pair of strings")
    
    # Handle empty case
    if not tasks:
        return []
    
    # Create task set for validation
    task_set = set(tasks)
    
    # Validate all dependencies reference known tasks
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
    
    # Detect circular dependencies using Kahn's algorithm
    queue = [task for task in tasks if in_degree[task] == 0]
    queue.sort()  # Lexicographic order
    
    result = []
    temp_in_degree = in_degree.copy()
    
    while queue:
        # Pick lexicographically smallest available task
        queue.sort()
        current = queue.pop(0)
        result.append(current)
        
        # Process neighbors
        for neighbor in graph[current]:
            temp_in_degree[neighbor] -= 1
            if temp_in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all tasks were processed (no cycles)
    if len(result) != len(tasks):
        raise ValueError("Circular dependency exists")
    
    return result
