#encoding=utf-8

import nltk


def classify(classifier, whole_set, separator):
    if isinstance(separator, float):
        separator = int(len(whole_set) * separator)
    train_set = whole_set[separator:]
    test_set = whole_set[:separator]
    try:
        clssfr = classifier.train(train_set)
        print nltk.classify.accuracy(clssfr, test_set)
    except AttributeError:
        clssfr = classifier(train_set)
        print clssfr.evaluate(test_set)
    return clssfr


# 性别鉴定
    
def gender_features(word):
    return {'last_letter': word[-1]}
    

def identify_gender():
    import random
    from nltk.corpus import names

    names = ([(name, 'male') for name in names.words('male.txt')] +
             [(name, 'female') for name in names.words('female.txt')])
    random.shuffle(names)
    featuresets = [(gender_features(n), g) for n, g in names]
    return classify(nltk.NaiveBayesClassifier, featuresets, 500)


# 选择正确的特征

# 过多的feature造成过拟合

def gender_features2(name):
    name = name.lower()
    
    features = {'firstletter': name[0], 'lastletter': name[-1]}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features['count(%s)' % letter] = name.count(letter)
        features['has(%s)' % letter] = letter in name
    return features


def identify_gender2():
    import random
    from nltk.corpus import names

    names = ([(name, 'male') for name in names.words('male.txt')] +
             [(name, 'female') for name in names.words('female.txt')])
    random.shuffle(names)
    featuresets = [(gender_features2(n), g) for n, g in names]
    return classify(nltk.NaiveBayesClassifier, featuresets, 500)


def gender_features3(name):
    return {'suffix1': name[-1], 'suffix2': name[-2:]}


def identify_gender3():
    import random
    from nltk.corpus import names

    names = ([(name, 'male') for name in names.words('male.txt')] +
             [(name, 'female') for name in names.words('female.txt')])
    random.shuffle(names)
    featuresets = [(gender_features3(n), g) for n, g in names]
    return classify(nltk.NaiveBayesClassifier, featuresets, 500)

    
# 文档分类
    
def document_features(doc, allwords):
    docset = set(doc)
    return {'contains(%s)' % word: word in docset for word in allwords}


def classify_document():
    from nltk.corpus import movie_reviews
    import random

    documents = [(list(movie_reviews.words(fileid)), category)
                 for category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]
    random.shuffle(documents)
    all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
    allwords = [w for w, _ in all_words.most_common(2000)]
    featuresets = [(document_features(d, allwords), c) for d, c in documents]
    return classify(nltk.NaiveBayesClassifier, featuresets, 0.1)
    

def pos_features(word, common_suffixes):
    return {'endswith(%s)' % suffix: word.lower().endswith(suffix) for suffix in common_suffixes}


def classify_document1():
    from nltk.corpus import brown

    suffix_fdist = nltk.FreqDist()
    for word in brown.words():
        word = word.lower()
        suffix_fdist[word[-1]] += 1
        suffix_fdist[word[-2:]] += 1
        suffix_fdist[word[-3:]] += 1
    common_suffixes = [s for s, _ in suffix_fdist.most_common(100)]
    tagged_words = brown.tagged_words(categories='news')
    featuresets = [(pos_features(w, common_suffixes), g) for w, g in tagged_words]
    return featuresets
    #return classify(nltk.DecisionTreeClassifier, featuresets, 0.1)

    
#探索上下文语境

def pos_features(sentence, i):
    word = sentence[i]
    features = {
        'suffix1': word[-1],
        'suffix2': word[-2:],
        'suffix3': word[-3:]
    }
    features['prev-word'] = sentence[i - 1] if i > 0 else '<START>'
    return features


def context_pos():
    tagged_sents = nltk.corpus.brown.tagged_sents(categories='news')
    featuresets = []
    for tagged_sent in tagged_sents:
        untagged_sent = nltk.tag.untag(tagged_sent)
        for i, (word, tag) in enumerate(tagged_sent):
            featuresets.append((pos_features(untagged_sent, i), tag))
    return classify(nltk.NaiveBayesClassifier, featuresets, 0.1)

    
#序列分类

def pos_features(sentence, i, history):
    word = sentence[i]
    features = {
        'suffix1': word[-1],
        'suffix2': word[-2:],
        'suffix3': word[-3:]
    }
    if i > 0:
        features['prev-word'] = sentence[i-1]
        features['prev-tag'] = history[i-1]
    else:
        features['prev-word'] = '<START>'
        features['prev-tag'] = '<START>'
    return features


class ConsecutivePosTagger(nltk.TaggerI):
    def __init__(self, train_sents):
        train_set = []
        for tagged_sent in train_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = pos_features(untagged_sent, i, history)
                train_set.append((featureset, tag))
                history.append(tag)
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = pos_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)


def consecutive_tag():
    return classify(ConsecutivePosTagger, nltk.corpus.brown.tagged_sents(categories='news'), 0.1)

    
#句子分割

def punct_features(tokens, i):
    return {
        'next-word-capitalized': tokens[i + 1][0].isupper(),
        'prevword': tokens[i - 1].lower(),
        'punct': tokens[i],
        'prev-word-is-one-char': len(tokens[i - 1]) == 1
    }


def sent_sep():
    tokens = []
    boundaries = set()
    offset = 0
    for sent in nltk.corpus.treebank_raw.sents():
        tokens += sent
        offset += len(sent)
        boundaries.add(offset - 1)

    featuresets = [(punct_features(tokens, i), (i in boundaries))
                   for i in range(1, len(tokens) - 1)
                   if tokens[i] in '.?!']
    return classify(nltk.NaiveBayesClassifier, featuresets, 0.1)


# 识别对话行为类型

def dialogue_act_features(post):
    return {'contains(%s)' % word.lower(): True for word in nltk.word_tokenize(post)}


def dialog_classify():
    posts = nltk.corpus.nps_chat.xml_posts()[:10000]
    featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
    return classify(nltk.NaiveBayesClassifier, featuresets, 0.1)


# 识别文字蕴含

def rte_features(rtepair):
    extractor = nltk.RTEFeatureExtractor(rtepair)
    return {
        'word_overlap': len(extractor.overlap('word')),
        'word_hyp_extra': len(extractor.hyp_extra('word')),
        'ne_overlap': len(extractor.overlap('ne')),
        'ne_hyp_extra': len(extractor.hyp_extra('ne'))
    }


# 熵和信息增益

def entropy(labels):
    import math

    freqdist = nltk.FreqDist(labels)
    probs = [freqdist.freq(l) for l in freqdist]
    return -sum([p * math.log(p, 2) for p in probs])
    