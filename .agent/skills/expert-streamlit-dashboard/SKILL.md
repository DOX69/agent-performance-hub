---
name: expert-streamlit-dashboard
description: "Expert guidance for building high-performance, professional, and minimalist Streamlit dashboards. Focuses on caching strategies, SQL optimization, and clean data-first UX."
version: "1.0.0"
tags:
  - streamlit
  - dashboard
  - data-visualization
  - sql-optimization
  - python
  - ux-design
---

# Expert Streamlit Dashboard Patterns

## Overview

This skill provides professional mental models and design patterns for building **production-grade Streamlit dashboards**. It emphasizes a "Data-First, Minimalist" aesthetic (avoiding "vibes" coding or excessive emojis) and rigorous performance optimization for SQL-backed applications.

## When to Use

- **Executive Reporting**: Building dashboards for decision-makers who need clear signals, not noise.
- **Large Datasets**: Handling millions of rows efficiently without crashing the browser or server.
- **Interactive Analytics**: Complex filtering scenarios where performance is critical.
- **Internal Tools**: Replacing spreadsheet workflows with robust data apps.

## The Mental Shift: "Vibe Coding" vs. Expert Engineering

| Feature | "Vibe Coding" (Amateur) | Expert Engineering |
| :--- | :--- | :--- |
| **Aesthetic** | Flashy, emoji-heavy, colorful | **Minimalist, whitespace-driven, professional** |
| **Data Loading** | `pd.read_csv` on every run | **Aggressive Caching (`@st.cache_data`)** |
| **SQL Strategy** | `SELECT *` into Pandas | **Push-down predicates (filter in SQL)** |
| **State** | Lost on refresh/interaction | **Persisted via `st.session_state` & URL params** |
| **Filters** | Cluttered main area | **Collapsible Sidebar with intelligent defaults** |

## Core Design Patterns

### 1. The "Data-First" Minimalist UI

Professional dashboards respect the user's attention.

**Pattern:**
-   **No Emojis in Headers**: Use clean typography.
-   **Key Metrics (KPIs) Top-Left**: The most valuable real estate.
-   **Consistent Color Palette**: Use `st.set_page_config` and `config.toml` to enforce brand colors, not random selections.
-   **Whitespace**: Use `st.container` and `st.columns` to create breathing room.

### 2. Performance: The Caching Strategy

Streamlit re-runs the entire script on *every* interaction. Without caching, your app is unusable.

**Pattern:**
-   **Data Cache (`@st.cache_data`)**: For serializable data (Pandas DataFrames, JSON).
    -   *Crucial:* Set `ttl` (Time To Live) to avoid stale data (e.g., `ttl=300` for 5 mins).
    -   *Crucial:* Set `max_entries` to prevent memory leaks.
-   **Resource Cache (`@st.cache_resource`)**: For database connections, ML models.

```python
@st.cache_resource
def get_db_connection():
    return mysql.connector.connect(...)

@st.cache_data(ttl=300, show_spinner=False)
def get_sales_data(start_date, end_date):
    # ... executes optimized SQL ...
    return df
```

### 3. SQL Optimization: Push-Down Computation

**Never** load a massive table into Pandas to filter it.

**Pattern:**
-   **Filter in SQL**: Pass dashboard filters (`start_date`, `region`) directly into the `WHERE` clause.
-   **Aggregate in SQL**: If the user wants "Sales by Month", do `GROUP BY` in SQL, not Pandas.
-   **Limit Rows**: Always have a safety valve (`LIMIT 10000`) or pagination.

*Bad:* `SELECT * FROM sales` -> `df[df['date'] > start]`
*Good:* `SELECT * FROM sales WHERE date > :start`

### 4. Intuitive Filtering System

Filters should be powerful but unobtrusive.

**Pattern:**
-   **Sidebar First**: Place all global controls in `st.sidebar`.
-   **Dynamic Defaults**: Set default filter values to the "most useful" view (e.g., "Last 7 Days" instead of "All Time").
-   **Form Batching**: For expensive queries, wrap filters in `st.form` so the app only re-runs when the user clicks "Apply".

```python
with st.sidebar.form(key='filters'):
    date_range = st.date_input("Date Range", [])
    submit_button = st.form_submit_button(label='Update Dashboard')

if submit_button:
    # Run query
```

### 5. Advanced State Management

Don't let users lose their place.

**Pattern:**
-   **URL Sync**: Sync key filter states to URL parameters using `st.query_params` so links can be shared.
-   **Session State**: Use `st.session_state` to store intermediate calculations or user preferences that shouldn't trigger a full data reload.

## Expert Checklist

Before deploying your dashboard:

-   [ ] **Load Test**: Does it handle 1M rows? (If not, optimize SQL).
-   [ ] **Cache Hit Rate**: Are expensive queries actually being cached? (Check debug logs).
-   [ ] **Visual Hierarchy**: clear distinction between KPIs, Charts, and Data Tables.
-   [ ] **Mobile Responsiveness**: Do columns stack correctly on smaller screens?
-   [ ] **Error Handling**: Are `st.error` or `st.warning` used instead of raw Python tracebacks?

## Common Anti-Patterns

❌ **"The Wall of Text"**: Dumping a raw dataframe (`st.dataframe(df)`) without specific intent.
❌ **"Blocking Queries"**: Running long SQL queries in the main thread without a spinner or cache.
❌ **"Widget Explosion"**: Putting 20 filters on the screen at once. Use "Advanced Filters" expanders.
❌ **"Hardcoded Secrets"**: Never put DB credentials in code. Use `.streamlit/secrets.toml`.
