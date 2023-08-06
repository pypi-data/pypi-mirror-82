# Copyright 2019 Splunk Inc. All rights reserved.
"""Splunk app file resource abstraction module. Parsers provided for xml, lxml-xml and lxml format."""

# Python Standard Libraries
import os
import logging

# Third-Party Libraries
import bs4


logger = logging.getLogger(__name__)


class FileResource(object):
    def __init__(self, file_path, ext="", app_file_path="", file_name=""):
        self.file_path = file_path
        self.app_file_path = app_file_path
        self.ext = ext
        self.file_name = file_name
        self.tags = []

    def exists(self):
        return os.path.isfile(self.file_path)

    def parse(self, fmt):
        try:
            if fmt in ["xml", "lxml-xml", "lxml"]:
                return bs4.BeautifulSoup(open(self.file_path), "lxml")
        except Exception as e:
            logging.error(str(e))
            raise
        else:
            logging.error("%s file is not supported!", fmt)
            raise Exception("{} file is not supported!".format(fmt))
