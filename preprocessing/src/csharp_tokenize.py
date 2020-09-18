from antlr4 import *
from preprocessing.src.csharp.CSharpParser import CSharpParser
from preprocessing.src.csharp.CSharpLexer import CSharpLexer
from preprocessing.src.tokenize_common import process_string, indent_lines, unprocess_string

import re

"""
CSharp Tokens
"""
CSHARP_TOKEN2CHAR = {'STOKEN0': "//",
                    'STOKEN1': "/*",
                    'STOKEN2': "*/",
                    'STOKEN3': "/**",
                    'STOKEN4': "**/",
                    'STOKEN5': '"""',
                    'STOKEN6': '\\n'
                    }
CSHARP_CHAR2TOKEN = {"//": ' STOKEN0 ',
                    "/*": ' STOKEN1 ',
                    "*/": ' STOKEN2 ',
                    "/**": ' STOKEN3 ',
                    "**/": ' STOKEN4 ',
                    '"""': ' STOKEN5 ',
                    '\\n': ' STOKEN6 '
                    }

def cs_is_comment(token : Token):
    t = token.type
    return CSharpLexer.SINGLE_LINE_COMMENT <= t and t <= CSharpLexer.DELIMITED_COMMENT

CS_STRING_TYPES = {CSharpLexer.FORMAT_STRING, CSharpLexer.REGULAR_STRING, CSharpLexer.INTERPOLATION_STRING}

def cs_is_string(token : Token):
    t = token.type
    return t  in CS_STRING_TYPES

CS_SKIP_TYPES = {CSharpLexer.WHITESPACES, CSharpLexer.DIRECTIVE_WHITESPACES}

def cs_should_skip(token : Token):
    t = token.type
    return t in CS_SKIP_TYPES

def tokens_of(s):
    assert isinstance(s, str)
    stream = InputStream(s.replace(r'\r', ''))
    lexer = CSharpLexer(stream)
    return lexer.getAllTokens()

def tokenize_csharp(s, keep_comments=False):
    try:
        tokens = []
        for token in tokens_of(s):
            if not keep_comments and cs_is_comment(token):
                continue
            if cs_is_string(token):
                com = process_string(token.text, CSHARP_CHAR2TOKEN, CSHARP_TOKEN2CHAR, False)
                tokens.append(com)
            elif not cs_should_skip(token):
                tokens.append(token.text)
        return tokens
    except KeyboardInterrupt:
        raise

line_breaking_tokens = {
    CSharpLexer.CLOSE_BRACE,
    CSharpLexer.OPEN_BRACE,
    CSharpLexer.SEMICOLON,
    CSharpLexer.DELIMITED_COMMENT,
    CSharpLexer.COMMENTS_CHANNEL,
    CSharpLexer.SINGLE_LINE_COMMENT
}

def detokenize_csharp(s):
    assert isinstance(s, list)            
    if isinstance(s, list):
        s = ' '.join(s)
    assert isinstance(s, str)
    try:
        tokens = tokens_of(s)
        untok_s = []
        for token in tokens:
            if cs_is_string(token):
                unprocessed = unprocess_string(token.text, False)
                untok_s.append(unprocessed)
            else:
                untok_s.append(token.text)
        return ' '.join(untok_s)
    except KeyboardInterrupt:
        raise