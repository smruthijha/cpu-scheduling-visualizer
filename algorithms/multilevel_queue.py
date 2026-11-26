from collections import deque


def multilevel_queue(processes, quantum=2):
    """
    Multilevel Queue (MLQ) Scheduling:
    - Queue 1 (High Priority / Interactive Foreground): Round Robin with time quantum
      Assigned if Priority <= 1 (or lowest priority value)
    - Queue 2 (Low Priority / Batch Background): First-Come First-Served (FCFS)
      Assigned if Priority > 1
    Preemption: Queue 1 has strict priority over Queue 2. If a process arrives in
    Queue 1 while Queue 2 is executing, Queue 2 is preempted.
    """
    if not processes:
        return [], []

    sorted_proc = sorted(processes, key=lambda p: (p["arrival"], p["id"]))
    n = len(sorted_proc)

    remaining_burst = {p["id"]: p["burst"] for p in sorted_proc}
    arrival_times = {p["id"]: p["arrival"] for p in sorted_proc}
    burst_times = {p["id"]: p["burst"] for p in sorted_proc}
    priorities = {p["id"]: p.get("priority", 1) for p in sorted_proc}

    # Queue designation: priority <= 1 is Queue 1 (Interactive RR), else Queue 2 (Batch FCFS)
    q1_pids = {p["id"] for p in sorted_proc if priorities[p["id"]] <= 1}

    first_start = {}
    completion_times = {}

    current_time = 0
    completed = 0
    raw_gantt = []

    q1 = deque()  # Round Robin
    q2 = deque()  # FCFS
    arrived = set()

    # Time tracking for current quantum in Q1
    q1_current_proc = None
    q1_quantum_left = 0

    while completed < n:
        # Check newly arrived processes
        for p in sorted_proc:
            pid = p["id"]
            if pid not in arrived and arrival_times[pid] <= current_time:
                arrived.add(pid)
                if pid in q1_pids:
                    q1.append(pid)
                else:
                    q2.append(pid)

        # Decide which process executes
        if q1 or (q1_current_proc is not None and remaining_burst[q1_current_proc] > 0):
            # Queue 1 has priority
            if q1_current_proc is None or q1_quantum_left == 0:
                if q1:
                    q1_current_proc = q1.popleft()
                    q1_quantum_left = quantum
                else:
                    q1_current_proc = None

            if q1_current_proc is not None:
                selected_pid = q1_current_proc
                if selected_pid not in first_start:
                    first_start[selected_pid] = current_time

                raw_gantt.append((selected_pid, current_time, current_time + 1))
                remaining_burst[selected_pid] -= 1
                q1_quantum_left -= 1
                current_time += 1

                if remaining_burst[selected_pid] == 0:
                    completion_times[selected_pid] = current_time
                    completed += 1
                    q1_current_proc = None
                    q1_quantum_left = 0
                elif q1_quantum_left == 0:
                    # Quantum expired, check newly arrived before pushing back
                    for p in sorted_proc:
                        pid = p["id"]
                        if pid not in arrived and arrival_times[pid] <= current_time:
                            arrived.add(pid)
                            if pid in q1_pids:
                                q1.append(pid)
                            else:
                                q2.append(pid)
                    q1.append(selected_pid)
                    q1_current_proc = None
                continue

        elif q2:
            # Queue 2 executes (FCFS)
            selected_pid = q2[0]
            if selected_pid not in first_start:
                first_start[selected_pid] = current_time

            raw_gantt.append((selected_pid, current_time, current_time + 1))
            remaining_burst[selected_pid] -= 1
            current_time += 1

            if remaining_burst[selected_pid] == 0:
                completion_times[selected_pid] = current_time
                completed += 1
                q2.popleft()
            continue

        else:
            # CPU idle until next process arrives
            next_arrivals = [arrival_times[p["id"]] for p in sorted_proc if remaining_burst[p["id"]] > 0]
            if next_arrivals:
                next_arr = min(next_arrivals)
                raw_gantt.append(("Idle", current_time, next_arr))
                current_time = next_arr
            else:
                break

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
        q_name = "Q1 (Interactive RR)" if pid in q1_pids else "Q2 (Batch FCFS)"

        results.append({
            "Process": pid,
            "Queue": q_name,
            "Arrival Time": arr,
            "Burst Time": burst,
            "Priority": priorities[pid],
            "Completion Time": comp,
            "Waiting Time": wt,
            "Turnaround Time": tat,
            "Response Time": rt
        })

    return results, gantt
