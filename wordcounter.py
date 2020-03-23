"""
Noah Engel
Wednesday, February 13th 2019

Program is designed to identify redundancies and weak points
in essays that are given in a .txt format.
"""

# import nltk
# nltk.download('popular')

from nltk.corpus import wordnet as wn

fname = input("Enter file name: ")

out_name = input("Enter output file name: ")
out_name = out_name + '.txt'

out = open(out_name, 'w')

word_dict, two_word_dict, three_word_dict, four_word_dict = {}, {}, {}, {}
dictionaries = [word_dict, two_word_dict, three_word_dict, four_word_dict]

passive_words = ["is", "are", "be", "being", "become",
                 "have", "am", "was", "were", "been", "will"]

poor_words = ["help", "helping", "helped", "said", "says"]


def get_bad_words(lst):
    """
    Returns either a complete list of adverbs or adjectives

    Parameters
    ----------
    lst - list of adjectives or adverbs from a nltk language processor
          that can be converted from synset form to string form

    Returns
    --------
    return_list - the same list but all adjectives or adverbs are in
                  string form
    """
    return_list = []

    for wrd in lst:
        full_name = wrd.name()
        modified_name = full_name[0:len(full_name) - 5]
        return_list.append(modified_name)

    return return_list


adjectives = get_bad_words(wn.all_synsets(wn.ADJ))
adverbs = get_bad_words(wn.all_synsets(wn.ADV))

three_before = "nah"
two_before = "random"  # arbitrary
last_word = "spam"  # just to start - arbitrary

sinning_words = dict()
sinning_words['poor_count'] = 0
sinning_words["that_count"], sinning_words["passive_count"] = 0, 0

grammar_marks = [',', '.', '"']

adverb_lst, adjective_lst = [], []


def make_word_appropriate(wrd, grammar_marks):
    """
    Function is used to make every word in the dictionary
    consistent from a grammatical and possessive perspective

    Parameters
    -----------
    wrd (String) - word from the text file that needs to be
                   "corrected"

    grammar_marks (List) - list of symbols that may be mistakenly
                           lumped into a word during processing

    Returns
    -------
    word (String) - "corrected" form of the word to ensure consistency within
                    the dictionary
    """
    last_char = wrd[len(wrd) - 1]
    last_two_chars = wrd[len(wrd) - 2:len(wrd)]
    first_char = wrd[0]

    if first_char == '"':
        wrd = wrd[1:len(wrd)]

    if last_char in grammar_marks:
        wrd = wrd[0:len(wrd) - 1]

    if last_two_chars == "'s":
        wrd = wrd[0:len(wrd) - 2]

    return wrd.lower()  # consistent casing


def make_dictionaries(wrd, last_wrd, two_before, three_before, dictionaries):
    """
    Makes dictionaries containing phrases of one, two, and three words
    long. Used to spot obvious repetitions.

    Parameters
    ----------
    word (String) - the word being evaluated
    last_word (String) - the word immediately preceding the word in question
    two_before (String) - n-2 position from the word in question
    three_before (String) - n-3 position from the word in question

    Returns
    -------
    dictionaries (List) - List of dictionaries containing {phrase: frequency}
                          Phrase length given by the dictionary in question.
    """
    two_word_phrase = last_wrd + " " + wrd
    three_word_phrase = two_before + " " + two_word_phrase
    four_word_phrase = three_before + " " + three_word_phrase

    phrase_type = [wrd, two_word_phrase, three_word_phrase, four_word_phrase]

    for phrase, phrase_dict in zip(phrase_type, dictionaries):
        if phrase in phrase_dict:
            phrase_dict[phrase] += 1
        else:
            phrase_dict[phrase] = 1

    return dictionaries


def check_for_sins(wrd, sinning_words, adjective_lst, adverb_lst):
    """
    Checks for 'bad' or, more accurately, uninformative words.

    Parameters
    ----------
    word (String) - the word being evaluated
    sinning_words (List) - List of in-essay words deemed to be ineffective
    adjective_lst (List) - List of in-essay adjectives as defined by NLTK
    adverb_lst (List) - List of in-essay adverbs as defined by NLTK

    Returns
    -------
    sinning_words (List) - List of in-essay words deemed to be ineffective
    adjective_lst (List) - List of in-essay adjectives as defined by NLTK
    adverb_lst (List) - List of in-essay adverbs as defined by NLTK
    """

    if wrd.lower() == 'that':
        sinning_words["that_count"] += 1

    if wrd.lower() in passive_words:
        sinning_words["passive_count"] += 1

    if wrd.lower() in poor_words:
        sinning_words["poor_count"] += 1

    if wrd.lower() in adjectives:
        adjective_lst.append(word.lower())

    if wrd.lower() in adverbs:
        adverb_lst.append(word.lower())

    return sinning_words, adjective_lst, adverb_lst


with open(fname, 'r', encoding="utf-8") as f:
    for line in f:
        words = line.split()

        for word in words:
            # compensate for problems with words (eg grammatical technicalities)a
            word = make_word_appropriate(word, grammar_marks)

            # update the dictionaries with running word totals
            dictionaries = make_dictionaries(word, last_word, two_before, three_before, dictionaries)

            # reassign for the future
            three_before = two_before
            two_before = last_word
            last_word = word

            # check for words that can be improved
            sinning_words, adjective_lst, adverb_lst = check_for_sins(word, sinning_words, adjective_lst, adverb_lst)


# "sorting" the dictionaries by frequency of phrases and/or words
sorted_word = sorted(word_dict.items(), key=lambda kv: kv[1])
sorted_words = sorted(two_word_dict.items(), key=lambda kv: kv[1])
sorted_phrases = sorted(three_word_dict.items(), key=lambda kv: kv[1])
sorted_sentences = sorted(four_word_dict.items(), key=lambda kv: kv[1])

sorted_dicts = [sorted_word, sorted_words, sorted_phrases, sorted_sentences]

for dictionary in sorted_dicts:
    for (word, count) in dictionary:
        if count > 1:
            word = word.encode("ascii", "ignore")
            out.write("You used '{}' {} times.\n".format(word, count))
    out.write("\n-----------------------------------\n\n")

out.write("You said 'that' {} times.\n\n".format(sinning_words["that_count"]))

out.write("You said at least {} forms of 'to be.'\nYou may wish "
          "to correct this to put your essay in a more active form.\n\n".format(sinning_words["passive_count"]))

out.write("You said at least {} uninformative words.\n".format(sinning_words["poor_count"]))

out.write("\n-----------------------------------\n\n")

for adv in adverb_lst:
    out.write("The following is an adverb: {} - {} time(s).\n".format(adv, word_dict[adv]))

out.write("\n-----------------------------------\n\n")

for adj in adjective_lst:
    out.write("The following is an adjective: {} - {} time(s).\n".format(adj, word_dict[adj]))
