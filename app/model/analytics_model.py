
import pandas as pd
import streamlit as st

def show_analytics(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        insights = ""

        date_column_pairs = [
            ("Start Date", "End Date"),
            ("Launch Date", "Closure Date"),
            ("Begin Date", "Finish Date"),
            ("Start Date", "End Date"),
            ("Launch Date", "End Date"),
        ]
        
        start_col = None
        end_col = None
        project_name_col = None  

        potential_project_columns = ["Project Title", "Campaign Name", "Project Name", "Title"]
        
        for col in potential_project_columns:
            if col in df.columns:
                project_name_col = col
                break

        for start_name, end_name in date_column_pairs:
            if start_name in df.columns and end_name in df.columns:
                start_col = start_name
                end_col = end_name
                break

        if start_col and end_col:
            df[start_col] = pd.to_datetime(df[start_col])
            df[end_col] = pd.to_datetime(df[end_col])
            
            df['Duration'] = (df[end_col] - df[start_col]).dt.days
            
            longest_duration_row = df.loc[df['Duration'].idxmax()]
            longest_duration = longest_duration_row['Duration']
            longest_project = longest_duration_row[project_name_col] if project_name_col else "Unknown Project"
            
            insights += f"\nLongest project duration:\n  - {longest_duration} days (Project: {longest_project})\n"

        for column in df.columns:
            if column in [start_col, end_col, 'Duration']:
                continue  
            col_data = df[column]
            col_type = col_data.dtype

            if pd.api.types.is_numeric_dtype(col_type):
                max_value = col_data.max()
                min_value = col_data.min()
                
                max_project = df.loc[col_data.idxmax()][project_name_col] if project_name_col else "Unknown Project"
                min_project = df.loc[col_data.idxmin()][project_name_col] if project_name_col else "Unknown Project"
                
                insights += f"\nColumn: {column}\n"
                insights += f"  - Mean: {col_data.mean():.2f}\n"
                insights += f"  - Median: {col_data.median():.2f}\n"
                insights += f"  - Standard Deviation: {col_data.std():.2f}\n"
                insights += f"  - Max: {max_value:.2f} (Project: {max_project})\n"
                insights += f"  - Min: {min_value:.2f} (Project: {min_project})\n"

            elif pd.api.types.is_string_dtype(col_type):
                value_counts = col_data.value_counts()
                most_common_value = value_counts.index[0]
                most_common_count = value_counts.iloc[0]

                if value_counts.nunique() == 1 or (value_counts == most_common_count).all():
                    insights += f"\nColumn: {column}\n"
                    insights += f"  - All values are equally common.\n"
                else:
                    insights += f"\nColumn: {column}\n"
                    insights += f"  - Most common value: {most_common_value} (occurs {most_common_count} times)\n"

            elif pd.api.types.is_datetime64_any_dtype(col_type):
                insights += f"\nColumn: {column}\n"
                insights += f"  - Date range: {col_data.min().date()} to {col_data.max().date()}\n"

            else:
                insights += f"\nColumn: {column}\n"
                insights += f"  - Unique values: {col_data.nunique()}\n"

        if not insights:
            insights = "No actionable insights could be derived from the data."

        return df, insights

    except Exception as e:
        st.error(f"Error processing the file: {e}")
        return None, None
