import jieba
from collections import defaultdict
import pdb
import pickle as pkl

word_dict = defaultdict(int)
segs = []

stopwords = set([line.strip() for line in open('stop_words.txt', 'r', encoding='utf-8').readlines()])
# punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
# ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
# 々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
# ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')
punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')

with open('cmb.txt', 'r') as f:
    for line in f:
        # line = lambda s: ''.join(filter(lambda x: x not in punct, s))
        seg_sentence = jieba.lcut(line, cut_all=False)
        seg_sentence = list(filter(lambda x: x not in punct, seg_sentence))
        # pdb.set_trace()
        for w in seg_sentence:
            if w in stopwords or w in punct or w.isdigit():
                continue
            word_dict[w] += 1
        segs.append(seg_sentence)

with open('word_dict.pkl', 'wb') as f:
    pkl.dump(word_dict, f)
with open('word_list.pkl', 'wb') as f:
    pkl.dump(segs, f)
