import streamlit as st
import datetime
import pandas as pd

# Initialize session state for filters
if "filters" not in st.session_state:
    st.session_state.filters = []

st.title("Time Range Filter")
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

def apply_filters(df, filters):
            mask = pd.Series(False, index=df.index)

            for filter in enumerate(filters):
                date_mask = (df[timestamp_col].date() >= filter[1]['start_date']) & (df[timestamp_col].date() <= filter[1]['end_date'])
                time_mask = (df[timestamp_col].time() >= filter[1]['start_time']) & (df[timestamp_col].time() <= filter[1]['end_time'])
                mask = mask | (date_mask & time_mask)
            
            return df[mask]

if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Check if there's a timestamp column
        timestamp_cols = df.select_dtypes(include=['datetime64']).columns
        timestamp_col = st.selectbox(
            "Select the timestamp column:",
            df.columns)
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    
        st.write("Dataset Info:")
        st.write(f"- Total records: {len(df)}")
        st.write(f"- Date range: {df[timestamp_col].min()} to {df[timestamp_col].max()}")

        # Date range selection
        date_range = st.date_input(
            "Select date range",
            value=(df[timestamp_col].min(), df[timestamp_col].max()),
            min_value=df[timestamp_col].min(), max_value=df[timestamp_col].max()
        )

        # Time range selection
        col1, col2 = st.columns(2)

        with col1:
            start_time = st.time_input("Start time", datetime.time(0, 0), step=300)
            
        with col2:
            end_time = st.time_input("End time", datetime.time(23, 59), step=300)

        if st.button("Add Filter"):
            # Create a filter dictionary
            new_filter = {
                "start_date": date_range[0],
                "end_date": date_range[1],
                "start_time": start_time,
                "end_time": end_time
                #"sensor_list": ADD LIST OF SENSORS TO APPLY RULE TO
            }
            
            st.session_state.filters.append(new_filter)
            st.success("Filter added successfully!")

        # Display current filters
        if st.session_state.filters:
            st.subheader("Current Filters")
            for idx, filter in enumerate(st.session_state.filters):
                dis_col1, dis_col2 = st.columns(2)
                with dis_col1:
                    st.write(f"Filter {idx + 1}:")
                    st.write(f"Date Range: {filter['start_date']} to {filter['end_date']}")
                    st.write(f"Time Range: {filter['start_time']} to {filter['end_time']}")
                with dis_col2:
                    if st.button("❌", key=f"delete_{idx}"):
                        st.session_state.filters.pop(idx)
                        st.rerun()

            if st.button("Clear All Filters"):
                st.session_state.filters = []
                st.success("All filters cleared!")

        st.subheader("Display filtered data:")
        if st.button("Apply Filters"):
            st.write(st.session_state.filters)
            #apply_filters(df, st.session_state.filters)
            st.success("Filters successfully applied")

            '''
            apply_filters(df, st.session_state.filters)
            '''

    except Exception as e:
        st.error(f"Error processing the file: {str(e)}")
else:
    st.info("Please upload a CSV file to begin.")
