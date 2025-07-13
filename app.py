# app.py (The Professional Analyst Bot)

# STEP 1: IMPORT THE LIBRARIES
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

#
# STEP 2: DEFINE THE "BRAIN" OF THE BOT WITH REFINED OUTPUT
#
def professional_analysis(df):
    """
    Performs focused data analysis and returns results in DataFrames for clean display.
    """
    # --- Create a DataFrame for Data Information (Column Types and Non-Null Counts) ---
    info_df = pd.DataFrame({
        "Column": df.columns,
        "Non-Null Count": df.notna().sum(),
        "Data Type": df.dtypes
    }).reset_index(drop=True)

    # --- Get the Statistical Summary as a DataFrame ---
    statistical_summary_df = df.describe().reset_index().rename(columns={'index': 'Metric'})

    analysis_results = {
        "info_df": info_df,
        "statistical_summary_df": statistical_summary_df,
        "correlation_matrix_fig": None
    }

    # --- Generate the Correlation Matrix Figure for Numerical Columns ---
    numerical_cols = df.select_dtypes(include=['number']).columns
    if len(numerical_cols) > 1:
        corr_matrix = df[numerical_cols].corr()
        fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='viridis', fmt=".2f", ax=ax_corr)
        ax_corr.set_title('Correlation Matrix of Numerical Columns', fontsize=16)
        analysis_results["correlation_matrix_fig"] = fig_corr
        
    return analysis_results

#
# STEP 3: BUILD THE PROFESSIONAL STREAMLIT INTERFACE
#
st.set_page_config(layout="wide", page_title="Professional Analyst Bot")

# --- App Title and Description ---
st.title('The Professional Analyst Bot 📈')
st.markdown("""
This advanced tool performs a comprehensive exploratory data analysis. 
Upload your CSV to generate key statistical summaries, correlation heatmaps, and custom visualizations, all presented in a clean, professional format.
""")

# --- File Uploader ---
uploaded_file = st.file_uploader("Upload your CSV file to begin", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.header("Data Preview")
    st.dataframe(df.head())

    # --- Main Analysis Section ---
    with st.spinner('Generating professional analysis report...'):
        analysis = professional_analysis(df)
        st.success('Report Generated!')

    # --- Display Summaries in Professional Tables ---
    st.header("📊 Core Data Summaries")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("1. Data Information (Columns, Types, Non-Nulls)", expanded=True):
            # Displaying the info summary as a proper table
            st.dataframe(analysis['info_df'])

    with col2:
        with st.expander("2. Statistical Summary", expanded=True):
            # Displaying the statistical summary as a proper table
            st.dataframe(analysis['statistical_summary_df'])
            
    # --- Display Correlation Matrix if it exists ---
    if analysis['correlation_matrix_fig']:
        with st.expander("3. Correlation Matrix Heatmap", expanded=True):
            st.pyplot(analysis['correlation_matrix_fig'])
            st.info("""
            **How to Read This Heatmap:** This chart shows the relationship between numerical variables. 
            - Values close to **1.0** (dark green) indicate a strong positive correlation (as one variable increases, the other tends to increase).
            - Values close to **-1.0** (light yellow) indicate a strong negative correlation (as one variable increases, the other tends to decrease).
            - Values near **0** indicate a weak or no linear relationship.
            """)
            
    # --- Interactive Plotting Section ---
    st.header("🎨 Interactive Custom Plotting")
    st.write("Select columns and a plot type to create your own visualizations.")
    
    plot_col1, plot_col2 = st.columns([1, 2]) # Give more space to the plot
    
    with plot_col1:
        plot_type = st.selectbox("Select Plot Type", ["Histogram", "Bar Chart", "Scatter Plot"])
        
        all_columns = df.columns.tolist()
        numerical_columns = df.select_dtypes(include=['number']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

        # Dynamically show options based on plot type
        if plot_type == "Histogram" and numerical_columns:
            selected_col = st.selectbox("Select Numerical Column", numerical_columns)
        elif plot_type == "Bar Chart" and categorical_columns and numerical_columns:
            selected_cat_col = st.selectbox("Select Categorical Column (X-Axis)", categorical_columns)
            selected_num_col = st.selectbox("Select Numerical Column (Y-Axis)", numerical_columns)
        elif plot_type == "Scatter Plot" and len(numerical_columns) >= 2:
            x_axis = st.selectbox("Select X-Axis", numerical_columns, index=0)
            y_axis = st.selectbox("Select Y-Axis", numerical_columns, index=1 if len(numerical_columns) > 1 else 0)

    with plot_col2:
        # Generate and display the selected plot
        fig_interactive, ax_interactive = plt.subplots()
        plot_generated = False

        if plot_type == "Histogram" and 'selected_col' in locals():
            sns.histplot(df[selected_col], kde=True, ax=ax_interactive, color='skyblue')
            ax_interactive.set_title(f'Distribution of {selected_col}')
            plot_generated = True
        elif plot_type == "Bar Chart" and 'selected_cat_col' in locals() and 'selected_num_col' in locals():
            sns.barplot(x=df[selected_cat_col], y=df[selected_num_col], ax=ax_interactive, palette='mako')
            ax_interactive.set_title(f'{selected_num_col} by {selected_cat_col}')
            plt.setp(ax_interactive.get_xticklabels(), rotation=45, ha="right")
            plot_generated = True
        elif plot_type == "Scatter Plot" and 'x_axis' in locals() and 'y_axis' in locals():
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax_interactive, alpha=0.7)
            ax_interactive.set_title(f'{y_axis} vs. {x_axis}')
            plot_generated = True
        
        if plot_generated:
            st.pyplot(fig_interactive)
        else:
            st.info("Please select columns to generate a plot. Some plot types require specific column types (numerical/categorical).")


    # --- Download Report ---
    st.header("⬇️ Download Report")
    report_contents = (
        "PROFESSIONAL DATA ANALYSIS REPORT\n"
        "====================================\n\n"
        "1. DATA INFORMATION\n"
        "-------------------\n" +
        analysis['info_df'].to_string() + "\n\n" +
        "2. STATISTICAL SUMMARY\n"
        "----------------------\n" +
        analysis['statistical_summary_df'].to_string()
    )
    st.download_button(
        label="Download Summaries as .txt File",
        data=report_contents,
        file_name="professional_analysis_report.txt",
        mime="text/plain"
    )

else:
    st.info("Awaiting CSV file upload.")
