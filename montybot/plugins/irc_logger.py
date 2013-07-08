from .metaclass import PluginMetaClass

LINK_LOG_FILE = 'links_in_channel.txt'


class IRCLogger(object):
    """ A somewhat generic logger class """
    __metaclass__ = PluginMetaClass

    log_string_format = u"{user} ({timestamp}): {note}"

    def __init__(self, log_file):
        self.log_file = log_file

    def log(self, message, source):
        # message is an object containing a timestamp and the text encapsulated
        # in message.text
        with open(self.log_file, 'a') as link_log:
            link_log.write("\r%s\n" %
             self.log_string_format.format(user=source,
                                           timestamp=message.timestamp,
                                           note=message.text))
