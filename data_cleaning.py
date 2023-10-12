import emoji
import string
import csv

# TODO: FILL THIS IN -- change to specific conversation label
CONVERSATION = "MAHI"

DATE_COUNTS = {}
WORD_COUNTS = {}
AUTHOR_COUNTS = {}
TIME_COUNTS = {}


# Writes dictionary to specific csv output
def write_dict_to_csv(dictionary, filename):
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # TODO: FILL THIS IN -- change based on desired CSV header
        csv_writer.writerow(['CONVERSATION', 'OMG COUNT'])
        for key, value in dictionary.items():
            csv_writer.writerow([key, value])

# Process text message
def all_caps_with_emojis(input_string):
    words = input_string.split()
    modified_words = []
    for word in words:
        if emoji.emoji_count(word) > 0:
            modified_words.append(word)
        else:
            word = word.strip(string.punctuation)
            modified_words.append(word.upper())
    modified_string = ' '.join(modified_words)
    return modified_string

# Process "date" field --> returns month, day and adjusted 24 HR time
def process_date(date):
    month_mapping = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
        'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
        'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    parts = date.split()
    month_num = month_mapping.get(parts[0], None)
    day = parts[1].rstrip(',')
    time = parts[2][:5]
    am_pm = parts[3]
    full_time = parts[3]
    just_hour = full_time.split(':')[0]
    am_pm_tracker = parts[4]
    # Convert to military time
    if am_pm_tracker == "PM":
        just_hour = int(just_hour) + 12
        just_hour = str(just_hour)
    formatted_date_time = f"{month_num}/{day} {time}{am_pm}"
    return formatted_date_time, just_hour

# Process the raw iMessage .txt file, return cleaned messages with dates, remove replies
def process(filename):
    paragraphs = []
    current_paragraph = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                if line[0] != "":
                    current_paragraph.append(line)
            else:
                if current_paragraph:
                    paragraphs.append(current_paragraph)
                    current_paragraph = []
    if current_paragraph:
        paragraphs.append(current_paragraph)
    # Process spaces to remove reply threads in original file
    labeled_paragraphs = []
    for para in paragraphs:
        original_paragraph = ""
        for item in para:
            original_paragraph += item
        if len(para) >= 3:
            labeled_para = []
            date = para[0]
            print(date)
            author = para[1]
            # Process author of message
            if author not in AUTHOR_COUNTS:
                AUTHOR_COUNTS[author] = 1
            else:
                AUTHOR_COUNTS[author] += 1
            message = para[2]
            # Process date of message
            labeled_para.append("RAW DATE: " + date)
            new_date, hour = process_date(date)
            new_date = new_date.split()[0]
            # Throw an error if something is wrong with the date -- this requires manually changing the .txt input
            if not new_date[0].isdigit():
                raise Exception("This date is not a number: " + new_date + " find this in file to see the problem.")
            labeled_para.append("NEW DATE: " + new_date)
            # Process date and time of message
            if new_date not in DATE_COUNTS:
                DATE_COUNTS[new_date] = 1
            else:
                DATE_COUNTS[new_date] += 1
            if int(hour) not in TIME_COUNTS:
                TIME_COUNTS[int(hour)] = 1
            else:
                TIME_COUNTS[int(hour)] += 1

            # Process messages that are not an image attachment, do not begin with "/User"
            if message[:3] != "/Us":
                # Can use to check processing
                # labeled_para.append("RAW MESSAGE: " + message)
                all_caps_message = all_caps_with_emojis(message)
                # Process message
                for word in all_caps_message.split():
                    if word not in WORD_COUNTS:
                        WORD_COUNTS[word] = 1
                    else:
                        WORD_COUNTS[word] += 1
                labeled_para.append("ALL CAPS MESSAGE: " + all_caps_message)
            labeled_paragraphs.append(labeled_para)
    return labeled_paragraphs


if __name__ == '__main__':
    # TODO: FILL THIS IN --- put specific file to process here
    filename = "floss.txt"
    paragraphs = process(filename)
    # Useful for debugging output
    # for idx, paragraph in enumerate(paragraphs, start=1):
    #     print(f"ITEM {idx}:")
    #     for line in paragraph:
    #         print(line)
    #

    # sort time in chronological order, sort words in descending order by count
    TIME_COUNTS = {k: TIME_COUNTS[k] for k in sorted(TIME_COUNTS)}
    WORD_COUNTS = sorted_dict = dict(sorted(WORD_COUNTS.items(), key=lambda item: item[1], reverse=True))

    # print(DATE_COUNTS)
    # print(WORD_COUNTS)
    # print(AUTHOR_COUNTS)

    # Dictionaries below were hardcoded by examining printed WORD_COUNTS output for each file, selecting top words
    alex_word_counts = {
        'GRIND': 542,
        'INSANE': 503,
        'SLEEP': 484,
        'WORK': 476,
        'STARTUP': 415,
        'SCHOOL': 299,
        'SCAM': 249,
        'DREAM': 241,
        'FAMILY': 234,
        'FOOD': 219,
        'GPU': 198,
        'GRINDING': 195
    }
    friendchat_word_counts = {
        'PAPER': 58,
        'WORK': 53,
        'PUB': 37,
        'AI': 29,
        'STANFORD': 23,
        'ZOOM': 18,
        'RESULTS': 19,
        'RESEARCH': 17,
        'CS': 17,
        'GATES': 17,
        'DINNER': 13,
        'GRIND': 12
    }
    teaching_word_counts = {
        'LECTURE': 27,
        'WORK': 25,
        'KAREL': 23,
        'STUDENTS': 19,
        'CODE': 18,
        'SECTION': 14,
        'PROBLEM': 13,
        'PROBLEMS': 13,
        'SLIDES': 13,
        'CONTINENTAL': 12,
        'FOOD': 12,
        'ATTENDANCE': 12
    }
    research_word_counts = {
        'WORK': 72,
        'SLIDES': 60,
        'PITCH': 54,
        'EMAIL': 50,
        'ZOOM': 43,
        'NOTES': 41,
        'INTERVIEW': 39,
        'CLASS': 30,
        'MONDAY': 30,
        'TEAM': 27,
        'HEALTH': 26,
        'THURSDAY': 24
    }

    # Search WORD_COUNTS output for "OMG" for each file, manually create dict to write to CSV
    omg_counts = {
        'ALEX': 3.132,
        'BROTHER': 0.42,
        'FAMILY CHAT': 0.29,
        'FRIEND CHAT': 4.747,
        'MAHI': 4.593,
        'MOM': 0.86,
        'TEACHING CHAT': 0.74,
        'RESEARCH CHAT': 1.83
    }

    write_dict_to_csv(omg_counts, 'omg-counts.csv')



