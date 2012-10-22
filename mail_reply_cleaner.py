#!/usr/bin/env python2
# coding: utf-8

# Copyright (c) 2012 Álvaro Justen <alvarojusten@gmail.com>
# License: GPLv3+ <https://www.gnu.org/licenses/gpl-3.0.html>

from re import compile as regexp_compile, DOTALL


REGEXP_SIGNATURE = regexp_compile(r'\n--[ ]*\n[^(--)]*$', flags=DOTALL)
REGEXP_NUMBERS = regexp_compile(r'[^0-9]*', flags=DOTALL)

def clean_mail(message):
    '''Clean reply lines from `message`

    `message` must be a `unicode` object. This function will return a new
    `unicode` object with lines cleaned. It will execute the following filters:

    - Remove signature ('--\n' + other lines in the end of message)
    - Remove reply lines (started with '>')
    - Do not remove reply lines if it have reply (example: '> question\nanswer')
    - Remove reply-header lines (example: 'On ... <some@one> wrote:\n> reply'

    started with '>' removed. There is an heuristic
    to remove lines like "On ... some@one wrote:" (that appear just before
    lines started with '>').
    '''
    if type(message) is not unicode:
        raise ValueError('`message` must be Unicode')
    message = message.strip()
    message = REGEXP_SIGNATURE.sub('', message).strip()
    inverted_lines = message.split('\n')[::-1]
    new_message = []
    inside_a_reply = inverted_lines[0].startswith('>')
    for line in inverted_lines:
        is_reply = line.startswith('>')
        if is_reply and inside_a_reply:
            continue
        elif not is_reply and inside_a_reply:
            if not line.strip():
                continue
            else:
                inside_a_reply = False
                is_reply_header = '@' in line and \
                                  len(REGEXP_NUMBERS.sub('', line)) >= 4
                if not is_reply_header:
                    new_message.append(line)
        else:
            new_message.append(line)
            inside_a_reply = False
    return u'\n'.join(new_message[::-1]).strip()
