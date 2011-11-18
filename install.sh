#!/bin/sh

unamestr=`uname`
if [ "$unamestr" == 'Linux' ]; then
	SUBLIME_SHARED_FOLDER="~/.config/sublime-text-2"
elif [ "$unamestr" == 'Darwin' ]; then
	SUBLIME_SHARED_FOLDER="~/Library/Application Support/Sublime Text 2"
else
	echo 'Unsupported platform!'
	echo 'Please inspect the install.sh script and manually set the SUBLIME_SHARED_FOLDER variable.'
	exit 1
fi

echo "Installing to: ${SUBLIME_SHARED_FOLDER}"

INSTALL_SOURCE=`dirname "$0"`
INSTALL_SOURCE="${INSTALL_SOURCE}/install/Packages"

ls $INSTALL_SOURCE | while read package
do
	echo "  ${package}"
	cp -rf "${INSTALL_SOURCE}/${package}" "${SUBLIME_SHARED_FOLDER}"
done

echo "Done."
