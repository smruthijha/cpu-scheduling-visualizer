def edf(processes):
    """
    Earliest Deadline First (EDF) - Preemptive Real-Time Scheduling.
    Each process dictionary contains:
      - 'id': Process identifier
      - 'arrival': Arrival Time
      - 'burst': CPU Burst Time
      - 'deadline': Absolute Deadline (defaults to arrival + burst * 2 if missing)
    """
    if not processes:
        return [], []

    # Sort processes by arrival time and id
    sorted_proc = sorted(processes, key=lambda p: (p["arrival"], p["id"]))
    n = len(sorted_proc)

    # Initialize process parameters
    remaining_burst = {p["id"]: p["burst"] for p in sorted_proc}
    arrival_times = {p["id"]: p["arrival"] for p in sorted_proc}
    burst_times = {p["id"]: p["burst"] for p in sorted_proc}
    # If deadline not explicitly set, calculate reasonable default
    deadlines = {
        p["id"]: p.get("deadline", p.get("priority", 0) * 4 if p.get("priority", 0) > 0 else p["arrival"] + p["burst"] * 2)
        for p in sorted_proc
    }

    first_start = {}
    completion_times = {}

    current_time = 0
    completed = 0
    raw_gantt = []

    while completed < n:
        # Arrived and unfinished processes
        available = [
            p["id"] for p in sorted_proc
            if arrival_times[p["id"]] <= current_time and remaining_burst[p["id"]] > 0
        ]

        if not available:
            # Advance time to next arrival
            next_arrival = min(
                arrival_times[p["id"]] for p in sorted_proc if remaining_burst[p["id"]] > 0
            )
            raw_gantt.append(("Idle", current_time, next_arrival))
            current_time = next_arrival
            continue

        # Select process with earliest absolute deadline (EDF)
        # Tie breaker: earliest arrival, then PID
        selected_pid = min(
            available,
            key=lambda pid: (deadlines[pid], arrival_times[pid], pid)
        )

        if selected_pid not in first_start:
            first_start[selected_pid] = current_time

        # Run for 1 time unit (preemptive check)
        raw_gantt.append((selected_pid, current_time, current_time + 1))
        remaining_burst[selected_pid] -= 1
        current_time += 1

        if remaining_burst[selected_pid] == 0:
            completion_times[selected_pid] = current_time
            completed += 1

    # Merge contiguous Gantt intervals
    gantt = []
    for item in raw_gantt:
        pid, start, end = item
        if gantt and gantt[-1]["process"] == pid and gantt[-1]["end"] == start:
            gantt[-1]["end"] = end
        else:
            gantt.append({"process": pid, "start": start, "end": end})

    results = []
    for p in sorted_proc:
        pid = p["id"]
        arr = arrival_times[pid]
        burst = burst_times[pid]
        comp = completion_times[pid]
        tat = comp - arr
        wt = tat - burst
        rt = first_start[pid] - arr
        dl = deadlines[pid]
        met = "Yes" if comp <= dl else "No (Violated)"

        results.append({
            "Process": pid,
            "Arrival Time": arr,
            "Burst Time": burst,
            "Deadline": dl,
            "Completion Time": comp,
            "Waiting Time": wt,
            "Turnaround Time": tat,
            "Response Time": rt,
            "Met Deadline": met
        })

    return results, gantt
