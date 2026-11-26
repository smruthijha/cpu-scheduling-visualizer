
def srtf(processes):
    """
    Shortest Remaining Time First (Preemptive SJF)
    """
    if not processes:
        return [], []

    processes = sorted(processes, key=lambda p: (p["arrival"], p["id"]))
    n = len(processes)

    remaining_burst = {p["id"]: p["burst"] for p in processes}
    arrival_times = {p["id"]: p["arrival"] for p in processes}
    burst_times = {p["id"]: p["burst"] for p in processes}
    
    first_start = {}
    completion_times = {}

    current_time = 0
    completed = 0
    raw_gantt = []

    while completed < n:
        # Arrived and unfinished
        available = [
            p["id"] for p in processes
            if arrival_times[p["id"]] <= current_time and remaining_burst[p["id"]] > 0
        ]

        if not available:
            # CPU is idle until next process arrives
            next_arrival = min(
                arrival_times[p["id"]] for p in processes if remaining_burst[p["id"]] > 0
            )
            raw_gantt.append(("Idle", current_time, next_arrival))
            current_time = next_arrival
            continue

        # Process with minimum remaining burst time, tie-breaker: arrival time, id
        selected_pid = min(
            available,
            key=lambda pid: (remaining_burst[pid], arrival_times[pid], pid)
        )

        if selected_pid not in first_start:
            first_start[selected_pid] = current_time

        # Run for 1 time unit
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
    for p in processes:
        pid = p["id"]
        arr = arrival_times[pid]
        burst = burst_times[pid]
        comp = completion_times[pid]
        tat = comp - arr
        wt = tat - burst
        rt = first_start[pid] - arr

        res = {
            "Process": pid,
            "Arrival Time": arr,
            "Burst Time": burst,
            "Completion Time": comp,
            "Waiting Time": wt,
            "Turnaround Time": tat,
            "Response Time": rt
        }
        if "priority" in p:
            res["Priority"] = p["priority"]
        results.append(res)

    return results, gantt
