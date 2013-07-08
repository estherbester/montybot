import random

video = 'https://www.youtube.com/watch?v=zGxwbhkDjZM'

SMARTASS_REPLY_LIST = [
    'No comprendo',
    'Quoi?!',
    'What the *what*?',
    "Ain't nobody got time for dat! %s" % video
]


def smartass_reply():
    return random.choice(SMARTASS_REPLY_LIST)
