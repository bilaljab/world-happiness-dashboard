import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="World Happiness Report",
    page_icon="🌍",
    layout="wide",
)

# ─────────────────────────────────────────────
#  TOKENS — full dark, one accent
# ─────────────────────────────────────────────
BG       = "#0E1117"   # page background
SURFACE  = "#161B22"   # cards / sidebar
SURFACE2 = "#1C2333"   # nested surfaces
BORDER   = "#2D3748"   # dividers / borders
ACCENT   = "#3B82F6"   # single blue
TEXT1    = "#F0F4F8"   # primary
TEXT2    = "#8892A4"   # secondary
TEXT3    = "#4A5568"   # muted
BAR_BASE = "#1E3A5F"   # non-highlighted bar

st.markdown(f"""
<style>
  /* ── Reset ── */
  html, body, [class*="css"] {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif;
  }}

  /* ── Full dark background everywhere ── */
  .stApp,
  .stApp > div,
  [data-testid="stAppViewContainer"],
  [data-testid="stHeader"],
  [data-testid="block-container"] {{
      background-color: {BG} !important;
  }}

  /* ── Sidebar — same dark, thin border ── */
  section[data-testid="stSidebar"],
  section[data-testid="stSidebar"] > div,
  section[data-testid="stSidebar"] .block-container {{
      background-color: {SURFACE} !important;
      border-right: 1px solid {BORDER} !important;
  }}

  /* ── Main container width ── */
  .block-container {{
      padding-top: 2rem !important;
      padding-bottom: 3rem !important;
      max-width: 1080px !important;
  }}

  /* ── Hide streamlit chrome ── */
  #MainMenu, footer, header {{ visibility: hidden !important; }}

  /* ── Streamlit widget text colours ── */
  label, .stSelectbox label, .stSlider label,
  .stMultiSelect label, p, span {{
      color: {TEXT2} !important;
  }}
  h1, h2, h3, h4 {{ color: {TEXT1} !important; }}

  /* ── Selectbox / multiselect ── */
  [data-testid="stSelectbox"] > div > div,
  [data-testid="stMultiSelect"] > div > div {{
      background-color: {SURFACE2} !important;
      border: 1px solid {BORDER} !important;
      color: {TEXT1} !important;
  }}

  /* ── Slider track ── */
  [data-testid="stSlider"] .st-emotion-cache-1dp5vir,
  [data-testid="stSlider"] [class*="SliderTrack"] {{
      background: {ACCENT} !important;
  }}

  /* ─── Page header ─── */
  .pg-eyebrow {{
      font-size: 0.68rem; font-weight: 700;
      letter-spacing: 0.14em; text-transform: uppercase;
      color: {ACCENT}; margin: 0 0 0.5rem 0;
  }}
  .pg-title {{
      font-size: 2rem; font-weight: 800;
      color: {TEXT1}; margin: 0 0 0.35rem 0;
      letter-spacing: -0.02em; line-height: 1.2;
  }}
  .pg-sub {{
      font-size: 0.88rem; color: {TEXT2}; margin: 0;
  }}
  .pg-divider {{
      height: 1px; background: {BORDER};
      margin: 1.5rem 0 2rem 0;
  }}

  /* ─── KPI grid ─── */
  .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1px;
      background: {BORDER};
      border: 1px solid {BORDER};
      border-radius: 10px;
      overflow: hidden;
      margin-bottom: 2.5rem;
  }}
  .kpi-cell {{
      background: {SURFACE};
      padding: 1.3rem 1.5rem;
  }}
  .kpi-label {{
      font-size: 0.68rem; font-weight: 700;
      letter-spacing: 0.1em; text-transform: uppercase;
      color: {TEXT3}; margin-bottom: 0.45rem;
  }}
  .kpi-val {{
      font-size: 1.7rem; font-weight: 800;
      color: {TEXT1}; line-height: 1; margin-bottom: 0.2rem;
  }}
  .kpi-val.ac {{ color: {ACCENT}; }}
  .kpi-note {{
      font-size: 0.72rem; color: {TEXT3};
  }}

  /* ─── Chart section headers ─── */
  .ch-label {{
      font-size: 0.68rem; font-weight: 700;
      letter-spacing: 0.12em; text-transform: uppercase;
      color: {TEXT3}; margin-bottom: 0.3rem;
  }}
  .ch-title {{
      font-size: 1.1rem; font-weight: 700;
      color: {TEXT1}; margin: 0 0 0.2rem 0;
  }}
  .ch-desc {{
      font-size: 0.82rem; color: {TEXT2};
      margin: 0 0 1rem 0;
  }}

  /* ─── Insight strip ─── */
  .insight {{
      display: flex; gap: 0.9rem;
      background: {SURFACE};
      border: 1px solid {BORDER};
      border-radius: 8px;
      padding: 1rem 1.2rem;
      margin-top: 0.75rem;
  }}
  .ins-bar {{
      width: 3px; background: {ACCENT};
      border-radius: 2px; flex-shrink: 0;
  }}
  .ins-lbl {{
      font-size: 0.65rem; font-weight: 700;
      letter-spacing: 0.12em; text-transform: uppercase;
      color: {ACCENT}; margin-bottom: 0.3rem;
  }}
  .ins-txt {{
      font-size: 0.85rem; color: {TEXT2}; line-height: 1.65;
  }}
  .ins-txt strong {{ color: {TEXT1}; }}

  .section-gap {{ margin-bottom: 2.8rem; }}

  /* ─── Sidebar labels ─── */
  .sb-title {{
      font-size: 0.68rem; font-weight: 700;
      letter-spacing: 0.1em; text-transform: uppercase;
      color: {TEXT3}; margin: 1.4rem 0 0.5rem 0;
  }}

  /* ─── Footer ─── */
  .pg-footer {{
      padding: 1.5rem 0 0.5rem 0;
      border-top: 1px solid {BORDER};
      font-size: 0.72rem; color: {TEXT3};
  }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("happiness.csv", encoding="latin-1")

df = load_data()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f'<p style="font-size:1rem;font-weight:800;color:{TEXT1};margin:0 0 0.1rem 0;">World Happiness</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:0.75rem;color:{TEXT2};margin:0 0 0.5rem 0;">Interactive Report · 2005–2023</p>', unsafe_allow_html=True)

    st.markdown(f'<p class="sb-title">Year</p>', unsafe_allow_html=True)
    all_years = sorted(df["year"].unique(), reverse=True)
    selected_year = st.selectbox("", options=all_years, index=0, label_visibility="collapsed")

    st.markdown(f'<p class="sb-title">Top N Countries</p>', unsafe_allow_html=True)
    top_n = st.slider("", min_value=5, max_value=20, value=10, label_visibility="collapsed")

    st.markdown(f'<p class="sb-title">Country Comparison</p>', unsafe_allow_html=True)
    all_countries = sorted(df["Country name"].unique())
    defaults = [c for c in ["Finland","Saudi Arabia","United States","Japan","Afghanistan"] if c in all_countries]
    selected_countries = st.multiselect("", options=all_countries, default=defaults,
                                        max_selections=8, label_visibility="collapsed")

    st.markdown(f'<p class="sb-title">Scatter Color</p>', unsafe_allow_html=True)
    color_map = {
        "Social support": "Social Support",
        "Freedom to make life choices": "Freedom",
        "Healthy life expectancy at birth": "Life Expectancy",
    }
    color_factor = st.selectbox("", options=list(color_map.keys()),
                                format_func=lambda x: color_map[x],
                                label_visibility="collapsed")

    st.markdown(f'<p style="font-size:0.68rem;color:{TEXT3};margin-top:2rem;line-height:1.6;">Source: World Happiness Report<br>165 countries · 2,363 records</p>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PREPARE DATA
# ─────────────────────────────────────────────
df_year   = df[df["year"] == selected_year].copy()
df_top    = df_year.dropna(subset=["Life Ladder"]).nlargest(top_n, "Life Ladder")
df_bottom = df_year.dropna(subset=["Life Ladder"]).nsmallest(1, "Life Ladder")
global_avg        = df.groupby("year")["Life Ladder"].mean().reset_index()
global_avg_score  = df_year["Life Ladder"].mean()
df_scatter        = df_year.dropna(subset=["Life Ladder","Log GDP per capita",color_factor])

happiest_country = df_top.iloc[0]["Country name"]
happiest_score   = df_top.iloc[0]["Life Ladder"]
n_countries      = df_year["Country name"].nunique()
unhappiest       = df_bottom.iloc[0]["Country name"]
unhappiest_score = df_bottom.iloc[0]["Life Ladder"]

# ─────────────────────────────────────────────
#  CHART HELPER
# ─────────────────────────────────────────────
def dark_ax(ax, fig, grid="x"):
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(colors=TEXT2, labelsize=8.5, length=0)
    ax.xaxis.label.set_color(TEXT2)
    ax.yaxis.label.set_color(TEXT2)
    ax.set_axisbelow(True)
    gc = "#2D3748"
    if grid == "x":
        ax.yaxis.grid(True, color=gc, linewidth=0.7); ax.xaxis.grid(False)
    elif grid == "y":
        ax.xaxis.grid(True, color=gc, linewidth=0.7); ax.yaxis.grid(False)
    else:
        ax.grid(True, color=gc, linewidth=0.7)

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<p class="pg-eyebrow">Global Wellbeing Index · {selected_year}</p>
<h1 class="pg-title">World Happiness Report</h1>
<p class="pg-sub">Analyzing happiness scores across 165 countries using the Life Ladder scale</p>
<div class="pg-divider"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  KPI ROW
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-cell">
    <div class="kpi-label">Happiest Country</div>
    <div class="kpi-val ac">{happiest_country}</div>
    <div class="kpi-note">Score {happiest_score:.2f} / 10</div>
  </div>
  <div class="kpi-cell">
    <div class="kpi-label">Global Average</div>
    <div class="kpi-val">{global_avg_score:.2f}</div>
    <div class="kpi-note">Out of 10.0</div>
  </div>
  <div class="kpi-cell">
    <div class="kpi-label">Countries Ranked</div>
    <div class="kpi-val">{n_countries}</div>
    <div class="kpi-note">in {selected_year}</div>
  </div>
  <div class="kpi-cell">
    <div class="kpi-label">Lowest Score</div>
    <div class="kpi-val">{unhappiest}</div>
    <div class="kpi-note">Score {unhappiest_score:.2f} / 10</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CHART 1 — BAR
# ─────────────────────────────────────────────
st.markdown(f"""
<p class="ch-label">Chart 01 / Rankings</p>
<h2 class="ch-title">Top {top_n} Happiest Countries — {selected_year}</h2>
<p class="ch-desc">Life Ladder score comparison with global average reference line</p>
""", unsafe_allow_html=True)

fig1, ax1 = plt.subplots(figsize=(10, max(3.5, top_n * 0.48)))
dark_ax(ax1, fig1, "y")

bar_colors = [ACCENT if i == 0 else BAR_BASE for i in range(len(df_top))]
bars = ax1.barh(
    df_top["Country name"][::-1],
    df_top["Life Ladder"][::-1],
    color=bar_colors[::-1], height=0.6, edgecolor="none"
)
for bar, val in zip(bars, df_top["Life Ladder"][::-1]):
    ax1.text(bar.get_width() + 0.06, bar.get_y() + bar.get_height() / 2,
             f"{val:.2f}", va="center", ha="left",
             color=TEXT2, fontsize=8.5, fontweight="600")

ax1.axvline(global_avg_score, color=TEXT3, linewidth=1, linestyle="--",
            label=f"Global avg  {global_avg_score:.2f}")
ax1.set_xlim(0, df_top["Life Ladder"].max() + 0.7)
ax1.set_xlabel("Life Ladder Score", fontsize=9, labelpad=8)
ax1.legend(facecolor=SURFACE, edgecolor=BORDER, labelcolor=TEXT2,
           fontsize=8.5, framealpha=1, loc="lower right")
ax1.tick_params(axis="y", labelcolor=TEXT1, labelsize=9)
plt.tight_layout(pad=1)
st.pyplot(fig1, use_container_width=True)
plt.close()

st.markdown(f"""
<div class="insight">
  <div class="ins-bar"></div>
  <div>
    <div class="ins-lbl">Key Insight</div>
    <div class="ins-txt">
      <strong>{happiest_country}</strong> leads with {happiest_score:.2f}/10.
      Top-ranked countries share a consistent pattern: strong social support,
      high economic output, and individual freedom — pointing to systemic
      policy factors rather than wealth alone.
    </div>
  </div>
</div>
<div class="section-gap"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CHART 2 — LINE
# ─────────────────────────────────────────────
st.markdown(f"""
<p class="ch-label">Chart 02 / Trends</p>
<h2 class="ch-title">Happiness Over Time — 2005 to 2023</h2>
<p class="ch-desc">Country trajectories vs. global average trend</p>
""", unsafe_allow_html=True)

fig2, ax2 = plt.subplots(figsize=(11, 4.5))
dark_ax(ax2, fig2, "x")

ax2.fill_between(global_avg["year"], global_avg["Life Ladder"], alpha=0.05, color=ACCENT)
ax2.plot(global_avg["year"], global_avg["Life Ladder"],
         color=BORDER, linewidth=1.5, linestyle="--",
         label="Global Average", zorder=2)

palette = [ACCENT, "#EF4444", "#22C55E", "#F59E0B", "#A855F7", "#06B6D4", "#EC4899", "#84CC16"]

if selected_countries:
    for i, country in enumerate(selected_countries):
        cd = df[df["Country name"] == country].sort_values("year")
        if len(cd):
            col = palette[i % len(palette)]
            ax2.plot(cd["year"], cd["Life Ladder"],
                     color=col, linewidth=2, marker="o", markersize=3.5,
                     label=country, zorder=3)
            last = cd.iloc[-1]
            ax2.annotate(f"{country}  {last['Life Ladder']:.1f}",
                         xy=(last["year"], last["Life Ladder"]),
                         xytext=(7, 0), textcoords="offset points",
                         color=col, fontsize=7.5, va="center", fontweight="600")
else:
    st.info("Select at least one country from the sidebar.")

ax2.set_xlabel("Year", fontsize=9, labelpad=8)
ax2.set_ylabel("Life Ladder", fontsize=9, labelpad=8)
ax2.set_xlim(df["year"].min() - 0.5, df["year"].max() + 3.5)
ax2.set_ylim(bottom=0)
ax2.legend(facecolor=SURFACE, edgecolor=BORDER, labelcolor=TEXT2,
           fontsize=8, ncol=3, loc="upper left", framealpha=1)
plt.tight_layout(pad=1)
st.pyplot(fig2, use_container_width=True)
plt.close()

if selected_countries:
    best, best_gain = None, -99
    for c in selected_countries:
        cd = df[df["Country name"] == c].sort_values("year")
        if len(cd) >= 2:
            g = cd.iloc[-1]["Life Ladder"] - cd.iloc[0]["Life Ladder"]
            if g > best_gain: best_gain, best = g, c
    direction = "improved" if best_gain > 0 else "declined"
    st.markdown(f"""
<div class="insight">
  <div class="ins-bar"></div>
  <div>
    <div class="ins-lbl">Key Insight</div>
    <div class="ins-txt">
      <strong>{best}</strong> {direction} most among selected countries
      ({abs(best_gain):+.2f} pts). Global happiness is not a smooth upward
      curve — geopolitical shocks and economic crises leave visible marks in the data.
    </div>
  </div>
</div>
<div class="section-gap"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CHART 3 — SCATTER
# ─────────────────────────────────────────────
st.markdown(f"""
<p class="ch-label">Chart 03 / Correlation</p>
<h2 class="ch-title">Does Wealth Predict Happiness? — {selected_year}</h2>
<p class="ch-desc">Log GDP per capita vs. Life Ladder · color = {color_map[color_factor]}</p>
""", unsafe_allow_html=True)

fig3, ax3 = plt.subplots(figsize=(11, 5.5))
dark_ax(ax3, fig3, "both")

corr_val = 0
if len(df_scatter):
    sc = ax3.scatter(
        df_scatter["Log GDP per capita"], df_scatter["Life Ladder"],
        c=df_scatter[color_factor], cmap="Blues",
        vmin=df_scatter[color_factor].quantile(0.05),
        vmax=df_scatter[color_factor].quantile(0.95),
        s=65, alpha=0.92, edgecolors=BORDER, linewidths=0.4, zorder=3
    )
    cbar = plt.colorbar(sc, ax=ax3, pad=0.02, fraction=0.025)
    cbar.ax.yaxis.set_tick_params(color=TEXT3, labelsize=8)
    cbar.outline.set_edgecolor(BORDER)
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color=TEXT2, fontsize=8)
    cbar.set_label(color_map[color_factor], color=TEXT2, fontsize=8.5)

    highlight = ["Finland","Afghanistan","Saudi Arabia","Kuwait",
                 "United States","Costa Rica","Denmark","Japan"]
    for _, row in df_scatter.iterrows():
        if row["Country name"] in highlight:
            ax3.annotate(row["Country name"],
                         xy=(row["Log GDP per capita"], row["Life Ladder"]),
                         xytext=(7, 3), textcoords="offset points",
                         color=TEXT1, fontsize=7.5, fontweight="600")

    z  = np.polyfit(df_scatter["Log GDP per capita"], df_scatter["Life Ladder"], 1)
    xl = np.linspace(df_scatter["Log GDP per capita"].min(),
                     df_scatter["Log GDP per capita"].max(), 200)
    ax3.plot(xl, np.poly1d(z)(xl), color=ACCENT, linewidth=1.5,
             linestyle="--", alpha=0.7, label="Trend line", zorder=2)

    corr_val = df_scatter[["Log GDP per capita","Life Ladder"]].corr().iloc[0, 1]
    ax3.set_xlabel("Log GDP per Capita", fontsize=9, labelpad=8)
    ax3.set_ylabel("Life Ladder Score", fontsize=9, labelpad=8)
    ax3.legend(facecolor=SURFACE, edgecolor=BORDER, labelcolor=TEXT2,
               fontsize=8.5, framealpha=1)

plt.tight_layout(pad=1)
st.pyplot(fig3, use_container_width=True)
plt.close()

st.markdown(f"""
<div class="insight">
  <div class="ins-bar"></div>
  <div>
    <div class="ins-lbl">Key Insight</div>
    <div class="ins-txt">
      Correlation between GDP and happiness = <strong>{corr_val:.2f}</strong> — strong but not deterministic.
      <strong>Costa Rica</strong> outranks wealthier nations through social cohesion and personal
      freedom, suggesting smart policy can raise wellbeing beyond what income alone can explain.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="pg-footer">
  World Happiness Report · 2005–2023 · 165 countries · 2,363 records · Source: Gallup World Poll
</div>
""", unsafe_allow_html=True)
