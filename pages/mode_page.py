import streamlit as st
import pandas as pd
import plotly.express as px

from data_utils import load_data

runs, batches, changes, downtime = load_data()


# ============================================================
# LOCAL HELPERS
# ============================================================
def ensure_datetime(df, col):
    if df is not None and col in df.columns:
        df = df.copy()
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def apply_dashboard_style():
    st.markdown("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&display=swap');

      :root {
        --blue:       #1E90FF;
        --blue-dk:    #1270cc;
        --blue-lt:    #dbeeff;
        --blue-md:    #93c5fd;

        --bg:         #e8edf5;
        --surface:    #f4f7fb;
        --surface2:   #edf1f8;
        --sidebar-bg: #1a2744;

        --border:     #d0d8e8;
        --border-strong: #b8c4d8;

        --emerald:    #059669;
        --emerald-lt: #d1fae5;
        --rose:       #dc2626;
        --rose-lt:    #fee2e2;

        --ink:        #0f1d35;
        --ink-mid:    #2d3f5e;
        --ink-soft:   #4e6080;
        --ink-faint:  #7a90b0;
      }

      html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background: var(--bg) !important;
        color: var(--ink) !important;
        font-family: 'Inter', sans-serif !important;
      }

      [data-testid="stHeader"] {
        background: transparent !important;
        box-shadow: none !important;
      }

      .block-container {
        padding-top: 1rem;
        padding-bottom: 1.5rem;
        padding-left: 1.4rem;
        padding-right: 1.4rem;
      }

      section[data-testid="stSidebar"] {
        background: var(--sidebar-bg) !important;
      }

      section[data-testid="stSidebar"] * {
        color: #c8d8f0 !important;
      }

      [data-testid="stSidebar"] h2,
      [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
      }

      [data-testid="stSidebar"] [data-testid="stSelectbox"] label {
        color: #7a9fc8 !important;
        font-size: 0.68rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
      }

      [data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
        background: #1e2f55 !important;
        border: 1px solid #2e4070 !important;
        border-radius: 8px !important;
        color: #e0eaf8 !important;
        font-size: 0.85rem !important;
      }

      [data-testid="stDataFrame"] {
        background: var(--surface) !important;
        border-radius: 10px !important;
        border: 1px solid var(--border) !important;
        overflow: hidden;
      }

      [data-testid="stDataFrame"] th {
        background: var(--sidebar-bg) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.75rem !important;
      }

      [data-testid="stDataFrame"] td {
        color: var(--ink) !important;
      }

      h1, h2, h3 {
        letter-spacing: -0.02em;
        color: var(--ink) !important;
      }

      .page-header {
        background: var(--sidebar-bg);
        border-radius: 14px;
        padding: 26px 32px;
        margin-bottom: 22px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 16px rgba(15,29,53,0.12);
      }

      .page-header-left {
        display: flex;
        flex-direction: column;
        gap: 8px;
      }

      .page-header h1 {
        font-family: 'Inter', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        margin: 0 !important;
        letter-spacing: -0.03em !important;
        line-height: 1.1 !important;
      }

      .page-header h1 span {
        color: var(--blue) !important;
      }

      .page-header .subtitle {
        font-size: 1rem !important;
        color: #b8cce8 !important;
        margin: 0 !important;
        font-weight: 400 !important;
      }

      .page-header-right {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 6px;
      }

      .header-badge {
        background: var(--blue) !important;
        color: #ffffff !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        padding: 5px 14px !important;
        border-radius: 20px !important;
        letter-spacing: 0.06em !important;
      }

      .header-meta {
        font-family: 'DM Mono', monospace !important;
        font-size: 0.75rem !important;
        color: #b8cce8 !important;
      }

      .section-title {
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        color: var(--ink) !important;
        margin-bottom: 14px !important;
        padding-bottom: 8px !important;
        border-bottom: 3px solid var(--blue) !important;
        display: inline-block !important;
      }

      .kpi-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-left: 5px solid var(--blue);
        border-radius: 10px;
        padding: 18px 22px;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(15,29,53,0.06);
      }

      .kpi-label {
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        color: var(--ink-soft) !important;
        margin-bottom: 7px !important;
      }

      .kpi-value {
        font-family: 'DM Mono', monospace !important;
        font-size: 1.75rem !important;
        font-weight: 500 !important;
        color: var(--ink) !important;
        line-height: 1.2 !important;
      }

      .kpi-delta {
        font-family: 'DM Mono', monospace !important;
        font-size: 0.72rem !important;
        margin-top: 6px !important;
      }

      .kpi-delta.up { color: var(--emerald); }
      .kpi-delta.down { color: var(--rose); }
      .kpi-delta.neu { color: var(--ink-faint); }

      .info-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 16px 18px;
        box-shadow: 0 2px 6px rgba(15,29,53,0.05);
      }

      .info-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--ink-soft);
        margin-bottom: 8px;
      }

      .info-value {
        font-size: 0.96rem;
        color: var(--ink);
        margin-bottom: 8px;
        font-weight: 600;
      }

      .insight-tag {
        display: inline-block;
        background: var(--blue-lt);
        border: 1.5px solid var(--blue-md);
        color: var(--blue-dk);
        font-size: 0.78rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 100px;
        margin: 3px 3px 3px 0;
      }

      .mode-card {
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 12px;
        background-color: var(--surface);
      }

      .mode-card-title {
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 6px;
        color: var(--ink);
      }

      .mode-card-meta {
        font-size: 13px;
        color: var(--ink-soft);
      }

      hr {
        border-color: var(--border) !important;
        margin: 1.4rem 0 !important;
      }
    </style>
    """, unsafe_allow_html=True)


def section_title(title: str):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def kpi_html(label, value, delta="", direction="neu"):
    delta_html = f'<div class="kpi-delta {direction}">{delta}</div>' if delta else ""
    return f"""
    <div class="kpi-card">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      {delta_html}
    </div>
    """


def summarize_boundaries(series):
    vals = pd.to_numeric(series, errors="coerce").dropna().tolist()
    vals = sorted(set(vals))
    if not vals:
        return "", ""

    def fmt(v):
        return str(int(v)) if float(v).is_integer() else str(v)

    top_3 = ", ".join(fmt(v) for v in vals[:3])
    all_vals = ", ".join(fmt(v) for v in vals)
    return top_3, all_vals


BLUE = "#1E90FF"
AMBER = "#d97706"
EMERALD = "#059669"
ROSE = "#dc2626"
NAVY = "#1a2744"
COLOR_SEQ = [BLUE, NAVY, EMERALD, AMBER, ROSE, "#7c3aed", "#0891b2", "#db2777"]

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#f4f7fb",
    font=dict(family="Inter, sans-serif", color="#4e6080", size=12),
    title_font=dict(family="Inter, sans-serif", color="#0f1d35", size=14),
    xaxis=dict(gridcolor="#d0d8e8", linecolor="#d0d8e8", tickfont=dict(size=11), tickcolor="#7a90b0"),
    yaxis=dict(gridcolor="#d0d8e8", linecolor="#d0d8e8", tickfont=dict(size=11), tickcolor="#7a90b0"),
    margin=dict(l=20, r=20, t=44, b=20),
    hovermode="x unified",
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11, color="#2d3f5e")),
)


def apply_plot_theme(fig, height=320):
    fig.update_layout(**PLOT_LAYOUT, height=height)
    return fig


# ============================================================
# PREP
# ============================================================
runs = ensure_datetime(runs, "run_date")
apply_dashboard_style()

st.markdown(
    """
    <div class="page-header">
      <div class="page-header-left">
        <h1>⚙️ Mode <span>Boundary Analysis</span></h1>
        <p class="subtitle">Operator workflow · adjustment reference · grower completion</p>
      </div>
      <div class="page-header-right">
        <span class="header-badge">MODE WORKFLOW</span>
        <span class="header-meta">Grower-specific checking with variety/version reference</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if changes is None:
    st.info("changes_raw.csv not found.")
    st.stop()

