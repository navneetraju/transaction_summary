import pandas as pd
import xlsxwriter
from io import BytesIO

def generate_report(df: pd.DataFrame):
    # Calculate the average number of transactions per day
    df = df[['Date', 'Time', 'Trans Num', 'Card #', 'Tender Type']]

    average_number_of_transactions_per_day = round(df.groupby(by=['Date'])[['Trans Num']].nunique().mean().iloc[0], 1)

    n_unique_customers_per_day = df.groupby(by=['Date'])[['Card #']].nunique().rename(
        columns={'Card #': 'Number of Unique Customers'})

    average_unique_customers_per_day = round(n_unique_customers_per_day['Number of Unique Customers'].mean(), 1)

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Summary")

    # --------------------------------------------------------------------
    # 3. Define some formats
    # --------------------------------------------------------------------
    bold_format = workbook.add_format({'bold': True})
    border_format = workbook.add_format({'border': 1})
    bold_border_format = workbook.add_format({'bold': True, 'border': 1})

    # Set column widths (adjust as you like)
    worksheet.set_column(0, 0, 20)  # Column A width
    worksheet.set_column(1, 1, 25)  # Column B width

    # --------------------------------------------------------------------
    # 4. Write the average number of transactions (in bold, with border)
    # --------------------------------------------------------------------
    # If you want the label bold but not the cell with a border, you can do so:
    worksheet.write(0, 0, "Average Number of Transactions per Day", bold_format)
    worksheet.write(0, 1, average_number_of_transactions_per_day, bold_border_format)

    # --------------------------------------------------------------------
    # 5. Write the table of unique customers with an outline
    # --------------------------------------------------------------------
    start_row = 2  # Leave one blank row after the average

    # Write header row with bold + border
    worksheet.write(start_row, 0, "Date", bold_border_format)
    worksheet.write(start_row, 1, "Number of Unique Customers", bold_border_format)

    # Write each row with a border
    row_counter = start_row + 1
    for row_num, (date, row) in enumerate(n_unique_customers_per_day.iterrows(), start=start_row + 1):
        worksheet.write(row_num, 0, str(date), border_format)
        worksheet.write(row_num, 1, row['Number of Unique Customers'], border_format)

    worksheet.write(row_counter+1, 0, "Average Number of Unique Customers per Day", bold_border_format)
    worksheet.write(row_counter+1, 1, average_unique_customers_per_day, bold_border_format)

    # --------------------------------------------------------------------
    # 6. Close and save
    # --------------------------------------------------------------------
    workbook.close()

    return output