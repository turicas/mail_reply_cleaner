#!/usr/bin/env python2
# coding: utf-8

# Copyright (c) 2012 Álvaro Justen <alvarojusten@gmail.com>
# License: GPLv3+ <https://www.gnu.org/licenses/gpl-3.0.html>

import unittest

from textwrap import dedent

from mail_reply_cleaner import clean_mail


class TestMailCleaner(unittest.TestCase):
    def test_should_raise_ValueError_if_string_is_not_unicode(self):
        with self.assertRaises(ValueError):
            clean_mail('this is a test')

    def test_normal_mail_should_return_same_string_stripped(self):
        text = dedent(u'''
        this is a normal message
        without signature
        and without '>' in the start of lines
        ''')
        result = clean_mail(text)
        self.assertEqual(result, text.strip())
        self.assertEqual(type(result), unicode)

    def test_should_remove_signature(self):
        text = dedent(u'''
        this is a normal message
        without signature
        and without '>' in the start of lines

        --
        this is a signature
        ''').strip()
        expected = dedent(u'''
        this is a normal message
        without signature
        and without '>' in the start of lines
        ''').strip()
        result = clean_mail(text)
        self.assertEqual(result, expected)

        text_2 = dedent(u'''
        this is a normal message
        without signature
        and without '>' in the start of lines

        --
        this is NOT a signature
        bla bla bla

        ----
        bla bla bla

        --
        this IS a signature!
        ''').strip()
        expected_2 = dedent(u'''
        this is a normal message
        without signature
        and without '>' in the start of lines

        --
        this is NOT a signature
        bla bla bla

        ----
        bla bla bla
        ''').strip()
        result_2 = clean_mail(text_2)
        self.assertEqual(result_2, expected_2)

    def test_should_remove_lines_that_starts_with_reply_symbol(self):
        text = dedent(u'''
        this is a normal message

        > without signature
        > and without '>' in the start of lines
        ''').strip()
        expected = dedent(u'''
        this is a normal message
        ''').strip()
        result = clean_mail(text)
        self.assertEqual(result, expected)

    def test_should_remove_lines_that_starts_with_reply_symbol_only_if_in_the_end(self):
        text = dedent(u'''
        this is a normal message

        > without signature
        > and without '>' in the start of lines
        > this should not be removed

        here some text

        > this should be removed
        ''').strip()
        expected = dedent(u'''
        this is a normal message

        > without signature
        > and without '>' in the start of lines
        > this should not be removed

        here some text
        ''').strip()
        result = clean_mail(text)
        self.assertEqual(result, expected)

    def test_should_remove_one_line_just_before_the_reply_symbol(self):
        text = dedent(u'''
        this is a normal message

        On 2012-10-22 <someone@mail> wrote:
        > without signature
        > and without '>' in the start of lines
        > this should not be removed
        ''').strip()
        expected = dedent(u'''
        this is a normal message
        ''').strip()
        result = clean_mail(text)
        self.assertEqual(result, expected)

        text_2 = dedent(u'''
        this is a normal message

        On 2012-10-22 <someone@mail> wrote:
        > without signature
        > and without '>' in the start of lines
        > this should not be removed

        bla bla bla
        ''').strip()
        expected_2 = dedent(u'''
        this is a normal message

        On 2012-10-22 <someone@mail> wrote:
        > without signature
        > and without '>' in the start of lines
        > this should not be removed

        bla bla bla
        ''').strip()
        result_2 = clean_mail(text_2)
        self.assertEqual(result_2, expected_2)

        text_3 = dedent(u'''
        this is a normal message

        On 2012-10-22 <someone@mail> wrote:
        > without signature
        > and without '>' in the start of lines
        > this should not be removed

        bla bla bla

        On 2012-10-21 <other@mail> wrote:
        > spam
        > eggs
        > ham
        ''').strip()
        expected_3 = dedent(u'''
        this is a normal message

        On 2012-10-22 <someone@mail> wrote:
        > without signature
        > and without '>' in the start of lines
        > this should not be removed

        bla bla bla
        ''').strip()
        result_3 = clean_mail(text_3)
        self.assertEqual(result_3, expected_3)

        text_4 = dedent(u'''
        this is a normal message

        On 2012-10-22 <someone@mail> wrote:
        > without signature
        > and without '>' in the start of lines
        > this should not be removed

        bla bla bla

        On 2012-10-21 <other@mail> wrote:
        > spam
        > eggs
        > ham

        spam eggs ham

        --
        my signature
        multiline
        ''').strip()
        expected_4 = dedent(u'''
        this is a normal message

        On 2012-10-22 <someone@mail> wrote:
        > without signature
        > and without '>' in the start of lines
        > this should not be removed

        bla bla bla

        On 2012-10-21 <other@mail> wrote:
        > spam
        > eggs
        > ham

        spam eggs ham
        ''').strip()
        result_4 = clean_mail(text_4)
        self.assertEqual(result_4, expected_4)

        text_5 = dedent(u'''
        this is a normal message

        On 2012-10-22 <someone@mail> wrote:
        > without signature
        > and without '>' in the start of lines
        > this should not be removed

        bla bla bla

        On 2012-10-21 <other@mail> wrote:
        > spam
        > eggs
        > ham


        --
        my signature
        multiline
        ''').strip()
        expected_5 = dedent(u'''
        this is a normal message

        On 2012-10-22 <someone@mail> wrote:
        > without signature
        > and without '>' in the start of lines
        > this should not be removed

        bla bla bla
        ''').strip()
        result_5 = clean_mail(text_5)
        self.assertEqual(result_5, expected_5)

        text_6 = dedent(u'''
        this is a normal message

        On 2012-10-22 <someone@mail> wrote:

        > without signature
        > and without '>' in the start of lines
        > this should not be removed

        --
        spam
        eggs ham

        ''').strip()
        expected_6 = dedent(u'''
        this is a normal message
        ''').strip()
        result_6 = clean_mail(text_6)
        self.assertEqual(result_6, expected_6)

        text_7 = dedent(u'''
        this is a normal message

        this line has @ but not numbers

        > without signature
        > and without '>' in the start of lines
        > this should not be removed
        ''').strip()
        expected_7 = dedent(u'''
        this is a normal message

        this line has @ but not numbers
        ''').strip()
        result_7 = clean_mail(text_7)
        self.assertEqual(result_7, expected_7)

    #TODO: test for empty strings
