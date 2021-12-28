import click

from pyproject import scripts
from pyproject.helpers import PyProject


@click.group()
def pyproject():
    """pyproject CLI"""


@pyproject.command()
@click.argument("project_name")
def start(project_name: str):
    package_name = scripts.poetry_new(project_name)
    project = PyProject(project_name, package_name)

    scripts.remove_tests(project)
    scripts.add_dev_dependencies(project)
    scripts.set_dev_configuration(project)
    scripts.add_gitignore(project)
