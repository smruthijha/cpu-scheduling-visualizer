
def priority_scheduling(processes, lower_is_higher=True):

    processes = sorted(
        processes,
        key=lambda p: (p["arrival"], p["id"])
    )

    current_time = 0
    completed = []
    results = []
    gantt = []

    while len(completed) < len(processes):

        # Find processes that have arrived
        available = [
            p for p in processes
            if p["arrival"] <= current_time
            and p["id"] not in completed
        ]

        # Handle CPU idle time
        if not available:
            next_process = min(
                [p for p in processes if p["id"] not in completed],
                key=lambda p: (p["arrival"], p["id"])
            )

            gantt.append({
                "process": "Idle",
                "start": current_time,
                "end": next_process["arrival"]
            })

            current_time = next_process["arrival"]
            continue

        # Select process with highest priority
        if lower_is_higher:
            selected = min(
                available,
                key=lambda p: (
                    p["priority"],
                    p["arrival"],
                    p["id"]
                )
            )
        else:
            selected = max(
                available,
                key=lambda p: (
                    p["priority"],
                    -p["arrival"]
                )
            )

        pid = selected["id"]
        arrival = selected["arrival"]
        burst = selected["burst"]

        start = current_time
        completion = start + burst

        waiting = start - arrival
        turnaround = completion - arrival
        response = start - arrival

        results.append({
            "Process": pid,
            "Arrival Time": arrival,
            "Burst Time": burst,
            "Priority": selected["priority"],
            "Completion Time": completion,
            "Waiting Time": waiting,
            "Turnaround Time": turnaround,
            "Response Time": response
        })

        gantt.append({
            "process": pid,
            "start": start,
            "end": completion
        })

        current_time = completion
        completed.append(pid)

    return results, gantt
