import streamlit as st
import pandas as pd

from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.srtf import srtf
from algorithms.priority import priority_scheduling
from algorithms.priority_preemptive import priority_preemptive
from algorithms.round_robin import round_robin
from algorithms.multilevel_queue import multilevel_queue
from algorithms.edf import edf
from algorithms.multiprocessor import multiprocessor_scheduling

from utils.calculations import calculate_averages
from utils.gantt_chart import create_gantt_chart, create_comparison_chart
from utils.simulator import get_simulation_snapshot


# -----------------------------------------------------------------------------
# APPLICATION CONFIGURATION
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="CPU Scheduling Visualizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': 'CPU Scheduling Visualizer v2.0 - Professional OS Simulation Tool'
    }
)



# -----------------------------------------------------------------------------
# DESIGN SYSTEM & THEMING (PROFESSIONAL GRADE)
# -----------------------------------------------------------------------------
# Professional color palette with semantic meaning
COLOR_PALETTE = {
    # Primary brand colors
    "brand-primary": "#1e293b",        # Slate 900 - primary background
    "brand-primary-light": "#0f172a",  # Slate 800 - secondary background
    "brand-secondary": "#64748b",      # Slate 500 - muted text
    "brand-accent": "#3b82f6",         # Sky 500 - primary accent
    "brand-success": "#10b981",        # Emerald 500 - success
    "brand-warning": "#f59e0b",        # Amber 500 - warning
    "brand-error": "#ef4444",          # Red 500 - error
    "brand-info": "#6366f1",           # Indigo 500 - info

    # Status semantic colors
    "status-active": "#10b981",
    "status-idle": "#64748b",
    "status-waiting": "#f59e0b",
    "status-critical": "#ef4444",

    # Chart colors - enhanced distinct palette
    "chart-blue": "#3b82f6",
    "chart-emerald": "#10b981",
    "chart-amber": "#f59e0b",
    "chart-purple": "#8b5cf6",
    "chart-cyan": "#06b6d4",
    "chart-pink": "#ec4899",
    "chart-orange": "#f97316",

    # Background gradients
    "gradient-start": "#0f172a",
    "gradient-end": "#1e293b",
    "card-bg": "rgba(30, 41, 59, 0.5)",
    "card-bg-light": "rgba(15, 23, 42, 0.7)",

    # Neutral colors
    "neutral-50": "#f8fafc",
    "neutral-100": "#f1f5f9",
    "neutral-200": "#e2e8f0",
    "neutral-300": "#cbd5e1",
    "neutral-400": "#94a3b8",
    "neutral-500": "#64748b",
    "neutral-600": "#475569",
    "neutral-700": "#1e293b",
    "neutral-800": "#0f172a",
    "neutral-900": "#0a0a0d",
}

# Typography scale
TYPOGRAPHY = {
    "font-family": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    "font-family-mono": "'JetBrains Mono', monospace",
    "heading-1": {"fontSize": "2rem", "fontWeight": 700, "letterSpacing": "-0.02em"},
    "heading-2": {"fontSize": "1.5rem", "fontWeight": 600, "letterSpacing": "-0.01em"},
    "heading-3": {"fontSize": "1.25rem", "fontWeight": 600},
    "body": {"fontSize": "0.875rem", "fontWeight": 400},
    "caption": {"fontSize": "0.75rem", "fontWeight": 500, "textTransform": "uppercase", "letterSpacing": "0.05em"},
    "small": {"fontSize": "0.6875rem"},
    "xs": {"fontSize": "0.625rem"},
}

# CSS variables injection
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');

/* ==========================================================================
   DESIGN TOKENS  (single source of truth - every var() used below is defined here)
   ========================================================================== */
:root {
    /* Surfaces */
    --bg-app: #0f172a;
    --bg-sunken: #0b1220;
    --bg-surface: #1e293b;
    --bg-surface-2: #273449;

    /* Borders */
    --border: #334155;
    --border-strong: #475569;

    /* Text */
    --text-strong: #f8fafc;
    --text: #e2e8f0;
    --text-muted: #94a3b8;

    /* Brand / semantic (light tints, readable on dark surfaces) */
    --accent: #3b82f6;
    --accent-strong: #2563eb;
    --accent-hover: #1d4ed8;
    --brand-accent: #60a5fa;
    --brand-success: #34d399;
    --brand-warning: #fbbf24;
    --brand-error: #f87171;
    --brand-info: #818cf8;
    --status-active: #34d399;

    /* Neutral scale (kept for inline styles in the app body) */
    --neutral-50: #f8fafc;
    --neutral-100: #f1f5f9;
    --neutral-200: #e2e8f0;
    --neutral-300: #cbd5e1;
    --neutral-400: #94a3b8;
    --neutral-500: #64748b;
    --neutral-600: #475569;

    --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-family-mono: 'JetBrains Mono', 'SF Mono', Consolas, monospace;

    --radius-sm: 4px;
    --radius-md: 8px;
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.35);
}

/* ==========================================================================
   BASE: APP SHELL, SIDEBAR, HEADER BAR
   ========================================================================== */
.stApp,
[data-testid="stAppViewContainer"] {
    background-color: var(--bg-app);
    font-family: var(--font-family);
}

.stApp .block-container {
    padding-top: 3rem;
    max-width: 1400px;
}

