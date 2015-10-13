'''
Name: TweetViz_Hashtag_Generator
Description: This file will have class and functions which will help in understanding the user input. It
             also parse the user statement to generate tweeter hashtags.
Developer: Harsha Kadekar
Reference: For generating hashtags from sentence = "http://thetokenizer.com/2013/05/09/efficient-way-to-extract-the-main-topics-of-a-sentence/"
                                                    https://gist.github.com/5539628.git
                                                    shlomibabluki/np_extractor.py
'''

import nltk
from nltk.corpus import brown

# This is taken from above reference.
# ---------------------------------------------------------------------------------------------------------------------
# This is our fast Part of Speech tagger
#############################################################################
brown_train = brown.tagged_sents(categories='news')
regexp_tagger = nltk.RegexpTagger(
    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
     (r'(-|:|;)$', ':'),
     (r'\'*$', 'MD'),
     (r'(The|the|A|a|An|an)$', 'AT'),
     (r'.*able$', 'JJ'),
     (r'^[A-Z].*$', 'NNP'),
     (r'.*ness$', 'NN'),
     (r'.*ly$', 'RB'),
     (r'.*s$', 'NNS'),
     (r'.*ing$', 'VBG'),
     (r'.*ed$', 'VBD'),
     (r'.*', 'NN')
])
unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)
#############################################################################


# This is our semi-CFG; Extend it according to your own needs
#############################################################################
cfg = {}
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NNI"
cfg["NNI+NN"] = "NNI"
cfg["JJ+JJ"] = "JJ"
cfg["JJ+NN"] = "NNI"
#############################################################################
# -----------------------------------------------------------------------------------------


class TweetVizHashTagGenerator(object):

    def __init__(self, user_statement = ''):
        self._userstatement = user_statement
        pass

    @property
    def user_statement(self):
        return self._userstatement

    @user_statement.setter
    def user_statement(self, value):
        self._userstatement = value

    # Following code is taken from reference.
    # ----------------------------------------------------------------------------------------------------------
    # Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")
    def normalize_tags(self, tagged):
        n_tagged = []
        for t in tagged:
            if t[1] == "NP-TL" or t[1] == "NP":
                n_tagged.append((t[0], "NNP"))
                continue
            if t[1].endswith("-TL"):
                n_tagged.append((t[0], t[1][:-3]))
                continue
            if t[1].endswith("S"):
                n_tagged.append((t[0], t[1][:-1]))
                continue
            n_tagged.append((t[0], t[1]))
        return n_tagged

    # Extract the main topics from the sentence
    def extract(self):

        tokens = nltk.word_tokenize(self._userstatement)
        tags = self.normalize_tags(bigram_tagger.tag(tokens))

        merge = True
        while merge:
            merge = False
            for x in range(0, len(tags) - 1):
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = cfg.get(key, '')
                if value:
                    merge = True
                    tags.pop(x)
                    tags.pop(x)
                    match = "%s %s" % (t1[0], t2[0])
                    pos = value
                    tags.insert(x, (match, pos))
                    break

        matches = []
        for t in tags:
            if t[1] == "NNP" or t[1] == "NNI":
            # if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN":
                matches.append(t[0])
        return matches

    # ------------------------------------------------------------------------------------------------------------

    def hash_tag_generator(self):
        '''
        name: hash_tag_generator
        description: This function will parse the self._userstatement. If it has only hashtag then it will return
                     same thing. Else it will return you a list of hashtags.
        :return: list of hash tags
        '''
        hashtag_list = []
        if self._userstatement is not None and self._userstatement.__len__() > 0:
            temp_list = self.extract()

            temp_sent = self._userstatement.replace(' ', '')
            hashtag_list.append(temp_sent)

            for string in temp_list:
                temp_sent = string.replace(' ', '')
                hashtag_list.append(temp_sent)

        return hashtag_list

'''
# Main method, just run "python np_extractor.py"
def main():

    sentence = "Swayy is a beautiful new dashboard for discovering and curating online content."
    np_extractor = TweetVizHashTagGenerator(sentence)

    result = np_extractor.hash_tag_generator()
    print(sentence)
    print "This sentence is about: %s" % ", ".join(result)
    np_extractor.user_statement = "RCB is playing well in IPL 2015"
    result = np_extractor.hash_tag_generator()
    print(np_extractor.user_statement)
    print "This sentence is about: %s" % ", ".join(result)
    np_extractor.user_statement = "Sundevil is awesome"
    result = np_extractor.hash_tag_generator()
    print(np_extractor.user_statement)
    print "This sentence is about: %s" % ", ".join(result)

if __name__ == '__main__':
    main()
'''
