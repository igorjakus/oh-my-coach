import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

# Generating example data
np.random.seed(42)
dates = pd.date_range(start="2025-01-01", periods=100)
values = np.random.normal(0, 1, 100).cumsum()
df = pd.DataFrame({"date": dates, "value": values})

# 1. Matplotlib - static plot
plt.figure(figsize=(10, 6))
plt.plot(df["date"], df["value"])
plt.title("Matplotlib - Static Plot")
plt.savefig("matplotlib_plot.png")
plt.close()

# 2. Seaborn - prettier but still static
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x="date", y="value")
plt.title("Seaborn - Aesthetic but Static")
plt.savefig("seaborn_plot.png")
plt.close()

# 3. Plotly - interactive plot
fig = px.line(df, x="date", y="value", title="Plotly - Interactive Plot")
# Adding analysis tools
fig.update_layout(
    hovermode="x unified",
    updatemenus=[
        dict(
            type="buttons",
            showactive=False,
            buttons=[
                dict(
                    label="Reset Zoom",
                    method="relayout",
                    args=[{"xaxis.range": [None, None], "yaxis.range": [None, None]}],
                )
            ],
        )
    ],
)

# Save as interactive HTML
fig.write_html("plotly_interactive.html")

# 4. Plotly - advanced visualization
fig = go.Figure()

# Adding main line
fig.add_trace(
    go.Scatter(
        x=df["date"],
        y=df["value"],
        name="Value",
        line=dict(color="blue"),
        hovertemplate="Date: %{x}<br>Value: %{y:.2f}<extra></extra>",
    )
)

# Adding confidence interval
std = df["value"].std()
fig.add_trace(
    go.Scatter(
        x=df["date"],
        y=df["value"] + std,
        fill=None,
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip",
    )
)

fig.add_trace(
    go.Scatter(
        x=df["date"],
        y=df["value"] - std,
        fill="tonexty",
        mode="lines",
        line=dict(width=0),
        name="Confidence Interval",
        fillcolor="rgba(0,0,255,0.2)",
        hoverinfo="skip",
    )
)

fig.update_layout(
    title="Plotly - Advanced Interactive Visualization",
    xaxis_title="Date",
    yaxis_title="Value",
    hovermode="x unified",
    # Adding buttons for different Y-axis scales
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0.7,
            y=1.2,
            showactive=True,
            buttons=[
                dict(label="Linear", method="relayout", args=[{"yaxis.type": "linear"}]),
                dict(label="Logarithmic", method="relayout", args=[{"yaxis.type": "log"}]),
            ],
        )
    ],
)

fig.write_html("plotly_advanced.html")
