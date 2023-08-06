"""

    Greynir: Natural language processing for Icelandic

    Settings module

    Copyright (C) 2020 Miðeind ehf.

    This software is licensed under the MIT License:

        Permission is hereby granted, free of charge, to any person
        obtaining a copy of this software and associated documentation
        files (the "Software"), to deal in the Software without restriction,
        including without limitation the rights to use, copy, modify, merge,
        publish, distribute, sublicense, and/or sell copies of the Software,
        and to permit persons to whom the Software is furnished to do so,
        subject to the following conditions:

        The above copyright notice and this permission notice shall be
        included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
        MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
        IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
        CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
        TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
        SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


    This module reads and interprets the GreynirCorrect.conf
    configuration file. The file can include other files using the $include
    directive, making it easier to arrange configuration sections into logical
    and manageable pieces.

    Sections are identified like so: [ section_name ]

    Comments start with # signs.

    Sections are interpreted by section handlers.

"""

from typing import Dict, Set, List, Tuple
import os
import locale
import threading

from contextlib import contextmanager
from collections import defaultdict

from pkg_resources import resource_stream


# The sorting locale used by default in the changedlocale function
_DEFAULT_SORT_LOCALE = ("IS_is", "UTF-8")
# A set of all valid argument cases
_ALL_CASES = frozenset(("nf", "þf", "þgf", "ef"))
_ALL_GENDERS = frozenset(("kk", "kvk", "hk"))

# A set of all strings that should be interpreted as True
TRUE = {"true", "True", "1", "yes", "Yes"}


@contextmanager
def changedlocale(new_locale=None):
    """ Change locale for collation temporarily within a context (with-statement) """
    # The newone locale parameter should be a tuple: ('is_IS', 'UTF-8')
    old_locale = locale.getlocale(locale.LC_COLLATE)
    try:
        locale.setlocale(locale.LC_COLLATE, new_locale or _DEFAULT_SORT_LOCALE)
        yield locale.strxfrm  # Function to transform string for sorting
    finally:
        locale.setlocale(locale.LC_COLLATE, old_locale)


def sort_strings(strings, loc=None):
    """ Sort a list of strings using the specified locale's collation order """
    # Change locale temporarily for the sort
    with changedlocale(loc) as strxfrm:
        return sorted(strings, key=strxfrm)


class ConfigError(Exception):

    """ Exception class for configuration errors """

    def __init__(self, s):
        super().__init__(s)
        self.fname = None
        self.line = 0

    def set_pos(self, fname, line):
        """ Set file name and line information, if not already set """
        if not self.fname:
            self.fname = fname
            self.line = line

    def __str__(self):
        """ Return a string representation of this exception """
        s = Exception.__str__(self)
        if not self.fname:
            return s
        return "File {0}, line {1}: {2}".format(self.fname, self.line, s)


class LineReader:
    """ Read lines from a text file, recognizing $include directives """

    def __init__(self, fname, outer_fname=None, outer_line=0):
        self._fname = fname
        self._line = 0
        self._inner_rdr = None
        self._outer_fname = outer_fname
        self._outer_line = outer_line

    def fname(self):
        return self._fname if self._inner_rdr is None else self._inner_rdr.fname()

    def line(self):
        return self._line if self._inner_rdr is None else self._inner_rdr.line()

    def lines(self):
        """ Generator yielding lines from a text file """
        self._line = 0
        try:
            with resource_stream(__name__, self._fname) as inp:
                # Read config file line-by-line
                for b in inp:
                    # We get byte strings; convert from utf-8 to strings
                    s = b.decode("utf-8")
                    self._line += 1
                    # Check for include directive: $include filename.txt
                    if s.startswith("$") and s.lower().startswith("$include "):
                        iname = s.split(maxsplit=1)[1].strip()
                        # Do some path magic to allow the included path
                        # to be relative to the current file path, or a
                        # fresh (absolute) path by itself
                        head, _ = os.path.split(self._fname)
                        iname = os.path.join(head, iname)
                        rdr = self._inner_rdr = LineReader(
                            iname, self._fname, self._line
                        )
                        for incl_s in rdr.lines():
                            yield incl_s
                        self._inner_rdr = None
                    else:
                        yield s
        except (IOError, OSError):
            if self._outer_fname:
                # This is an include file within an outer config file
                c = ConfigError(
                    "Error while opening or reading include file '{0}'"
                    .format(self._fname)
                )
                c.set_pos(self._outer_fname, self._outer_line)
            else:
                # This is an outermost config file
                c = ConfigError(
                    "Error while opening or reading config file '{0}'"
                    .format(self._fname)
                )
            raise c


