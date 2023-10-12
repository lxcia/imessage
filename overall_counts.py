import pandas as pd

# Takes CSVs of CONVERSATION, DATE, MESSAGE COUNT and outputs DATE, TOTAL MESSAGE COUNT
# Sum of messages sent across all conversations that date
def overall_counts():
    csv_files = ["1-alex.csv", "1-brother.csv", "1-csbridge.csv", "1-familychat.csv", "1-floss.csv", "1-mom.csv", "1-researchchat.csv", "1-teachingchat.csv"]
    combined_data = pd.DataFrame()
    for file in csv_files:
        df = pd.read_csv(file)
        combined_data = combined_data.append(df, ignore_index=True)
    result = combined_data.groupby('DATE')['MESSAGE COUNT'].sum().reset_index()
    result.to_csv('overall_counts.csv', index=False)

if __name__ == '__main__':
    overall_counts()