mode_df = changes.copy()
runs_df = runs.copy()
batches_df = batches.copy() if batches is not None else None

# ============================================================
# JOIN DATA
# ============================================================
if "run_id" in mode_df.columns and "run_id" in runs_df.columns:
    join_cols = [c for c in ["run_id", "batch_id", "grower", "variety", "run_date"] if c in runs_df.columns]
    mode_df = mode_df.merge(
        runs_df[join_cols],
        on="run_id",
        how="left",
        suffixes=("", "_run")
    )

if batches_df is not None and "batch_id" in mode_df.columns and "batch_id" in batches_df.columns:
    batch_link_cols = [
        c for c in ["batch_id", "grower", "variety", "decfile_version", "defect_1", "defect_2", "defect_3"]
        if c in batches_df.columns
    ]
    mode_df = mode_df.merge(
        batches_df[batch_link_cols],
        on="batch_id",
        how="left",
        suffixes=("", "_batch")
    )

# ============================================================
# CLEAN
# ============================================================
for col in [
    "grower", "variety", "decfile_version", "mode", "check_class",
    "reason", "action", "sensitivity", "accuracy"
]:
    if col in mode_df.columns:
        mode_df[col] = (
            mode_df[col]
            .fillna("")
            .astype(str)
            .str.strip()
            .replace("", pd.NA)
        )

