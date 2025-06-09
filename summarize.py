import sys, re, sqlite3, os, argparse

from src.constants import DEFAULT_DATABASE_FILE, OUTPUT_DIRECTORY, SOCIAL_PRONOUNS

pronoun_list = SOCIAL_PRONOUNS
personal_pronoun_list = ["I", "you", "he", "she", "we", "they"]
preposition_and_conjunction_list = ["and", "with", "for", "to", "from", "before"]


def regexp(expression, text, search=re.search):
    """Provides a regex function for SQL Lite

    Args:
        expression (string): regular expression
        text (string): text to search
    """
    return 1 if search(expression, text) else 0


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


def print_pronoun_count_summary(pronouns, connection, file):
    """Prints out the preposition / conjunction combinations with the pronoun

    Args:
        query_pronoun (string): pronoun
        connection (Connection): connection to the database
        file (TextIOWrapper): file to write to
    """
    intro = "\n## Summary \n"
    table_columns = get_table_columns(["Pronoun", "Count"])
    
    file.write(intro)
    file.write(table_columns)
    
    print(pronouns)
    
    for pronoun in pronouns:
        cursor = connection.cursor()
        query = f"SELECT * FROM post WHERE post.pronoun='{pronoun}'"

        cursor.execute(query)

        output = cursor.fetchall()
        count = len(output)
        file.write(f"| {pronoun} | {count}|\n")
        connection.commit()
        


def print_preps_and_conjunctions(query_pronoun,connection, file):
    """Prints out the preposition / conjunction combinations with the pronoun

    Args:
        query_pronoun (string): pronoun
        connection (Connection): connection to the database
        file (TextIOWrapper): file to write to
    """
    intro = f"\n### &lt;preposition|conjunction&gt; + {query_pronoun} \n"
    table_columns = get_table_columns([f"&lt;preposition / conjunction&gt; + {query_pronoun}", "Count"])
    
    file.write(intro)
    file.write(table_columns)

    
    for word in preposition_and_conjunction_list:
        cursor = connection.cursor()
        query = f"SELECT * FROM post WHERE pronoun='{query_pronoun}' AND text REGEXP('\\b({word})\\s({query_pronoun})')"

        cursor.execute(query)

        output = cursor.fetchall()
        file.write(f"| {word} + {query_pronoun}  | {len(output)} |\n")

        connection.commit()


def print_associated_pronouns(query_pronoun, connection, file):
    """Prints out personal pronouns in the discours with the pronoun

    Args:
        query_pronoun (string): pronoun
        connection (Connection): connection to the database
        file (TextIOWrapper): file to write to
    """
    intro = "\n### Co-occuring Personal Pronouns \n"
    table_columns = get_table_columns(["Personal Pronoun", "Count"])

    file.write(intro)
    file.write(table_columns)
    
    for word in personal_pronoun_list:
        cursor = connection.cursor()
        query = f"SELECT * FROM post WHERE pronoun='{query_pronoun}' AND LOWER(text) REGEXP('\\b({word})\\b')"
        
        cursor.execute(query)
        
        output = cursor.fetchall()
        file.write(f"| {word} | {len(output)} |\n")
        connection.commit()

def print_positions(query_pronoun, connection, file):
    """Prints out the preposition / conjunction combinations with the pronoun

    Args:
        query_pronoun (string): pronoun
        connection (Connection): connection to the database
        file (TextIOWrapper): file to write to
    """
    intro = "\n### Positioning in the Discourse \n"
    table_columns = get_table_columns(["Position", "Count"])

    file.write(intro)
    file.write(table_columns)

    start_query = f"SELECT * FROM post WHERE pronoun='{query_pronoun}' AND LOWER(text) REGEXP('^{query_pronoun}')"
    end_query = f"SELECT * FROM post WHERE pronoun='{query_pronoun}' AND LOWER(text) REGEXP('{query_pronoun}$')"
    middle_query = f"SELECT * FROM post WHERE pronoun='{query_pronoun}' AND LOWER(text) REGEXP('([^^]({query_pronoun})[^$])')"
    solo_query = f"SELECT * FROM post WHERE pronoun='{query_pronoun}' AND LOWER(text) REGEXP('^{query_pronoun}$')"

    position_dict = {
        "start": start_query,
        "middle": middle_query,
        "end": end_query,
        "only": solo_query
    }
    
    for position, query in position_dict.items():
        cursor = connection.cursor()
        cursor.execute(query)
        output = cursor.fetchall()
        file.write(f"| {position} | {len(output)} |\n")
        connection.commit()

def main(argv):
    parser = argparse.ArgumentParser();
    parser.add_argument("-d", "--database", help="relative path to a sqlite database", default=DEFAULT_DATABASE_FILE, type=str)
    parser.add_argument("-o", "--outputFile", help="Name of the summary file", default="summary", type=str)
    args = parser.parse_args()
    
    database_file = args.database
    output_file = f"{OUTPUT_DIRECTORY}/{args.outputFile}.md"
    
    if  not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    try:

        
        with open(output_file, 'w', encoding="utf-8") as file:
            try:
                sqlite_connection = sqlite3.connect(database_file)
                sqlite_connection.create_function('regexp', 2, regexp)
                
                print_pronoun_count_summary(pronoun_list, sqlite_connection, file)
                
                for pronoun in pronoun_list:
                    file.write(f"## {pronoun.capitalize()}\n")
                    print_preps_and_conjunctions( pronoun, sqlite_connection,file)
                    print_positions(pronoun, sqlite_connection, file )
                    print_associated_pronouns( pronoun, sqlite_connection, file)
                    file.write("\n\n")

                sqlite_connection.close()

            except sqlite3.Error as connection_error:
                print('An error occured -', connection_error)

            finally:
                if sqlite_connection:
                    sqlite_connection.close()
                    print('SQLite Connection closed')
    except Exception as main_error:
        print("Kinda all the way failed")
        print(main_error)
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
     