import json
from mock import Mock
from ConfigParser import SafeConfigParser

from slackclient import SlackClient

from message import Message
from plugins.creative_quit import CreativeQuitPlugin
from plugins.puppy_plugin.puppy_plugin import PuppyCommandPlugin

CONFIG_FILE = 'slack.conf'

MESSAGE_CHANGED = u'message_changed'


class SlackBot(object):
    handled = False   
    commands = {}

    def __init__(self, settings, plugins):
        self.settings = settings.get('slack', {})
        self.factory = Mock(message_plugins=[],
                            taunt_plugins=[],
                            command_plugins=plugins)
        self.slack =  SlackClient(self.settings.get('token', ''))
        self.nickname = self.settings.get('slackbot_id')
        self._add_plugins(plugins)

    def _add_plugins(self, plugins):
        for plugin in plugins:
            try:
                self.commands.update(plugin.install(self))
            except Exception as e:
                print "Could not install %s: %s" % (plugin.name, e)

    def listen(self):
        if self.slack.rtm_connect():
            while True: 
                for event in self.slack.rtm_read():
                    self.handle(event)
                    
        else:
            print "Connection failed"   

    def msg(self, channel, message):
        self.slack.rtm_send_message(channel, message)

    # channel = channel from read message
    def handle(self, message):
        # TODO: handle direct messages?
        #print message
        #print '*'*160
        try:
            message = self._ensure_valid_message(message)
        except KeyError as e:
            return 
        if self._is_valid_command(message): 
            try:
                command = Message(message[u'user'], 
                                  message[u'channel'],
                                  message[u'text'], 
                                  self)
                command.handle()
            except KeyError as e:
                print 'Cannot handle this message because %s: %s' % (e, message)
            except Exception as error:
                print error

    def _ensure_valid_message(self, message):
        if message[u'type'] != 'message':
            return message
        if message.get('subtype', '') == MESSAGE_CHANGED:
            # reformat it to be like a fresh message
            message[u'text'] = message[u'message'][u'text']
            message[u'user'] = message[u'message'][u'user']
        return message

    def _is_valid_command(self, message):
        if self.nickname in message.get(u'user', ''):
            return False
        if self.settings.get('no_roam', True) and \
            message.get(u'channel', '') not in self.settings.get('allowed_channels', []):
            return False
        return self.nickname in message.get(u'text', '')


def read_config(config_file):
    config = SafeConfigParser()
    config.read(config_file)
    config_dict = {}
    for section in config.sections():
        config_dict[section] = dict(config.items(section))
    if not config_dict:
        raise Exception("No configs were loaded from %s" % config_file)
    return config_dict


def main():
    commands = [PuppyCommandPlugin, CreativeQuitPlugin]
    settings = read_config(CONFIG_FILE)
    bot = SlackBot(settings, commands)
    bot.listen()


if __name__ == "__main__":
    main()
