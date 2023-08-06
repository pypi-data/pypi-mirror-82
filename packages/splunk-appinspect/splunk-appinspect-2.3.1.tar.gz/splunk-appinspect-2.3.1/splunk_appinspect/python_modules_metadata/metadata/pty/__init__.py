"""
interfaces that are unique to the Unix operating system, or in some cases to some or many variants of it.
"""

from splunk_appinspect.python_modules_metadata.metadata_common.metadata_consts import TagConsts
from splunk_appinspect.python_modules_metadata.metadata_common.metadata_decorator import tags


@tags(TagConsts.UNIX_SPECIFIX_SERVICES)
def fork():
    """
    Connect the child's controlling terminal to a pseudo-terminal
    """
    pass

@tags(TagConsts.UNIX_SPECIFIX_SERVICES)
def openpty():
    """
    Open a new pseudo-terminal pair
    """
    pass

@tags(TagConsts.UNIX_SPECIFIX_SERVICES)
def spawn():
    """
    Spawn a process
    """
    pass