from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.srtf import srtf
from algorithms.priority import priority_scheduling
from algorithms.priority_preemptive import priority_preemptive
from algorithms.round_robin import round_robin
from algorithms.edf import edf
from algorithms.multilevel_queue import multilevel_queue
from algorithms.multiprocessor import multiprocessor_scheduling

from utils.calculations import calculate_averages
from utils.gantt_chart import create_gantt_chart
from utils.simulator import get_simulation_snapshot


def test_visualizer():
    processes = [
        {"id": "P1", "arrival": 0, "burst": 5, "priority": 2, "deadline": 10},
        {"id": "P2", "arrival": 1, "burst": 3, "priority": 1, "deadline": 6},
        {"id": "P3", "arrival": 2, "burst": 8, "priority": 3, "deadline": 25},
        {"id": "P4", "arrival": 3, "burst": 6, "priority": 2, "deadline": 18}
    ]

    algos = [
        ("FCFS", lambda: fcfs(processes)),
        ("SJF (Non-Preemptive)", lambda: sjf(processes)),
        ("SRTF (Preemptive)", lambda: srtf(processes)),
        ("Priority (Non-Preemptive)", lambda: priority_scheduling(processes, True)),
        ("Priority (Preemptive)", lambda: priority_preemptive(processes, True)),
        ("Round Robin (q=2)", lambda: round_robin(processes, 2)),
        ("Multilevel Queue (MLQ)", lambda: multilevel_queue(processes, 2)),
        ("Real-Time EDF", lambda: edf(processes)),
        ("Dual-Core SMP", lambda: multiprocessor_scheduling(processes, 2))
    ]

    print("=" * 80)
    print("SYLLABUS-ALIGNED CPU SCHEDULING ALGORITHMS TEST SUITE")
    print("=" * 80)

    for name, fn in algos:
        results, gantt = fn()
        metrics = calculate_averages(results, gantt)
        fig = create_gantt_chart(gantt, f"{name} Gantt")
        assert fig is not None, f"Gantt chart generation failed for {name}"
        assert len(results) == 4, f"Results incomplete for {name}"
        print(f"✓ {name:<26} | AWT: {metrics['Average Waiting Time']:<5} | ATAT: {metrics['Average Turnaround Time']:<5} | Util: {metrics['CPU Utilization (%)']:<5}% | Tput: {metrics['Throughput']:<6} | CS: {metrics['Context Switches']}")

    # Test Simulator Snapshot
    res_rr, gantt_rr = round_robin(processes, 2)
    snap = get_simulation_snapshot(processes, gantt_rr, 4)
    assert snap["current_time"] == 4
    print("✓ Simulator Snapshot at t=4: CPU =", snap["running_process"], "| Ready Queue =", snap["ready_queue"])

    # Test Dual Core Snapshot
    res_mp, gantt_mp = multiprocessor_scheduling(processes, 2)
    snap_mp = get_simulation_snapshot(processes, gantt_mp, 3)
    assert snap_mp["current_time"] == 3
    print("✓ Dual-Core Snapshot at t=3: CPU =", snap_mp["running_process"])

    print("=" * 80)
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    test_visualizer()
