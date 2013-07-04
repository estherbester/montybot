# TODO: This sucks.

from get_puppy import get_puppy


def puppy():
    return "Puppy time! %s" % get_puppy('puppies')


def corgi():
    return "OMG corgi! %s" % get_puppy('corgies')


def pug():
    return "Pug for you: %s" % get_puppy('pugs')


def doxy():
    return "Dachshund time: %s" % get_puppy('doxies')


class PuppyCommandPlugin(object):
    """
    Commands to respond to for puppy links
    """
    commands = {
        'puppy time': puppy,
        'corgi time': corgi,
        'pug please': pug,
        'hotdog': doxy
    }

    @classmethod
    def install(cls):
        return cls.commands
