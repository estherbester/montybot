from plugin_metaclass import PluginMetaClass
LINK_LOG_FILE = 'links_in_channel.txt'


class IRCLogger(object):

    __metaclass__ = PluginMetaClass

    log_string_format = u"{user} ({timestamp}): {note}"

    def __init__(self, log_file):
        self.log_file = log_file

    def log(self, link, source):
        with open(self.log_file, 'a') as link_log:
            link_log.write("\r%s\n" % self.log_string_format.format(user=source,
                                                                  timestamp=link.timestamp,
                                                                  url=link.url,
                                                                  note=link.formatted_string))
