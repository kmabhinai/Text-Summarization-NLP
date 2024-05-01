import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """The Avengers are an all-star ensemble cast of established superhero characters from the Marvel Comics portfolio. Diegetically, these superheroes usually operate independently but occasionally assemble as a team to tackle especially formidable villains. This in contrast to certain other superhero teams such as the X-Men, whose characters were created specifically to be part of their team, with the team being central to their identity. The Avengers were created to create a new line of books to sell and to cross-promote Marvel Comics characters. An Iron Man fan might buy an Avengers book because Iron Man appears in them, and perhaps in turn take an interest in Thor, who appears in the same book as Iron Man's friend and comrade.[2] The cast usually features a few highly popular characters who have their own solo books, such as Iron Man, alongside a number of lesser-known characters who benefit from exposure, such as Quicksilver.[3]"""


def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    # print(stopwords)

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(rawdocs)
    # print(doc)

    tokens = [token.text for token in doc]
    # print(tokens)

    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1
    # print(word_freq)

    max_freq = max(word_freq.values())
    print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq
    # print(word_freq)

    sent_tokens = [sent for sent in doc.sents]
    # print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    # print(sent_scores)

    select_len = int(len(sent_tokens) * 0.30)
    print(select_len)

    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    # print(summary)

    final_summary = [word.text for word in summary]
    summary = " ".join(final_summary)
    # print(text)
    # print(summary)

    # print("Length of original text ",len(text.split(' ')))
    # print("Length of Summary text ",len(summary.split(' ')))

    return summary, doc, len(rawdocs.split(" ")), len(summary.split(" "))
