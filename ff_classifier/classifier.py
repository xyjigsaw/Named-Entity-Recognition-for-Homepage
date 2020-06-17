# Name: classifier
# Author: Reacubeth
# Time: 2020/3/12 9:43
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

import fasttext as ff
import jieba
import text_toolkit
import os


class Model:
    def __init__(self, gen_train_data=False):
        self.gen_train_data = gen_train_data
        if os.path.exists("ff_classifier/try.ftm"):
            self.classifier = ff.load_model("ff_classifier/try.ftm")
        else:
            self.classifier = ff.train_supervised("ff_classifier/train_data.txt", epoch=100, dim=50, lr=0.1, wordNgrams=2, minCount=0, loss="softmax")
            self.classifier.save_model("ff_classifier/try.ftm")  # 保存模型

    def single_predict(self, string, stopwords=None):
        if not stopwords:
            stopwords = ['年', '为', '于', '月', '日']
        texts = []
        segments = jieba.lcut(string)
        segments = filter(lambda x: x not in stopwords and x != ' ', segments)
        segments = filter(lambda x: x not in text_toolkit.match_symbol(x) and x not in text_toolkit.match_digit(x),
                          segments)
        texts.append(" ".join(segments))
        pre, prob = self.classifier.predict(texts)
        if self.gen_train_data:
            self.gen_train_model_data(string, pre[0][0])
        if '__label__' in pre[0][0]:
            label = pre[0][0][pre[0][0].index('__label__') + len('__label__'):]
            return label, float(prob[0][0])
        return pre[0][0], float(prob[0][0])

    def gen_train_model_data(self, string, label, stopwords=None):
        if not stopwords:
            stopwords = ['年', '为', '于', '月', '日']

        segments = jieba.lcut(string.strip('\n'))
        # segments = filter(lambda x: len(x) > 1, segments)
        segments = filter(lambda x: x not in stopwords, segments)
        segments = filter(lambda x: x not in text_toolkit.match_digit(x), segments)
        segments = filter(lambda x: x not in text_toolkit.match_date(x), segments)
        segments = filter(lambda x: x not in text_toolkit.match_symbol(x) and x != ' ', segments)
        dn = "output/"
        os.makedirs(dn, exist_ok=True)
        with open(dn + "for_train_archive.txt", "a+", encoding='utf-8') as f:
            f.write(label + " " + " ".join(segments) + '\n')

    def get_labels(self):
        return self.classifier.get_labels()
