Quick Install
=============

If you're using Mac OS X (or Linux), you can quickly install all of the extentions here "as-is", using
the `./install.sh` script. It installs into your Sublime Text 2's shared folder (it's OS-dependent).
The script tries to detect it and has been tested on Mac OS X and Ubuntu.

1. Quit all running instances of Sublime Text 2
2. Run `./install.sh`

After that, you may need to adjust the settings in the following files:

* `$SUBLIME_SHARED_FOLDER/Packages/User/Base\ File.sublime-settings` -- you may need to adjust the
  `font_face` and `font_size` properties (you may not have my fonts installed).
* `$SUBLIME_SHARED_FOLDER/Packages/User/Global.sublime-settings` -- you may need to comment this line
  if you're experiencing glitches/rendering problems in the chrome UI of Sublime.

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

Settings
--------

In the `settings/` folder you will find all of my SublimeText 2's configuration files, including
key bindings, chrome UI themes, global settings, etc. These files reside under my `Packages/User`
folder. In them you may stumble on references to plugins not (yet) present in this repository.
They're probably plugins from
[theblacklion's sublime_plugins project](https://bitbucket.org/theblacklion/sublime_plugins/overview).

Installation
------------

* **To install a plugin**, you just need to place the corresponding Python file into your
  [SublimeText 2's `Packages` folder](http://sublimetext.info/docs/en/basic_concepts.html#the-packages-directory).
  The location of this folder is OS-specific. You can find more details on the subject in the
  [unofficial documentation](http://sublimetext.info/docs/en/extensibility/plugins.html).

* **To install a snippet**, you need to place the snippet file under any subfolder of `Packages`. If you
  place the snippet deeper in the file hierarchy, it will not be automatically loaded by SublimeText 2.

* **As for the settings**, you can just place the appropriate config file somewhere under your `Packages/User`
  folder. I use hardlinks between my clone of this Git repo and the file under `Packages/User`.