
from collections import deque


def round_robin(processes, quantum):

    if quantum <= 0:
        raise ValueError("Time quantum must be greater than zero")

    processes = sorted(
        processes,
        key=lambda p: (p["arrival"], p["id"])
    )

    n = len(processes)

    remaining = {
        p["id"]: p["burst"] for p in processes
    }

    first_start = {}
    completion_time = {}

    ready_queue = deque()
    gantt = []

    current_time = 0
    index = 0

    while len(completion_time) < n:

        # Add arrived processes to ready queue
        while (
            index < n
            and processes[index]["arrival"] <= current_time
        ):
            ready_queue.append(processes[index])
            index += 1

        # Handle CPU idle time
        if not ready_queue:

            if index < n:
                next_arrival = processes[index]["arrival"]

                gantt.append({
                    "process": "Idle",
                    "start": current_time,
                    "end": next_arrival
                })

                current_time = next_arrival
                continue

            break

        # Select next process
        process = ready_queue.popleft()

        pid = process["id"]

        # Record first response time
        if pid not in first_start:
            first_start[pid] = current_time

        start = current_time

        # Execute for quantum or remaining burst
        execution_time = min(
            quantum,
            remaining[pid]
        )

        current_time += execution_time
        remaining[pid] -= execution_time

        gantt.append({
            "process": pid,
            "start": start,
            "end": current_time
        })

        # Add newly arrived processes
        while (
            index < n
            and processes[index]["arrival"] <= current_time
        ):
            ready_queue.append(processes[index])
            index += 1

        # Check process completion
        if remaining[pid] == 0:

            completion_time[pid] = current_time

        else:
            # Move unfinished process to queue
            ready_queue.append(process)

    results = []

    for p in processes:

        pid = p["id"]

        arrival = p["arrival"]
        burst = p["burst"]

        completion = completion_time[pid]

        turnaround = completion - arrival
        waiting = turnaround - burst
        response = first_start[pid] - arrival

        results.append({
            "Process": pid,
            "Arrival Time": arrival,
            "Burst Time": burst,
            "Completion Time": completion,
            "Waiting Time": waiting,
            "Turnaround Time": turnaround,
            "Response Time": response
        })

    return results, gantt
