
import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import numpy as np


DB_HOST="localhost"
DB_PORT=3306
DB_USER="root"
DB_PASSWORD="Amol@1985"
DB_NAME="flight_analytics"

connection = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)


if connection.is_connected():
    st.success("✅ MySQL Database Connected Successfully")   

cursor = connection.cursor()

cursor.execute("SELECT * FROM flights")
data = cursor.fetchall()
for row in data:
    print(row)



# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Air Tracker - Flight Analytics",
    page_icon="✈️",
    layout="wide"
)

# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="Amol@1985",
            database="flight_analytics"
        )
        return connection

    except mysql.connector.Error as e:
        st.error(f"Database connection failed: {e}")
        return None


# =========================================================
# RUN SQL QUERY
# =========================================================

def run_query(query, params=None):

    connection = get_connection()

    if connection is None:
        return pd.DataFrame()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(query, params or ())

        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return pd.DataFrame(data)

    except mysql.connector.Error as e:
        st.error(f"SQL Error: {e}")
        return pd.DataFrame()


# =========================================================
# TITLE
# =========================================================

st.title("✈️ Air Tracker - Flight Analytics")
st.markdown(
    "### SQL + Python + Streamlit Flight Analytics Dashboard"
)

st.divider()


# =========================================================
# DATABASE CHECK
# =========================================================

connection = get_connection()

if connection is None:
    st.stop()

connection.close()

st.success("✅ MySQL Database Connected Successfully")


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.title("🔎 Filters")

# ---------------------------------------------------------
# STATUS FILTER
# ---------------------------------------------------------

status_df = run_query("""
    SELECT DISTINCT status
    FROM flights
    WHERE status IS NOT NULL
    ORDER BY status
""")

status_list = ["All"]

if not status_df.empty:
    status_list += status_df["status"].tolist()

selected_status = st.sidebar.selectbox(
    "Flight Status",
    status_list
)


# ---------------------------------------------------------
# ORIGIN FILTER
# ---------------------------------------------------------

origin_df = run_query("""
    SELECT DISTINCT origin_iata
    FROM flights
    WHERE origin_iata IS NOT NULL
    ORDER BY origin_iata
""")

origin_list = ["All"]

if not origin_df.empty:
    origin_list += origin_df["origin_iata"].tolist()

selected_origin = st.sidebar.selectbox(
    "Origin Airport",
    origin_list
)


# ---------------------------------------------------------
# AIRLINE FILTER
# ---------------------------------------------------------

airline_df = run_query("""
    SELECT DISTINCT airline_code
    FROM flights
    WHERE airline_code IS NOT NULL
    ORDER BY airline_code
""")

airline_list = ["All"]

if not airline_df.empty:
    airline_list += airline_df["airline_code"].tolist()

selected_airline = st.sidebar.selectbox(
    "Airline",
    airline_list
)


# =========================================================
# KPI SECTION
# =========================================================

st.subheader("📊 Dashboard Summary")

# Total Airports
airport_count = run_query("""
    SELECT COUNT(*) AS total_airports
    FROM airport
""")

total_airports = 0

if not airport_count.empty:
    total_airports = int(airport_count.iloc[0]["total_airports"])


# Total Flights
flight_count = run_query("""
    SELECT COUNT(*) AS total_flights
    FROM flights
""")

total_flights = 0

if not flight_count.empty:
    total_flights = int(flight_count.iloc[0]["total_flights"])


# Average Delay
delay_data = run_query("""
    SELECT AVG(avg_delay_min) AS avg_delay
    FROM airport_delays
""")

avg_delay = 0

if not delay_data.empty and delay_data.iloc[0]["avg_delay"] is not None:
    avg_delay = float(delay_data.iloc[0]["avg_delay"])


# Cancelled Flights
cancelled_data = run_query("""
    SELECT COUNT(*) AS cancelled
    FROM flights
    WHERE status = 'Cancelled'
""")

cancelled_flights = 0

if not cancelled_data.empty:
    cancelled_flights = int(cancelled_data.iloc[0]["cancelled"])


# KPI Cards

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "✈️ Total Airports",
        f"{total_airports:,}"
    )

with col2:
    st.metric(
        "🛫 Total Flights",
        f"{total_flights:,}"
    )

with col3:
    st.metric(
        "⏱️ Average Delay",
        f"{avg_delay:.2f} min"
    )

with col4:
    st.metric(
        "❌ Cancelled Flights",
        f"{cancelled_flights:,}"
    )


st.divider()


# =========================================================
# FLIGHT DATA WITH FILTER
# =========================================================

st.subheader("🛫 Flight Data")

query = """
    SELECT
        flight_id,
        flight_number,
        aircraft_registration,
        origin_iata,
        destination_iata,
        scheduled_departure,
        actual_departure,
        scheduled_arrival,
        actual_arrival,
        status,
        airline_code
    FROM flights
    WHERE 1=1
"""

params = []

if selected_status != "All":
    query += " AND status = %s"
    params.append(selected_status)

if selected_origin != "All":
    query += " AND origin_iata = %s"
    params.append(selected_origin)