for col in ["boundary_before", "boundary_after"]:
    if col in mode_df.columns:
        mode_df[col] = pd.to_numeric(mode_df[col], errors="coerce")

if batches_df is not None:
    for col in ["grower", "variety", "decfile_version", "defect_1", "defect_2", "defect_3"]:
        if col in batches_df.columns:
            batches_df[col] = (
                batches_df[col]
                .fillna("")
                .astype(str)
                .str.strip()
                .replace("", pd.NA)
            )

# ============================================================
# SIDEBAR FILTERS — V3 STYLE
# ============================================================
with st.sidebar:
    st.markdown("### ⚙️ Mode")
    st.markdown("#### Filters")

    available_varieties = ["All varieties"]
    if "variety" in mode_df.columns:
        available_varieties += sorted(mode_df["variety"].dropna().astype(str).unique().tolist())

    selected_mode_variety = st.selectbox(
        "Variety",
        available_varieties,
        key="mode_variety_selector"
    )

    mode_temp = mode_df.copy()
    if selected_mode_variety != "All varieties" and "variety" in mode_temp.columns:
        mode_temp = mode_temp[mode_temp["variety"].astype(str) == selected_mode_variety]

    available_growers = ["All growers"]
    if "grower" in mode_temp.columns:
        available_growers += sorted(mode_temp["grower"].dropna().astype(str).unique().tolist())

    selected_mode_grower = st.selectbox(
        "Grower",
        available_growers,
        key="mode_grower_selector"
    )

    if selected_mode_grower != "All growers" and "grower" in mode_temp.columns:
        mode_temp = mode_temp[mode_temp["grower"].astype(str) == selected_mode_grower]

    available_versions = ["All versions"]
    if "decfile_version" in mode_temp.columns:
        available_versions += sorted(mode_temp["decfile_version"].dropna().astype(str).unique().tolist())

    selected_version = st.selectbox(
        "Dec File Version",
        available_versions,
        key="mode_version_selector"
    )

# ============================================================
# EXACT SELECTION + REFERENCE POOL
# ============================================================
filtered_mode = mode_df.copy()
if selected_mode_variety != "All varieties" and "variety" in filtered_mode.columns:
    filtered_mode = filtered_mode[filtered_mode["variety"].astype(str) == selected_mode_variety]
if selected_mode_grower != "All growers" and "grower" in filtered_mode.columns:
    filtered_mode = filtered_mode[filtered_mode["grower"].astype(str) == selected_mode_grower]
if selected_version != "All versions" and "decfile_version" in filtered_mode.columns:
    filtered_mode = filtered_mode[filtered_mode["decfile_version"].astype(str) == selected_version]

variety_pool = mode_df.copy()
if selected_mode_variety != "All varieties" and "variety" in variety_pool.columns:
    variety_pool = variety_pool[variety_pool["variety"].astype(str) == selected_mode_variety]
if selected_version != "All versions" and "decfile_version" in variety_pool.columns:
    variety_pool = variety_pool[variety_pool["decfile_version"].astype(str) == selected_version]

# ============================================================
# KPI OVERVIEW
# ============================================================
total_changes = len(filtered_mode)
adjustments_count = 0
checks_count = 0
unique_modes = filtered_mode["mode"].dropna().nunique() if "mode" in filtered_mode.columns else 0

if "action" in filtered_mode.columns:
    adjustments_count = filtered_mode["action"].astype(str).str.lower().str.startswith("a").sum()
    checks_count = filtered_mode["action"].astype(str).str.lower().str.startswith("c").sum()

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(kpi_html("Total Changes", f"{total_changes:,}"), unsafe_allow_html=True)
with k2:
    st.markdown(kpi_html("Adjustments", f"{adjustments_count:,}", "boundary changed"), unsafe_allow_html=True)
