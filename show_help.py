import sublime, sublime_plugin
import webbrowser
import os.path
import urllib

class ShowHelpCommand(sublime_plugin.TextCommand):
    HELP_RESOURCES = {
        '__default__':      'http://www.google.com/search?q=%s',
        'PHP':              'http://php.net/%s',
        'Ruby':             'http://apidock.com/ruby/search/quick?query=%s',
        'Ruby on Rails':    'http://apidock.com/rails/search/quick?query=%s',
    }

    def run(self, edit):
        for s in reversed(self.view.sel()):
            word_region = self.view.word(s)
            word = self.view.substr(word_region)

            syntax_name, _ = os.path.splitext(os.path.basename(self.view.settings().get('syntax')))
            help_resources = self.view.settings().get('help_resources', {})

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
