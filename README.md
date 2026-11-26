# ⚡ CPU Scheduling Visualizer & Benchmark Suite

An interactive, modern simulation and benchmarking platform for Operating Systems CPU scheduling, built with **Streamlit**, **Plotly**, and **Pandas**.

---

## 🌟 Key Features

1. **CPU Scheduling Algorithms Supported**:
   - **FCFS** (First-Come, First-Served)
   - **SJF** (Shortest Job First — Non-Preemptive)
   - **SRTF** (Shortest Remaining Time First — Preemptive SJF)
   - **Priority Scheduling** (Non-Preemptive, with configurable priority order)
   - **Priority Scheduling** (Preemptive)
   - **Round Robin** (with configurable Time Quantum)
   - **Multilevel Queue (MLQ)** (Foreground RR + Background FCFS)
   - **Real-Time EDF** (Earliest Deadline First with deadline tracking)
   - **Dual-Core SMP** (Symmetric Multiprocessing across 2 processor cores)
   - **🏆 Compare All Algorithms** (simultaneous multi-algorithm benchmarking matrix)

2. **Interactive Visualizations**:
   - **Multi-Core Gantt Timeline**: Horizontal bar charts with millisecond time boundaries, process color coding, and multi-core support.
   - **Interactive Step-by-Step Dispatch Scrubber**: Step through clock cycles ($t=0 \dots \text{Makespan}$) with Play/Next/Prev/Reset controls, watching the CPU Core, Ready Queue in RAM, and Process States evolve live.

3. **Demonstration Presets**:
   - Standard Workload (P1-P4)
   - Convoy Effect Demo (FCFS vs SJF)
   - Preemption Showdown (SJF vs SRTF)
   - Starvation & Priority Inversion Demo
   - Round Robin Time Slicing Demo
   - Real-Time Deadlines Demo (for EDF)
   - Dual-Core SMP Parallelism Demo

4. **Telemetry & Performance Metrics**:
   - Average Waiting Time ($AWT$)
   - Average Turnaround Time ($ATAT$)
   - Average Response Time ($ART$)
   - CPU Utilization Percentage ($\%$)
   - System Throughput ($\text{processes} / \text{unit time}$)
   - Context Switches count
   - One-click CSV export of scheduling reports.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Virtual environment (`venv`)

### Installation & Run
```powershell
# 1. Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 2. Install dependencies (if not already installed)
pip install -r requirements.txt

# 3. Launch the visualizer dashboard
streamlit run app.py
```

### Running the Test Suite
```powershell
python test.py
```

---

## 📂 Project Structure

```
CPU-Scheduling-Visualizer/
├── algorithms/
│   ├── fcfs.py                 # First-Come First-Served
│   ├── sjf.py                  # Shortest Job First (Non-Preemptive)
│   ├── srtf.py                 # Shortest Remaining Time First (Preemptive)
│   ├── priority.py             # Priority Scheduling (Non-Preemptive)
│   ├── priority_preemptive.py  # Priority Scheduling (Preemptive)
│   ├── round_robin.py          # Round Robin Scheduling
│   ├── multilevel_queue.py     # Multilevel Queue Scheduling (Foreground RR + Background FCFS)
│   ├── edf.py                  # Real-Time Earliest Deadline First (EDF)
│   └── multiprocessor.py       # Dual-Core Symmetric Multiprocessing (SMP)
├── utils/
│   ├── calculations.py         # Scheduling Criteria (WT, TAT, RT, CPU Util, Throughput, CS)
│   ├── gantt_chart.py          # Single & Multi-Core Plotly Gantt charts & comparison graphs
│   └── simulator.py            # Step-by-step CPU dispatch & ready queue state snapshot generator
├── app.py                      # Main Streamlit dashboard application
├── test.py                     # Automated test suite
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```
