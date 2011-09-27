SublimeText 2 Extensions
========================

Here you can find some [SublimeText 2](http://sublimetext.com/2) extensions I've written to make this
great editor even more convenient. The extensions include plugins, snippets and also some configuration
options and key bindings. Basically, everything major I found the need to modify in order to suit my
needs better.

Plugins
-------

Plugins live under the `plugins/` folder. Each plugin usually spans only a single Python file.

To find out more about the purpose or example usage of a given plugin, please check the
corresponding Python file. The description of the plugin should be at the beginning of the file.

Snippets
--------

Snippets reside under the `snippets/` folder. They're just small XML files. You can easily customize
them if you wish. You can find more info about snippets in the
[unofficial documentation](http://sublimetext.info/docs/en/extensibility/snippets.html).

Installation
------------

* To install a plugin, you just need to place the corresponding Python file into your
  [SublimeText 2's `Packages` folder](http://sublimetext.info/docs/en/basic_concepts.html#the-packages-directory).
  The location of this folder is OS-specific. You can find more details on the subject in the
  [unofficial documentation](http://sublimetext.info/docs/en/extensibility/plugins.html).

* To install a snippet, you need to place the snippet file under any subfolder of `Packages`. If you
  place the snippet deeper in the file hierarchy, it will not be automatically loaded by SublimeText 2.