class AllowedMultiples:

    # Set of word forms allowed to appear more than once in a row
    SET: Set[str] = set()

    @staticmethod
    def add(word):
        AllowedMultiples.SET.add(word)


class WrongCompounds:

    # Dictionary structure: dict { wrong_compound : "right phrase" }
    DICT: Dict[str, Tuple[str, ...]] = {}

    @staticmethod
    def add(word, parts):
        if word in WrongCompounds.DICT:
            raise ConfigError("Multiple definition of '{0}' in wrong_compounds section".format(word))
        assert isinstance(parts, tuple)
        WrongCompounds.DICT[word] = parts


class SplitCompounds:

    # Dict of the form { first_part : set(second_part_stem) }
    DICT: Dict[str, Set[str]] = defaultdict(set)

    @staticmethod
    def add(first_part, second_part_stem):
        if (
            first_part in SplitCompounds.DICT
            and second_part_stem in SplitCompounds.DICT[first_part]
        ):
            raise ConfigError(
                "Multiple definition of '{0}' in split_compounds section"
                .format(first_part + " " + second_part_stem)
            )
        SplitCompounds.DICT[first_part].add(second_part_stem)


class UniqueErrors:

    # Dictionary structure: dict { wrong_word : (tuple of right words) }
    DICT: Dict[str, Tuple[str, ...]] = {}

    @staticmethod
    def add(word, corr):
        if word in UniqueErrors.DICT:
            raise ConfigError("Multiple definition of '{0}' in unique_errors section".format(word))
        UniqueErrors.DICT[word] = corr


class MultiwordErrors:

    # Dictionary structure: dict { phrase tuple: error specification }
    # List of tuples of multiword error phrases and their word category lists
    LIST: List[Tuple[Tuple[str, ...], str, List[str]]] = []
    # Parsing dictionary keyed by first word of phrase
    DICT: Dict[str, List[Tuple[Tuple[str, ...], int]]] = defaultdict(list)
    # Error dictionary, { phrase : (error_code, right_phrase, right_parts_of_speech) }
    ERROR_DICT: Dict[Tuple[str, ...], str] = dict()

    @staticmethod
    def add(words, error):
        if words in MultiwordErrors.ERROR_DICT:
            raise ConfigError(
                "Multiple definition of '{0}' in multiword_errors section"
                .format(" ".join(words))
            )
        MultiwordErrors.ERROR_DICT[words] = error

        # Add to phrase list
        ix = len(MultiwordErrors.LIST)

        a = error.split(",")
        if len(a) != 2:
            raise ConfigError("Expected two comma-separated parameters within $error()")
        code = a[0].strip()
        replacement = a[1].strip().split()

        # Append the phrase and the error specification in tuple form
        MultiwordErrors.LIST.append((words, code, replacement))

        # Dictionary structure: dict { firstword: [ (restword_list, phrase_index) ] }
        MultiwordErrors.DICT[words[0]].append((words[1:], ix))

    @staticmethod
    def get_phrase(ix):
        """ Return the original phrase with index ix """
        return MultiwordErrors.LIST[ix][0]

    @staticmethod
    def get_phrase_length(ix):
        """ Return the count of words in the original phrase with index ix """
        return len(MultiwordErrors.LIST[ix][0])

    @staticmethod
    def get_code(ix):
        """ Return the error code with index ix """
        return MultiwordErrors.LIST[ix][1]

    @staticmethod
    def get_replacement(ix):
        """ Return the replacement phrase with index ix """
        return MultiwordErrors.LIST[ix][2]


