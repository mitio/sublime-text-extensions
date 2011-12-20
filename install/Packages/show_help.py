'''
A simple plugin which allows you to quickly open up in your browser a help page
for a given function or keyword which is currently under your cursor.

You may want to add this command in your key bindings file ("Key Bindings - User").
For example, you could add something like this:

    // Show help on the current word (TextMate-style help)
    { "keys": ["ctrl+h"], "command": "show_help" },

You can modify existing or add additional help resource URLs by creating a "help_resources"
key in your User-settings file and a corresponding dictionary of "syntax name - help resource URL"
pairs, like so:

    "help_resources":
    {
        "Ruby": "http://google.com/search?q=%s",
        'PHP":  "http://php.net/%s"
    }

"%s" will be replaced with the word under your cursor when you invoke the command.

The default help resource URL is a Google search. In this case, the syntax name is also added
to the search query to help in narrowing results down. You can use that syntax name to define
a more precise help resource URL in your settings. The syntax name for the current view is also
visible in the bottom right corner of your status bar.

@author: Dimitar Dimitrov <wireman@gmail.com>

@license: MIT (http://www.opensource.org/licenses/mit-license.php)
'''

import sublime, sublime_plugin
import webbrowser
import os.path
import urllib

class ShowHelpCommand(sublime_plugin.TextCommand):
    SETTING_NAME   = 'help_resources'
    HELP_RESOURCES = {
        '__default__':      'http://www.google.com/search?q=%s',
        'PHP':              'http://php.net/%s',
        'Ruby':             'http://apidock.com/ruby/search/quick?query=%s',
        'Ruby on Rails':    'http://apidock.com/rails/search/quick?query=%s',
        'RSpec':            'http://apidock.com/rspec/search/quick?query=%s',
    }

    def run(self, edit):
        for s in reversed(self.view.sel()):
            word_region = self.view.word(s)
            word = self.view.substr(word_region)

            syntax_name, _ = os.path.splitext(os.path.basename(self.view.settings().get('syntax')))
            help_resources = self.view.settings().get(self.SETTING_NAME, {})

            if type(help_resources) == dict:
                help_resource = help_resources.get(syntax_name, self.HELP_RESOURCES.get(syntax_name))

                if not help_resource:
                    help_resource = self.HELP_RESOURCES['__default__']
                    word += ' ' + syntax_name

                help_resource = help_resource % (urllib.quote(word))

                sublime.status_message('Showing help for "%s" in "%s"' % (word, syntax_name))
                webbrowser.open(help_resource)
            else:
                sublime.error_message(
                    'The setting "help_resources" has a wrong type of %s.\n'
                    'It should be a dictionary.\n\n'
                    'Please fix your settings file and try again.' % type(help_resources)
                )
