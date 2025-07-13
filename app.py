# app.py

# STEP 1: IMPORT THE LIBRARIES
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# STEP 2: DEFINE THE "BRAIN" OF THE BOT (This is the same as before)
def analyze_data(df):
    """
    Performs basic data analysis and generates a plot.
    """
    # --- Get a summary of the data ---
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_summary = buffer.getvalue()
    statistical_summary = df.describe().to_string()
    full_summary = "DATA INFORMATION:\n" + info_summary + "\n\nSTATISTICAL SUMMARY:\n" + statistical_summary

    # --- Generate a plot (a histogram of the first numerical column) ---
    fig, ax = plt.subplots() # Create a figure and axis object for the plot
    numerical_cols = df.select_dtypes(include=['number']).columns

    if not numerical_cols.empty:
        first_numerical_col = numerical_cols[0]
        df[first_numerical_col].hist(ax=ax) # Draw the histogram on the axis
        ax.set_title(f'Histogram of {first_numerical_col}')
        ax.set_xlabel(first_numerical_col)
        ax.set_ylabel('Frequency')
    else:
        fig = None # If there's no numerical data, there's no figure to return

    return full_summary, fig

#
# STEP 3: BUILD THE STREAMLIT USER INTERFACE
# This replaces the ipywidgets code from Colab.
#

# Set the title of the web app
st.title('My First Data Analyst Bot')
st.write("Upload your CSV file and the bot will provide a quick analysis!")

# Create the file uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# This 'if' block runs automatically when a file is uploaded
if uploaded_file is not None:
    # Read the uploaded CSV file into a pandas DataFrame
    df = pd.read_csv(uploaded_file)

    # Show a "spinner" while the analysis is running
    with st.spinner('Analyzing your data...'):
        # Run the analysis function on the data
        summary, plot_figure = analyze_data(df)

        st.success('Analysis Complete!')

        # Display the results on the webpage
        st.header("Data Preview")
        st.dataframe(df.head()) # Show the first few rows of the data

        st.header("Data Summary")
        st.text(summary) # Show the text summary

        if plot_figure:
            st.header("Generated Plot")
            st.pyplot(plot_figure) # Display the matplotlib chart
        else:
            st.warning("Could not generate a plot as no numerical data was found in the file.")