class TabooWords:

    # Dictionary structure: dict { taboo_word : suggested_replacement }
    DICT: Dict[str, str] = {}

    @staticmethod
    def add(word, replacement):
        if word in TabooWords.DICT:
            raise ConfigError("Multiple definition of '{0}' in taboo_words section".format(word))
        TabooWords.DICT[word] = replacement


class Suggestions:

    # Dictionary structure: dict { bad_word : [ suggested_replacements ] }
    DICT: Dict[str, List[str]] = {}

    @staticmethod
    def add(word, replacements):
        if word in Suggestions.DICT:
            raise ConfigError("Multiple definition of '{0}' in suggestions section".format(word))
        Suggestions.DICT[word] = replacements


class CapitalizationErrors:

    # Set of wrongly capitalized words
    SET: Set[str] = set()
    # Reverse capitalization (íslendingur -> Íslendingur, Danskur -> danskur)
    SET_REV: Set[str] = set()

    @staticmethod
    def add(word):
        """ Add the given (wrongly capitalized) word stem to the stem set """
        if word in CapitalizationErrors.SET:
            raise ConfigError(
                "Multiple definition of '{0}' in capitalization_errors section"
                .format(word)
            )
        CapitalizationErrors.SET.add(word)
        if word.islower():
            CapitalizationErrors.SET_REV.add(word.title())
        else:
            assert word.istitle()
            CapitalizationErrors.SET_REV.add(word.lower())


class OwForms:

    # dict { wrong_word_form : (lemma, correct_word_form, id, cat, tag) }
    DICT: Dict[str, Tuple[str, str, int, str, str]] = dict()

    @staticmethod
    def contains(word):
        """ Check whether the word form is in the error forms dictionary,
            either in its original casing or in a lower case form """
        d = OwForms.DICT
        if word.islower():
            return word in d
        return word in d or word.lower() in d

    @staticmethod
    def add(wrong_form, meaning):
        OwForms.DICT[wrong_form] = meaning

    @staticmethod
    def get_lemma(wrong_form):
        return OwForms.DICT[wrong_form][0]

    @staticmethod
    def get_correct_form(wrong_form):
        """ Return a corrected form of the given word, attempting
            to emulate the lower/upper/title case of the word """
        # First, try the original casing of the wrong form
        c = OwForms.DICT.get(wrong_form)
        if c is not None:
            # Found it: we're done
            return c[1]
        # Lookup a lower case version
        c = OwForms.DICT.get(wrong_form.lower())
        if c is None:
            # Not found: can't correct
            return wrong_form
        form = c[1]
        if wrong_form.istitle():
            return form.title()
        if wrong_form.isupper():
            return form.upper()
        return form

    @staticmethod
    def get_id(wrong_form):
        return OwForms.DICT[wrong_form][2]

    @staticmethod
    def get_category(wrong_form):
        return OwForms.DICT[wrong_form][3]

    @staticmethod
    def get_tag(wrong_form):
        return OwForms.DICT[wrong_form][4]


class CIDErrorForms:

    # dict { wrong_word_form : (lemma, correct_word_form, id, cat, tag) }
    DICT: Dict[str, Tuple[str, str, int, str, str]] = dict()

    @staticmethod
    def contains(word):
        """ Check whether the word form is in the error forms dictionary,
            either in its original casing or in a lower case form """
        d = CIDErrorForms.DICT
        if word.islower():      # TODO isn't this if-clause unnecessary?
            return word in d
        return word in d or word.lower() in d

    @staticmethod
    def add(wrong_form, meaning):
        CIDErrorForms.DICT[wrong_form] = meaning

    @staticmethod
    def get_lemma(wrong_form):
        return CIDErrorForms.DICT[wrong_form][0]

    @staticmethod
    def get_correct_form(wrong_form: str) -> str:
        """ Return a corrected form of the given word, attempting
            to emulate the lower/upper/title case of the word """
        # First, try the original casing of the wrong form
        c = CIDErrorForms.DICT.get(wrong_form)
        if c is not None:
            # Found it: we're done
            return c[1]
        # Lookup a lower case version
        c = CIDErrorForms.DICT.get(wrong_form.lower())
        if c is None:
            # Not found: can't correct
            return wrong_form
        form = c[1]
        if wrong_form.istitle():
            return form.title()
        if wrong_form.isupper():
            return form.upper()
        return form

    @staticmethod
    def get_id(wrong_form):
        return CIDErrorForms.DICT[wrong_form][2]

    @staticmethod
    def get_category(wrong_form):
        return CIDErrorForms.DICT[wrong_form][3]

    @staticmethod
    def get_tag(wrong_form):
        return CIDErrorForms.DICT[wrong_form][4]