[data-testid="stHeader"] {
    background: rgba(15, 23, 42, 0.92);
}
[data-testid="stHeader"] button,
[data-testid="stSidebarCollapseButton"] button,
[data-testid="stExpandSidebarButton"] {
    color: var(--text-muted) !important;
}

[data-testid="stSidebar"] {
    background-color: var(--bg-sunken);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] hr,
.stApp hr {
    border-color: var(--border);
}

/* ==========================================================================
   TYPOGRAPHY / TEXT VISIBILITY
   ========================================================================== */
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
    color: var(--text-strong);
    font-family: var(--font-family);
    letter-spacing: -0.01em;
}

.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li {
    color: var(--text);
}

.stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stWidgetLabel"] label {
    color: var(--text) !important;
    font-weight: 500;
    font-size: 0.85rem;
}

.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stCaptionContainer"] p {
    color: var(--text-muted) !important;
}

[data-testid="stTooltipIcon"] svg {
    color: var(--text-muted);
}

/* ==========================================================================
   HEADER BANNER
   ========================================================================== */
.system-header {
    background: linear-gradient(135deg, #0b1220 0%, #1e293b 100%);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-md);
    padding: 18px 24px;
    margin-bottom: 20px;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: space-between;
    align-items: center;
    box-shadow: var(--shadow-md);
}
.system-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-strong);
    letter-spacing: -0.02em;
}
.system-subtitle {
    font-size: 0.875rem;
    color: var(--text-muted);
    margin-top: 4px;
}

/* ==========================================================================
   TELEMETRY (METRIC) CARDS
   ========================================================================== */
.telemetry-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: var(--radius-md);
    padding: 14px 16px;
    margin-bottom: 16px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.telemetry-card:hover {
    border-color: var(--border-strong);
    box-shadow: var(--shadow-md);
}
.telemetry-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-muted);
    margin-bottom: 4px;
}
.telemetry-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text-strong);
    font-family: var(--font-family-mono);
    margin: 2px 0;
    line-height: 1.2;
    overflow-wrap: anywhere;
}
.telemetry-sub {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 2px;
}

/* Themed variants (used by the benchmark "leader" cards, which hold long text) */
.telemetry-card-accent  { border-left-color: var(--accent); }
.telemetry-card-success { border-left-color: #10b981; }
.telemetry-card-info    { border-left-color: #6366f1; }
.telemetry-card-warning { border-left-color: #f59e0b; }
.telemetry-card-error   { border-left-color: #ef4444; }
.telemetry-card-accent .telemetry-value,
.telemetry-card-success .telemetry-value,
.telemetry-card-info .telemetry-value {
    font-size: 1.15rem;
    font-family: var(--font-family);
}

/* ==========================================================================
   BUTTONS  (secondary, primary, download - all with explicit text colour)
   ========================================================================== */
.stApp .stButton > button,
.stApp .stDownloadButton > button {
    background: var(--bg-surface);
    color: var(--text);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-md);
    font-family: var(--font-family);
    font-weight: 600;
    font-size: 0.85rem;
    min-height: 2.5rem;
    padding: 0.4rem 1rem;
    transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease, box-shadow 0.15s ease;
}
.stApp .stButton > button p,
.stApp .stDownloadButton > button p {
    color: inherit !important;
    font-weight: 600;
}
.stApp .stButton > button:hover,
.stApp .stDownloadButton > button:hover {
    background: var(--bg-surface-2);
    border-color: var(--brand-accent);
    color: var(--brand-accent);
    box-shadow: var(--shadow-md);
}
.stApp .stButton > button:active {
    transform: translateY(1px);
}
.stApp .stButton > button:focus-visible,
.stApp .stDownloadButton > button:focus-visible {
    outline: 2px solid var(--brand-accent);
    outline-offset: 2px;
}
.stApp .stButton > button:disabled {
    opacity: 0.45;
    cursor: not-allowed;
}

/* Primary action buttons */
.stApp .stButton > button[kind="primary"],
.stApp .stButton > button[data-testid="stBaseButton-primary"] {
    background: var(--accent-strong);
    border-color: var(--accent-strong);
    color: #ffffff;
}
.stApp .stButton > button[kind="primary"]:hover,
.stApp .stButton > button[data-testid="stBaseButton-primary"]:hover {
    background: var(--accent-hover);
    border-color: var(--accent-hover);
    color: #ffffff;
}

/* Download button: outlined accent, fills on hover */
.stApp .stDownloadButton > button {
    background: transparent;
    border-color: var(--accent);
    color: var(--brand-accent);
}
.stApp .stDownloadButton > button:hover {
    background: var(--accent-strong);
    border-color: var(--accent-strong);
    color: #ffffff;
}

/* ==========================================================================
   INPUTS, SELECTS, RADIO, SLIDER
   ========================================================================== */
.stApp [data-baseweb="select"] > div,
.stApp [data-baseweb="input"],
.stApp [data-baseweb="base-input"] {
    background-color: var(--bg-surface) !important;
    border-color: var(--border-strong) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text) !important;
}
.stApp [data-baseweb="select"] > div:hover,
.stApp [data-baseweb="input"]:hover {
    border-color: var(--brand-accent) !important;
}
.stApp [data-baseweb="select"] *,
.stApp input {
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
}
.stApp [data-testid="stNumberInputStepUp"],
.stApp [data-testid="stNumberInputStepDown"] {
    background: var(--bg-surface-2);
    color: var(--text);
}

/* Dropdown menus render in a portal outside .stApp, so no .stApp prefix here */
[data-baseweb="popover"] > div,
[data-baseweb="menu"],
ul[role="listbox"] {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-md);
}
[data-baseweb="menu"] li,
ul[role="listbox"] li,
[data-baseweb="popover"] li {
    background: transparent !important;
    color: var(--text) !important;
}
[data-baseweb="menu"] li:hover,
ul[role="listbox"] li:hover,
ul[role="listbox"] li[aria-selected="true"] {
    background: var(--bg-surface-2) !important;
    color: var(--brand-accent) !important;
}

/* Radio */
.stApp [data-testid="stRadio"] label[data-baseweb="radio"] {
    border-radius: var(--radius-md);
    padding: 6px 10px;
    transition: background 0.15s ease;
}
.stApp [data-testid="stRadio"] label[data-baseweb="radio"]:hover {
    background: var(--bg-surface-2);
}
.stApp [data-testid="stRadio"] label[data-baseweb="radio"] p {
    color: var(--text) !important;
    font-size: 0.85rem;
}

/* Slider */
.stApp [data-testid="stTickBarMin"],
.stApp [data-testid="stTickBarMax"] {
    color: var(--text-muted) !important;
}
.stApp [data-testid="stSliderThumbValue"] {
    color: var(--brand-accent) !important;
    font-weight: 600;
}

/* ==========================================================================
   TABS
   ========================================================================== */
.stApp [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 1px solid var(--border);
}
.stApp button[data-baseweb="tab"] {
    background: transparent;
    color: var(--text-muted);
    padding: 10px 18px;
    border-radius: var(--radius-md) var(--radius-md) 0 0;
    transition: color 0.2s ease, background 0.2s ease;
}
.stApp button[data-baseweb="tab"] p {
    color: inherit !important;
    font-weight: 600;
    font-size: 0.92rem;
}
.stApp button[data-baseweb="tab"]:hover {
    color: var(--text-strong);
    background: rgba(148, 163, 184, 0.08);
}
.stApp button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--brand-accent);
    background: var(--bg-surface);
}
.stApp [data-baseweb="tab-highlight"] {
    background-color: var(--accent) !important;
    height: 3px;
}
.stApp [data-baseweb="tab-border"] {
    background-color: var(--border) !important;
}

