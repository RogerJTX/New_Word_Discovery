'''
description: 基于互信息和左右熵的新词发现算法
             New word discovery algorithm based on mutual information and left and right entropy
author: jtx
data: 2020-11-25
application: Patents
'''

from collections import Counter
import numpy as np
import re


def n_gram_words(text, n_gram):
    """
    To get n_gram word frequency dict
    input: str of the chinese sentence ，int of n_gram
    output: word frequency dict

    """
    words = []
    for i in range(1, n_gram + 1):
        words += [text[j:j + i] for j in range(len(text) - i + 1)]
    words_freq = dict(Counter(words))
    return words_freq


def PMI_filter(word_freq_dic, min_p):
    """
    To get words witch  PMI  over the threshold
    input: word frequency dict , min threshold of PMI
    output: condinated word list

    """
    new_words = []
    for word in word_freq_dic:
        if len(word) == 1:
            pass
        else:
            p_x_y = min([word_freq_dic.get(word[:i]) * word_freq_dic.get(word[i:]) for i in range(1, len(word))])
            mpi = p_x_y / word_freq_dic.get(word)
            if mpi > min_p:
                new_words.append(word)
    return new_words


def calculate_entropy(char_list):
    """
    To calculate entropy for  list  of char
    input: char list
    output: entropy of the list  of char
    """
    char_freq_dic = dict(Counter(char_list))
    entropy = (-1) * sum(
        [char_freq_dic.get(i) / len(char_list) * np.log2(char_freq_dic.get(i) / len(char_list)) for i in char_freq_dic])
    return entropy


def Entropy_left_right_filter(condinate_words, text, min_entropy):
    """
    To filter the final new words from the condinated word list by entropy threshold
    input:  condinated word list ,min threshold of Entropy of left or right
    output: final word list
    """
    final_words = []
    for word in condinate_words:
        try:
            left_right_char = re.findall('(.)%s(.)' % word, text)

            left_char = [i[0] for i in left_right_char]
            left_entropy = calculate_entropy(left_char)

            right_char = [i[1] for i in left_right_char]
            right_entropy = calculate_entropy(right_char)

            if min(right_entropy, left_entropy) > min_entropy:
                final_words.append(word)
        except:
            pass
    return final_words


# read the data and preprocessing the data to a whole str
stop_word=['【','】',')','(','、','，','“','”','。','\n','《','》',' ','-','！','？','.','\'','[',']','：','/','.','"','\u3000','’','．',',','…','?']
with open("test.txt") as f:
    text = f.read()
for i in stop_word:
    text=text.replace(i,"")

# finding the new words
min_p = 4
min_e = 2
n_gram = n_gram_words(text,min_p)
condinate = PMI_filter(n_gram ,min_e )
final = Entropy_left_right_filter(condinate,text,1)


print(final)