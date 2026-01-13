import streamlit as st
import pandas as pd

def main():
    st.set_page_config(layout="wide") # Set page layout to wide for better use of space
    st.title("Auditor Performance and Salary Analysis")

    # Custom CSS for table alignment and potentially font size (re-adding some for general readability)
    st.markdown("""
        <style>
            /* Left-align the table */
            table {
                margin-left: 0 !important;
                margin-right: auto !important;
            }
            /* General font size for the table content */
            .dataframe {
                font-size: 1.1em; 
            }
            .dataframe th, .dataframe td {
                padding: 8px 10px; /* Adjust padding for better spacing */
            }
        </style>
        """, unsafe_allow_html=True)

    st.sidebar.header("Upload Files")
    audit_file = st.sidebar.file_uploader("Upload Audit Data (CSV or XLSX)", type=["csv", "xlsx"])
    mfs_file = st.sidebar.file_uploader("Upload MFS Data (CSV)", type=["csv"])

    if audit_file is not None and mfs_file is not None:
        try:
            # --- Process Audit Data ---
            if audit_file.name.endswith('.csv'):
                df_audit = pd.read_csv(audit_file)
            else: # .xlsx
                df_audit = pd.read_excel(audit_file)

            # Ensure 're_audited' and 'mismatch_found_in_reaudit' are boolean
            df_audit['re_audited'] = df_audit['re_audited'].astype(bool)
            df_audit['mismatch_found_in_reaudit'] = df_audit['mismatch_found_in_reaudit'].astype(bool)

            # Group by auditor name (assigned_to) for audit performance
            auditor_performance = df_audit.groupby('assigned_to').agg(
                audit_visited=('visit_id', 'nunique'),
                re_audit_visited=('re_audited', lambda x: (x == True).sum()),
                mismatch_found_no_audit=('mismatch_found_in_reaudit', lambda x: (x == False).sum()),
                mismatch_found_yes_audit=('mismatch_found_in_reaudit', lambda x: (x == True).sum())
            ).reset_index()

            # Calculate % of yes count/re-audited for audit data
            auditor_performance['% Mismatch in Re-Audit'] = (
                auditor_performance['mismatch_found_yes_audit'] / auditor_performance['re_audit_visited']
            ).fillna(0) * 100

            # Add Unit Price column
            unit_price = 3
            auditor_performance['Unit Price'] = unit_price
            
            # Calculate Actual Payable based on audit_visited and unit price
            auditor_performance['Calculated Payable'] = auditor_performance['audit_visited'] * auditor_performance['Unit Price']

            # Rename columns for better display
            auditor_performance.rename(columns={
                'assigned_to': 'Auditor Name',
                'audit_visited': 'Audit Visited',
                're_audit_visited': 'Re-Audit Visited (True)',
                'mismatch_found_no_audit': 'Mismatch Found No (Audit)',
                'mismatch_found_yes_audit': 'Mismatch Found Yes (Audit)'
            }, inplace=True)

            # --- Process MFS Data ---
            df_mfs = pd.read_csv(mfs_file, header=2)
            mfs_data = df_mfs[['Auditor Name', 'Full Name', 'MFS Number', 'MFS Provider']].copy()

            # --- Merge Data ---
            combined_df = pd.merge(
                auditor_performance,
                mfs_data,
                on='Auditor Name',
                how='left'
            )

            st.write("### Combined Auditor Performance and Salary Analysis")
            # Display the DataFrame as HTML to avoid Streamlit's default scrolling behavior
            st.markdown(combined_df.to_html(index=False), unsafe_allow_html=True)
            st.info("Note: Displaying the full table as HTML removes interactive features like sorting and column resizing.")

        except Exception as e:
            st.error(f"An error occurred during file processing: {e}")
    else:
        st.info("Please upload both audit data and MFS data files to see the analysis.")

if __name__ == "__main__":
    main()