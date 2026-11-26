def get_simulation_snapshot(processes, gantt, t):
    """
    Computes CPU dispatch state, Ready Queue, and per-process status at time t.
    Supports both Single-Core and Multi-Core execution timelines.
    """
    max_time = max(item["end"] for item in gantt) if gantt else 0
    t = min(max(0, t), max_time)

    # 1. Identify which processes are actively executing on CPU core(s) during [start, end)
    running_by_core = {}
    running_pids = set()

    if t < max_time:
        for item in gantt:
            if item["start"] <= t < item["end"]:
                core = item.get("core", "CPU Core 0")
                pid = item["process"]
                running_by_core[core] = pid
                if pid != "Idle":
                    running_pids.add(pid)

        if not running_by_core:
            display_running = "Idle"
        elif len(running_by_core) == 1:
            display_running = list(running_by_core.values())[0]
        else:
            display_running = " | ".join(f"{c}: {p}" for c, p in sorted(running_by_core.items()))
    else:
        display_running = "Finished"

    # Calculate completed burst per process up to time t
    burst_completed = {p["id"]: 0 for p in processes}
    for item in gantt:
        pid = item["process"]
        if pid == "Idle":
            continue
        overlap_start = max(item["start"], 0)
        overlap_end = min(item["end"], t)
        if overlap_end > overlap_start:
            burst_completed[pid] += (overlap_end - overlap_start)

    # Completion times from gantt
    last_gantt_end = {}
    for item in gantt:
        pid = item["process"]
        if pid != "Idle":
            last_gantt_end[pid] = max(last_gantt_end.get(pid, 0), item["end"])

    # Classify each process status
    ready_queue = []
    completed = []
    upcoming = []
    process_states = []

    for p in processes:
        pid = p["id"]
        arr = p["arrival"]
        total_b = p["burst"]
        done_b = burst_completed.get(pid, 0)
        rem_b = max(0, total_b - done_b)
        comp_time = last_gantt_end.get(pid, 0)

        if arr > t:
            state = "Not Arrived"
            badge_color = "#94A3B8"
            upcoming.append(pid)
        elif done_b >= total_b or (comp_time <= t and comp_time > 0):
            state = "Terminated"
            badge_color = "#059669"
            completed.append(pid)
        elif pid in running_pids:
            state = "Executing"
            badge_color = "#2563EB"
        else:
            state = "Ready"
            badge_color = "#D97706"
            ready_queue.append(pid)

        process_states.append({
            "Process": pid,
            "Arrival": arr,
            "Total Burst": total_b,
            "Executed": done_b,
            "Remaining": rem_b,
            "Status": state,
            "Color": badge_color
        })

    return {
        "current_time": t,
        "max_time": max_time,
        "running_process": display_running,
        "running_pids": list(running_pids),
        "ready_queue": ready_queue,
        "completed": completed,
        "upcoming": upcoming,
        "process_states": process_states
    }