/* ==========================================================================
   EXPANDERS, TABLES, ALERTS
   ========================================================================== */
.stApp [data-testid="stExpander"] {
    background: transparent;
    border: none;
}
.stApp [data-testid="stExpander"] details {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
}
.stApp [data-testid="stExpander"] summary {
    color: var(--text-strong);
}
.stApp [data-testid="stExpander"] summary p {
    color: var(--text-strong) !important;
    font-weight: 600;
}
.stApp [data-testid="stExpander"] summary svg {
    color: var(--text-muted);
}

.stApp [data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    overflow: hidden;
}

/* ==========================================================================
   STATUS BADGE
   ========================================================================== */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    background: rgba(16, 185, 129, 0.14);
    border: 1px solid rgba(52, 211, 153, 0.45);
    color: var(--status-active);
}
.status-dot {
    width: 7px;
    height: 7px;
    background: var(--status-active);
    border-radius: 50%;
    animation: pulse-status 2s ease-in-out infinite;
}
@keyframes pulse-status {
    0%, 100% { opacity: 1; box-shadow: 0 0 4px rgba(52, 211, 153, 0.6); }
    50%      { opacity: 0.5; box-shadow: 0 0 8px rgba(52, 211, 153, 0.9); }
}

/* ==========================================================================
   CPU DISPATCH CORE (previously unstyled)
   ========================================================================== */
.dispatch-core-box {
    background: var(--bg-surface);
    border: 1px solid var(--accent);
    border-radius: var(--radius-md);
    padding: 16px;
    text-align: center;
    min-height: 110px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.dispatch-header {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--brand-accent);
}
.dispatch-proc {
    font-family: var(--font-family-mono);
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-strong);
    margin: 6px 0;
    line-height: 1.2;
    overflow-wrap: anywhere;
}
.dispatch-sub {
    font-size: 0.78rem;
    color: var(--text-muted);
}

/* ==========================================================================
   QUEUE PANELS & PROCESS CHIPS
   ========================================================================== */
.queue-panel {
    background: var(--bg-sunken);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 12px 14px;
    min-height: 110px;
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}
.empty-tray-msg {
    color: var(--text-muted);
    font-style: italic;
    font-size: 0.85rem;
}
.badge-proc-queue,
.badge-proc-done {
    font-family: var(--font-family-mono);
    font-size: 0.82rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: var(--radius-sm);
}
.badge-proc-queue {
    background: rgba(59, 130, 246, 0.18);
    border: 1px solid #3b82f6;
    color: #bfdbfe;
}
.badge-proc-done {
    background: rgba(16, 185, 129, 0.18);
    border: 1px solid #10b981;
    color: #a7f3d0;
}

/* ==========================================================================
   SECTION LABELS
   ========================================================================== */
.section-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-muted);
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)



