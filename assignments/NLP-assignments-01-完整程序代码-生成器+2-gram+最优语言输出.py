import random
import jieba
from collections import Counter
import matplotlib.pyplot as plt
import codecs, sys
import re

if sys.getdefaultencoding() != 'utf-8':
    sys.setdefaultencoding('utf-8')


origin_path = r"D:\\assignments\\train.txt"
target_path = r"D:\\assignments\\train_output.txt"

origin = codecs.open(origin_path, 'r', encoding="utf8")
target = codecs.open(target_path, 'w', encoding="utf8")

te2 = []

for line in origin.readlines():
    line=re.sub(r'[0-9]|/d+|[-$+\s\?\？]|[a-z]|[A-Z]','',line)
    for i in line:
        te2.append(i)

target.writelines(te2)

origin.close()
target.close()

corpus = 'D:\\assignments\\train_output.txt'
o_file = open(corpus, 'r', encoding="utf8")
FILE = o_file.read()

def generate_by_pro(text_corpus, length = 20):
    return ''.join(random.sample(text_corpus, length))

#print(generate_by_pro(FILE))

#print(list(jieba.cut('小明和小东在踢足球')))

def cut(string):
    return list(jieba.cut(string))

TOKENS = cut(FILE)

words_count = Counter(TOKENS)
words_with_fre = [f for w, f in words_count.most_common(100)]
#print(words_with_fre)

_bi_gram_words = [
    TOKENS[i] + TOKENS[i+1] for i in range(len(TOKENS)-1)
]

#print(_bi_gram_words[:10])

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

#print('-----------------------------')
#print(_bi_gram_model('法律要求残疾保险吗'))
#print(_bi_gram_model('健康保险的保额'))
#print(_bi_gram_model('哈哈哈哈哈'))
#print(_bi_gram_model('瞎混看了怕啊我人'))
#print(_bi_gram_model('我们到了应该上学的年纪'))
#print(_bi_gram_model('我们到了应该放学的年级'))

insurance = '''
保险 = 对象 种类 业务
对象 = 孩子的 | 我的 | 父母的
种类 = 人寿保险 | 重大疾病保险 | 意外伤害保险 | 汽车保险
业务 = 保费多少 | 保修范围 | 涉及哪些疾病 | 可以支付养老院么'''

def sentence_generator(grammar_str: str, target, stmt_split='=', or_split='|'):
    sentence_rules = dict()
    for line in grammar_str.split('\n'):
        if not line: continue
        stmt, expr = line.split(stmt_split)
        sentence_rules[stmt.strip()] = expr.split(or_split)

    generated = generate(sentence_rules, target=target)
    return generated

def generate(grammar_rule,target):
    if target in grammar_rule:
        candidates = grammar_rule[target]
        candidate = random.choice(candidates)
        return ''.join(generate(grammar_rule,target=c.strip( ))for c in candidate.split( ))
    else:
        return target

def random_sentences():
    sen_Pro = []
    i = int(input('请设置想要生成的句子数目：'))
    j = 0
    while j < i:
        _insurance_sentence = sentence_generator(insurance, target='保险')
        #print(_insurance_sentence)
        sen_Pro.append((_insurance_sentence, _bi_gram_model(_insurance_sentence)))
        print(sen_Pro[j])
        j = j+1
    return sen_Pro

def generate_best():
    s_Pro = random_sentences()
    s_Pro = sorted(s_Pro,key=lambda x: x[1], reverse=True)
    #print('-----------------')
    #print(s_Pro)
    print('The best sentence is：' + s_Pro[0][0] +' 概率为：' + str(s_Pro[0][1]))

generate_best()


#Q: 这个模型有什么问题？ 你准备如何提升？
#Ans:1、过于依赖语料库，不同内容的文本以及文本的规模有局限性；2、结果不是很准确。至于提升...要学其他的模型叻~
