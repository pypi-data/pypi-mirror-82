#  This file is managed by 'repo_helper'. Don't edit it directly.
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This file is distributed under the same license terms as the program it came with.
#  There will probably be a file called LICEN[S/C]E in the same directory as this file.
#
#  In any case, this program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# This script based on https://github.com/rocky/python-uncompyle6/blob/master/__pkginfo__.py
#

# stdlib
import pathlib

__all__ = [
		"__copyright__",
		"__version__",
		"modname",
		"pypi_name",
		"__license__",
		"__author__",
		"short_desc",
		"author",
		"author_email",
		"github_username",
		"web",
		"github_url",
		"repo_root",
		"install_requires",
		"extras_require",
		"project_urls",

		"import_name",
		]

__copyright__ = """
2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
"""

__version__ = "0.0.6"
modname = "coverage_pyver_pragma"
pypi_name = "coverage_pyver_pragma"
import_name = "coverage_pyver_pragma"
__license__ = "GNU Lesser General Public License v3 or later (LGPLv3+)"
short_desc = 'Plugin for Coverage.py to selectively ignore branches depending on the Python version.'
__author__ = author = 'Dominic Davis-Foster'
author_email = 'dominic@davis-foster.co.uk'
github_username = "domdfcoding"
web = github_url = "https://github.com/domdfcoding/coverage_pyver_pragma"
repo_root = pathlib.Path(__file__).parent
install_requires = (repo_root / "requirements.txt").read_text(encoding="utf-8").split('\n')
extras_require = {'all': []}



conda_description = """Plugin for Coverage.py to selectively ignore branches depending on the Python version.


Before installing please ensure you have added the following channels: domdfcoding, conda-forge"""
__all__.append("conda_description")


project_urls = {
		"Documentation": "https://coverage_pyver_pragma.readthedocs.io",
		"Issue Tracker": f"{github_url}/issues",
		"Source Code": github_url,
		}
