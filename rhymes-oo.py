'''
File: rhymes-oo.py
Author: Justin Nichols
Purpose: Find all words that have perfect rhymes with a given word
(out of a given list)
CSC120, Section 1, Fall 18
'''


# Abbreviations in this code:
#   'cand' = candidate
#   'pl' = phoneme list
#   'pls' = phoneme lists
#   'prons' = pronunciations


# importing sys so that Python can exit gracefully in response to
user-errors
import sys


class WordMap:
    '''
    Purpose: Accepts two input-files: one pronuns-file and one queried-word.
             Creates Word-objs to store data about particular words.
             Creates a dict (self._word_strs_to_objs) that maps the str-form
                 of different words to their corresponding Word-objs.
             Finds all words that rhyme perfectly with the queried word,
                 and prints them out in alphabetical order.
    Initialized Attributes: self._word_strs_to_objs, the dict described above.
    '''
    def __init__(self):
        self._word_strs_to_objs = {}


    def process_prons_file(self):
        '''
        Purpose: Accepts the name of a pronuns-file as input.
                 Parses the file.
                 Makes Word-objs as needed to store data.
        '''

        # attempting to open the input file
        prons_fname = input()
        try:
            prons_file_it_obj = open(prons_fname)
        except FileNotFoundError:
            print('ERROR: Could not open file ' + prons_fname)
            sys.exit(1)

        # making appropriate Word-objects
        for word_pron_info_line in prons_file_it_obj:
            word_pron_info_list = word_pron_info_line.split()
            
            # Performs the following, as needed:
            # 1. Creates word-objs
            # 2. Adds word-strs and word-objs to keys and values (respectively)
            #     of self_word_strs_to_objs
            word_str_form = word_pron_info_list[0].lower()
            if word_str_form not in self._word_strs_to_objs:
                word_obj_form = Word(word_str_form)
                self._word_strs_to_objs[word_str_form] = word_obj_form
            else:
                word_obj_form = self._word_strs_to_objs[word_str_form]

            pl = tuple(word_pron_info_list[1:])
            word_obj_form.add_pl(pl)


    def find_print_perfect_rhymes(self):
        '''
        Purpose: Accepts a query-word as input.
        Prints out all words in the dict that rhyme perfectly with the
                     queried word
        '''
        input_word_str_form_case_not_set = input()
        input_word_str_form = input_word_str_form_case_not_set.lower()

        # making sure the input-word is actually in the pronuns-dict
        assert input_word_str_form in self._word_strs_to_objs, \
            print('ERROR: the word input by the user is not in the '
                     'pronunciation dictionary '\
                     + input_word_str_form_case_not_set)

        input_word_obj_form = self._word_strs_to_objs[input_word_str_form]
        # initializing all_perfect_rhymes as a set to avoid duplicates
        all_perfect_rhymes = set()

        # checking each rhyme-candidate in the dict
        for cand_word_str_form in self._word_strs_to_objs:
            cand_word_obj_form = self._word_strs_to_objs[cand_word_str_form]
            if input_word_obj_form == cand_word_obj_form:
                all_perfect_rhymes.add(cand_word_str_form)

        # converting all_perfect_rhymes into a list now so it can be sorted
        all_perfect_rhymes = list(all_perfect_rhymes)
        all_perfect_rhymes.sort()

        for rhyme in all_perfect_rhymes:
            print(rhyme)


    def __str__(self):
        return ('WordMap object. Handles input dict and query-word. '
            'Creates Word-objects to process former and evaluate latter.')


class Word:
    '''
    Purpose: Keeps track of data about a word.
    Determines whether or not it rhymes perfectly with another word.
    Initialized Attributes: self._str_form, the str-representation of the word.
        self._all_pls, a set. Contains the pls of the word.
    '''
    def __init__(self, word_str_form):
        self._str_form = word_str_form
        self._all_pls = set()


    def prim_stress_index(self, pl):
        '''
        Purpose: finds the syllable that receives the most emphasis in a word
        Parameters: pl, a list of the phonemes in a word
        Return: Either:
                    1. i, the index value of the syllable which receives primary stress
                    2. -1, the value returned if the word has no primary stress
        '''         
        for i in range(len(pl)):
            if pl[i][-1] == '1':
                return i
        return -1


    def is_perfect_rhyme(self, input_word_pl, cand_word_pl):
        '''
        Purpose: Determines whether word rhymes perfectly with other word.
        Returns: a boole. True if the two words rhyme perfectly, False
                     otherwise.
        '''

        # making sure rhyme-candidate does in-fact have a primary stress
        cand_word_prim_stress_index = self.prim_stress_index(cand_word_pl)
        cand_word_has_prim_stress = (cand_word_prim_stress_index != -1)

        #seeing if current word rhymes perfectly with queried word
        if cand_word_has_prim_stress:
            input_word_prim_stress_index = \
                                         self.prim_stress_index(input_word_pl)

            input_word_tail = input_word_pl[input_word_prim_stress_index:]
            cand_word_tail = cand_word_pl[cand_word_prim_stress_index:]
            tails_match = (input_word_tail == cand_word_tail)

            # CAN WE USE NUMBERS IN VAR NAMES?
            input_word_prim_stress_1st_syll = \
                                            (input_word_prim_stress_index == 0)
            cand_word_prim_stress_1st_syll = (cand_word_prim_stress_index == 0)
            # case where neither word has prim stress on 1st syllable
            if not (input_word_prim_stress_1st_syll or \
                    cand_word_prim_stress_1st_syll):
                input_word_prior_phoneme = input_word_pl\
                                           [input_word_prim_stress_index -1]
                cand_word_prior_phoneme = cand_word_pl\
                                          [cand_word_prim_stress_index - 1]
                prior_phoneme_diff_each_word = (input_word_prior_phoneme \
                                                != cand_word_prior_phoneme)
            # case where both words have prim stress on 1st syllable
            elif (input_word_prim_stress_1st_syll and \
                  cand_word_prim_stress_1st_syll):
                prior_phoneme__diff_each_word = False
            # case where precisely one word has prim stress on 1st syllable
            else:
                prior_phoneme_diff_each_word = True
            
            return (tails_match and prior_phoneme_diff_each_word)

        return False


    # getters
    def get_all_pls(self):
        return self._all_pls

    # setter
    def add_pl(self, pl):
        self._all_pls.add(pl)


    # special methods
    def __eq__(self, cand_word_obj_form):

            input_word_all_pls = self._all_pls
            cand_word_all_pls = cand_word_obj_form.get_all_pls()

            for input_word_pl in input_word_all_pls:
                for cand_word_pl in cand_word_all_pls:
                    if self.is_perfect_rhyme(input_word_pl, cand_word_pl):
                        return True

            return False


    def __str__(self):
        return 'Word object corresponding to: \'{}\''.format(self._str_form)


def main():
    word_map = WordMap()
    word_map.process_prons_file()
    word_map.find_print_perfect_rhymes()


main()