class CDErrorForms:

    # dict { wrong_word_form : (lemma, correct_word_form, id, cat, tag) }
    DICT: Dict[str, Tuple[str, str, int, str, str]] = dict()

    @staticmethod
    def contains(word):
        """ Check whether the word form is in the error forms dictionary,
            either in its original casing or in a lower case form """
        d = CDErrorForms.DICT
        if word.islower():
            return word in d
        return word in d or word.lower() in d

    @staticmethod
    def add(wrong_form, meaning):
        CDErrorForms.DICT[wrong_form] = meaning

    @staticmethod
    def get_lemma(wrong_form):
        return CDErrorForms.DICT[wrong_form][0]

    @staticmethod
    def get_correct_form(wrong_form):
        """ Return a corrected form of the given word, attempting
            to emulate the lower/upper/title case of the word """
        # First, try the original casing of the wrong form
        c = CDErrorForms.DICT.get(wrong_form)
        if c is not None:
            # Found it: we're done
            return c[1]
        # Lookup a lower case version
        c = CDErrorForms.DICT.get(wrong_form.lower())
        if c is None:
            # Not found: can't correct
            return wrong_form
        form = c[1]
        if wrong_form.istitle():
            return form.title()
        if wrong_form.isupper():
            return form.upper()
        return form

    @staticmethod
    def get_id(wrong_form):
        return CDErrorForms.DICT[wrong_form][2]

    @staticmethod
    def get_category(wrong_form):
        return CDErrorForms.DICT[wrong_form][3]

    @staticmethod
    def get_tag(wrong_form):
        return CDErrorForms.DICT[wrong_form][4]


class Morphemes:

    # dict { morpheme : [ preferred PoS ] }
    BOUND_DICT: Dict[str, List[str]] = {}
    # dict { morpheme : [ excluded PoS ] }
    FREE_DICT: Dict[str, List[str]] = {}

    @staticmethod
    def add(morph, boundlist, freelist):
        if not boundlist:
            raise ConfigError("A definition of allowed PoS is necessary with morphemes")
        Morphemes.BOUND_DICT[morph] = boundlist
        # The freelist may be empty
        Morphemes.FREE_DICT[morph] = freelist


