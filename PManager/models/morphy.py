# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
import re

class trackMorphy():
    text = u''  # текст для обработки
    tags = []  # массив тэгов (каждый тэг является объектом Tags)
    allowWordClasses = ['NN', 'NNS']

    # parse text and returns array of tags
    def parseTags(self, text=u''):

        from pattern.en import lemma, tag

        if text:
            self.text = text

        tags = {}
        if len(self.text) > 0:
            for word, type in tag(self.text):
                if type in self.allowWordClasses:
                    wordUpper = unicode(word).upper()
                    if re.match('([A-z\-\._]+)', wordUpper):
                        lemm = lemma(wordUpper)
                        if len(lemm) > 2 and len(lemm) < 50:
                            if lemm in tags:
                                tags[lemm]['weight'] += 1
                            else:
                                tags[lemm] = {
                                    'weight': 1,
                                    'norm': lemm.upper()
                                }

        return tags