with k3:
    st.markdown(kpi_html("Checks", f"{checks_count:,}", "boundary verified"), unsafe_allow_html=True)
with k4:
    st.markdown(kpi_html("Unique Modes", f"{unique_modes:,}"), unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# CURRENT SELECTION + TOP DEFECTS
# ============================================================
top_l, top_r = st.columns([1.15, 0.85])

with top_l:
    section_title("Current Selection")

    top_defect_tags = []
    if batches_df is not None:
        batch_sel = batches_df.copy()

        if selected_mode_variety != "All varieties" and "variety" in batch_sel.columns:
            batch_sel = batch_sel[batch_sel["variety"].astype(str) == selected_mode_variety]
        if selected_mode_grower != "All growers" and "grower" in batch_sel.columns:
            batch_sel = batch_sel[batch_sel["grower"].astype(str) == selected_mode_grower]
        if selected_version != "All versions" and "decfile_version" in batch_sel.columns:
            batch_sel = batch_sel[batch_sel["decfile_version"].astype(str) == selected_version]

        defect_cols = [c for c in ["defect_1", "defect_2", "defect_3"] if c in batch_sel.columns]
        if defect_cols:
            defects = batch_sel[defect_cols].melt(value_name="defect")["defect"].dropna().astype(str).str.strip()
            defects = defects[defects != ""]
            if not defects.empty:
                top_defect_tags = defects.value_counts().head(8).index.tolist()

    grower_text = selected_mode_grower if selected_mode_grower != "All growers" else "All growers"
    variety_text = selected_mode_variety if selected_mode_variety != "All varieties" else "All varieties"
    version_text = selected_version if selected_version != "All versions" else "All versions"

    tags_html = "".join([f'<span class="insight-tag">{t}</span>' for t in top_defect_tags]) if top_defect_tags else '<span class="insight-tag">No defects recorded</span>'

    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-label">Variety</div>
            <div class="info-value">{variety_text}</div>

            <div class="info-label">Grower</div>
            <div class="info-value">{grower_text}</div>

            <div class="info-label">Dec File Version</div>
            <div class="info-value">{version_text}</div>

            <div class="info-label">Main Recorded Defects</div>
            <div>{tags_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_r:
    section_title("Top Defects for Selection")

    top_defects_mode = pd.DataFrame(columns=["Defect", "Count"])

    if batches_df is not None:
        batch_sel = batches_df.copy()

        if selected_mode_variety != "All varieties" and "variety" in batch_sel.columns:
            batch_sel = batch_sel[batch_sel["variety"].astype(str) == selected_mode_variety]
        if selected_mode_grower != "All growers" and "grower" in batch_sel.columns:
            batch_sel = batch_sel[batch_sel["grower"].astype(str) == selected_mode_grower]
        if selected_version != "All versions" and "decfile_version" in batch_sel.columns:
            batch_sel = batch_sel[batch_sel["decfile_version"].astype(str) == selected_version]

        defect_cols = [c for c in ["defect_1", "defect_2", "defect_3"] if c in batch_sel.columns]
        if defect_cols:
            mode_defects = (
                batch_sel[defect_cols]
                .melt(value_name="defect")["defect"]
                .dropna()
                .astype(str)
                .str.strip()
            )
            mode_defects = mode_defects[mode_defects != ""]
            if not mode_defects.empty:
                top_defects_mode = mode_defects.value_counts().reset_index()
                top_defects_mode.columns = ["Defect", "Count"]

    if not top_defects_mode.empty:
        fig_def = px.bar(
            top_defects_mode.head(8),
            x="Count",
            y="Defect",
            orientation="h",
            color_discrete_sequence=[ROSE]
        )
        fig_def.update_traces(hovertemplate="%{y}: %{x}<extra></extra>")
        apply_plot_theme(fig_def, height=320)
        st.plotly_chart(fig_def, use_container_width=True)
    else:
        st.info("No defect data available for the current selection.")

st.markdown("---")

# ============================================================
# TOP ADJUSTED MODES
# ============================================================
section_title("Top Adjusted Modes")

adjusted_mode_table = pd.DataFrame(
    columns=[
        "Check",
        "Mode",
        "Check Class",
        "Count",
        "Reference Boundaries",
        "Sensitivity",
        "Accuracy"
    ]
)

if "mode" in filtered_mode.columns and "action" in filtered_mode.columns:
    adjusted = filtered_mode[
        filtered_mode["action"].astype(str).str.lower().str.startswith("a")
    ].copy()

    if not adjusted.empty:
        rows = []
        group_cols = ["mode"]
        if "check_class" in adjusted.columns:
            group_cols.append("check_class")

        for keys, grp in adjusted.groupby(group_cols, dropna=False):
            if isinstance(keys, tuple):
                mode_name = keys[0]
                check_class = keys[1]
            else:
                mode_name = keys
                check_class = ""

            _, allb = summarize_boundaries(grp["boundary_after"]) if "boundary_after" in grp.columns else ("", "")

            sensitivity_text = ""
            if "sensitivity" in grp.columns:
                sensitivity_vals = sorted(set(grp["sensitivity"].dropna().astype(str)))
                sensitivity_text = ", ".join(sensitivity_vals)

            accuracy_text = ""
            if "accuracy" in grp.columns:
                accuracy_vals = sorted(set(grp["accuracy"].dropna().astype(str)))
                accuracy_text = ", ".join(accuracy_vals)

            rows.append({
                "Check": False,
                "Mode": mode_name,
                "Check Class": check_class,
                "Count": len(grp),
                "Reference Boundaries": allb,
                "Sensitivity": sensitivity_text,
                "Accuracy": accuracy_text,
            })

        adjusted_mode_table = (
            pd.DataFrame(rows)
            .sort_values(["Count", "Mode", "Check Class"], ascending=[False, True, True])
            .reset_index(drop=True)
        )

if not adjusted_mode_table.empty:
    st.data_editor(
        adjusted_mode_table,
        use_container_width=True,
        height=320,
        hide_index=True,
        column_config={"Check": st.column_config.CheckboxColumn("Check")},
        disabled=["Mode", "Check Class", "Count", "Reference Boundaries", "Sensitivity", "Accuracy"]
    )
else:
    st.info("No adjusted mode data available for the current filters.")

st.markdown("---")

# ============================================================
# STEP 1
# ============================================================
section_title("Step 1 — Select the defect to investigate")

available_reason_items = []
if "reason" in filtered_mode.columns:
    split_reasons = (
        filtered_mode["reason"]
        .dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .astype(str)
        .str.strip()
    )
    split_reasons = split_reasons[split_reasons != ""]
    available_reason_items = sorted(split_reasons.unique().tolist())

selected_reason = st.selectbox(
    "Select defect / reason",
    ["All"] + available_reason_items,
    key="mode_reason_selector"
)

related_modes = pd.DataFrame()

if selected_reason != "All":
    reason_related_df = filtered_mode.copy()

    reason_related_df["reason_item"] = (
        reason_related_df["reason"]
        .fillna("")
        .astype(str)
        .str.split(",")
    )
    reason_related_df = reason_related_df.explode("reason_item")
    reason_related_df["reason_item"] = reason_related_df["reason_item"].astype(str).str.strip()

    reason_related_df = reason_related_df[
        reason_related_df["reason_item"] == selected_reason
    ].copy()

    if not reason_related_df.empty:
        rows = []
        for keys, grp in reason_related_df.groupby(["mode", "check_class"], dropna=False):
            mode_name = keys[0]
            check_class = keys[1]

            _, allb = summarize_boundaries(grp["boundary_after"]) if "boundary_after" in grp.columns else ("", "")

            sensitivity_text = ""
            if "sensitivity" in grp.columns:
                sensitivity_vals = sorted(set(grp["sensitivity"].dropna().astype(str)))
                sensitivity_text = ", ".join(sensitivity_vals)

            accuracy_text = ""
            if "accuracy" in grp.columns:
                accuracy_vals = sorted(set(grp["accuracy"].dropna().astype(str)))
                accuracy_text = ", ".join(accuracy_vals)

            rows.append({
                "Mode": mode_name,
                "Check Class": check_class,
                "Count": len(grp),
                "Reference Boundaries": allb,
                "Sensitivity": sensitivity_text,
                "Accuracy": accuracy_text
            })

        related_modes = (
            pd.DataFrame(rows)
            .sort_values(["Count", "Mode"], ascending=[False, True])
            .reset_index(drop=True)
        )

        st.dataframe(related_modes, use_container_width=True, height=260)
    else:
        st.info("No related modes found for this defect / reason.")
else:
    st.info("Choose a defect / reason above to see related modes.")

st.markdown("---")

# ============================================================
# STEP 2
# ============================================================
section_title("Step 2 — Review what this mode can also detect")

mode_options_from_reason = []
if not related_modes.empty and "Mode" in related_modes.columns:
    mode_options_from_reason = related_modes["Mode"].dropna().astype(str).unique().tolist()

selected_related_mode = st.selectbox(
    "Select a mode from the results",
    ["All"] + sorted(mode_options_from_reason),
    key="mode_related_mode_selector"
)

if selected_related_mode != "All":
    selected_mode_rows = filtered_mode[
        filtered_mode["mode"].astype(str) == selected_related_mode
    ].copy()

    other_reason_counts = pd.DataFrame(columns=["Recorded Reason", "Count"])

    if "reason" in selected_mode_rows.columns:
        split_mode_reasons = (
            selected_mode_rows["reason"]
            .dropna()
            .astype(str)
            .str.split(",")
            .explode()
            .astype(str)
            .str.strip()
        )
        split_mode_reasons = split_mode_reasons[split_mode_reasons != ""]

        if not split_mode_reasons.empty:
            other_reason_counts = split_mode_reasons.value_counts().reset_index()
            other_reason_counts.columns = ["Recorded Reason", "Count"]

    if not other_reason_counts.empty:
        card_cols = st.columns(3)
        for idx, row in other_reason_counts.iterrows():
            col = card_cols[idx % 3]
            with col:
                st.markdown(
                    f"""
                    <div class="mode-card">
                        <div class="mode-card-title">{row['Recorded Reason']}</div>
                        <div class="mode-card-meta">Count: {int(row['Count'])}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("No other recorded reasons found for this mode.")
else:
    st.info("Select one mode above to see what else it is able to detect.")

st.markdown("---")

# ============================================================
# STEP 3
# ============================================================
section_title("Step 3 — Review unchecked modes for this grower")

next_modes_table = pd.DataFrame(
    columns=[
        "Check",
        "Mode",
        "Check Class",
        "Count",
        "Reference Boundaries",
        "Sensitivity",
        "Accuracy"
    ]
)

if selected_mode_variety != "All varieties" and selected_mode_grower != "All growers":
    grower_pool = variety_pool.copy()
    if "grower" in grower_pool.columns:
        grower_pool = grower_pool[grower_pool["grower"].astype(str) == selected_mode_grower]

    checked_pairs = set()
    if not grower_pool.empty:
        for keys, grp in grower_pool.groupby(["mode", "check_class"], dropna=False):
            checked_pairs.add((str(keys[0]), str(keys[1])))

    rows = []
    if not variety_pool.empty:
        for keys, grp in variety_pool.groupby(["mode", "check_class"], dropna=False):
            mode_name = str(keys[0])
            check_class = str(keys[1])

            if (mode_name, check_class) in checked_pairs:
                continue

            _, allb = summarize_boundaries(grp["boundary_after"]) if "boundary_after" in grp.columns else ("", "")

            sensitivity_text = ""
            if "sensitivity" in grp.columns:
                sensitivity_vals = sorted(set(grp["sensitivity"].dropna().astype(str)))
                sensitivity_text = ", ".join(sensitivity_vals)

            accuracy_text = ""
            if "accuracy" in grp.columns:
                accuracy_vals = sorted(set(grp["accuracy"].dropna().astype(str)))
                accuracy_text = ", ".join(accuracy_vals)

            rows.append({
                "Check": False,
                "Mode": mode_name,
                "Check Class": check_class,
                "Count": len(grp),
                "Reference Boundaries": allb,
                "Sensitivity": sensitivity_text,
                "Accuracy": accuracy_text
            })

    if rows:
        next_modes_table = (
            pd.DataFrame(rows)
            .sort_values(["Count", "Mode", "Check Class"], ascending=[False, True, True])
            .reset_index(drop=True)
        )

if selected_mode_variety == "All varieties" or selected_mode_grower == "All growers":
    st.info("Choose a specific variety and grower to see which modes are not yet checked for this grower.")
elif not next_modes_table.empty:
    st.data_editor(
        next_modes_table,
        use_container_width=True,
        height=300,
        hide_index=True,
        column_config={"Check": st.column_config.CheckboxColumn("Check")},
        disabled=["Mode", "Check Class", "Count", "Reference Boundaries", "Sensitivity", "Accuracy"]
    )
else:
    st.info("No additional unchecked modes found for this grower under the selected variety/version.")
