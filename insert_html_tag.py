import sublime, sublime_plugin

class InsertHtmlTagCommand(sublime_plugin.TextCommand):
    TAG_NAME = 'div'

    def run(self, edit):
        new_selection_positions = []

        for s in self.view.sel():
            open_tag  = '<%s>' % (self.TAG_NAME)
            close_tag = '</%s>' % (self.TAG_NAME)

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
            self.view.sel().add(sublime.Region(p, p + len(self.TAG_NAME)))
