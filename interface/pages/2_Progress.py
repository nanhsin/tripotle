import streamlit as st
import altair as alt
import pandas as pd
from datetime import datetime, timedelta
import pyarrow

st.title("🎵 LyricsMaster")
st.subheader("Let's check your progress!")
st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])

def progress_left():
    with col1:
        st.subheader("Learner A")
        st.write("ID: ilovelyrics")
        st.write("Time Spent: 3 days 15 mins")


data = {
    "Date": ["2025/02/20", "2025/02/21", "2025/02/22", "2025/02/23", "2025/02/24", "2025/02/25", "2025/02/26", "2025/02/27", "2025/02/28"],
    "Saved": [3, 6, 4, 5, 3, 6, 4, 4, 5],
    "Reviewed": [2, 4, 4, 2, 1, 3, 2, 4, 2],
}

df = pd.DataFrame(data)
df["Date"] = pd.to_datetime(df["Date"])

# --- Reshape for Altair ---
df_melted = df.melt("Date", var_name="Status", value_name="Count")

# --- Altair Bar Chart ---
chart = alt.Chart(df_melted).mark_bar().encode(
    x=alt.X("yearmonthdate(Date):O", title="Date", axis=alt.Axis(labelAngle=-45)),
    y=alt.Y("Count:Q"),
    color=alt.Color("Status:N", scale=alt.Scale(range=["#A9CCE3", "#21618C"])),
    # column="Status:N",
    xOffset="Status:N"
).properties(
    width=300,
    height=300,
    title="Vocabulary Progress for the Past Month"
)
# .configure_title(
#     fontSize=16,
#     anchor='start'
# )


def progress_right():
    with col2:
        # st.write("In progress")
        st.altair_chart(chart, use_container_width=True)

# def progress_page():
#     # Page title and header
#     st.title("English Music Recommender")
#     st.markdown("Let's check out your progress!")
#     st.markdown("---")

#     # User information section
#     col1, col2 = st.columns(2)
#     with col1:
#         st.subheader("Rita Wang")
#         st.write("ID: ritaycw")
#     with col2:
#         st.write("Age: 26-30")
#         st.write("Level: Easy")
#         st.write("Time Spent: 3 days _ mins")

#     st.markdown("---")

    # # Progress section
    # st.subheader("Song Progress for the Past Month")

    # # Create sample data for the chart with consistent lengths
    # num_days = 30  # Last 30 days
    # dates = pd.date_range(datetime.now() - timedelta(days=num_days-1), datetime.now(), freq='D')

    # # Generate consistent length arrays
    # learned = [5 + i*2 for i in range(num_days)]  # Linear progression
    # completed = [2 + i*2 for i in range(num_days)]  # Linear progression

    # # Ensure all arrays have the same length
    # assert len(dates) == len(learned) == len(completed), "Arrays must be of equal length"

    # progress_data = pd.DataFrame({
    #     'Date': dates,
    #     'Learned': learned,
    #     'Completed': completed
    # })

    # # Melt the data for Altair
    # melted_data = progress_data.melt('Date', var_name='Progress Type', value_name='Count')

    # # Create Altair chart
    # chart = alt.Chart(melted_data).mark_line(point=True).encode(
    #     x='Date:T',
    #     y='Count:Q',
    #     color='Progress Type:N',
    #     tooltip=['Date', 'Progress Type', 'Count']
    # ).properties(
    #     width=700,
    #     height=400,
    #     title='Song Progress Over the Past Month'
    # ).interactive()
    
    # st.altair_chart(chart)
    
    # # Progress lists
    # col1, col2 = st.columns(2)
    # with col1:
    #     st.markdown("**Learned**")
    #     st.write("- Shape of You")
    #     st.write("- Perfect")
    #     st.write("- Thinking Out Loud")
    
    # with col2:
    #     st.markdown("**Completed**")
    #     st.write("- Photograph")
    #     st.write("- Castle on the Hill")
    #     st.write("- Galway Girl")

# Run the page
if __name__ == "__main__":
    progress_left()
    progress_right()