class Settings:

    """ Global settings """

    _lock = threading.Lock()
    loaded = False
    DEBUG = os.environ.get("DEBUG", "").strip() in TRUE

    # Configuration settings from the GreynirCorrect.conf file

    @staticmethod
    def _handle_settings(s):
        """ Handle config parameters in the settings section """
        a = s.lower().split("=", maxsplit=1)
        par = a[0].strip().lower()
        val = a[1].strip()
        if val.lower() == "none":
            val = None
        elif val.lower() == "true":
            val = True
        elif val.lower() == "false":
            val = False
        try:
            if par == "debug":
                Settings.DEBUG = val in TRUE
            else:
                raise ConfigError("Unknown configuration parameter '{0}'".format(par))
        except ValueError:
            raise ConfigError("Invalid parameter value: {0} = {1}".format(par, val))

    @staticmethod
    def _handle_allowed_multiples(s):
        """ Handle config parameters in the allowed_multiples section """
        assert s
        if len(s.split()) != 1:
            raise ConfigError("Only one word per line allowed in allowed_multiples section")
        if s in AllowedMultiples.SET:
            raise ConfigError("'{0}' is repeated in allowed_multiples section".format(s))
        AllowedMultiples.add(s)

    @staticmethod
    def _handle_wrong_compounds(s):
        """ Handle config parameters in the wrong_compounds section """
        a = s.lower().split(",", maxsplit=1)
        if len(a) != 2:
            raise ConfigError("Expected comma between compound word and its parts")
        word = a[0].strip().strip("\"")
        parts = a[1].strip().strip("\"").split()
        if not word:
            raise ConfigError("Expected word before the comma in wrong_compounds section")
        if len(parts) < 2:
            raise ConfigError("Missing word part(s) in wrong_compounds section")
        if len(word.split()) != 1:
            raise ConfigError("Multiple words not allowed before comma in wrong_compounds section")
        WrongCompounds.add(word, tuple(parts))

    @staticmethod
    def _handle_split_compounds(s):
        """ Handle config parameters in the split_compounds section """
        parts = s.split()
        if len(parts) != 2:
            raise ConfigError("Missing word part(s) in split_compounds section")
        SplitCompounds.add(parts[0], parts[1])

    @staticmethod
    def _handle_unique_errors(s):
        """ Handle config parameters in the unique_errors section """
        a = s.lower().split(",", maxsplit=1)
        if len(a) != 2:
            raise ConfigError("Expected comma between error word and its correction")
        word = a[0].strip()
        if len(word) < 3:
            raise ConfigError("Expected nonempty word before comma in unique_errors section")
        if word[0] != "\"" or word[-1] != "\"":
            raise ConfigError("Expected word in double quotes in unique_errors section")
        word = word[1:-1]
        corr = a[1].strip()
        if len(corr) < 3:
            raise ConfigError("Expected nonempty word after comma in unique_errors section")
        if corr[0] != "\"" or corr[-1] != "\"":
            raise ConfigError("Expected word in double quotes after comma in unique_errors section")
        corr = corr[1:-1]
        corr = tuple(corr.split())
        if not word:
            raise ConfigError("Expected word before the comma in unique_errors section")
        if len(word.split()) != 1:
            raise ConfigError("Multiple words not allowed before the comma in unique_errors section")
        UniqueErrors.add(word, corr)

    @staticmethod
    def _handle_capitalization_errors(s):
        """ Handle config parameters in the capitalization_errors section """
        CapitalizationErrors.add(s)

    @staticmethod
    def _handle_taboo_words(s):
        """ Handle config parameters in the taboo_words section """
        a = s.lower().split()
        if len(a) != 2:
            raise ConfigError("Expected taboo word and a suggested replacement")
        if a[1].count("_") != 1:
            raise ConfigError("Suggested replacement should include word category (_xx)")
        TabooWords.add(a[0].strip(), a[1].strip())

    @staticmethod
    def _handle_suggestions(s):
        """ Handle config parameters in the suggestions section """
        a = s.lower().split()
        if len(a) < 2:
            raise ConfigError("Expected bad word and at least one suggested replacement")
        if any(w.count("_") != 1 for w in a[1:]):
            raise ConfigError("Suggested replacements should include word category (_xx)")
        Suggestions.add(a[0].strip(), [w.strip() for w in a[1:]])

    @staticmethod
    def _handle_multiword_errors(s):
        """ Handle config parameters in the multiword_errors section """
        a = s.lower().split("$error", maxsplit=1)
        if len(a) != 2:
            raise ConfigError("Expected phrase followed by $error(...)")
        phrase = tuple(a[0].strip().split())
        if len(phrase) < 2:
            raise ConfigError("Multiword phrase must contain at least two words")
        error = a[1].strip()
        if len(error) < 3:
            raise ConfigError("Incomplete error specification for multiword phrase")
        if error[0] != "(" or error[-1] != ")":
            raise ConfigError("Error specification should be enclosed in parentheses")
        MultiwordErrors.add(phrase, error[1:-1])

    @staticmethod
    def _handle_ow_forms(s):
        """ Handle config parameters in the ow_forms section """
        split = s.strip().split(";")
        if len(split) != 6:
            raise ConfigError("Expected wrong form;lemma;correct form;id;category;tag")
        wrong_form = split[0].strip()
        correct_form = split[2].strip()
        if wrong_form == correct_form:
            return
            # !!! TODO: Should do this:
            # raise ConfigError(
            #     "Wrong form identical to correct form for '{0}'".format(wrong_form)
            # )
        meaning = (
            split[1].strip(),  # Lemma (stofn)
            correct_form,      # Correct form (ordmynd)
            split[3].strip(),  # Id (utg)
            split[4].strip(),  # Category (ordfl)
            split[5].strip(),  # Tag (beyging)
        )
        OwForms.add(wrong_form, meaning)

    @staticmethod
    def _handle_error_forms(s):
        """ Handle config parameters in the error_forms section """
        split = s.strip().split(";")
        if len(split) != 7:
            raise ConfigError("Expected wrong form;lemma;correct form;id;category;tag;errortype")
        wrong_form = split[0].strip()
        correct_form = split[2].strip()
        if wrong_form == correct_form:
            print(s)
            raise ConfigError(
                "Wrong form identical to correct form for '{0}'".format(wrong_form)
            )
        meaning = (
            split[1].strip(),  # Lemma (stofn)
            correct_form,      # Correct form (ordmynd)
            split[3].strip(),  # Id (utg)
            split[4].strip(),  # Category (ordfl)
            split[5].strip(),  # Tag (beyging)
        )
        etype = split[6].strip()
        if etype == "cid":
            CIDErrorForms.add(wrong_form, meaning)  # context-independent errors
        elif etype == "cd":
            CDErrorForms.add(wrong_form, meaning)   # context-dependent errors
        else:
            raise ConfigError("Wrong error type given, expected 'cid' or 'cd'")

    @staticmethod
    def _handle_morphemes(s):
        """ Process the contents of the [morphemes] section """
        freelist = []
        boundlist = []
        spl = s.split()
        if len(spl) < 2:
            raise ConfigError(
                "Expected at least a prefix and an attachment specification"
            )
        m = spl[0]
        for pos in spl[1:]:
            if pos:
                if pos.startswith("+"):
                    boundlist.append(pos[1:])
                elif pos.startswith("-"):
                    freelist.append(pos[1:])
                else:
                    raise ConfigError(
                        "Attachment specification should start with '+' or '-'"
                    )
        Morphemes.add(m, boundlist, freelist)

    @staticmethod
    def read(fname):
        """ Read configuration file """

        with Settings._lock:

            if Settings.loaded:
                return

            CONFIG_HANDLERS = {
                "settings": Settings._handle_settings,
                "allowed_multiples": Settings._handle_allowed_multiples,
                "wrong_compounds": Settings._handle_wrong_compounds,
                "split_compounds": Settings._handle_split_compounds,
                "unique_errors": Settings._handle_unique_errors,
                "capitalization_errors": Settings._handle_capitalization_errors,
                "taboo_words": Settings._handle_taboo_words,
                "suggestions": Settings._handle_suggestions,
                "multiword_errors": Settings._handle_multiword_errors,
                "morphemes": Settings._handle_morphemes,
                "ow_forms": Settings._handle_ow_forms,
                "error_forms": Settings._handle_error_forms,
            }
            handler = None  # Current section handler

            rdr = None
            try:
                rdr = LineReader(fname)
                for s in rdr.lines():
                    # Ignore comments
                    ix = s.find("#")
                    if ix >= 0:
                        s = s[0:ix]
                    s = s.strip()
                    if not s:
                        # Blank line: ignore
                        continue
                    if s[0] == "[" and s[-1] == "]":
                        # New section
                        section = s[1:-1].strip().lower()
                        if section in CONFIG_HANDLERS:
                            handler = CONFIG_HANDLERS[section]
                            continue
                        raise ConfigError("Unknown section name '{0}'".format(section))
                    if handler is None:
                        raise ConfigError("No handler for config line '{0}'".format(s))
                    # Call the correct handler depending on the section
                    try:
                        handler(s)
                    except ConfigError as e:
                        # Add file name and line number information to the exception
                        # if it's not already there
                        e.set_pos(rdr.fname(), rdr.line())
                        raise e

            except ConfigError as e:
                # Add file name and line number information to the exception
                # if it's not already there
                if rdr:
                    e.set_pos(rdr.fname(), rdr.line())
                raise e

            Settings.loaded = True
