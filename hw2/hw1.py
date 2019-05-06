spam_corpus = [["i", "am", "spam", "spam", "i", "am"], ["i", "do", "not", "like", "that", "spamiam"]]
ham_corpus = [["do", "i", "like", "green", "eggs", "and", "ham"], ["i", "do"]]

from probability import BayesNet, enumeration_ask, elimination_ask, gibbs_ask
import math

# Utility variables
T, F = True, False

tokens = []

spam_hash = {}
for m in spam_corpus:
    for w in m:
        if w in spam_hash:
            spam_hash[w] += 1
        else:
            spam_hash[w] = 1
        if not w in tokens:
            tokens.append(w)

ham_hash = {}
for m in ham_corpus:
    for w in m:
        if w in ham_hash:
            ham_hash[w] += 1
        else:
            ham_hash[w] = 1
        if not w in tokens:
            tokens.append(w)


probs = {}
for t in tokens:
    g = 0
    if t in ham_hash:
        g = ham_hash[t] * 2

    b = 0
    if t in spam_hash:
        b = spam_hash[t] * 2

    if b + g < 1:
        continue

    probs[t] = max(.01, min(.99, float(min(1.0, b / 2) / (min(1.0, g / 2) + min(1.0, b / 2)))))


def analyze(message):
    prod = 1
    for w in message:
        if w not in probs:
            prod *= .4
        else:
            prod *= probs[w]
    inv_prod = 1
    for w in message:
        if w not in probs:
            inv_prod *= .6
        else:
            inv_prod *= 1 - probs[w]

    return prod / (prod + inv_prod)


m1 = ['and']
m2 = ['do']
m3 = ['spam']
m4 = ['ham']


print("and", analyze(m1))
print("do", analyze(m2))
print("spam", analyze(m3))
print("ham", analyze(m4))