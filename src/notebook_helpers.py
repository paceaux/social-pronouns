import re
from datetime import datetime

def uriToUrl(atUri: str) -> str:
    """converts Bluesky URI to bluesky URL

    Args:
        atUri (str): raw URI

    Raises:
        Exception: An error if it isn't sent a string

    Returns:
        str: an https string
    """
    regex = re.compile("^at://([^/]+)/([^/]+)/([^/]+)$", re.IGNORECASE)
    match = regex.findall(atUri)

    if not isinstance(atUri, str):
        raise Exception('this only converts strings')
    
    if match is None:
        return atUri


    did, collection, rkey = match[0]

    if collection == 'app.bsky.feed.post':
        return f"https://bsky.app/profile/{did}/post/{rkey}"
    else:
        return atUri

make_link = lambda s: f'<a href="{uriToUrl(s)}">Post</a>'

def mark(text: str, pattern) -> str:
    """Wraps instances of a term with <mark>

    Args:
        text (str): full text
        pattern (str): a regular expression

    Raises:
        Exception: An error for the wrong type

    Returns:
        str: a string with all instances wrapped
    """
    if not isinstance(text, str):
        raise Exception('this only converts strings')
    regex = re.compile(f"\\b{pattern}\\b", re.IGNORECASE)
    new_text = re.sub(regex, '<mark>\\1</mark>', text)

    return new_text

def format_time(text: str) -> str:
    dt = datetime.fromisoformat(text)
    date = dt.date()
    time = dt.time()
    return f'{date.strftime("%b %d, %Y")} {time.strftime("%I:%M%p")}'

prettify_time = lambda s: f'{format_time(s)}'

def get_frequency_dict(rows, regex, no_flags= False):
    """Creates a dictionary of frequencies

    Args:
        rows ([str]): rows from the database
        regex (str): the regular expression pattern
        no_flags (bool, optional): Turns off the flags. Defaults to False.

    Raises:
        ValueError: An error if stuff goes wrong

    Returns:
        dict: A key value dictionary where the value will the <n> occurences
    """
    freq_dict = {}
    if not regex:
        raise ValueError("A Regular expression must be provided")

    for row in rows:
        message = row[2].strip()
        if isinstance(regex, re.Pattern):
            search_results = re.findall(regex, message)
        else:
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