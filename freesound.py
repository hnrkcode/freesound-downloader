#!/usr/bin/env python3.6

import re
import sys
import argparse
import urllib
import os.path
from urllib import request
from bs4 import BeautifulSoup


class FreesoundDownloader:

    def __init__(self):
        self.output_path = os.path.join(os.path.dirname(__file__), "downloads")

    def _valid_url(self, url):
        pattern = "https://freesound.org/people/[a-zA-Z0-9\W]+/sounds/[0-9]+[\W]{0,2}"
        match = re.match(pattern, url)
        if not match:
            print("Not a valid url.")
        return match

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
        parser = argparse.ArgumentParser()
        parser.add_argument("url", help="url to the sound file's page.")
        args = parser.parse_args()

        if self._valid_url(args.url):
            self._download(args.url)

if __name__ == "__main__":

    freesound = FreesoundDownloader()
    freesound.main()
