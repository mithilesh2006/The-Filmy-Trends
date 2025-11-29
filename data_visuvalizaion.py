from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px 

df = pd.read_csv("Datasets/final_movies_dataset.csv") #loading the final merged dataset

def explode_genres(source_df): #handling multiple genres per movie
    exploded_df = source_df.copy()
    exploded_df['Genre'] = exploded_df['Genre'].fillna('Unknown').str.replace(r'[|/;]', ',', regex=True)
    exploded_df['Genre'] = exploded_df['Genre'].str.split(',')
    exploded_df = exploded_df.explode('Genre')
    exploded_df['Genre'] = exploded_df['Genre'].astype(str).str.strip()
    exploded_df = exploded_df[exploded_df['Genre'].ne('') & exploded_df['Genre'].ne('Unknown')]
    return exploded_df

# Year and Industry setup
year_min, year_max = int(df['Year'].min()), int(df['Year'].max())
decade_marks = {y: f"{y}" for y in range((year_min // 10) * 10, year_max + 1, 10)}
industry_list = sorted(df['Industry'].dropna().unique().tolist())

# Colors
DISCRETE_COLORS = px.colors.qualitative.Set2 + px.colors.qualitative.Pastel
CONTINUOUS_SCALE = 'viridis'

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY]) #initializing the dash app
server = app.server

# Filters

controls = dbc.Card([
    html.Div("Filters", className="h5 mb-3 fw-bold"),
    dbc.Row([
        dbc.Col([
            html.Label("Select Industries:", className="fw-bold"),
            dcc.Dropdown(
                id="flt-industry",
                options=[{"label": i, "value": i} for i in industry_list],
                value=industry_list,
                multi=True,
                clearable=False
            )
        ], md=6), # to select Industries
        dbc.Col([
            html.Label("Select Year Range (Decade-wise):", className="fw-bold"),
            dcc.RangeSlider(
                id="flt-year",
                min=year_min,
                max=year_max,
                step=1,
                value=[max(year_min, year_max - 10), year_max],
                marks=decade_marks,
                tooltip={"placement": "bottom", "always_visible": False}
            )
        ], md=6) # to select Year Range
    ])
], body=True, className="shadow-sm rounded-4")

def kpi_card(id_value, title):
    return dbc.Card(dbc.CardBody([
        html.Div(title, className="text-muted small"),
        html.Div(id=id_value, className="h3 fw-semibold mb-0")
    ]), className="shadow-sm rounded-4")

kpis = dbc.Row([
    dbc.Col(kpi_card("kpi-movies", " Movies in selection"), md=3), #kpi that shows number of movies in selected year range and industries
    dbc.Col(kpi_card("kpi-med-rating", " Median rating"), md=3),   #median of rating in selected year range and industries
    dbc.Col(kpi_card("kpi-med-budget", " Median budget"), md=3),   #median of budget in selected year range and industries
    dbc.Col(kpi_card("kpi-top-genre", " Top genre"), md=3)         #top genre in selected year range and industries
], className="g-3")

# Tabs

tab_trend = dbc.Tab(label="Budget vs Year", tab_id="tab-trend", children=[
    dbc.Card(dbc.CardBody([
        dbc.Row([
            dbc.Col(dbc.RadioItems(
                id="trend-agg",
                options=[
                    {"label": "Average Budget", "value": "mean"},
                    {"label": "Total Budget", "value": "sum"}
                ],
                value="mean",
                inline=True
            ), md=6),
            dbc.Col(dbc.Checklist(
                id="trend-show-points",
                options=[{"label": " Show markers", "value": "markers"}],
                value=["markers"],
                inline=True
            ), md=6, className="text-md-end")
        ]),
        dcc.Graph(id="graph-trend", config={"displaylogo": False})
    ]))
])

tab_scatter = dbc.Tab(label="Budget vs Runtime", tab_id="tab-scatter", children=[
    dbc.Card(dbc.CardBody([
        dbc.Row([
            dbc.Col(dbc.Checklist(
                id="scatter-log",
                options=[
                    {"label": " Log X (Runtime)", "value": "logx"},
                    {"label": " Log Y (Budget)", "value": "logy"}
                ],
                value=[],
                inline=True
            ), md=8),
            dbc.Col(dcc.Slider(
                id="scatter-size",
                min=5, max=20, step=1, value=10,
                tooltip={"placement": "bottom", "always_visible": False}
            ), md=4)
        ]),
        dcc.Graph(id="graph-scatter", config={"displaylogo": False})
    ]))
])

tab_box = dbc.Tab(label="Rating Distributions", tab_id="tab-box", children=[
    dbc.Card(dbc.CardBody([
        dbc.Row([
            dbc.Col(dbc.RadioItems(
                id="box-dim",
                options=[
                    {"label": "By Industry", "value": "Industry"},
                    {"label": "By Genre", "value": "Genre"}
                ],
                value="Industry",
                inline=True
            ), md=6),
            dbc.Col(dbc.Checklist(
                id="box-show-points",
                options=[{"label": " Show all points", "value": "points"}],
                value=["points"],
                inline=True
            ), md=6, className="text-md-end")
        ]),
        dcc.Graph(id="graph-box", config={"displaylogo": False})
    ]))
])

tab_genre = dbc.Tab(label="Genre Explorer", tab_id="tab-genre", children=[
    dbc.Card(dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.Label("Top N Genres", className="fw-bold"),
                dcc.Slider(id="genre-topn", min=5, max=20, step=1, value=10)
            ], md=4),
            dbc.Col([
                html.Label("Sort by", className="fw-bold"),
                dcc.RadioItems(
                    id="genre-sort",
                    options=[
                        {"label": " Count (desc)", "value": "count"},
                        {"label": " Alphabetical", "value": "alpha"}
                    ],
                    value="count",
                    inline=True
                )
            ], md=4),
            dbc.Col([
                html.Label("Display Style", className="fw-bold"),
                dcc.RadioItems(
                    id="genre-style",
                    options=[
                        {"label": " Bar Chart", "value": "bar"},
                        {"label": " Treemap", "value": "treemap"}
                    ],
                    value="bar",
                    inline=True
                )
            ], md=4)
        ]),
        dcc.Graph(id="graph-genre", config={"displaylogo": False})
    ]))
])

