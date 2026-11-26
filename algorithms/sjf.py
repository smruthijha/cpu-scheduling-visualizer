
def sjf(processes):

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

        # Select process with shortest burst time
        selected = min(
            available,
            key=lambda p: (p["burst"], p["arrival"], p["id"])
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
