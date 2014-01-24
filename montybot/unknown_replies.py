import random

video = 'https://www.youtube.com/watch?v=zGxwbhkDjZM'
puppy_fail = 'http://gifs.gifbin.com/032013/1363630355_puppy_catch_fail.gif'

SMARTASS_REPLY_LIST = [
    'No comprendo',
    "You're gonna have to make a pull request for that",
    '<-- %s' % (puppy_fail,),
    'What the *what*?',
    "Ain't nobody got time for dat! %s" % video
]


def smartass_reply():
    return random.choice(SMARTASS_REPLY_LIST)
