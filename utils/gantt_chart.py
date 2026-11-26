import pandas as pd
import plotly.graph_objects as go

# Modern enterprise telemetry color palette
PROCESS_COLORS = [
    "#2563EB",  # Deep Blue
    "#059669",  # Emerald Green
    "#D97706",  # Amber
    "#7C3AED",  # Purple
    "#0891B2",  # Cyan
    "#EA580C",  # Burnt Orange
    "#4F46E5",  # Indigo
    "#DB2777",  # Deep Pink
    "#10B981",  # Mint
    "#6366F1",  # Light Indigo
]

IDLE_COLOR = "#475569"  # Slate grey for Idle


def get_process_color_map(processes):
    color_map = {}
    idx = 0
    for p in processes:
        if p == "Idle":
            color_map[p] = IDLE_COLOR
        elif p not in color_map:
            color_map[p] = PROCESS_COLORS[idx % len(PROCESS_COLORS)]
            idx += 1
    color_map["Idle"] = IDLE_COLOR
    return color_map


def create_gantt_chart(gantt, title="CPU Execution Timeline"):
    if not gantt:
        raise ValueError("No Gantt chart data available.")

    unique_procs = []
    for item in gantt:
        p = item["process"]
        if p not in unique_procs:
            unique_procs.append(p)

    color_map = get_process_color_map(unique_procs)
    max_time = max(item["end"] for item in gantt)
    min_time = min(item["start"] for item in gantt)
    total_span = max(1, max_time - min_time)

    # Detect cores
    cores = []
    for item in gantt:
        c = item.get("core", "CPU Core 0")
        if c not in cores:
            cores.append(c)
    cores.sort()

    fig = go.Figure()
    seen_in_legend = set()

    for item in gantt:
        pid = item["process"]
        duration = item["end"] - item["start"]
        is_idle = pid == "Idle"
        label = "IDLE" if is_idle else pid
        core_label = item.get("core", "CPU Core 0")

        show_leg = pid not in seen_in_legend
        seen_in_legend.add(pid)

        # Show interval text if bar is wide enough
        if duration >= max(1, total_span * 0.04):
            text_display = f"<b>{label}</b><br>[{item['start']} - {item['end']}]"
        else:
            text_display = f"<b>{label}</b>"

        fig.add_trace(go.Bar(
            x=[duration],
            y=[core_label],
            base=[item["start"]],
            orientation="h",
            name=label,
            legendgroup=pid,
            showlegend=show_leg,
            marker=dict(
                color=color_map.get(pid, "#475569"),
                line=dict(color="#0F172A", width=1.5)
            ),
            text=text_display,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="#FFFFFF", size=11, family="monospace"),
            hovertemplate=(
                f"<b>Process:</b> {label}<br>"
                f"<b>Core:</b> {core_label}<br>"
                f"<b>Dispatch:</b> t = {item['start']}<br>"
                f"<b>Completion:</b> t = {item['end']}<br>"
                f"<b>Span:</b> {duration} time units<extra></extra>"
            )
        ))

    dtick = 1 if total_span <= 30 else (2 if total_span <= 60 else 5)

    chart_height = 230 if len(cores) <= 1 else (150 * len(cores) + 80)

    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=15, family="sans-serif"),
            x=0.01,
            y=0.95
        ),
        barmode="stack",
        xaxis=dict(
            title="<b>Timeline (Time Units)</b>",
            dtick=dtick,
            range=[min_time - 0.2, max_time + 0.5],
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.2)",
            zeroline=True,
            zerolinecolor="rgba(148, 163, 184, 0.35)"
        ),
        yaxis=dict(
            title="<b>Processor Core</b>" if len(cores) > 1 else "",
            showticklabels=(len(cores) > 1),
            showgrid=False,
            autorange="reversed"
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.42 if len(cores) <= 1 else -0.25,
            xanchor="center",
            x=0.5
        ),
        height=chart_height,
        margin=dict(l=20, r=20, t=40, b=55)
    )

    return fig


def create_comparison_chart(all_results, metric="Average Waiting Time"):
    algorithms = list(all_results.keys())
    values = [all_results[alg]["averages"].get(metric, 0) for alg in algorithms]

    # For waiting, turnaround, response: lower is better. For utilization, throughput: higher is better.
    higher_is_better = metric in ["CPU Utilization (%)", "Throughput"]
    best_val = max(values) if higher_is_better else (min(values) if values else 0)

    colors = []
    for val in values:
        if val == best_val and val > 0:
            colors.append("#059669")  # Optimal in Emerald
        else:
            colors.append("#2563EB")  # Others in Blue

    fig = go.Figure(go.Bar(
        x=algorithms,
        y=values,
        marker=dict(
            color=colors,
            line=dict(color="#0F172A", width=1.5)
        ),
        text=[f"<b>{v}</b>" for v in values],
        textposition="outside"
    ))

    fig.update_layout(
        title=dict(
            text=f"<b>{metric} Comparison</b>",
            font=dict(size=15)
        ),
        xaxis=dict(title="<b>Algorithm</b>"),
        yaxis=dict(
            title=f"<b>{metric}</b>",
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.2)"
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=25, r=25, t=45, b=45)
    )

    return fig
