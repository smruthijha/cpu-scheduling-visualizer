def calculate_averages(results, gantt=None, *args, **kwargs):
    """
    Computes scheduling criteria: Waiting Time, Turnaround Time, Response Time,
    CPU Utilization, Throughput, and Context Switches.
    Safely accepts optional num_cores as positional or keyword argument.
    """
    total_processes = len(results)

    if total_processes == 0:
        return {
            "Average Waiting Time": 0.0,
            "Average Turnaround Time": 0.0,
            "Average Response Time": 0.0,
            "CPU Utilization (%)": 0.0,
            "Throughput": 0.0,
            "Total Execution Time": 0,
            "Context Switches": 0
        }

    total_waiting = sum(p["Waiting Time"] for p in results)
    total_turnaround = sum(p["Turnaround Time"] for p in results)
    total_response = sum(p["Response Time"] for p in results)
    total_burst = sum(p["Burst Time"] for p in results)

    # Determine num_cores
    num_cores = kwargs.get("num_cores", 1)
    if args and len(args) > 0 and isinstance(args[0], (int, float)):
        num_cores = int(args[0])

    # Auto-detect number of distinct cores if present in gantt
    if gantt:
        cores_found = set(item.get("core", "CPU Core 0") for item in gantt)
        if len(cores_found) > 1:
            num_cores = max(num_cores, len(cores_found))

    # Calculate CPU Utilization & Makespan from Gantt chart if available
    makespan = 0
    context_switches = 0
    if gantt and len(gantt) > 0:
        makespan = max(item["end"] for item in gantt)
        # Group by core to count context switches per processor
        core_groups = {}
        for item in gantt:
            c = item.get("core", "CPU Core 0")
            if c not in core_groups:
                core_groups[c] = []
            core_groups[c].append(item)

        for c, items in core_groups.items():
            for i in range(len(items) - 1):
                curr_p = items[i]["process"]
                next_p = items[i + 1]["process"]
                if curr_p != next_p and curr_p != "Idle" and next_p != "Idle":
                    context_switches += 1
    else:
        makespan = max(p["Completion Time"] for p in results) if results else 0

    cpu_utilization = round((total_burst / (makespan * num_cores) * 100), 2) if makespan > 0 else 0.0
    throughput = round(total_processes / makespan, 4) if makespan > 0 else 0.0

    return {
        "Average Waiting Time": round(total_waiting / total_processes, 2),
        "Average Turnaround Time": round(total_turnaround / total_processes, 2),
        "Average Response Time": round(total_response / total_processes, 2),
        "CPU Utilization (%)": cpu_utilization,
        "Throughput": throughput,
        "Total Execution Time": makespan,
        "Context Switches": context_switches
    }
