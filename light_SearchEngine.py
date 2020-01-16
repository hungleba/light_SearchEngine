###
### Author: Hung Le Ba
### Description: The program take user input as a file or a word,
###              then compare it to the frequency within the dictionary
###              by applying the symspell algorithm to solve the
###              edit distance problem. The program then return
###              the most similar and frequent word appear in the
###              dictionary, otherwise, return 'no result'.
###
import stringdist

'''
Ask the user necessary information on preferable dictionary
'''
dic_name = input("Would you like to use your dictionary or the default one? (new or default): ")
while (dic_name != 'new' and dic_name!= 'default'):
    dic_name = input("Choose between 'new' or 'default': ")
if (dic_name == 'new'):
    fname = input("Your dictionary file name: ")
else:
    fname = "frequency_dictionary_en_82_765.txt"
dictionary = {}

def user_input():
    '''
    Take user input on mode and return the
    processed file.
    inputText: a word if mode == text, a list if mode == file
    '''
    mode = input("Choose input mode (file or word): ")
    if (mode == "file"):
        inputFileName = input("File name: ")
        lines = open(inputFileName, 'r').readlines()
        inputText = ''
        for line in lines:
            line = line.strip('\n')
            inputText += (line+' ')
    elif (mode == "text"):
        inputText = input("Paste your text in here: ")
    return inputText.split(' ')

def get_deletes_list(w, delete_distance):
    """to return all possible combinations of the string with x number of deletes"""
    master_deletes_list = []
    queue = [w]

    for x in range(delete_distance):
        temporary_queue = []

        for word in queue:
            if len(word)>delete_distance:
                for c in range(len(word)):
                    word_minus_c = word[:c] + word[c+1:]
                    if word_minus_c not in master_deletes_list:
                        master_deletes_list.append(word_minus_c)
                    if word_minus_c not in temporary_queue:
                        temporary_queue.append(word_minus_c)
        queue = temporary_queue

    return master_deletes_list


def create_dictionary_entry(w,frequency):
    """
    the dictionary will be in the format of {"key":[[autocorrected word 1, autocorrected word 2, etc],frequency}
    """
    #Add the word
    if w not in dictionary:
        dictionary[w] = [[w],frequency]
    else:
        dictionary[w][0].append(w)
        dictionary[w] = [dictionary[w][0],frequency]
    deletes_list = get_deletes_list(w,2)

    for word in deletes_list:
        if word not in dictionary:
            dictionary[word] = [[w],0]
        else:
            dictionary[word][0].append(w)

def create_dictionary(fname):
    '''Scan, process, and store the dictionary information, ready to be called'''
    total_frequency =0
    with open(fname) as file:
        for line in file:
            create_dictionary_entry(line.split()[0],line.split()[1])
    for keyword in dictionary:
        total_frequency += float(dictionary[keyword][1])
    for keyword in dictionary:
        dictionary[keyword].append(float(dictionary[keyword][1])/float(total_frequency))

def get_suggestions(w):
    search_deletes_list = get_deletes_list(w,2)
    search_deletes_list.append(w)
    candidate_corrections = []

    #Does not correct words which are existing in the dictionary and that has a high frequency based on the word corpus
    if w in dictionary and int(dictionary[w][1])>10000:
        return w
    else:
        for query in search_deletes_list:
            if query in dictionary:
                for suggested_word in dictionary[query][0]:
                        edit_distance = float(stringdist.rdlevenshtein(w, suggested_word))
                        frequency = float(dictionary[suggested_word][1])
                        probability = float(dictionary[suggested_word][2])
                        score = frequency*(0.003**(edit_distance))

                        candidate_corrections.append((suggested_word,frequency,edit_distance,score))

        candidate_corrections = sorted(candidate_corrections, key=lambda x:int(x[3]), reverse=True)
        return candidate_corrections


def get_correction(w):

    try:
        return get_suggestions(w)[0][0]
    except:
        return "no result"

create_dictionary(fname)
for word in user_input():
    print(get_correction(word))
