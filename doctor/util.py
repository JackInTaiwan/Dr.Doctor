import random
import numpy as np

### Tensorflow
class data_batch () :
    def __init__(self, x_train, y_train, size) :
        self.x_train = x_train[:]
        self.y_train = y_train[:]
        self.size = size
        self.index = 0
        self.len = len(x_train)
    def generate_batch (self) :
        if self.index + self.size <= self.len :
            x_train_batch = self.x_train[self.index:self.index + self.size]
            y_train_batch = self.y_train[self.index:self.index + self.size]
            self.index += self.size
            return x_train_batch, y_train_batch
        else :
            self.index = 0
            train_pairs = list(zip(self.x_train, self.y_train))
            random.shuffle(train_pairs)
            self.x_train, self.y_train = list(zip(*train_pairs))
            self.x_train, self.y_train = np.array(self.x_train), np.array(self.y_train)
            x_train_batch = self.x_train[self.index: self.index + self.size]
            y_train_batch = self.y_train[self.index: self.index + self.size]
            self.index = self.index + self.size
            return x_train_batch, y_train_batch

def load_data(data_pic, data_label) :
    x_train, y_train = [], []
    label_len = len(data_label[0])
    count = [0 for i in range(label_len)]
    count_use = [0 for i in range(label_len)]
    p_height, p_width = data_pic[0].shape
    for pic, label in zip(data_pic, data_label) :
        index = list(label).index(1)
        count[index] += 1
    for pic, label in zip(data_pic, data_label) :
        index = list(label).index(1)
        if count[index] > 1000 and count_use[index] < 5000:
            x_train.append(pic.flatten())
            y_train.append(label)
            count_use[index] += 1
    label_use = len(np.array(count)[np.array(count)>1000])
    print ("Label size: %s" % label_use)
    print ("Top label: %s " % (max(count_use)/sum(count_use)))
    x_train, y_train = np.array(x_train), np.array(y_train)
    return x_train, y_train, label_len, p_height, p_width



### Data Process
def convert_s_to_picture_com(s, word_max_len = 16, sentence_max_words = 14) :

    partition = 4
    ss = s.split()
    word_len = 0
    sen_pict = []
    save = True if len(ss) <= sentence_max_words else False
    for word in ss :
        if word_max_len >= len(word) > 0 :
            word_len += 1
            pict = []
            for alph in word :
                if s_to_picture_encoding(alph) != None :
                    pict.append(s_to_picture_encoding(alph))
                else :
                    raise NameError("encoding error : %s in %s" % (alph, s))
            for _ in range(word_max_len-len(word)) :
                pict.append(s_to_picture_encoding(None))
            pict_com =[]
            for i, al in enumerate(pict) :
                if i % partition == 0 :
                    pict_com.append(al)
                else :
                    for j, element in enumerate(pict_com[-1]) :
                        if al[j] != 0 :
                            pict_com[-1][j] += al[j]
            sen_pict += pict_com
        elif len(word) > word_max_len : save = False
    for j in range(sentence_max_words - word_len) :
        null_pict = [[0] * 26 for m in range(word_max_len//partition)]
        sen_pict += null_pict
    sen_pict = np.array(sen_pict)
    return sen_pict


# The encoding table
def s_to_picture_encoding(alph) :
    alph_basis = "abcdefghijklmnopqrstuvwxyz"
    num_basis = "1234567890"
    punc_basis = '/-.+()'
    w = 100
    if alph == None :
        return [0 for _ in range(len(alph_basis))]
    elif alph.lower() in alph_basis :
        alph = alph.lower()
        index = alph_basis.index(alph)
        output = [0 for _ in range(len(alph_basis))]
        output[index] = w
        return output
    elif alph in num_basis :
        output = [0 for _ in range(len(alph_basis))]
        for i in range(num_basis.index(alph) * 2 + 2 ) :
            output[i] = w
        return output
    elif alph in punc_basis :
        output = [0 for _ in range(len(alph_basis))]
        for i in range(26) :
            if i % (punc_basis.index(alph) + 1) == 0 :
                output[i] = w
        return output
    else : return None


def convert_s_to_std_format(s) :
    max_length = 16

    #replacements = [" ", "&", ",", ";", "<", ">", "]", "[", "^", "*", "="]
    replacements = "abcdefghijklmnopqrstuvwxyz1234567890._- "
    #replacements = "abcdefghijklmnopqrstuvwxyz1234567890 "
    s_tmp = ""
    for a in s :
        if a in replacements :
            s_tmp += a
        else :
            s_tmp += " "
    s = s_tmp
    replacements_2 = ["_"]
    for rep in replacements_2 :
        s = s.replace(rep, "-")
    ss = s.split()
    if len(ss) > 16 :
        ss = ss[0:16]
    s = " ".join(ss)
    return s