#!/bin/sh

unamestr=`uname`
if [ "$unamestr" = 'Linux' ]; then
	SUBLIME_SHARED_FOLDER="$HOME/.config/sublime-text-2/"
elif [ "$unamestr" = 'Darwin' ]; then
	SUBLIME_SHARED_FOLDER="$HOME/Library/Application Support/Sublime Text 2/"
else
	echo 'Unsupported platform!'
	echo 'Please inspect the install.sh script and manually set the SUBLIME_SHARED_FOLDER variable.'
	exit 1
fi

echo "Installing the following packages to: ${SUBLIME_SHARED_FOLDER}"

INSTALL_SOURCE=`dirname "$0"`
INSTALL_SOURCE="${INSTALL_SOURCE}/install/Packages"

ls $INSTALL_SOURCE | while read package
do
	echo "  ${package}"
done

cp -r ${INSTALL_SOURCE} "${SUBLIME_SHARED_FOLDER}"

echo "Done."
