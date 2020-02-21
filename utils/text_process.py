# coding=utf-8
import nltk


def chinese_process(filein, fileout):
    with open(filein, 'r') as infile:
        with open(fileout, 'w') as outfile:
            for line in infile:
                output = list()
                line = nltk.word_tokenize(line)[0]
                for char in line:
                    output.append(char)
                    output.append(' ')
                output.append('\n')
                output = ''.join(output)
                outfile.write(output)


def text_to_code(tokens, dictionary, seq_len):
    code_str = ""
    eof_code = len(dictionary)
    for sentence in tokens:
        index = 0
        for word in sentence:
            code_str += (str(dictionary[word]) + ' ')
            index += 1
        while index < seq_len:
            code_str += (str(eof_code) + ' ')
            index += 1
        code_str += '\n'
    return code_str


def code_to_text(codes, dictionary):
    paras = ""
    eof_code = len(dictionary)
    for line in codes:
        numbers = map(int, line)
        for number in numbers:
            if number == eof_code:
                continue
            paras += (dictionary[str(number)])
        paras += '\n'
    return paras


def get_tokenlized(file):
    tokenlized = list()
    atoms = [
        'Li',
        'Na',
        'Al',
        'Si',
        'Cl',
        'Sc',
        'Zn',
        'As',
        'Se',
        'Br',
        'Sn',
        'Te',
        'Cn',
        'H',
        'B',
        'C',
        'N',
        'O',
        'F',
        'P',
        'S',
        'K',
        'V',
        'I',
    ]
    special = [
        '(', ')', '[', ']', '=', '#', '%', '0', '1', '2', '3', '4', '5',
        '6', '7', '8', '9', '+', '-', 'se', 'te', 'c', 'n', 'o', 's'
    ]
    padding = ['G', 'A', 'E']

    table = sorted(atoms, key=len, reverse=True) + special + padding
    table_len = len(table)

    with open(file) as raw:
        for text in raw:
            N = len(text)
            i = 0
            token = []
            while(i < N):
                for j in range(table_len):
                    symbol = table[j]
                    if symbol == text[i:i + len(symbol)]:
                        token.append(symbol)
                        i += len(symbol)
                        break                

            tokenlized.append(token)
    return tokenlized


def get_word_list(tokens):
    word_set = list()
    for sentence in tokens:
        for word in sentence:
            word_set.append(word)
    return list(set(word_set))


def get_dict(word_set):
    word_index_dict = dict()
    index_word_dict = dict()
    index = 0
    for word in word_set:
        word_index_dict[word] = str(index)
        index_word_dict[str(index)] = word
        index += 1
    return word_index_dict, index_word_dict

def text_precess(train_text_loc, test_text_loc=None):
    train_tokens = get_tokenlized(train_text_loc)
    if test_text_loc is None:
        test_tokens = list()
    else:
        test_tokens = get_tokenlized(test_text_loc)
    word_set = get_word_list(train_tokens + test_tokens)
    [word_index_dict, index_word_dict] = get_dict(word_set)

    if test_text_loc is None:
        sequence_len = len(max(train_tokens, key=len))
    else:
        sequence_len = max(len(max(train_tokens, key=len)), len(max(test_tokens, key=len)))
    with open('save/eval_data.txt', 'w') as outfile:
        outfile.write(text_to_code(test_tokens, word_index_dict, sequence_len))

    return sequence_len, len(word_index_dict) + 1
