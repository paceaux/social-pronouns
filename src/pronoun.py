import re

from src.regexes import PROFANITY_REGEX, NEGATION_REGEX, AFFIRMATION_REGEX, EMOJI_REGEX

def regexp(expression, text, search=re.search):
    """Provides a regex function for SQL Lite

    Args:
        expression (string): regular expression
        text (string): text to search
    """
    return 1 if search(expression, text) else 0

class PronounCollection:
    """
    A collection class for handling and analyzing posts associated with a specific pronoun
    from a database connection. Provides methods to retrieve rows and compute frequencies
    of profanities, negations, affirmations, and emojis in the messages.

    Attributes:
        pronoun (str): The pronoun to filter posts by.
        connection (sqlite3.Connection): The SQLite database connection.
        rows (list): Cached list of all rows for the pronoun.
    """

    def __init__(self, pronoun_name, connection):
        """
        Initializes the PronounCollection with a pronoun and a database connection.

        Args:
            pronoun_name (str): The pronoun to filter posts by.
            connection (sqlite3.Connection): The SQLite database connection.
        """
        self.pronoun = pronoun_name
        self.connection = connection
        self.rows = self.get_all_rows()
    
    def get_frequency_dict(self, regex, no_flags = False):
        freq_dict = {}
        if not regex:
            raise ValueError("A Regular expression must be provided")

        for row in self.rows:
            message = row[3].strip()
            search_results = re.findall(regex, message, flags=re.IGNORECASE) if not no_flags else re.findall(regex, message)

            for result_tuple in search_results:
                result_list = [item for item in list(result_tuple) if item !='']
                result = result_list[0]
                cleaned = result.lower().strip()
                if cleaned in freq_dict:
                    count = freq_dict.get(cleaned) + 1
                    freq_dict[cleaned] = count
                else:
                    freq_dict[cleaned] = 1

        return freq_dict
        
    def get_all_rows(self):
        """
        Retrieves all rows from the 'post' table where the pronoun matches self.pronoun.

        Returns:
            list: All rows from the database for the specified pronoun.
        """
        cursor = self.connection.cursor()
        query = f"SELECT * FROM post WHERE post.pronoun='{self.pronoun}'"

        cursor.execute(query)
        rows = cursor.fetchall()

        self.rows = rows
        self.connection.commit()

        return rows

    def get_profanity_frequencies(self):
        """
        Counts the frequency of each profanity found in the messages.

        Returns:
            dict: A dictionary mapping each profanity (str) to its occurrence count (int).
        """
        freq_dict = self.get_frequency_dict(PROFANITY_REGEX)
        sorted_dict = dict(sorted(freq_dict.items(), key=lambda item:item[1], reverse=True))

        return sorted_dict
    
    def get_profanity_rows(self):
        """
        Retrieves all rows where the message contains a profanity.

        Returns:
            list: Rows where a profanity is present in the message.
        """
        rows_with_term = []
        
        for row in self.rows:
            message = row[3].strip()
            has_result = re.findall(PROFANITY_REGEX, message, flags=re.IGNORECASE)
            if (has_result):
                rows_with_term.append(row)
        
        return rows_with_term

    def get_negation_frequencies(self):
        """
        Counts the frequency of each negation found in the messages.

        Returns:
            dict: A dictionary mapping each negation (str) to its occurrence count (int).
        """
        freq_dict = self.get_frequency_dict(NEGATION_REGEX)
        sorted_dict = dict(sorted(freq_dict.items(), key=lambda item:item[1], reverse=True))
        return sorted_dict

    def get_negation_rows(self):
        """
        Retrieves all rows where the message contains a negation.

        Returns:
            list: Rows where a negation is present in the message.
        """
        rows_with_term = []
        
        for row in self.rows:
            message = row[3].strip()
            has_result = re.search(NEGATION_REGEX, message, flags=re.IGNORECASE)
            if (has_result):
                rows_with_term.append(row)
        
        return rows_with_term
    
    def get_affirmation_frequencies(self):
        """
        Counts the frequency of each affirmation found in the messages.

        Returns:
            dict: A dictionary mapping each affirmation (str) to its occurrence count (int).
        """
        freq_dict = self.get_frequency_dict(AFFIRMATION_REGEX)
        sorted_dict = dict(sorted(freq_dict.items(), key=lambda item:item[1], reverse=True))
        return sorted_dict
        
    def get_affirmation_rows(self):
        """
        Retrieves all rows where the message contains an affirmation.

        Returns:
            list: Rows where a negation is present in the message.
        """
        rows_with_term = []
        
        for row in self.rows:
            message = row[3].strip()
            has_result = re.search(AFFIRMATION_REGEX, message, flags=re.IGNORECASE)
            if (has_result):
                rows_with_term.append(row)
        
        return rows_with_term
    
    def get_emoji_frequencies(self):
        """
        Counts the frequency of each emoji found in the messages.

        Returns:
            dict: A dictionary mapping each emoji (str) to its occurrence count (int).
        """
        freq_dict = self.get_frequency_dict(EMOJI_REGEX, True)
        sorted_dict = dict(sorted(freq_dict.items(), key=lambda item:item[1], reverse=True))
        return sorted_dict

    def get_emoji_rows(self):
        """
        Retrieves all rows where the message contains an emoji.

        Returns:
            list: Rows where an emoji is present in the message.
        """
        rows_with_term = []
        
        for row in self.rows:
            message = row[3].strip()
            has_result = re.search(EMOJI_REGEX, message)
            if (has_result):
                rows_with_term.append(row)
        
        return rows_with_term