import getopt, sys, sqlite3, re, datetime, os, argparse


from src.pronoun import PronounCollection
from src.constants import DEFAULT_DATABASE_FILE, OUTPUT_DIRECTORY, SOCIAL_PRONOUNS
from src.regexes import NEGATION_REGEX, AFFIRMATION_REGEX, PROFANITY_REGEX, EMOJI_REGEX

def get_cleaned_message(message):
    """
    Cleans a message string by replacing line breaks with HTML <br /> tags and stripping leading/trailing whitespace.

    Args:
        message (str): The input message string to be cleaned.

    Returns:
        str: The cleaned message with line breaks replaced and whitespace removed.
    """
    msg_no_linebreaks = message.replace("\n", "<br />")
    msg_stripped = msg_no_linebreaks.strip()

    return msg_stripped

def get_highlighted_message(message, pattern):
    """
    Highlights all substrings in the message that match the given regex pattern by wrapping them in <mark> HTML tags.

    Args:
        message (str): The input message string to search for matches.
        pattern (str or Pattern): The regular expression pattern to search for in the message.

    Returns:
        str: The message with all matches wrapped in <mark> tags for highlighting.
    """
    pattern = re.compile(pattern, flags= re.VERBOSE | re.IGNORECASE)

    def wrap_in_mark(match):
        value = match.group()
        return f"<mark>{value}</mark>"

    msg_highlighted = pattern.sub(wrap_in_mark, message)
    return msg_highlighted

def get_friendly_date(date_string):
    """Takes a date string and makes it human-readable

    Args:
        date_string (string): date from the database

    Returns:
        string: time string with day, month, year
    """
    friendly = ""
    clean_string = date_string.strip()
    try:
        d = datetime.datetime.fromisoformat(clean_string)
        friendly = d.strftime("%d %b %Y %H:%I:%S")
    except Exception:
        friendly = date_string

    return friendly

def get_table_columns(column_names):
    """Returns the starting part of a markdown table column

    Args:
        column_names (string): pronoun
    """
    table_headers = "\n |"
    table_body_start = "|"

    for column_name in column_names:
        table_headers = table_headers + f" {column_name} |"
        table_body_start = table_body_start + " --- |"

    table_headers = table_headers + "\n"
    table_body_start = table_body_start + "\n"

    return table_headers + table_body_start

def get_usage_table(rows, title, regex):
    title = f"\n## {title} \n"
    table_columns = get_table_columns(["date", "message"])
    table_body = ""
    
    for row in rows:
        date = row[2]
        message = row[3]
        msg_cleaned = get_cleaned_message(message)
        msg_highlighted = get_highlighted_message(msg_cleaned, regex)
        table_body = f"{table_body}|{get_friendly_date(date)}|{msg_highlighted}|\n"

    return f"{title}{table_columns}{table_body}"

def get_frequency_table(rows, title):
    title = f"\n## {title}\n"
    table_columns = get_table_columns(["Term", "Occurences"])
    table_body = ""
    
    for key, value in rows.items():
        table_body = f"{table_body}|{key}|{value}|\n"

    return f"{title}{table_columns}{table_body}"

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--database", help="relative path to a sqlite database", default=DEFAULT_DATABASE_FILE, type=str)
    parser.add_argument("-o", "--outputFile", help="Name of the output file. (If none is given, it will be the pronoun you provided)",)
    parser.add_argument("-p", "--pronoun", help="The social pronoun to analyze", default="bro", choices=SOCIAL_PRONOUNS, type=str)
    parser.add_argument("-s", "--profanities", help="Show all profanities using this pronoun.", action="store_true")
    parser.add_argument("-n", "--negations", help="Show all negations using this pronoun.", action="store_true")
    parser.add_argument("-a","--affirmations", help="Show all affirmations using this pronoun.", action="store_true")
    parser.add_argument("-e","--emojis", help="Show all emojis using this pronoun.", action="store_true")
    parser.add_argument("-u","--usage", help="Show usages for any of your provided parameters.", action="store_true")
    parser.add_argument("--allRows", help="Show all usages using this pronoun. (THIS WILL BE A VERY LARGE FILE)", action="store_true")
    args = parser.parse_args()
    
    social_pronoun = args.pronoun
    database_file = args.database
    
    output_file = f"{OUTPUT_DIRECTORY}/{social_pronoun}.md"
    
    if args.outputFile:
        output_file = f"{OUTPUT_DIRECTORY}/{args.outputFile}.md"

    if  not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    try:
        sqlite_connection = sqlite3.connect(database_file)
        collection = PronounCollection(social_pronoun, sqlite_connection )
    
        with open(output_file, 'w', encoding="utf-8") as file:
            file.write(f"# {social_pronoun}\n")
            all_rows = collection.rows     
            file.write(f"{len(collection.rows)} total rows")        

            if args.profanities:
                profanity_frequencies = collection.get_profanity_frequencies()
                profanity_frequency_table = get_frequency_table(profanity_frequencies, "Associated Profanities")
                file.write(profanity_frequency_table)
                
                if args.usage:
                    profanity_rows = collection.get_profanity_rows()
                    profanity_usage_table = get_usage_table(profanity_rows, "All use of profanity", r"((fuck|dick|ass)\w+)" )
                    file.write(profanity_usage_table)
            
            if args.negations:
                negation_frequencies = collection.get_negation_frequencies()
                negation_frequency_table = get_frequency_table(negation_frequencies, "Associated Negations")
                file.write(negation_frequency_table)
                
                if args.usage:
                    negation_rows = collection.get_negation_rows()
                    negation_usage_table = get_usage_table(negation_rows, "All use of negation", NEGATION_REGEX )
                    file.write(negation_usage_table)

            if args.affirmations:
                affirmation_frequencies = collection.get_affirmation_frequencies()
                affirmations_table = get_frequency_table(affirmation_frequencies, "Associated Affirmations")
                file.write(affirmations_table)

                if args.usage:
                    affirmation_rows = collection.get_affirmation_rows()
                    affirmation_usage_table = get_usage_table(affirmation_rows, "All use of affirmations", AFFIRMATION_REGEX )
                    file.write(affirmation_usage_table)
            
            if args.emojis:
                emoji_frequencies = collection.get_emoji_frequencies()
                emoji_table = get_frequency_table(emoji_frequencies, "Associated emojis")
                file.write(emoji_table)
                
                if args.usage:
                    emoji_rows = collection.get_emoji_rows()
                    affirmation_usage_table = get_usage_table(emoji_rows, "All use of affirmations", AFFIRMATION_REGEX )
                    file.write(affirmation_usage_table)
            
            # DANGER! This will make the file huge! 
            if args.allRows:  
                usage_table = get_usage_table(all_rows, f"All use of {social_pronoun}", social_pronoun)
                file.write(usage_table)
            
    except sqlite3.Error as connection_error:
        print('some DB error happened: ', connection_error)
    
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("SQLite connection closed")


if __name__ == "__main__":
    main(sys.argv[1:])