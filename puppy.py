# TODO: This sucks.

from get_puppy import get_puppy
from throttler import Throttler


class PupCommand(object):
    reply_string = "{prefix}: {msg}"

    puppies = {
        'puppy': "Puppy lottery!",
        'corgi': "OMG corgi!",
        'pug': "Pug for you",
        'doxy': "Dachshund time"
    }

    #throttler = Throttler('flickr')

    #@throttler.track
    def __init__(self, puppy_type):
        self.puppy_type = puppy_type

    def __call__(self):
        prefix = self.puppies.get(self.puppy_type, 'puppy')
        link = get_puppy(self.puppy_type)
        return self.reply_string.format(prefix=prefix, msg=link)


class PuppyCommandPlugin(object):
    """
    Commands to respond to for puppy links
    """
    name = 'Puppy Commands'
    MAX_CALLS = 80

    commands = {
        'puppy lottery': PupCommand('puppy'),
        'corgi time': PupCommand('corgi'),
        'pug please': PupCommand('pug'),
        'hotdog': PupCommand('doxy')
    }

    def __init__(self, bot_instance):
        self.bot_instance = bot_instance

    @classmethod
    def install(cls, bot_instance):
        cls.__init__(bot_instance)
        return cls.commands
