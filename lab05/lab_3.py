'''
This module implements the Bayesian network shown in the text, Figure 14.2.
It's taken from the AIMA Python code.

@author: kvlinden
@version Jan 2, 2013
'''

from probability import BayesNet, enumeration_ask, elimination_ask, gibbs_ask

# Utility variables
T, F = True, False

# From AIMA code (probability.py) - Fig. 14.2 - burglary example
cancer = BayesNet([
    ('Raise', '', 0.01),
    ('Sunny', '', 0.7),
    ('Happy', 'Sunny Raise', {(T, T): 1.0, (T, F): 0.7, (F, T): 0.9, (F, F): 0.1})
    ])

# Compute P(Raise | Sunny).
# Raise and Sunny are independant, so it should be the same as listed
print(enumeration_ask('Raise', dict(Sunny=T), cancer).show_approx())

# Compute P(Raise | Sunny ^ Happy).
# A * P(Happy ^ Raise ^ Sunny) = A * P(Happy | Raise ^ Sunny) * P(Sunny) * P(Raise)
# 1 * .7 * .01 = .007
# A * P(Happy ^ -Raise ^ Sunny) = A * P(Happy | -Raise ^ Sunny) * P(Sunny) * P(-Raise)
# .7 * .7 * .99 = .4851

# Normalized = .0142, .9858
# Raise is unlikely, and happy can easily be explained by Sunny
print(enumeration_ask('Raise', dict(Sunny=T, Happy=T), cancer).show_approx())

# These first 2 answers make sense, The raise is quite unlikely, so if it's sunny there isn't reason
# to think that it would be the raise.

# Raise is unlikely, and sunny is quite likely, so it can still easily explain happiness
print(enumeration_ask('Raise', dict(Happy=T), cancer).show_approx())
# Even when it's not sunny, it's still 10x more likely to be happy without a raise than to get a raise.
print(enumeration_ask('Raise', dict(Happy=T, Sunny=F), cancer).show_approx())

# These 2 answers make sense, the only way to get any likelihood of it being a raise is to know
# that it is not sunny to remove that potential explanation. Even still, it won't be super likely
# since the raise is much less likely than just being happy.