if selected_airline != "All":
    query += " AND airline_code = %s"
    params.append(selected_airline)

query += """
    ORDER BY scheduled_departure DESC
"""

flight_df = run_query(query, tuple(params))


if not flight_df.empty:

    st.dataframe(
        flight_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning("No flight data found.")


st.divider()


# =========================================================
# CHART 1 - FLIGHTS BY STATUS
# =========================================================

st.subheader("📈 Flight Status Analysis")

status_chart = run_query("""
    SELECT
        status,
        COUNT(*) AS total_flights
    FROM flights
    WHERE status IS NOT NULL
    GROUP BY status
    ORDER BY total_flights DESC
""")

if not status_chart.empty:

    fig1 = px.bar(
        status_chart,
        x="status",
        y="total_flights",
        title="Flights by Status",
        text="total_flights"
    )

    fig1.update_layout(
        xaxis_title="Flight Status",
        yaxis_title="Number of Flights"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )


# =========================================================
# CHART 2 - TOP DESTINATION AIRPORTS
# =========================================================

st.subheader("🌍 Top Destination Airports")

destination_df = run_query("""
    SELECT
        destination_iata,
        COUNT(*) AS total_flights
    FROM flights
    WHERE destination_iata IS NOT NULL
    GROUP BY destination_iata
    ORDER BY total_flights DESC
    LIMIT 10
""")

if not destination_df.empty:

    fig2 = px.bar(
        destination_df,
        x="destination_iata",
        y="total_flights",
        title="Top 10 Destination Airports",
        text="total_flights"
    )

    fig2.update_layout(
        xaxis_title="Destination Airport",
        yaxis_title="Number of Flights"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# =========================================================
# CHART 3 - AIRLINE FLIGHT COUNT
# =========================================================

st.subheader("🏢 Flights by Airline")

airline_chart = run_query("""
    SELECT
        airline_code,
        COUNT(*) AS total_flights
    FROM flights
    WHERE airline_code IS NOT NULL
    GROUP BY airline_code
    ORDER BY total_flights DESC
""")

if not airline_chart.empty:

    fig3 = px.pie(
        airline_chart,
        names="airline_code",
        values="total_flights",
        title="Flight Distribution by Airline"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )


# =========================================================
# CHART 4 - AIRPORT DELAYS
# =========================================================

st.subheader("⏱️ Airport Delay Analysis")

delay_chart = run_query("""
    SELECT
        airport_iata,
        AVG(avg_delay_min) AS average_delay
    FROM airport_delays
    GROUP BY airport_iata
    ORDER BY average_delay DESC
""")

if not delay_chart.empty:

    fig4 = px.bar(
        delay_chart,
        x="airport_iata",
        y="average_delay",
        title="Average Delay by Airport",
        text_auto=".2f"
    )

    fig4.update_layout(
        xaxis_title="Airport",
        yaxis_title="Average Delay (Minutes)"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )


st.divider()


# =========================================================
# AIRPORT DETAILS
# =========================================================

st.subheader("🏢 Airport Details")

airport_df = run_query("""
    SELECT
        airport_iata,
        airport_name,
        city,
        country
    FROM airport
    ORDER BY airport_iata
""")

if not airport_df.empty:

    st.dataframe(
        airport_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# =========================================================
# BUSIEST ROUTES
# =========================================================

st.subheader("🛣️ Busiest Flight Routes")

route_df = run_query("""
    SELECT
        origin_iata,
        destination_iata,
        COUNT(*) AS total_flights
    FROM flights
    WHERE origin_iata IS NOT NULL
      AND destination_iata IS NOT NULL
    GROUP BY origin_iata, destination_iata
    ORDER BY total_flights DESC
    LIMIT 10
""")

if not route_df.empty:

    route_df["route"] = (
        route_df["origin_iata"]
        + " → "
        + route_df["destination_iata"]
    )

    st.dataframe(
        route_df[
            ["route", "total_flights"]
        ],
        use_container_width=True,
        hide_index=True
    )


st.divider()


# =========================================================
# SEARCH FLIGHT
# =========================================================

st.subheader("🔍 Search Flight")

search_text = st.text_input(
    "Enter Flight Number or Airline Code"
)

if search_text:

    search_query = """
        SELECT
            flight_id,
            flight_number,
            aircraft_registration,
            origin_iata,
            destination_iata,
            scheduled_departure,
            actual_departure,
            scheduled_arrival,
            actual_arrival,
            status,
            airline_code
        FROM flights
        WHERE flight_number LIKE %s
           OR airline_code LIKE %s
        ORDER BY scheduled_departure DESC
    """

    search_value = "%" + search_text + "%"

    search_df = run_query(
        search_query,
        (search_value, search_value)
    )

    if not search_df.empty:

        st.dataframe(
            search_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning("No matching flight found.")


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    ### ✈️ Air Tracker - Flight Analytics

    **Technology:** Python | MySQL | Pandas | Plotly | Streamlit

    **Project Domain:** Aviation / Data Analytics
    """
)

