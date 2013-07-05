# TODO: This sucks.

from get_puppy import get_puppy


class PupCommand(object):
    reply_string = "{prefix}: {msg}"

    puppies = {
        'puppy': "Puppy lottery!",
        'corgi': "OMG corgi!",
        'pug': "Pug for you",
        'doxy': "Dachshund time"
    }

    def __init__(self, puppy_type):
        prefix = self.puppies.get(puppy_type, 'puppy')
        link = get_puppy(puppy_type)
        return self.reply_string.format(prefix=prefix, msg=link)


class PuppyCommandPlugin(object):
    """
    Commands to respond to for puppy links
    """
    name = 'Puppy Commands'

    MAX_CALLS = 80
    throttler = None

    commands = {
        'puppy time': PupCommand('puppy'),
        'corgi time': PupCommand('corgi'),
        'pug please': PupCommand('pug'),
        'hotdog': PupCommand('doxy')
    }

    @classmethod
    def install(cls):
        #cls.throttler = Throttler('flickr')
        return cls.commands
