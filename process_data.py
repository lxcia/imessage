import pandas as pd

# Concatenate all CSVs with CONVERSATION, DATE, MESSAGE for one chart
def combine_counts(file1, file2, file3, file4, file5, file6, file7, file8, output_file):
    df1 = pd.read_csv(file1, parse_dates=['DATE'])
    df2 = pd.read_csv(file2, parse_dates=['DATE'])
    df3 = pd.read_csv(file3, parse_dates=['DATE'])
    df4 = pd.read_csv(file4, parse_dates=['DATE'])
    df5 = pd.read_csv(file5, parse_dates=['DATE'])
    df6 = pd.read_csv(file6, parse_dates=['DATE'])
    df7 = pd.read_csv(file7, parse_dates=['DATE'])
    df8 = pd.read_csv(file8, parse_dates=['DATE'])
    all_dfs = [df1, df2, df3, df4, df5, df6, df7, df8]
    combined_df = pd.concat(all_dfs, ignore_index=True)
    combined_df = combined_df.fillna({'MESSAGE_COUNT': 0})
    combined_df.to_csv(output_file, index=False)

# Get total message count from one conversation in CSVs
def combine_and_calculate_totals(file1, file2, file3, file4, file5, file6, file7, file8, output_file):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df3 = pd.read_csv(file3)
    df4 = pd.read_csv(file4)
    df5 = pd.read_csv(file5)
    df6 = pd.read_csv(file6)
    df7 = pd.read_csv(file7)
    df8 = pd.read_csv(file8)
    combined_data = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8], ignore_index=True)
    result = combined_data.groupby('CONVERSATION')['MESSAGE COUNT'].sum().reset_index()
    result = result.rename(columns={'MESSAGE COUNT': 'TOTAL MESSAGE COUNT'})
    result.to_csv(output_file, index=False)

if __name__ == '__main__':
    file1 = '1-alex.csv'
    file2 = '1-brother.csv'
    file3 = '1-csbridge.csv'
    file4 = '1-familychat.csv'
    file5 = '1-friendchat.csv'
    file6 = '1-mahi.csv'
    file7 = '1-floss.csv'
    file8 = '1-mom.csv'
    output_file = 'combined_output.csv'
    combine_counts(file1, file2, file3, file4, file5, file6, file7, file8, output_file)
    output_file = 'message_totals.csv'
    combine_and_calculate_totals(file1, file2, file3, file4, file5, file6, file7, file8, output_file)