tab_hist = dbc.Tab(label="Histograms", tab_id="tab-hist", children=[
    dbc.Card(dbc.CardBody([
        html.H5(" Genre Distribution", className="fw-bold text-primary mb-2"),
        dcc.Graph(id="hist-genre", config={"displaylogo": False}),
        html.Hr(),
        html.H5(" Yearwise Movie Distribution", className="fw-bold text-primary mb-2"),
        dcc.Graph(id="hist-year", config={"displaylogo": False})
    ]))
])

# Layout

app.layout = dbc.Container([
    html.H1(" Movie Insight Dashboard", className="mt-4 mb-1 text-center fw-bold"),
    html.Div("Explore movie patterns across industries, decades, and genres",
             className="text-muted text-center mb-4"),
    controls,
    html.Br(),
    kpis,
    html.Br(),
    dbc.Tabs([tab_trend, tab_scatter, tab_box, tab_genre, tab_hist], id="tabs", active_tab="tab-trend")
], fluid=True)

# Helper Functions

def apply_filters(dff, year_range, industries):
    y_min, y_max = year_range
    mask = (dff['Year'] >= y_min) & (dff['Year'] <= y_max)
    mask &= dff['Industry'].isin(industries)
    return dff[mask].copy()

def friendly_currency(x):
    try:
        x = float(x)
        if x >= 1e9: return f"${x/1e9:.1f}B"
        if x >= 1e6: return f"${x/1e6:.1f}M"
        if x >= 1e3: return f"${x/1e3:.1f}K"
        return f"${x:,.0f}"
    except:
        return "—"

@app.callback(
    Output("kpi-movies", "children"),
    Output("kpi-med-rating", "children"),
    Output("kpi-med-budget", "children"),
    Output("kpi-top-genre", "children"),
    Input("flt-industry", "value"),
    Input("flt-year", "value")
)
def update_kpis(industries, year_range):
    dff = apply_filters(df, year_range, industries)
    if dff.empty:
        return "0", "—", "—", "—"
    movies_count = len(dff)
    med_rating = f"{dff['Rating'].median():.2f}"
    med_budget = friendly_currency(dff['Budget'].median())
    eg = explode_genres(dff)
    top_genre = eg['Genre'].value_counts().idxmax() if not eg.empty else "—"
    return str(movies_count), med_rating, med_budget, top_genre

# Trend Chart (TAB 1)

@app.callback(
    Output("graph-trend", "figure"),
    Input("flt-industry", "value"),
    Input("flt-year", "value"),
    Input("trend-agg", "value"),
    Input("trend-show-points", "value")
)
def update_trend(industries, year_range, agg, show_points):
    dff = apply_filters(df, year_range, industries)
    if dff.empty:
        return px.line(title="No data for selection.")
    grouped = dff.groupby(['Year', 'Industry'], as_index=False)['Budget'].agg(agg)
    fig = px.line(grouped, x="Year", y="Budget", color="Industry",
                  markers=("markers" in show_points),
                  title=f"{agg.title()} Budget by Year (per Industry)",
                  color_discrete_sequence=DISCRETE_COLORS)
    fig.update_layout(height=450, template="plotly_white")
    return fig

