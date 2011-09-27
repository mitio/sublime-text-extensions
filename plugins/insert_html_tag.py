'''
This plugin allows you to wrap your current selection with a pair of open and close HTML/HTML tags.
The selection is then moved onto the tag names so that you can easily change them if needed.

You may want to add this command in your key bindings file ("Key Bindings - User").
Suggested key binding:

    // Insert HTML tags around the selection
    { "keys": ["ctrl+w"], "command": "insert_html_tag" },

The default tag name inserted is "div". You can change this default by adding a "default_html_tag_to_insert"
key to your User-settings, like so:

    "default_html_tag_to_insert": "p"

@author: Dimitar Dimitrov <wireman@gmail.com>

@license: MIT (http://www.opensource.org/licenses/mit-license.php)
'''

import sublime, sublime_plugin

class InsertHtmlTagCommand(sublime_plugin.TextCommand):
    TAG_NAME     = 'div'
    SETTING_NAME = 'default_html_tag_to_insert'

    def run(self, edit):
        new_selection_positions = []
        tag_name = self.view.settings().get(self.SETTING_NAME, self.TAG_NAME)

        for s in self.view.sel():
            open_tag  = '<%s>' % (tag_name)
            close_tag = '</%s>' % (tag_name)

            open_position  = s.begin()
            close_position = s.end() + len(open_tag)

            # remove the current selection
            self.view.sel().subtract(s)

            # insert the opening and closing tags
            self.view.insert(edit, open_position, open_tag)
            self.view.insert(edit, close_position, close_tag)

            # prepare to select the opening and closing tags's names
            new_selection_positions.append(open_position + 1)
            new_selection_positions.append(close_position + 2)

        # create the new selections, if any
        for p in new_selection_positions:
            self.view.sel().add(sublime.Region(p, p + len(tag_name)))