# -----------------------------------------------------------------------------
# CHART LAYOUT POLISH (fixes overlapping titles / legends / toolbar)
# -----------------------------------------------------------------------------
PLOT_CONFIG = {"displayModeBar": False}   # hide the floating toolbar that covers chart titles

SHORT_ALGO_LABELS = {
    "FCFS": "FCFS",
    "SJF (Non-Preemptive)": "SJF",
    "SRTF (Preemptive SJF)": "SRTF",
    "Priority (Non-Preemptive)": "Priority<br>(NP)",
    "Priority (Preemptive)": "Priority<br>(P)",
    "Round Robin": "Round<br>Robin",
    "Multilevel Queue (MLQ)": "MLQ",
    "Real-Time EDF (Earliest Deadline First)": "EDF",
    "Dual-Core SMP (Multiprocessor)": "Dual-Core<br>SMP",
}


def polish_gantt(fig):
    """Move the legend above the plot so it never collides with the x-axis title."""
    fig.update_layout(
        title_x=0, title_xanchor="left", title_y=0.97, title_yanchor="top",
        margin=dict(l=60, r=30, t=100, b=70),
        legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="left", x=0, title_text=""),
    )
    fig.update_xaxes(automargin=True, title_standoff=12)
    fig.update_yaxes(automargin=True)
    return fig


def polish_comparison(fig):
    """Left-align titles, shorten x labels, remove redundant axis titles, add headroom for bar values."""
    xs = list(fig.data[0].x) if len(fig.data) and fig.data[0].x is not None else []
    fig.update_layout(
        title_x=0, title_xanchor="left", title_font_size=16,
        margin=dict(l=40, r=20, t=70, b=70), height=380,
    )
    fig.update_xaxes(
        title_text=None, tickmode="array", tickvals=xs,
        ticktext=[SHORT_ALGO_LABELS.get(str(x), str(x)) for x in xs],
        tickangle=0, tickfont_size=11, automargin=True,
    )
    fig.update_yaxes(title_text=None, automargin=True)
    fig.update_traces(cliponaxis=False, selector=dict(type="bar"))
    ys = []
    for t in fig.data:
        if getattr(t, "y", None) is not None:
            ys += [float(v) for v in t.y if v is not None]
    if ys and max(ys) > 0:
        fig.update_yaxes(range=[0, max(ys) * 1.25])
    return fig


# -----------------------------------------------------------------------------
# SYSTEM HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="system-header">
    <div>
        <div class="system-title">⚡ CPU Scheduling Visualizer</div>
        <div class="system-subtitle">Deterministic Process Dispatch Simulator & Comparative Profiler</div>
    </div>
    <div>
        <div class="status-badge">
            <span class="status-dot"></span>
            <span>Telemetry Active</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# SIDEBAR: SCHEDULING CONFIGURATION
# -----------------------------------------------------------------------------
st.sidebar.markdown("### ⚙️ Scheduling Configuration", help="Configure the scheduling algorithm and parameters")

algorithm = st.sidebar.selectbox(
    "Algorithm Selection",
    [
        "FCFS",
        "SJF (Non-Preemptive)",
        "SRTF (Preemptive SJF)",
        "Priority (Non-Preemptive)",
        "Priority (Preemptive)",
        "Round Robin",
        "Multilevel Queue (MLQ)",
        "Real-Time EDF (Earliest Deadline First)",
        "Dual-Core SMP (Multiprocessor)",
        "Compare All Algorithms"
    ],
    key="selected_algorithm",
    help="Select the CPU scheduling algorithm to simulate"
)

# Priority Order Toggle
priority_convention = "Lower Number = Higher Priority"
if "Priority" in algorithm or algorithm == "Compare All Algorithms":
    priority_convention = st.sidebar.radio(
        "Priority Convention",
        ["Lower Number = Higher Priority", "Higher Number = Higher Priority"],
        index=0,
        help="Standard OS convention: 0 or 1 is highest priority. Lower number = higher priority is typical."
    )
lower_is_higher = (priority_convention == "Lower Number = Higher Priority")

# Time Quantum
quantum = 2
if algorithm in ["Round Robin", "Multilevel Queue (MLQ)", "Compare All Algorithms"]:
    quantum = st.sidebar.number_input(
        "Time Quantum (Q)",
        min_value=1,
        value=2,
        step=1,
        key="selected_quantum",
        help="Allocated CPU time slice per round for Round Robin and MLQ Foreground Queue."
    )

# Workload Presets
st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Preset Scenarios", help="Load predefined workload scenarios for demonstration")

preset_name = st.sidebar.selectbox(
    "Load Scenario",
    [
        "Standard Workload (P1-P4)",
        "Convoy Effect Demo (FCFS vs SJF)",
        "Preemption Showdown (SJF vs SRTF)",
        "Starvation & Priority Inversion Demo",
        "Round Robin Time Slicing Demo",
        "Real-Time Deadlines Demo (for EDF)",
        "Dual-Core SMP Parallelism Demo"
    ],
    key="preset_selection",
    help="Select a preset scenario or customize processes below"
)

