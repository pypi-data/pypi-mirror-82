# Copyright 2019 Splunk Inc. All rights reserved.

"""
### Documentation standards
"""

# Python Standard Libraries
import codecs
import os

# Third-Party Libraries
import langdetect
from langdetect import DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Custom Libraries
import splunk_appinspect
from splunk_appinspect.splunk import normalizeBoolean
from splunk_appinspect.app_util import find_readmes

DetectorFactory.seed = 0
report_display_order = 50


@splunk_appinspect.tags("splunk_appinspect", "appapproval")
@splunk_appinspect.cert_version(min="1.0.0")
@splunk_appinspect.display(report_display_order=1)
def check_basic_readme(app, reporter):
    """Check that the app has a `<APP_DIR>/README` file that includes
    version support, system requirements, installation, configuration,
    troubleshooting and running of the app, or a link to online documentation.
    """
    readmes = find_readmes(app)
    if not readmes:
        reporter_output = "No README was found."
        reporter.fail(reporter_output)
    else:
        for readme in readmes:
            full_file_path = os.path.join(app.app_dir, readme)
            try:
                with codecs.open(full_file_path, encoding="utf-8") as file:
                    contents = file.read()
                    if contents.strip():
                        break
            except UnicodeDecodeError:
                # when file encoding is not utf-8, use filesize to determine if a file is empty
                # could not skip space characters in this check
                if os.stat(full_file_path).st_size > 0:
                    break
        else:
            reporter_output = "README file(s) found but appear to be empty. File: {}".format(
                readme
            )
            reporter.fail(reporter_output, readme)


@splunk_appinspect.tags("splunk_appinspect", "appapproval", "manual")
@splunk_appinspect.cert_version(min="1.0.0")
@splunk_appinspect.display(report_display_order=8)
def check_documentation_language(app, reporter):
    """Check that documentation is in English."""
    readmes = find_readmes(app)
    if not readmes:
        reporter.not_applicable("README not found.")
        return

    for readme in readmes:
        try:
            full_file_path = os.path.join(app.app_dir, readme)
            with codecs.open(full_file_path, encoding="utf-8") as file:
                contents = file.read()
                if not contents.strip():
                    reporter.not_applicable("README file is empty.")
                    continue
                lang = langdetect.detect(contents)
                if lang != "en":
                    reporter_output = (
                        'Language for README appears to be in "{}",'
                        ' not "en". Please verify this manually.'
                        " File: {}"
                    ).format(lang, readme)
                    reporter.manual_check(reporter_output, readme)
        except (UnicodeDecodeError, LangDetectException):
            reporter_output = (
                "Could not detect language of README file." " File: {}".format(readme)
            )
            reporter.manual_check(reporter_output, readme)


@splunk_appinspect.tags("splunk_appinspect", "appapproval", "manual")
@splunk_appinspect.cert_version(min="1.0.0")
@splunk_appinspect.display(report_display_order=9)
def check_editing_and_proofreading(reporter):
    """Check that documentation is free of major editing and
    proofreading (spelling, grammar, punctuation) issues.
    """
    # FIXME: Might be able to use a grammar checker (like http://pypi.python.org/pypi/language-check) to give advice
    reporter.manual_check("Documentation will be read during code review.")


@splunk_appinspect.tags("splunk_appinspect", "manual")
@splunk_appinspect.cert_version(min="1.0.0")
@splunk_appinspect.display(report_display_order=7)
def check_documented_included_open_source(reporter):
    """Check that all open source components used in developing the app are
    listed in the app's README files with the version number and a link to the
    project's website.
    """
    reporter.manual_check("Documentation will be read during code review.")


@splunk_appinspect.tags("splunk_appinspect", "manual")
@splunk_appinspect.cert_version(min="1.0.0")
@splunk_appinspect.display(report_display_order=3)
def check_search_acceleration(app, reporter):
    """Check that use of
    [report acceleration](https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Aboutsummaryindexing),
    search acceleration, or summary indexing is explained in the app's
    documentation.
    """
    # FIXME: Only warn if searches are accelerated or summary indexes are built.
    if app.file_exists("default", "savedsearches.conf"):
        reporter.manual_check(
            "App has a savedsearches.conf. Please verify that this file is documented."
        )
    else:
        reporter.not_applicable("No savedsearches.conf file exists.")


@splunk_appinspect.tags("splunk_appinspect", "manual")
@splunk_appinspect.cert_version(min="1.0.0")
@splunk_appinspect.display(report_display_order=2)
def check_custom_commands(app, reporter):
    """Check that use of [custom commands](https://dev.splunk.com/view/python-sdk/SP-CAAAEU2)
    is explained in the app's documentation.
    """
    if app.file_exists("default", "commands.conf"):
        reporter.manual_check("Documentation will be read during code review.")
    else:
        reporter.not_applicable("No commands.conf file exists.")


@splunk_appinspect.tags("splunk_appinspect", "manual")
@splunk_appinspect.cert_version(min="1.0.0")
@splunk_appinspect.display(report_display_order=5)
def check_dependencies(reporter):
    """Check that prerequisites of the app are explained in the app's
    documentation. All prerequisites must be either
    packaged with your app, or be available on Splunkbase.
    """
    reporter.manual_check("Documentation will be read during code review.")


@splunk_appinspect.tags("splunk_appinspect", "manual")
@splunk_appinspect.cert_version(min="1.5.0")
def check_archived_files(app, reporter):
    """Check that any compressed archives within the main release that
    need extracting are explained in the app's documentation.
    """
    archived_files = list(
        app.iterate_files(types=[".gz", ".tgz", ".spl", ".zip", ".tar"])
    )
    if archived_files:
        for _, file, _ in archived_files:
            reporter_output = (
                "Found archived {}. Please make sure any archived files in the app are documented."
            ).format(file)
            reporter.manual_check(reporter_output)
    else:
        reporter_output = "No archived files found in app."
        reporter.not_applicable(reporter_output)


@splunk_appinspect.tags("splunk_appinspect", "appapproval", "manual")
@splunk_appinspect.cert_version(min="1.6.0")
def check_outputs_documented(app, reporter):
    """Check that forwarding enabled in 'outputs.conf' is explained in the
    app's documentation.
    """
    if app.file_exists("default", "outputs.conf"):
        outputs_conf = app.outputs_conf()
        is_enabled_or_empty = True
        for section in outputs_conf.section_names():
            if outputs_conf.has_option(section, "disabled"):
                is_disabled = normalizeBoolean(outputs_conf.get(section, "disabled"))
                if is_disabled:
                    is_enabled_or_empty = False
                else:
                    is_enabled_or_empty = True
        if is_enabled_or_empty:
            reporter.manual_check("Documentation will be read during code review.")
    else:
        reporter.not_applicable("No outputs.conf file exists.")
