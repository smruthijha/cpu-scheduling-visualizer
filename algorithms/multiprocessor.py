def multiprocessor_scheduling(processes, num_cores=2):
    """
    Dual-Core / Multi-Processor Symmetric Multiprocessing (SMP) Scheduling.
    Processes are placed into a global shared Ready Queue (ordered by arrival time).
    Whenever any core (Core 0 or Core 1) becomes idle, it dispatches the next
    ready process from the shared queue (Self-scheduling SMP model).
    """
    if not processes:
        return [], []

    sorted_proc = sorted(processes, key=lambda p: (p["arrival"], p["id"]))
    n = len(sorted_proc)

    arrival_times = {p["id"]: p["arrival"] for p in sorted_proc}
    burst_times = {p["id"]: p["burst"] for p in sorted_proc}
    remaining_burst = {p["id"]: p["burst"] for p in sorted_proc}

    first_start = {}
    completion_times = {}

    # State of each core: {"pid": None, "busy_until": 0}
    cores = [{"core_id": i, "pid": None, "busy_until": 0} for i in range(num_cores)]

    current_time = 0
    completed = 0
    gantt = []
    ready_queue = []
    dispatched = set()

    while completed < n:
        # Add newly arrived processes to ready queue
        for p in sorted_proc:
            pid = p["id"]
            if pid not in dispatched and pid not in ready_queue and arrival_times[pid] <= current_time:
                ready_queue.append(pid)

        # Check if any busy core finishes at current_time
        for core in cores:
            if core["pid"] is not None and core["busy_until"] == current_time:
                pid = core["pid"]
                completion_times[pid] = current_time
                completed += 1
                core["pid"] = None

        # Assign available processes to idle cores
        for core in cores:
            if core["pid"] is None and ready_queue:
                pid = ready_queue.pop(0)
                dispatched.add(pid)
                core["pid"] = pid
                core["busy_until"] = current_time + burst_times[pid]

                if pid not in first_start:
                    first_start[pid] = current_time

                gantt.append({
                    "process": pid,
                    "start": current_time,
                    "end": core["busy_until"],
                    "core": f"CPU Core {core['core_id']}"
                })

        if completed >= n:
            break

        # Advance clock to next meaningful event:
        # Either the earliest core finish time or next process arrival
        future_times = []
        for core in cores:
            if core["pid"] is not None and core["busy_until"] > current_time:
                future_times.append(core["busy_until"])

        for p in sorted_proc:
            if arrival_times[p["id"]] > current_time:
                future_times.append(arrival_times[p["id"]])

        if future_times:
            next_time = min(future_times)
            current_time = next_time
        else:
            current_time += 1

    results = []
    for p in sorted_proc:
        pid = p["id"]
        arr = arrival_times[pid]
        burst = burst_times[pid]
        comp = completion_times[pid]
        tat = comp - arr
        wt = tat - burst
        rt = first_start[pid] - arr

        results.append({
            "Process": pid,
            "Arrival Time": arr,
            "Burst Time": burst,
            "Completion Time": comp,
            "Waiting Time": wt,
            "Turnaround Time": tat,
            "Response Time": rt
        })

    return results, gantt