PRESETS = {
    "Standard Workload (P1-P4)": pd.DataFrame({
        "Process": ["P1", "P2", "P3", "P4"],
        "Arrival Time": [0, 1, 2, 3],
        "Burst Time": [5, 3, 8, 6],
        "Priority": [2, 1, 3, 2],
        "Deadline": [10, 6, 25, 18]
    }),
    "Convoy Effect Demo (FCFS vs SJF)": pd.DataFrame({
        "Process": ["P1 (Heavy)", "P2 (Short)", "P3 (Short)", "P4 (Short)"],
        "Arrival Time": [0, 1, 2, 3],
        "Burst Time": [24, 3, 3, 2],
        "Priority": [3, 1, 2, 1],
        "Deadline": [30, 8, 12, 10]
    }),
    "Preemption Showdown (SJF vs SRTF)": pd.DataFrame({
        "Process": ["P1", "P2", "P3", "P4"],
        "Arrival Time": [0, 1, 2, 3],
        "Burst Time": [8, 4, 9, 5],
        "Priority": [2, 1, 4, 3],
        "Deadline": [16, 8, 28, 18]
    }),
    "Starvation & Priority Inversion Demo": pd.DataFrame({
        "Process": ["P1 (Low)", "P2 (High)", "P3 (High)", "P4 (Med)"],
        "Arrival Time": [0, 1, 2, 3],
        "Burst Time": [10, 3, 2, 4],
        "Priority": [4, 1, 1, 2],
        "Deadline": [25, 7, 8, 14]
    }),
    "Round Robin Time Slicing Demo": pd.DataFrame({
        "Process": ["P1", "P2", "P3"],
        "Arrival Time": [0, 0, 0],
        "Burst Time": [10, 4, 6],
        "Priority": [1, 2, 3],
        "Deadline": [22, 10, 16]
    }),
    "Real-Time Deadlines Demo (for EDF)": pd.DataFrame({
        "Process": ["Task A", "Task B", "Task C", "Task D"],
        "Arrival Time": [0, 1, 2, 4],
        "Burst Time": [4, 2, 6, 3],
        "Priority": [2, 1, 3, 2],
        "Deadline": [8, 5, 15, 9]
    }),
    "Dual-Core SMP Parallelism Demo": pd.DataFrame({
        "Process": ["P1", "P2", "P3", "P4", "P5", "P6"],
        "Arrival Time": [0, 0, 1, 2, 3, 4],
        "Burst Time": [6, 4, 7, 3, 5, 2],
        "Priority": [2, 1, 3, 1, 2, 1],
        "Deadline": [14, 8, 18, 9, 15, 8]
    })
}

if "last_preset" not in st.session_state or st.session_state["last_preset"] != preset_name:
    st.session_state["last_preset"] = preset_name
    st.session_state["current_table_data"] = PRESETS[preset_name].copy()

sidebar_run = st.sidebar.button("▶ Run Scheduling", key="sidebar_run_btn", type="primary", use_container_width=True)


# -----------------------------------------------------------------------------
# MAIN APP NAVIGATION TABS
# -----------------------------------------------------------------------------
tab_visualizer, tab_benchmark = st.tabs([
    "🖥️ Simulation & Telemetry",
    "🏆 Comparative Benchmark"
])


# -----------------------------------------------------------------------------
# WORKLOAD INPUT & ENGINE
# -----------------------------------------------------------------------------
with tab_visualizer:
    st.markdown("#### 📋 Process Workload Configuration")
    st.caption("Edit processes below, change arrival/burst/priority/deadline, or add new rows.")

    edited_data = st.data_editor(
        st.session_state.get("current_table_data", PRESETS["Standard Workload (P1-P4)"]),
        num_rows="dynamic",
        use_container_width=True,
        key="workload_editor",
        column_config={
            "Process": st.column_config.TextColumn("Process ID", required=True),
            "Arrival Time": st.column_config.NumberColumn("Arrival Time (AT)", min_value=0, step=1, required=True),
            "Burst Time": st.column_config.NumberColumn("Burst Time (BT)", min_value=1, step=1, required=True),
            "Priority": st.column_config.NumberColumn("Priority (PR)", min_value=0, step=1, required=True),
            "Deadline": st.column_config.NumberColumn("Deadline (DL - for EDF)", min_value=1, step=1, required=False)
        }
    )

    main_run = st.button("▶ Execute Simulation", key="main_run_btn", type="primary")

# Reset simulation scrubbers on algorithm change
if "last_seen_algo" not in st.session_state or st.session_state["last_seen_algo"] != algorithm:
    st.session_state["last_seen_algo"] = algorithm
    for k in list(st.session_state.keys()):
        if k.startswith("sim_time_") or k.startswith("slider_widget_"):
            st.session_state[k] = 0

has_validation_error = False
all_results = {}

