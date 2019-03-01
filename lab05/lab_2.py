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
    ('Cancer', '', 0.01),
    ('Test1', 'Cancer', {T: 0.90, F: 0.2}),
    ('Test2', 'Cancer', {T: 0.90, F: 0.2})
    ])

# Compute P(Cancer | Test1 ^ Test2).
# A * P(Test1 ^ Test2 ^ Cancer) = A * P(Cancer) * P(Test1 | Cancer) * P(Test2 | Cancer)
#                                 A * .01 * .9 * .9 = .0081
# A * P(-Cancer) * P(Test1 | -Cancer) * P(Test2 | -Cancer)
# A * .99 * .2 * .2 = 0.0396
# .0081 / (.0396 + .0081) = .17
# .0396 / (.0396 + .0081) = .83

# Even though both tests are true, the chance starts so low, and the tests have enough uncertainty
# to leave the answer still quite unlikely
print(enumeration_ask('Cancer', dict(Test1=T, Test2=T), cancer).show_approx())

# Compute P(Cancer | Test1 ^ -Test2).
# A * P(Test1 ^ -Test2 ^ Cancer) = A * P(Cancer) * P(Test1 | Cancer) * P(-Test2 | Cancer)
#                                 A * .01 * .9 * .1 = .0009
# A * P(-Cancer) * P(Test1 | -Cancer) * P(-Test2 | -Cancer)
# A * .99 * .2 * .8 = 0.1584
# .0009 / (.1584 + .0009) = .005
# .01584 / (.1584 + .0009) = .995

# 1 test being false makes it 3-4x less likely, which makes sense given the test is only ~4x as likely
# to work if cancer is present.
print(enumeration_ask('Cancer', dict(Test1=T, Test2=F), cancer).show_approx())

# These answers both make sense, though they aren't necessarily intuitive. Cancer is very unlikely and
# The tests have a fairly high 20% chance of false positive, so they wouldn't be that effective.
