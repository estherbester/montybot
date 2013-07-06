# TODO: This sucks.


from get_puppy import PupCommand


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
