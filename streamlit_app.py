@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --canvas: #f3f5f4;
    --surface: #ffffff;
    --sidebar: #142c2a;
    --sidebar-soft: #1d3b37;
    --ink: #172b2a;
    --muted: #71817d;
    --line: #e1e9e5;
    --accent: #168477;
    --accent-hover: #116b61;
    --gold: #d7a45b;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: var(--canvas);
    color: var(--ink);
}

section[data-testid="stSidebar"] {
    background: var(--sidebar);
}

section[data-testid="stSidebar"] * {
    color: #edf5f1 !important;
}

.brand {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: var(--ink);
}

.subtitle {
    color: var(--muted);
    margin-bottom: 25px;
}

.metric-card, .section-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 4px 14px rgba(23, 43, 42, 0.035);
}

.metric-label {
    color: var(--muted);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .7px;
    text-transform: uppercase;
}

.metric-value {
    color: var(--ink);
    font-size: 25px;
    font-weight: 800;
}

h1, h2, h3, h4 {
    color: var(--ink);
}

.stButton button {
    border-radius: 9px;
    font-weight: 700;
}

.stButton button[kind="primary"] {
    background: var(--accent);
    color: white;
    border-color: var(--accent);
}

.stButton button[kind="primary"]:hover {
    background: var(--accent-hover);
    border-color: var(--accent-hover);
}

div[data-testid="stProgress"] > div > div {
    background: var(--accent);
}

hr {
    border-color: var(--line);
}