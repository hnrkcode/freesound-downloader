#!/usr/bin/env python3.6

import re
import sys
import getopt
import urllib
import os.path
from urllib import request
from bs4 import BeautifulSoup


class FreesoundDownloader:

    def __init__(self):
        self.output_path = "downloads"

    def _help(self):
        """How to use the program."""
        msg = "Usage: python3 freesound.py [option] [url]"
        print(msg)

    def _clean(self, string):
        """Replace undesired characters."""
        pattern = "[\W\s]"
        replace_with = "_"
        cleaned = re.sub(pattern, replace_with, string)
        return cleaned

    def _download(self, url):
        """Download sound file from freesound.org"""
        # Open the url and get the html.
        try:
            req = request.urlopen(url)
        except urllib.error.HTTPError as err:
            print(err)
            return False
        else:
            html = req.read()
            soup = BeautifulSoup(html, 'html.parser')
            # Find the url to the file.
            title = self._clean(soup.find(property='og:title').attrs['content'])
            file = soup.find(property='og:audio').attrs['content']
            file = request.urlopen(file).read()
            if not os.path.isdir(self.output_path):
                os.mkdir(self.output_path)
            # Download the file.
            path = os.path.join(self.output_path, f"{title}.mp3")
            with open(path, 'wb') as output:
                output.write(file)
            return True

    def main(self):
        """Handles the arguments from the user."""
        try:
            opts, args = getopt.getopt(
                sys.argv[1:],
                "hd:",
                ["help", "download="]
                )
        except getopt.GetoptError as err:
            self._help()
            sys.exit(2)

        for opt, arg in opts:
            if opt in ('-d', '--download'):
                self._download(arg)
            elif opt in ("-h", "--help"):
                self._help()
                sys.exit()
            else:
                assert False, "unhandled option"


if __name__ == "__main__":

    freesound = FreesoundDownloader()
    freesound.main()
