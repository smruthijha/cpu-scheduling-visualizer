
def fcfs(processes):
    # Sort processes according to arrival time
    processes = sorted(
        processes,
        key=lambda p: (p["arrival"], p["id"])
    )

    current_time = 0
    results = []
    gantt = []

    for process in processes:

        pid = process["id"]
        arrival = process["arrival"]
        burst = process["burst"]

        # Handle CPU idle time
        if current_time < arrival:
            gantt.append({
                "process": "Idle",
                "start": current_time,
                "end": arrival
            })
            current_time = arrival

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

    return results, gantt
