"""A python program which converts disorginised file to excel/CSV file."""
import re
import csv

"""reading input data"""
my_text = open("vocab_text.txt", 'r')
text = my_text.read()
my_text.close()

text = re.sub("\nexample", 'Example', text, re.MULTILINE)
text = re.sub("\nExample |\nExample=", 'Example:', text, re.MULTILINE)
text = re.sub(r"\nExample:.[^=]+?(?=\nExample:)", "", text, re.DOTALL) 


def word_group(t1):
    """regroup each numbered paragraphs into new list with their respective
     index starting from 1"""
    grouped_text = re.split(r"^\d+\.", t1, 0, re.MULTILINE)
    return grouped_text[1:]


grouped_list = word_group(text)


def find_nth_topic(n):
    """
    find the topic of nth element in the grouped list
    """
    group_n = grouped_list[n]
    group_n = re.sub("^(\n)+", "", group_n)
    topic = re.findall(r"^.+", group_n)
    if topic:
        element = re.findall(r"\w.+", topic[0])
        return element[0]
    else:
        None


topics = []


def get_all_topics():
    """
    get all topic words
    """
    for d in range(len(grouped_list)):
        topics.append(find_nth_topic(d))


get_all_topics()


def get_all_terms(text_input):
    """
    get all defined terms in a string/ grouped list
    """
    pattern = re.compile(r"[A-Za-z][^\n]+?(?==.+?Example)", re.DOTALL)
    all_terms = pattern.findall(text_input)
    return all_terms


no_of_words = []    # this counts number of words in a group; required for 'topics_wz_num' function
for m in range(len(grouped_list)):
    no_of_words.append(len(get_all_terms(grouped_list[m])))


def topics_wz_num():
    """
    this helps to write numbers behind topics, e.g 1 Angry, 2 Angry, 3 Angry
    """
    global final_topics
    final_topics = []
    for num in range(len(topics)):
        x = 1
        while x <= no_of_words[num]:
            final_topics.append(str(x) + " " + topics[num])
            x += 1


topics_wz_num()


def get_all_definitions(text_input):
    """
        get all definitions in a string/ grouped list
    """
    pattern = re.compile(r"(?<==).+?(?=Example)", re.DOTALL)
    all_definitions = pattern.findall(text_input)
    return all_definitions


def get_all_examples(text_input):
    """
    get all examples in a string/ grouped list
    """
    pattern = re.compile(r"(?<=Example:).+?(?=^[A-Z])", re.DOTALL|re.MULTILINE)
    all_examples = pattern.findall(text_input)
    all_examples.append(re.findall("(?<=Example:).+\n{,3}$", text)[0])
    return all_examples


len_of_list = len(get_all_terms(text))
list_of_terms = get_all_terms(text)
list_of_definitions = get_all_definitions(text)
list_of_examples = get_all_examples(text)


for k in range(len_of_list):  # remove newlines
    list_of_terms[k] = re.sub("\n*", "", list_of_terms[k])
    list_of_definitions[k] = re.sub("\n*", "", list_of_definitions[k])
    list_of_examples[k] = re.sub("\n*", "", list_of_examples[k])

with open('final_CSV_file.csv', 'w') as f:  # convert the final list to csv format
    w = csv.writer(f, delimiter=',')
    w.writerow(['TOPIC', 'WORD', 'MEANING', 'SENTENCE'])
    for k in range(len_of_list):
        w.writerow([final_topics[k], list_of_terms[k], list_of_definitions[k], list_of_examples[k]])
f.close()

#End of Script
