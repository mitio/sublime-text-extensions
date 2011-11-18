'''
Collects views, creates a unified diff and pastes it into a scratch view.

You might want to override the following parameters within your file settings:
* diff_views_syntax_file
  Set this to your syntax file or None if you don't have one.

In order to access the commands you have to add these to your key bindings:
{ "keys": ["ctrl+d"], "command": "diff_views_mark" },
{ "keys": ["ctrl+shift+d"], "command": "diff_views_execute" },

You also might want to add this to your user defined Main.sublime-menu file:
{
    "caption": "Diff",
    "children": [
        {"caption": "Mark view for diff", "command": "diff_views_mark"},
        {"caption": "Diff marked views", "command": "diff_views_execute"}
    ]
}

@author: Oktay Acikalin <ok@ryotic.de>

@license: MIT (http://www.opensource.org/licenses/mit-license.php)

@since: 2011-02-27
'''

import os
import difflib

import sublime
import sublime_plugin


DEFAULT_DIFF_SYNTAX_FILE = 'Packages/Diff/Diff.tmLanguage'

views = []


class LineReader(object):

    def __init__(self, view):
        size = view.size()
        regions = view.split_by_newlines(sublime.Region(0, size))
        self.regions = regions
        self.index = 0
        self.view = view
        self.filename = view.file_name()
        self.name = os.path.basename(self.filename)
    
    def __iter__(self):
        return self
    
    def __len__(self):
        return len(self.regions)
    
    def __getitem__(self, pos):
        region = self.regions[pos]
        return self.view.substr(region)
    
    def __getslice__(self, start, stop):
        regions = self.regions[start:stop]
        return ['%s\n' % self.view.substr(region) for region in regions]

    def next(self):
        if self.index >= len(self.regions):
            raise StopIteration
        region = self.regions[self.index]
        self.index += 1
        return self.view.substr(region)


class DiffViewsMarkCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        global views
        views.append(self.view)
        views = views[-2:]
        sublime.status_message('Added "%s" for diff.' % self.view.file_name())


class DiffViewsExecuteCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        syntax_file = self.view.settings().get('diff_views_syntax_file',
                                               DEFAULT_DIFF_SYNTAX_FILE)
        # print views
        if len(views) < 2:
            sublime.status_message('Need at least 2 views for diff. Got %d.'
                                   % len(views))
            return
        left = LineReader(views[0])
        right = LineReader(views[1])
        diff = difflib.unified_diff(left, right,
                                    left.filename, right.filename, n=9)
        view = self.view.window().new_file()
        view.set_scratch(True)
        filename = '%s vs %s.patch' % (left.name, right.name)
        view.set_name(filename)
        edit = view.begin_edit()
        buffer = ''
        for line in diff:
            buffer += line
            if len(buffer) >= 1024:
                view.insert(edit, view.size(), buffer)
                buffer = ''
        if len(buffer):
            view.insert(edit, view.size(), buffer)
        view.end_edit(edit)
        settings = view.settings()
        # settings.set('line_numbers', False)
        if syntax_file:
            settings.set('syntax', syntax_file)
        # view.set_read_only(True)
