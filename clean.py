import pandas as pd


def clean_df(df_raw: pd.DataFrame):
    header_row_idx = df_raw.index[
        df_raw.iloc[:, 0].astype(str).str.contains("Date", case=False, na=False)
    ]
    if header_row_idx.empty:
        raise ValueError("Header row not found. Please check the file format.")
    header_row_idx = header_row_idx[0]

    # Slice the DataFrame from the header row onward and set it as the header
    df_cleaned = df_raw.iloc[header_row_idx:].copy()
    df_cleaned.columns = df_cleaned.iloc[0]  # Set the header row as columns
    df_cleaned = df_cleaned[1:]  # Drop the header row from the data

    # -------------------------------
    # 2. Remove footer rows
    # -------------------------------
    # Look for the first row where the first cell starts with "Transaction Count:"
    footer_rows = df_cleaned.index[
        df_cleaned.iloc[:, 0].astype(str).str.startswith("Transaction Count:")
    ]
    if not footer_rows.empty:
        footer_idx = footer_rows[0]
        # Slice off the footer rows (exclude the footer row and any rows after)
        df_cleaned = df_cleaned.loc[:footer_idx - 1]
    return df_cleaned