try:
    if edited_data.empty:
        st.error("Validation Error: Workload table cannot be empty. Please enter at least one process.")
        has_validation_error = True
        st.stop()

    if edited_data.isnull().any().any():
        raise ValueError("All table fields must be populated. No null values allowed.")

    if edited_data["Process"].duplicated().any():
        raise ValueError("Process identifiers must be strictly unique.")

    for column in ["Arrival Time", "Burst Time", "Priority"]:
        values = pd.to_numeric(edited_data[column], errors="raise")
        if (values < 0).any():
            raise ValueError(f"{column} cannot contain negative values.")
        if not (values % 1 == 0).all():
            raise ValueError(f"{column} must contain integer values.")

    if (pd.to_numeric(edited_data["Burst Time"]) <= 0).any():
        raise ValueError("Burst Time must be strictly greater than zero.")

    processes = []
    for _, row in edited_data.iterrows():
        p_dict = {
            "id": str(row["Process"]),
            "arrival": int(row["Arrival Time"]),
            "burst": int(row["Burst Time"]),
            "priority": int(row["Priority"])
        }
        if "Deadline" in row and pd.notnull(row["Deadline"]):
            p_dict["deadline"] = int(row["Deadline"])
        else:
            p_dict["deadline"] = int(row["Arrival Time"]) + int(row["Burst Time"]) * 2
        processes.append(p_dict)

    algorithms_map = {
        "FCFS": lambda: fcfs(processes),
        "SJF (Non-Preemptive)": lambda: sjf(processes),
        "SRTF (Preemptive SJF)": lambda: srtf(processes),
        "Priority (Non-Preemptive)": lambda: priority_scheduling(processes, lower_is_higher=lower_is_higher),
        "Priority (Preemptive)": lambda: priority_preemptive(processes, lower_is_higher=lower_is_higher),
        "Round Robin": lambda: round_robin(processes, quantum),
        "Multilevel Queue (MLQ)": lambda: multilevel_queue(processes, quantum),
        "Real-Time EDF (Earliest Deadline First)": lambda: edf(processes),
        "Dual-Core SMP (Multiprocessor)": lambda: multiprocessor_scheduling(processes, 2)
    }

    if algorithm == "Compare All Algorithms":
        selected_algorithms = list(algorithms_map.keys())
    else:
        selected_algorithms = [algorithm]

    for name in selected_algorithms:
        results, gantt = algorithms_map[name]()
        averages = calculate_averages(results, gantt)
        all_results[name] = {
            "results": results,
            "gantt": gantt,
            "averages": averages
        }

except Exception as e:
    st.error(f"Execution Error: {e}")
    has_validation_error = True


