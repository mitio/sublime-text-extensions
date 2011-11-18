'''
Converts text encoding of a file from one to another.
For using add something like this to your user definable key bindings file:
{ "keys": ["ctrl+super+e"], "command": "convert_encoding" }

@author: Oktay Acikalin <ok@ryotic.de>

@license: MIT (http://www.opensource.org/licenses/mit-license.php)

@since: 2011-02-11
'''

import sublime
import sublime_plugin


# See http://docs.python.org/library/codecs.html for more info.
DEFAULT_COMMAND = 'iso-8859-1 to utf8'


class ConvertEncodingCommand(sublime_plugin.TextCommand):
    '''
    A text command to convert text encoding of a file from one to another.
    '''

    def _replace(self, command):
        try:
            command = map(unicode.strip, command.split(' to '))
            from_, to_ = filter(lambda x: x.strip, command)
        except Exception, excp:
            print excp
            sublime.status_message('Error: Syntax is "<source> to <dest>"')
            return
        
        filename = self.view.file_name()

        try:
            fh = open(filename, 'rb')
            data = fh.read()
            fh.close()

            # print 'repr =', data.__repr__()
            unidata = unicode(data, from_)
            # print 'unicode =', unidata.__repr__()
            destdata = unidata.encode(to_)
            # print 'destdata =', destdata.__repr__()

            fh = open(filename, 'wb')
            fh.write(destdata)
            fh.close()
        except Exception, excp:
            print excp
            sublime.status_message('Error: %s' % excp)
            self.view.window().run_command('show_panel', dict(panel='console'))

    def run(self, edit):
        '''
        Tries to convert text encoding of a file from one to another.

        @type  edit: sublime.Edit
        @param edit: Object used for replacement actions.

        @return: None
        '''
        if self.view.is_dirty():
            sublime.status_message('File has been changed. Save it first!')
            return
        
        window = self.view.window()
        window.show_input_panel('Convert', DEFAULT_COMMAND,
                                self._replace, None, None)
