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

            # --- Extract Date Info for Header ---
            # Search for a column with 'date' in its name
            date_col = next((col for col in df_audit.columns if 'date' in col.lower()), None)
            header_title = "GP GLM Auditor's Salary"
            header_date_range = "Visit Date: [Date Not Found]"
            
            if date_col:
                # Attempt to parse dates
                try:
                    df_audit[date_col] = pd.to_datetime(df_audit[date_col])
                    valid_dates = df_audit[date_col].dropna()
                    if not valid_dates.empty:
                        start_date = valid_dates.min()
                        end_date = valid_dates.max()
                        
                        # Format: dd-Month-yyyy
                        start_str = start_date.strftime('%d-%B-%Y')
                        end_str = end_date.strftime('%d-%B-%Y')
                        
                        header_date_range = f"Visit Date: {start_str} to {end_str}"
                        # Salary month based on end date: e.g., December'2025
                        header_title = f"GP GLM Auditor's Salary- {end_date.strftime('%B')}'{end_date.year}"
                except Exception:
                    pass

            # Group by auditor name (assigned_to) for audit performance
            auditor_performance = df_audit.groupby('assigned_to').apply(lambda group: pd.Series({
                'audit_visited': group['visit_id'].nunique(),
                're_audit_visited': group['re_audited'].sum(),
                'mismatch_found_no_audit': group[group['re_audited'] == True]['mismatch_found_in_reaudit'].eq(False).sum(),
                'mismatch_found_yes_audit': group[group['re_audited'] == True]['mismatch_found_in_reaudit'].eq(True).sum()
            })).reset_index()

            # Calculate % for logic (keep as float)
            auditor_performance['mismatch_rate'] = (
                auditor_performance['mismatch_found_yes_audit'] / auditor_performance['re_audit_visited']
            ).fillna(0)

            # Performance Calculations
            unit_price = 3
            auditor_performance['Unit Price'] = unit_price
            auditor_performance['Max Payable'] = auditor_performance['audit_visited'] * unit_price
            auditor_performance['Fixed (75%)'] = auditor_performance['Max Payable'] * 0.75
            auditor_performance['Variable (25%)'] = (auditor_performance['Max Payable'] * 0.25) * (1 - auditor_performance['mismatch_rate'])
            auditor_performance['Actual Payable'] = auditor_performance['Fixed (75%)'] + auditor_performance['Variable (25%)']
            
            # Final Percentage for display
            auditor_performance['% Mismatch in Re-Audit'] = auditor_performance['mismatch_rate'] * 100

            # Rename columns for display
            auditor_performance.rename(columns={
                'assigned_to': 'Auditor Name',
                'audit_visited': 'Audited Visit',
                're_audit_visited': 'Re-Audited Visit',
                'mismatch_found_no_audit': 'Mismatch No',
                'mismatch_found_yes_audit': 'Mismatch Yes'
            }, inplace=True)

            # --- Process MFS Data ---
            df_mfs = pd.read_csv(mfs_file, header=2)
            mfs_data = df_mfs[['Auditor Name', 'Full Name', 'MFS Number', 'MFS Provider']].copy()
            
            # Ensure MFS Number starts with 0
            mfs_data['MFS Number'] = mfs_data['MFS Number'].apply(lambda x: f"0{int(x)}" if pd.notnull(x) and not str(x).startswith('0') else str(x))

            # --- Merge Data ---
            combined_df = pd.merge(
                auditor_performance,
                mfs_data,
                on='Auditor Name',
                how='left'
            )

            # Insert 'Sl' column at the beginning
            combined_df.insert(0, 'Sl', range(1, len(combined_df) + 1))

            # Add Grand Total row
            numeric_cols = ['Audited Visit', 'Re-Audited Visit', 'Mismatch No', 'Mismatch Yes', 'Max Payable', 'Fixed (75%)', 'Variable (25%)', 'Actual Payable']
            totals = combined_df[numeric_cols].sum()
            
            total_row = pd.DataFrame([{
                'Auditor Name': 'GRAND TOTAL',
                **totals.to_dict(),
                '% Mismatch in Re-Audit': (totals['Mismatch Yes'] / totals['Re-Audited Visit'] * 100) if totals['Re-Audited Visit'] > 0 else 0,
                'Unit Price': ''
            }])
            combined_df = pd.concat([combined_df, total_row], ignore_index=True)

            # Format columns for Frontend
            if '% Mismatch in Re-Audit' in combined_df.columns:
                combined_df['% Mismatch in Re-Audit'] = combined_df['% Mismatch in Re-Audit'].apply(
                    lambda x: f"{round(float(x))}%" if pd.notnull(x) and x != '' else ""
                )

            # Round numeric payment columns to whole numbers for display
            payment_cols = ['Max Payable', 'Fixed (75%)', 'Variable (25%)', 'Actual Payable']
            for col in payment_cols:
                combined_df[col] = combined_df[col].apply(lambda x: round(float(x)) if pd.notnull(x) and x != '' else x)

            cols_to_int = ['Sl', 'Audited Visit', 'Re-Audited Visit', 'Mismatch No', 'Mismatch Yes'] + payment_cols
            for col in cols_to_int:
                if col in combined_df.columns:
                    combined_df[col] = combined_df[col].fillna(0).astype(str).replace(r'\.0$', '', regex=True)
            
            combined_df.replace('0', '', inplace=True)
            combined_df.replace('nan', '', inplace=True)
            combined_df.loc[combined_df['Auditor Name'] == 'GRAND TOTAL', 'Sl'] = ''
            combined_df.fillna('', inplace=True)

            # Reorder columns to match image
            final_cols = [
                'Sl', 'Auditor Name', 'Audited Visit', 'Re-Audited Visit', 'Mismatch No', 'Mismatch Yes', 
                '% Mismatch in Re-Audit', 'Unit Price', 'Max Payable', 'Fixed (75%)', 'Variable (25%)', 
                'Actual Payable', 'Full Name', 'MFS Number', 'MFS Provider'
            ]
            combined_df = combined_df[final_cols]

            # Dynamic Header Display
            st.markdown(f"""
                <div style="text-align: center; border: 1px solid #e6e9ef; padding: 20px; background-color: #f8f9fb; border-radius: 10px; margin-bottom: 20px;">
                    <h1 style="margin: 0; color: #1f365d; font-size: 2em;">{header_title}</h1>
                    <p style="margin: 10px 0 0 0; font-size: 1.25em; color: #4a5568; font-weight: 500;">
                        [{header_date_range}]
                    </p>
                </div>
                """, unsafe_allow_html=True)
            # Using st.dataframe for interactive features like sorting, resizing, and cell selection
            st.dataframe(
                combined_df, 
                use_container_width=True, 
                hide_index=True,
                height=600
            )

            # Add download button for the combined DataFrame
            csv = combined_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Combined Data as CSV",
                data=csv,
                file_name="combined_auditor_performance.csv",
                mime="text/csv",
            )

        except Exception as e:
            st.error(f"An error occurred during file processing: {e}")
    else:
        st.info("Please upload both audit data and MFS data files to see the analysis.")

if __name__ == "__main__":
    main()