# -----------------------------------------------------------------------------
# TAB 1: SIMULATION & TELEMETRY DASHBOARD
# -----------------------------------------------------------------------------
with tab_visualizer:
    if not has_validation_error:
        st.markdown("---")

        display_algos = (
            [selected_algorithms[0]]
            if algorithm != "Compare All Algorithms"
            else list(all_results.keys())
        )

        for name in display_algos:
            data = all_results[name]
            results = data["results"]
            gantt = data["gantt"]
            averages = data["averages"]

            st.markdown(f"### 📊 {name} Performance Report")

            # 5 Standard Scheduling Criteria Telemetry Cards
            m1, m2, m3, m4, m5 = st.columns(5)

            with m1:
                st.markdown(f"""
                <div class="telemetry-card" style="border-left-color: #2563eb;">
                    <div class="telemetry-label">Average Waiting Time</div>
                    <div class="telemetry-value">{averages['Average Waiting Time']} <span style="font-size: 0.8rem; font-weight: normal; color: var(--neutral-400);">ms</span></div>
                    <div class="telemetry-sub">Mean queue waiting latency</div>
                </div>
                """, unsafe_allow_html=True)

            with m2:
                st.markdown(f"""
                <div class="telemetry-card" style="border-left-color: #059669;">
                    <div class="telemetry-label">Average Turnaround Time</div>
                    <div class="telemetry-value">{averages['Average Turnaround Time']} <span style="font-size: 0.8rem; font-weight: normal; color: var(--neutral-400);">ms</span></div>
                    <div class="telemetry-sub">Mean completion turnaround</div>
                </div>
                """, unsafe_allow_html=True)

            with m3:
                st.markdown(f"""
                <div class="telemetry-card" style="border-left-color: #d97706;">
                    <div class="telemetry-label">Average Response Time</div>
                    <div class="telemetry-value">{averages['Average Response Time']} <span style="font-size: 0.8rem; font-weight: normal; color: var(--neutral-400);">ms</span></div>
                    <div class="telemetry-sub">Mean initial dispatch delay</div>
                </div>
                """, unsafe_allow_html=True)

            with m4:
                st.markdown(f"""
                <div class="telemetry-card" style="border-left-color: #7c3aed;">
                    <div class="telemetry-label">CPU Utilization</div>
                    <div class="telemetry-value">{averages['CPU Utilization (%)']}%</div>
                    <div class="telemetry-sub">Active processor efficiency</div>
                </div>
                """, unsafe_allow_html=True)

            with m5:
                st.markdown(f"""
                <div class="telemetry-card" style="border-left-color: #0891b2;">
                    <div class="telemetry-label">Throughput & Switches</div>
                    <div class="telemetry-value">{averages['Throughput']} <span style="font-size: 0.75rem; font-weight: normal; color: var(--neutral-400);">p/ms</span></div>
                    <div class="telemetry-sub">{averages['Context Switches']} context switches</div>
                </div>
                """, unsafe_allow_html=True)

            # Gantt Timeline Chart
            st.markdown("##### ⏱️ Execution Timeline (Gantt Chart)")
            fig = polish_gantt(create_gantt_chart(gantt, f"{name} Dispatch Schedule"))
            st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

            # Interactive Step Simulation
            with st.expander(f"🔍 Step-by-Step Dispatch Simulation & Ready Queue ({name})", expanded=True):
                makespan = averages["Total Execution Time"]

                sim_key = f"sim_time_{name}"
                if sim_key not in st.session_state or st.session_state[sim_key] > makespan:
                    st.session_state[sim_key] = 0

                # Control buttons with improved styling
                ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4, ctrl_col5 = st.columns([1, 1, 1, 1, 2.5])

                with ctrl_col1:
                    if st.button("Reset (t=0)", key=f"btn_rst_{name}", use_container_width=True):
                        st.session_state[sim_key] = 0
                        st.rerun()

                with ctrl_col2:
                    if st.button("◀ Prev Step", key=f"btn_prev_{name}", use_container_width=True):
                        st.session_state[sim_key] = max(0, st.session_state[sim_key] - 1)
                        st.rerun()

                with ctrl_col3:
                    if st.button("Next Step ▶", key=f"btn_nxt_{name}", use_container_width=True):
                        st.session_state[sim_key] = min(makespan, st.session_state[sim_key] + 1)
                        st.rerun()

                with ctrl_col4:
                    if st.button("End (t=Max)", key=f"btn_end_{name}", use_container_width=True):
                        st.session_state[sim_key] = makespan
                        st.rerun()

                # Progress display
                with ctrl_col5:
                    curr_t = st.session_state[sim_key]
                    pct = int((curr_t / makespan * 100)) if makespan > 0 else 100
                    st.progress(pct / 100, text=f"Dispatch Progress: {pct}% (t = {curr_t} / {makespan} ms)")

                # Time scrubber
                t_val = st.slider(
                    "Clock Time Scrubber (t)",
                    min_value=0,
                    max_value=makespan,
                    step=1,
                    key=sim_key
                )
                snap = get_simulation_snapshot(processes, gantt, t_val)

                # Telemetry State Displays with professional cards
                c_core, c_queue, c_done = st.columns([1.5, 2, 1.8])

                with c_core:
                    st.markdown('<div class="section-label">CPU Dispatch Core</div>', unsafe_allow_html=True)
                    curr_exec = snap["running_process"]
                    if curr_exec == "Finished":
                        st.markdown("""
                        <div class="dispatch-core-box" style="border-color: var(--brand-success);">
                            <div class="dispatch-header" style="color: var(--status-active);">Execution Complete</div>
                            <div class="dispatch-proc" style="color: var(--status-active);">IDLE</div>
                            <div class="dispatch-sub">All tasks terminated</div>
                        </div>
                        """, unsafe_allow_html=True)
                    elif curr_exec == "Idle":
                        st.markdown("""
                        <div class="dispatch-core-box" style="border-color: var(--neutral-500);">
                            <div class="dispatch-header" style="color: var(--neutral-400);">Processor Idle</div>
                            <div class="dispatch-proc" style="color: var(--neutral-400);">NO TASK</div>
                            <div class="dispatch-sub">Awaiting process arrival</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="dispatch-core-box">
                            <div class="dispatch-header">Active Execution</div>
                            <div class="dispatch-proc">{curr_exec}</div>
                            <div class="dispatch-sub">Active at clock cycle t = {t_val}</div>
                        </div>
                        """, unsafe_allow_html=True)

                with c_queue:
                    st.markdown('<div class="section-label">Ready Queue (Memory / RAM)</div>', unsafe_allow_html=True)
                    rq = snap["ready_queue"]
                    if rq:
                        chips_html = "".join([f'<span class="badge-proc-queue">{p}</span>' for p in rq])
                        st.markdown(f'<div class="queue-panel">{chips_html}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="queue-panel"><span class="empty-tray-msg">Ready queue empty (no waiting processes)</span></div>', unsafe_allow_html=True)

                with c_done:
                    st.markdown('<div class="section-label">Terminated Processes</div>', unsafe_allow_html=True)
                    done = snap["completed"]
                    if done:
                        chips_html = "".join([f'<span class="badge-proc-done">{p}</span>' for p in done])
                        st.markdown(f'<div class="queue-panel">{chips_html}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="queue-panel"><span class="empty-tray-msg">No processes terminated yet</span></div>', unsafe_allow_html=True)

                st.write("")
                st.markdown('<div class="section-label">5-State Process Model Inspection Table</div>', unsafe_allow_html=True)
                snap_df = pd.DataFrame(snap["process_states"])[["Process", "Arrival", "Total Burst", "Executed", "Remaining", "Status"]]
                st.dataframe(snap_df, use_container_width=True, hide_index=True)

            # Performance Data Table
            st.markdown("##### 📑 Process Performance Summary Table")
            result_df = pd.DataFrame(results)
            st.dataframe(
                result_df,
                use_container_width=True,
                hide_index=True
            )

            # CSV Download - Enhanced with summary
            csv_data = result_df.to_csv(index=False).encode('utf-8')

            # Add summary information
            averages = data["averages"]
            summary_lines = [
                f"Scheduling Algorithm: {name}",
                f"Number of Processes: {len(results)}",
                f"",
                "Performance Metrics:",
                f"  • Average Waiting Time: {averages['Average Waiting Time']} ms",
                f"  • Average Turnaround Time: {averages['Average Turnaround Time']} ms",
                f"  • Average Response Time: {averages['Average Response Time']} ms",
                f"  • CPU Utilization: {averages['CPU Utilization (%)']}%",
                f"  • Throughput: {averages['Throughput']} processes/ms",
                f"  • Context Switches: {averages['Context Switches']}",
                f"  • Total Execution Time: {averages['Total Execution Time']} ms",
                f"",
                f"Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            ]
            full_csv = ("\n".join(summary_lines) + "\n" + csv_data.decode('utf-8')).encode('utf-8')

            st.download_button(
                label=f"📥 Export {name} Report as CSV",
                data=full_csv,
                file_name=f"{name.replace(' ', '_')}_scheduling_report.csv",
                mime='text/csv',
                help="Download scheduling results and performance summary as CSV"
            )
            # Show summary preview
            with st.expander("📊 View Performance Summary", expanded=False):
                st.markdown(f"""
                <div class="telemetry-card" style="border-left-color: var(--brand-accent); padding: 12px;">
                    <div class="telemetry-label">Performance Summary for {name}</div>
                    <div style="font-size: 0.875rem; margin-top: 8px;">
                        <div>Processes: {len(results)}</div>
                        <div>Avg Waiting Time: {averages['Average Waiting Time']} ms</div>
                        <div>Avg Turnaround Time: {averages['Average Turnaround Time']} ms</div>
                        <div>Avg Response Time: {averages['Average Response Time']} ms</div>
                        <div>CPU Utilization: {averages['CPU Utilization (%)']}%</div>
                        <div>Throughput: {averages['Throughput']} p/ms</div>
                        <div>Context Switches: {averages['Context Switches']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")


# -----------------------------------------------------------------------------
# TAB 2: COMPARATIVE BENCHMARK SUITE ("COMPARE ALL")
# -----------------------------------------------------------------------------
with tab_benchmark:
    st.markdown("### 🏆 Comprehensive Multi-Algorithm Benchmark")
    st.caption("Side-by-side performance profiling across all 5 scheduling criteria.")

    if not has_validation_error:
        bench_results = {}
        for algo_name, algo_fn in algorithms_map.items():
            res, g = algo_fn()
            avg = calculate_averages(res, g)
            bench_results[algo_name] = {
                "results": res,
                "gantt": g,
                "averages": avg
            }

        comparison = []
        for name, data in bench_results.items():
            comparison.append({
                "Algorithm": name,
                **data["averages"]
            })

        comparison_df = pd.DataFrame(comparison)

        # Find best performers (excluding dual-core for single-core fairness)
        single_core_df = comparison_df[~comparison_df["Algorithm"].str.contains("Dual-Core")]
        best_wt = single_core_df.loc[single_core_df["Average Waiting Time"].idxmin()]
        best_tat = single_core_df.loc[single_core_df["Average Turnaround Time"].idxmin()]
        best_util = single_core_df.loc[single_core_df["CPU Utilization (%)"].idxmax()]

        # Enhanced metric cards with themed styling
        metric_cols = st.columns(3)
        with metric_cols[0]:
            st.markdown(f"""
            <div class="telemetry-card telemetry-card-accent">
                <div class="telemetry-label">Optimal Waiting Time Leader</div>
                <div class="telemetry-value" style="color: var(--brand-accent);">{best_wt['Algorithm']}</div>
                <div class="telemetry-sub">Lowest AWT: {best_wt['Average Waiting Time']} ms</div>
            </div>
            """, unsafe_allow_html=True)

        with metric_cols[1]:
            st.markdown(f"""
            <div class="telemetry-card telemetry-card-success">
                <div class="telemetry-label">Optimal Turnaround Leader</div>
                <div class="telemetry-value" style="color: var(--brand-success);">{best_tat['Algorithm']}</div>
                <div class="telemetry-sub">Lowest ATAT: {best_tat['Average Turnaround Time']} ms</div>
            </div>
            """, unsafe_allow_html=True)

        with metric_cols[2]:
            st.markdown(f"""
            <div class="telemetry-card telemetry-card-info">
                <div class="telemetry-label">Peak CPU Utilization</div>
                <div class="telemetry-value" style="color: var(--brand-info);">{best_util['Algorithm']}</div>
                <div class="telemetry-sub">Max Efficiency: {best_util['CPU Utilization (%)']}%</div>
            </div>
            """, unsafe_allow_html=True)

        # Styled comparison table
        st.markdown("##### 📊 Comparative Benchmark Matrix")
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)

        # Enhanced comparative visualization charts
        c_chart1, c_chart2 = st.columns(2)
        with c_chart1:
            fig_wt = polish_comparison(create_comparison_chart(bench_results, "Average Waiting Time"))
            st.plotly_chart(fig_wt, use_container_width=True, config=PLOT_CONFIG)

        with c_chart2:
            fig_tat = polish_comparison(create_comparison_chart(bench_results, "Average Turnaround Time"))
            st.plotly_chart(fig_tat, use_container_width=True, config=PLOT_CONFIG)

        c_chart3, c_chart4 = st.columns(2)
        with c_chart3:
            fig_util = polish_comparison(create_comparison_chart(bench_results, "CPU Utilization (%)"))
            st.plotly_chart(fig_util, use_container_width=True, config=PLOT_CONFIG)

        with c_chart4:
            fig_tput = polish_comparison(create_comparison_chart(bench_results, "Throughput"))
            st.plotly_chart(fig_tput, use_container_width=True, config=PLOT_CONFIG)