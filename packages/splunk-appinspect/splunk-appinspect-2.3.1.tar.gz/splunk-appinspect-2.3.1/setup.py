# Copyright 2016 Splunk Inc. All rights reserved.

"""A setup tools configuration to be used for building and distribution."""

import setuptools
import os

# Information Configuration Goes Here
author = "Splunk"
author_email = "appinspect@splunk.com"
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "License :: Other/Proprietary License",
    "Natural Language :: English",
    "Operating System :: MacOS",
    "Operating System :: Microsoft",
    "Operating System :: Unix",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Software Development :: Testing",
    "Topic :: Utilities",
]
description = "Automatic validation checks for Splunk Apps"
download_url = "http://dev.splunk.com/goto/appinspectdownload"
home_page_url = "https://splunk.com"
# Specifies installation library dependencies
install_requires = [
    "beautifulsoup4==4.8.1",
    "chardet==3.0.4",
    "click==7.0",
    "pillow==7.1.2",
    "six==1.12.0",
    "future==0.17.1",
    "futures-then==0.1.1",
    "jinja2==2.11.1",
    "langdetect==1.0.7",
    "lxml==4.5.1",
    "Markdown==3.1.1",
    "painter==0.3.1",
    "regex==2019.6.8",  # Python re module does not support PCRE, so use another one
    "ipaddress==1.0.22",
    "enum34==1.1.6; python_version < '3.4'",
    "jsoncomment==0.3.3",
    "mako==1.0.12",
    "PyYAML==5.3",
]

platform_specific_install_requirements = []

if os.name == "nt":
    platform_specific_install_requirements = [
        "pywin32==224",
    ]
else:
    platform_specific_install_requirements = [
        "python-magic==0.4.18",
    ]


install_requires += platform_specific_install_requirements
keywords = ["AppInspect", "Certification", "Splunk", "Splunk AppInspect", "Testing"]
license = "Other/Proprietary License"
long_description = (
    "AppInspect is a tool for assessing a Splunk App's"
    " compliance with Splunk recommended development practices,"
    " by using static analysis. AppInspect is open for"
    " extension, allowing other teams to compose checks that"
    " meet their domain specific needs for semi- or"
    " fully-automated analysis and validation of Splunk Apps."
)
name = "splunk-appinspect"
package_data = {
    "splunk_appinspect": [
        "*.txt",  # Includes the banned_wordslist.txt
        "version/VERSION.txt",  # Includes the VERSION file
        "checks/**",  # Includes the checks directory
        "templates/*.html",  # Includes the templates for documentation generation
        "python_analyzer/trustedlibs/lib_files/*.csv",
        "splunk/telemetry/list.csv",
    ]
}
platforms = ["MacOS", "Microsoft", "Unix"]
scripts = ["scripts/splunk-appinspect"]

# execfile("splunk_appinspect/version/version.py")
exec(open("./splunk_appinspect/version/version.py").read())
__version__ = get_version(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "splunk_appinspect", "version"
    )
)

# now we have an `__version__` variable

# Setup tools configuration goes here
setuptools.setup(
    author=author,
    author_email=author_email,
    classifiers=classifiers,
    description=description,
    download_url=download_url,
    install_requires=install_requires,
    keywords=keywords,
    license=license,
    long_description=long_description,
    name=name,
    packages=setuptools.find_packages(),
    package_data=package_data,
    platforms=platforms,
    url=home_page_url,
    entry_points={
        "console_scripts": ["splunk-appinspect=splunk_appinspect:main.execute",],
    },
    version=__version__,
)
