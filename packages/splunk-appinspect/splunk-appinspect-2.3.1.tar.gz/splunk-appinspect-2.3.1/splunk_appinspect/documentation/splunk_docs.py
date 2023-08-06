# Copyright 2019 Splunk Inc. All rights reserved.

"""
Helper module for documentation links generation
"""

# Python Standard Libraries
# Third-Party Libraries
# N/A
# Custom Libraries

from splunk_appinspect.splunk_defined_conf_file_list import LATEST_CONFS


class DocumentationLinks(object):
    """Represents links to Splunk Docs sites"""

    @staticmethod
    def get_splunk_docs_link(conf_file):
        """Returns the Splunk Doc link for a conf file."""
        if conf_file in LATEST_CONFS:
            uri_path = conf_file.replace(".", "")
            return "https://docs.splunk.com/Documentation/Splunk/latest/Admin/{}".format(
                uri_path
            )

        return "Unable to find doc link for {}".format(conf_file)
