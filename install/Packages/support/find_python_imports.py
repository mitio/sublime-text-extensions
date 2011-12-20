'''
A script to parse some text and extract all imports.

@author: Oktay Acikalin <ok@ryotic.de>

@license: MIT (http://www.opensource.org/licenses/mit-license.php)

@since: 2011-02-20
'''

import string


MODULE_CHARS = string.letters + string.digits + '_' + '.'
SYMBOL_CHARS = string.letters + string.digits + '_'
CONTENT_WHITESPACE = string.whitespace + ';'
MAX_CYCLES = 1000


def consume_chars(content, chars):
    '''
    Consumes content from given content as long as it contains given chars.

    @type  content: str
    @param content: Content to consume.
    @type    chars: str
    @param   chars: Chars to accept.

    @rtype:  tuple
    @return: Consumed text and rest of content.
    '''
    pos = 0
    consumed = None
    pos = 0
    for char in content:
        if char not in chars:
            break
        pos += 1
    consumed = content[:pos]
    content = content[pos:]
    return consumed, content.lstrip(' \t')


def consume_words(content, words):
    '''
    Consumes content from given content as long as it contains given words.

    @type  content: str
    @param content: Content to consume.
    @type    words: list
    @param   words: List of words to accept.

    @rtype:  tuple
    @return: Consumed text and rest of content.
    '''
    consumed = None
    for word in words:
        if content.startswith(word):
            consumed = content[:len(word)]
            content = content[len(word):]
            break
    return consumed, content.lstrip(' \t')


def parse(content):
    '''
    Parses given contents and returns all imports found.

    @type  content: str
    @param content: Text to parse.

    @rtype:  list
    @return: A list of imports as tuple(type, module, symbols)
    '''
    imports = []
    max_cycles = MAX_CYCLES
    cycle = 0
    while content:
        # print cycle, 'content ='
        # print repr(content)
        cycle += 1
        if cycle > max_cycles:
            raise Exception('Endless loop detected.')
        action, content = consume_words(content.lstrip(CONTENT_WHITESPACE),
                                        ['from', 'import'])
        # print action
        if action == 'from':
            module, content = consume_chars(content, MODULE_CHARS)
            # print module
            action, content = consume_words(content, ['import'])
            # print action
            if not action:
                raise Exception('Syntax error!')
            is_bracket, content = consume_words(content, ['('])
            if is_bracket:
                # print 'IS BRACKET'
                symbols = []
                cycle_ = 0
                while len(content):
                    # print cycle_, 'content =', repr(content)
                    cycle_ += 1
                    if cycle_ > MAX_CYCLES:
                        raise Exception('Endless loop detected.')
                    is_bracket, content = consume_words(content, [')'])
                    if is_bracket:
                        break
                    symbol, content = consume_chars(content, SYMBOL_CHARS)
                    is_alias, content = consume_words(content, ['as'])
                    if is_alias:
                        alias, content = consume_chars(content, MODULE_CHARS)
                        # print 'as'
                        # print alias
                        symbol = (symbol, alias)
                    # print symbol
                    if symbol:
                        symbols.append(symbol)
                    _, content = consume_words(content, [',', '\n'])
                # print 'symbols =', symbols
            else:
                # print 'NO BRACKET'
                symbols = []
                cycle_ = 0
                while len(content):
                    # print cycle_, 'content =', repr(content)
                    cycle_ += 1
                    if cycle_ > MAX_CYCLES:
                        raise Exception('Endless loop detected.')
                    is_eol, content = consume_words(content, ['\n', ';'])
                    if is_eol:
                        break
                    symbol, content = consume_chars(content, SYMBOL_CHARS)
                    is_alias, content = consume_words(content, ['as'])
                    if is_alias:
                        alias, content = consume_chars(content, MODULE_CHARS)
                        # print 'as'
                        # print alias
                        symbol = (symbol, alias)
                    # print symbol
                    if symbol:
                        symbols.append(symbol)
                    _, content = consume_words(content, [','])
                # print 'symbols =', symbols
            imports.append(('from_a_import_b', module, symbols))
        elif action == 'import':
            cycle_ = 0
            while len(content):
                # print cycle_, 'content =', repr(content)
                cycle_ += 1
                if cycle_ > MAX_CYCLES:
                    raise Exception('Endless loop detected.')
                is_eol, content = consume_words(content, ['\n', ';'])
                if is_eol:
                    break
                module, content = consume_chars(content, MODULE_CHARS)
                is_alias, content = consume_words(content, ['as'])
                if is_alias:
                    alias, content = consume_chars(content, MODULE_CHARS)
                    # print 'as'
                    # print alias
                    module = (module, alias)
                # print module
                if module:
                    imports.append(('import', module, []))
                _, content = consume_words(content, [','])

        else:
            # print 'ELSE'
            # Here we test if it makes sense to further try to understand.
            module = content if '\n' not in content else \
                     content[:content.find('\n')]
            module, rest = consume_chars(module, MODULE_CHARS)
            is_alias, rest = consume_words(rest, ['as'])
            if is_alias:
                alias, rest = consume_chars(rest, MODULE_CHARS)
                if alias:  # Since we detected an alias, let's throw rest away.
                    rest = ''
            # print 'module =', repr(module), repr(is_alias)
            # print 'rest =', repr(rest)
            if not rest and module:  # Looks like we got only a word in a line.
                module, content = consume_chars(content, MODULE_CHARS)
                # print module
                is_alias, content = consume_words(content, ['as'])
                if is_alias:
                    alias, content = consume_chars(content, MODULE_CHARS)
                    # print 'as'
                    # print alias
                    module = (module, alias)
                imports.append(('textref', module, []))
            else:
                # Let's give up on rest of content.
                content = '' if '\n' not in content else \
                          content[content.find('\n'):]
        # print '---'
    return imports


