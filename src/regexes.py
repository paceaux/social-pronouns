import re


# PROFANITY_REGEX = "((\b)?(fuck)(\w+)?)|((\\b)?shit(\w+)?)|((\\b)dick(\\w+|\\b))|((\\b)ass(\\w+|\\b))|((\\b)cocks?\\b)|((\\b)cunts?\\b)|((\\b)twats?\\b)|(wtf)|(stfu)|((\\b)damn(ed|it)?\b)"
PROFANITY_REGEX = "(\\b|\w*)?((fuck|shit|dick|cock|cunt|twat|damn)(\\w+)?)|(\\b)?(ass(hole|wad|face|head)?)|(wtf|stfu|omfg|fml|lmfao)(\\b)"
NEGATION_REGEX = "\\b(n(o+(pe)?|a+(h|w)?|uh))\\b"
AFFIRMATION_REGEX = "\\b(y((e+|a+|u+)(a+)?(y|h|s|p)?)\\b)"
EMOJI_REGEX =  re.compile(
    "(["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "])"
    )