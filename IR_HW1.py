import os
import codecs
import math
import re
from collections import Counter


def get_total_words(filepath):
    total_words = []
    for root, dirs, files in os.walk(filepath):
        for name in files:
            content = open(os.path.join(root, name), "r").read().lower()
            content = re.sub('[^a-z\ \']+', " ", content)
            total_words.extend(content.split())

    return total_words


def unique_words(total_words):
    total_words_count = Counter(total_words)
    return total_words_count


def words_occur_only_once(words_count):
    words_occur_only_once = []
    for word, count in words_count.items():
        if count == 1:
            words_occur_only_once.append(word)

    return words_occur_only_once


def get_top_30(unique_word_set):
    dic = {}
    for i in unique_word_set:
        if i not in dic:
            dic[i] = 1
        elif i in dic:
            dic[i] += 1
    t = sorted(dic.items(), key=lambda x: -x[1])[:30]

    return t


def freq_tf(number_of_occurences, number_of_uniq_wrds):
    return number_of_occurences / number_of_uniq_wrds


def freq_Idf(total_files, number_of_files_for_word):
    return math.log(total_files / number_of_files_for_word)


def number_of_files_word_in(wordToSearch, filepath):
    fileCount = 0
    for root, dirs, files in os.walk(filepath):
        for name in files:
            infile = open(filepath + "\\" + name, 'r')
            data = infile.read()
            words = data.split()
            if wordToSearch in words:
                fileCount += 1

    return fileCount


if __name__ == '__main__':
    file_path = "C:\\Users\\meeta\\Desktop\\Transcripts"
    number_of_files = len(os.listdir(file_path))
    total_word_set = get_total_words(file_path)
    total_words = len(total_word_set)
    unique_words = unique_words(total_word_set)
    words_occur_only_once = words_occur_only_once(unique_words)
    top_thirty_words = unique_words.most_common(30)

    number_of_docs_for_word = []
    probabilities = {}
    idf = {}
    tf_idf = {}
    for word, count in top_thirty_words:
        for files in os.listdir(file_path):
            content = open(os.path.join(file_path, files)).read().lower()
            content = re.sub('[^a-z\ \']+', " ", content)
            if word in content.split():
                number_of_docs_for_word.append(word)
        probabilities[word] = round(count / total_words, 5)

    words_docu_count = Counter(number_of_docs_for_word)

    # idf
    for word, count_of_docs in words_docu_count.items():
        idf[word] = round(math.log10(number_of_files / count_of_docs), 5)

    # tf*idf
    for word, count in top_thirty_words:
        tf_idf[word] = round(idf[word] * count, 5)

    list = os.listdir(file_path)
    number_files = len(list)


print("Total files: ", number_files, "Total Words: ", total_words)
print("Total unique words: ", str(len(unique_words)))
print("Number of words occur only once: ", str(len(words_occur_only_once)))
print("Term frequency for 30 most common words: ", str(top_thirty_words))
print("Idf: ", str(idf))
print("Tf*Idf: ", str(tf_idf))
print("Probabilities: ", str(probabilities))
print("Average number of words per document: " + str(round(sum(unique_words.values()) / number_of_files, 5)))