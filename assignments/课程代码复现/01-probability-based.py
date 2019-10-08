import random
import jieba
from collections import Counter
import matplotlib.pyplot as plt

corpus = 'D:\\assignments\\article_9k.txt'
FILE = open(corpus).read()

def generate_by_pro(text_corpus, length = 20):
    return ''.join(random.sample(text_corpus, length))

print(generate_by_pro(FILE))

print(list(jieba.cut('小明和小东在踢足球')))

def cut(string):
    return list(jieba.cut(string))

TOKENS = cut(FILE)

words_count = Counter(TOKENS)
words_with_fre = [f for w, f in words_count.most_common(100)]
print(words_with_fre)

_bi_gram_words = [
    TOKENS[i] + TOKENS[i+1] for i in range(len(TOKENS)-1)
]

print(_bi_gram_words[:10])

_bi_gram_word_counts = Counter(_bi_gram_words)

#def get_1_gram_count(word):
#    if word in words_count: return words_count[word]
#    else:
#        return words_count.most_common()[-1][-1]

#def get_2_gram_count(word):
#    if word in _bi_gram_word_counts: return _bi_gram_word_counts[word]
#    else:
#        return _bi_gram_word_counts.most_common()[-1][-1]
#most_common()[-1][-1]  最少的值

def get_gram_count(word,wc):  #简化代码
    if word in wc: return wc[word]
    else:
        return wc.most_common()[-1][-1]

#print(get_gram_count('XXX',words_count))

def _bi_gram_model(sentence):
    tokens = cut(sentence)
    probability = 1
    for i in  range(len(tokens)-1):
        word = tokens[i]
        next_word = tokens[i+1]
        #pro = _bi_gram_word_counts[words+next_word] / words_count[next_word]
        #pro = get_gram_count([word+next_word], _bi_gram_word_counts) / get_gram_count(next_word, words_count)
        _two_gram_c = get_gram_count(word+next_word, _bi_gram_word_counts)
        _one_gram_c = get_gram_count(word, words_count)
        pro = _two_gram_c / _one_gram_c
        probability *= pro

    return probability

print('-----------------------------')
print(_bi_gram_model('状涩切品束日政化枪设越设月拍全成流仍发新'))
print(_bi_gram_model('此外自本周6月12日起'))
print(_bi_gram_model('爸爸和妈妈在拌嘴'))
print(_bi_gram_model('我们到了应该上学的年纪'))
print(_bi_gram_model('我们到了应该上学的年级'))
print(_bi_gram_model('我们到了应该放学的年级'))