def filter_imports(imports):
    '''
    Filters all imports of given import list.

    @type  imports: list
    @param imports: List with imports from parse() above.

    @rtype:  list
    @return: List of filtered entries.
    '''
    results = []
    for entry in imports:
        if entry[0] in ('import', 'from_a_import_b'):
            results.append(entry)
    return results


def filter_textrefs(imports):
    '''
    Filters all textual references of given import list.

    @type  imports: list
    @param imports: List with imports from parse() above.

    @rtype:  list
    @return: List of filtered entries.
    '''
    results = []
    for entry in imports:
        if entry[0] == 'textref':
            results.append(entry)
    return results


def main():
    '''
    Little routine to test the code above and make sure that it works properly.
    This test has to be used manually (contains no asserts).

    @return: None
    '''
    content = '''
    #!/usr/bin/env python

    """
    File header

    See code.app.verbose for more! Or here:
    code.app.things
    """

    a = b

    from code.app.process.exception import (StopProcess,
        ContinueProcess, ProcessException)
    from code.app.util.event import Event
    from code.app.util.event import Event, Bla, Blub
    from code.app.process.exception import StopProcess, \
        ContinueProcess, ProcessException
    import string
    import string as ding
    from code.app.util.event import Event as ding
    

    from code.app.process.exception import (StopProcess,
        ContinueProcess, ProcessException as BlaaaaException)
    from code.app.util.event import Event as tric, bla as tic, blub as trac

    from code.app.process.exception import StopProcess as a, \
        ContinueProcess as c, ProcessException
    
    import ..code.app.util
    from ..code.app.util import bla
    from ..code.app.util import bla as blub
    code.app.process.exception
    code.app.process.exception as bam <-- look here!

    import a; import b as some;from d import g; import c
    import a,b,c;import d, e, f;

    class Bla(bam):

        def function():
            from code.utils import some_things
            print some_things
        
        def another_function():
            import code.utils.some_things
            print some_things
    '''
    imports = parse(content)
    for import_ in imports:
        print import_
    print
    print 'Got %d import statements.' % len(filter_imports(imports))
    print 'Got %d textual references.' % len(filter_textrefs(imports))


if __name__ == '__main__':
    main()
