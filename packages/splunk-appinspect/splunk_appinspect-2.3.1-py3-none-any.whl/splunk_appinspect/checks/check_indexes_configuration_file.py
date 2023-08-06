# Copyright 2019 Splunk Inc. All rights reserved.

"""
### Indexes.conf file standards

Ensure that the index configuration file located in the **/default** folder is well formed and valid. For more, see [indexes.conf](http://docs.splunk.com/Documentation/Splunk/latest/Admin/Indexesconf).
"""

# Python Standard Library
import logging
import os

# Third Party library
import six

# Custom Libraries
import splunk_appinspect

report_display_order = 2
logger = logging.getLogger(__name__)


@splunk_appinspect.cert_version(min="1.1.23")
@splunk_appinspect.tags("splunk_appinspect")
def check_indexes_conf_does_not_exist(app, reporter):
    """Check that the app does not create indexes."""
    if app.file_exists("default", "indexes.conf"):
        file_path = os.path.join("default", "indexes.conf")
        reporter_output = (
            "Apps and add-ons should not create indexes. Indexes"
            " should only be defined by Splunk System"
            " Administrators to meet the data storage and"
            " retention needs of the installation. Consider"
            " using Tags or Source Types to identify data"
            " instead index location. File: {}"
        ).format(file_path)
        reporter.fail(reporter_output, file_path)


@splunk_appinspect.cert_version(min="1.1.7")
@splunk_appinspect.tags("splunk_appinspect", "cloud", "private_app")
def check_validate_default_indexes_not_modified(app, reporter):
    """Check that no default Splunk indexes are modified by the app."""
    default_indexes = [
        "_audit",
        "_internal",
        "_introspection",
        "_thefishbucket",
        "history",
        "main",
        "provider-family:hadoop",
        "splunklogger",
        "summary",
        "volume:_splunk_summaries",
    ]
    if app.file_exists("default", "indexes.conf"):
        file_path = os.path.join("default", "indexes.conf")
        indexes_config = app.get_config("indexes.conf")
        for section in indexes_config.sections():
            if section.name in default_indexes:
                reporter_output = (
                    "The default Splunk index [{}] was modified which is not "
                    "allowed in the Splunk Cloud. Please remove this stanza. "
                    "File: {}, Line: {}."
                ).format(section.name, file_path, section.lineno)
                reporter.fail(reporter_output, file_path, section.lineno)
    else:
        reporter_output = "No `default/indexes.conf`file exists."
        reporter.not_applicable(reporter_output)


@splunk_appinspect.cert_version(min="1.5.0")
@splunk_appinspect.tags("splunk_appinspect")
def check_index_definition_has_required_options(app, reporter):
    """Check that all index definitions exist all required options including:
    homePath, coldPath, and thawedPath.
    """
    required_options = ["homePath", "coldPath", "thawedPath"]
    filter_section_prefix = ("provider-family:", "provider:", "volume:")
    virtual_index_required_option = "vix.provider"

    if app.file_exists("default", "indexes.conf"):
        file_path = os.path.join("default", "indexes.conf")
        indexes_config = app.get_config("indexes.conf")
        for section in indexes_config.sections():
            # not check default stanza
            if section.name == "default":
                continue
            # not check provider-family, provider and volume
            if section.name.startswith(filter_section_prefix):
                continue
            # not check virtual index
            if section.has_option(virtual_index_required_option):
                continue
            for required_option in required_options:
                if not section.has_option(required_option):
                    lineno = section.lineno
                    reporter_output = (
                        "The {} index definition does not have the required option: {}. "
                        "File: {}, Line: {}."
                    ).format(section.name, required_option, file_path, lineno)
                    reporter.fail(reporter_output, file_path, lineno)
    else:
        reporter_output = "No `default/indexes.conf` file exists."
        reporter.not_applicable(reporter_output)