# Scatter Chart (TAB 2)

@app.callback(
    Output("graph-scatter", "figure"),
    Input("flt-industry", "value"),
    Input("flt-year", "value"),
    Input("scatter-log", "value"),
    Input("scatter-size", "value")
)
def update_scatter(industries, year_range, log_opts, size_val):
    dff = apply_filters(df, year_range, industries)
    if dff.empty:
        return px.scatter(title="No data for selection.")
    fig = px.scatter(
        dff, x="Duration", y="Budget", color="Language", size="Rating",
        hover_data=["Name", "Year", "Genre"],
        size_max=size_val, color_discrete_sequence=DISCRETE_COLORS,
        title="Budget vs Runtime (Bubble size = Rating)"
    )
    if "logx" in log_opts: fig.update_xaxes(type="log")
    if "logy" in log_opts: fig.update_yaxes(type="log")
    fig.update_layout(height=450, template="plotly_white")
    return fig

# Box Plot (TAB 3)

@app.callback(
    Output("graph-box", "figure"),
    Input("flt-industry", "value"),
    Input("flt-year", "value"),
    Input("box-dim", "value"),
    Input("box-show-points", "value")
)
def update_box(industries, year_range, dim, show_points):
    dff = apply_filters(df, year_range, industries)
    if dim == "Genre":
        dff = explode_genres(dff)
    if dff.empty:
        return px.box(title="No data for selection.")
    pts = "all" if "points" in show_points else False
    fig = px.box(dff, x=dim, y="Rating", color=dim, points=pts,
                 color_discrete_sequence=DISCRETE_COLORS,
                 title=f"Distribution of Ratings by {dim}")
    fig.update_layout(height=450, template="plotly_white", showlegend=False)
    return fig

# Genre Explorer (TAB 4)

@app.callback(
    Output("graph-genre", "figure"),
    Input("flt-industry", "value"),
    Input("flt-year", "value"),
    Input("genre-topn", "value"),
    Input("genre-sort", "value"),
    Input("genre-style", "value")
)
def update_genre(industries, year_range, topn, sort_mode, style):
    dff = apply_filters(df, year_range, industries)
    eg = explode_genres(dff)
    if eg.empty:
        return px.bar(title="No genre data.")
    counts = eg['Genre'].value_counts().reset_index()
    counts.columns = ['Genre', 'Count']
    if sort_mode == "alpha":
        counts = counts.sort_values('Genre')
    else:
        counts = counts.sort_values('Count', ascending=False)
    counts = counts.head(topn)
    if style == "treemap":
        fig = px.treemap(counts, path=['Genre'], values='Count', title="Top Genres (Treemap)")
    else:
        fig = px.bar(counts, x="Genre", y="Count", color="Count",
                     color_continuous_scale=CONTINUOUS_SCALE, title="Top Genres")
    fig.update_layout(height=450, template="plotly_white")
    return fig

# Histograms (TAB 5)

@app.callback(
    Output("hist-genre", "figure"),
    Output("hist-year", "figure"),
    Input("flt-industry", "value"),
    Input("flt-year", "value")
)
def update_histograms(industries, year_range):
    dff = apply_filters(df, year_range, industries)
    eg = explode_genres(dff)

    # Genre Histogram
    if eg.empty:
        fig_genre = px.histogram(title="No genre data.")
    else:
        fig_genre = px.histogram(
            eg, x="Genre", color="Industry",
            barmode="group",
            title="Genre Distribution (Filtered by Industry and Year)",
            color_discrete_sequence=DISCRETE_COLORS
        )
        fig_genre.update_layout(height=400,bargap=0.05, template="plotly_white", xaxis_title="Genre", yaxis_title="Movie Count")

    # Yearwise Histogram
    if dff.empty:
        fig_year = px.histogram(title="No year data.")
    else:
        fig_year = px.histogram(
            dff, x="Year", color="Industry", nbins=20,
            title="Yearwise Movie Distribution",
            color_discrete_sequence=DISCRETE_COLORS
        )
        fig_year.update_layout(height=400, bargap=0.2, template="plotly_white", xaxis_title="Year", yaxis_title="Movie Count")

    return fig_genre, fig_year

if __name__ == "__main__": #running the dash app
    
    print(" Dashboard running at http://127.0.0.1:8051")
    app.run(jupyter_mode="inline", jupyter_height=900, debug=True, port=8051)