@splunk_appinspect.cert_version(min="1.5.3")
@splunk_appinspect.tags("cloud", "private_app")
def check_indexes_conf_properties(app, reporter):
    """Check that indexes.conf only contains the required 'homePath' , 'coldPath', and 'thawedPath' properties
    or the optional 'frozenTimePeriodInSecs', 'disabled', 'datatype' and 'repFactor' properties.
    All other properties are prohibited.
    This check is cloud only because indexes are not allowed via check_indexes_conf_does_not_exist.
    """

    # Check rules are defined in https://jira.splunk.com/browse/ACD-2053, ACD-2448 and ACD-3020

    property_white_list = ["homePath", "coldPath", "thawedPath"]
    property_optional_white_list = [
        "frozenTimePeriodInSecs",
        "disabled",
        "datatype",
        "repFactor",
    ]
    if app.file_exists("default", "indexes.conf"):
        file_path = os.path.join("default", "indexes.conf")
        conf_file = app.get_config("indexes.conf")
        # check for all sections in this .conf file
        for section in conf_file.sections():
            # check for all properties
            for option_name, option_value, option_lineno in section.items():
                # in white list
                if option_name in property_white_list:
                    legal_path = _get_legal_path(section.name, option_name)
                    actual_path = option_value
                    if legal_path != actual_path:
                        reporter_output = (
                            "In stanza {}, property {} should be {}, but is {} here. "
                            "File: {}, Line: {}."
                        ).format(
                            section.name,
                            option_name,
                            legal_path,
                            actual_path,
                            file_path,
                            option_lineno,
                        )
                        reporter.fail(reporter_output, file_path, option_lineno)
                # not in option_white_list
                elif option_name not in property_optional_white_list:
                    reporter_output = (
                        "Illegal property {} found in stanza {}. Only properties [{}]"
                        " are allowed in default/indexes.conf. File: {}, Line: {}."
                    ).format(
                        option_name,
                        section.name,
                        ", ".join(property_white_list + property_optional_white_list),
                        file_path,
                        option_lineno,
                    )
                    reporter.fail(reporter_output, file_path, option_lineno)


def _get_legal_path(index_name, property_name):
    """
        [<index_name>]
        homePath   = $SPLUNK_DB/<index_name>/db
        coldPath   = $SPLUNK_DB/<index_name>/colddb
        thawedPath = $SPLUNK_DB/<index_name>/thaweddb
    """
    pattern = "$SPLUNK_DB/{}/{}"
    pattern_dict = {"homePath": "db", "coldPath": "colddb", "thawedPath": "thaweddb"}
    return pattern.format(index_name, pattern_dict[property_name])


@splunk_appinspect.tags("cloud", "python3_version", "private_app")
@splunk_appinspect.cert_version(min="2.1.0")
def check_coldToFrozenScript_has_valid_python_version_property(
    app, reporter, target_splunk_version
):
    """Check that all the coldToFrozenScript in `indexes.conf` are explicitly
    set the python.version to python3.
    """
    if target_splunk_version < "splunk_8_0":
        return

    if app.file_exists("default", "indexes.conf"):
        file_path = os.path.join("default", "indexes.conf")
        indexes_config = app.get_config("indexes.conf")
        for section in indexes_config.sections():
            if section.has_option("coldToFrozenScript"):
                if (
                    not section.has_option("python.version")
                    or section.get_option("python.version").value != "python3"
                ):
                    reporter_output = "The python.version of coldToFrozenScript should be explicitly set to python3."
                    reporter.fail(reporter_output, file_path, section.lineno)
                elif six.PY3:
                    target_script = os.path.basename(
                        section.get_option("coldToFrozenScript")
                        .value.strip()
                        .split()[-1]
                        .strip('"')
                    )
                    for directory, filename, _ in app.iterate_files(types=[".py"]):
                        if filename == target_script:
                            full_file_path = app.get_filename(
                                os.path.join(directory, filename)
                            )
                            import ast

                            try:
                                with open(full_file_path, "rb") as f:
                                    ast.parse(f.read())
                            except:
                                reporter.fail(
                                    "coldToFrozenScript option {} specifies a script that is not Python 3 compatible, "
                                    "Please upgrade your Python script to be Python 3 "
                                    "compatible.".format(
                                        section.get_option("coldToFrozenScript").value
                                    ),
                                    file_path,
                                    section.lineno,
                                )
                            break

    else:
        reporter_output = "indexes.conf does not exist."
        reporter.not_applicable(reporter_output)
