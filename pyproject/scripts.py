import os
import shutil
import subprocess
from pathlib import Path

from tomlkit import nl, table

from pyproject.helpers import PyProject


def __remove_unwanted_newline(file: Path):
    with open(file, "r+") as f:
        new_f = f.readlines()
        f.seek(0)
        for i, line in enumerate(new_f):
            # remove line 14
            if i != 14:
                f.write(line)
        f.truncate()


def poetry_new(project_name: str) -> str:
    cmd = ["poetry", "new", project_name]
    output = subprocess.run(cmd, capture_output=True)
    shell_output = output.stdout.decode()

    # propagating poetry output
    print(shell_output)

    package_name = shell_output.split(" ")[2]

    return package_name


def remove_tests(pyproject: PyProject):
    print("Removing pytest from development dependencies...")

    # removes the tests/ directory
    tests_path = pyproject.path / "tests"
    shutil.rmtree(tests_path)

    # removes pytest from development dependencies
    doc = pyproject.toml_doc
    doc["tool"]["poetry"]["dev-dependencies"].remove("pytest")

    pyproject.save_toml_doc(doc)


def add_dev_dependencies(pyproject: PyProject):
    os.chdir(pyproject.path)
    cmd = ["poetry", "add", "--dev", "black", "flake8", "isort"]
    subprocess.run(cmd)

    os.chdir(pyproject.path.parent)


def set_isort_profile(pyproject: PyProject):
    doc = pyproject.toml_doc

    isort = table()
    isort["profile"] = "black"

    doc["tool"]["isort"] = isort
    doc["tool"]["isort"].add(nl())

    pyproject.save_toml_doc(doc)

    __remove_unwanted_newline(pyproject.toml_path)


def set_flake8_config(pyproject: PyProject):
    flake8_template = Path(__file__).parent / "templates" / ".flake8.template"
    flake8_file = pyproject.path / ".flake8"

    shutil.copyfile(flake8_template, flake8_file)


def set_dev_configuration(pyproject: PyProject):
    print("Setting development configurations for isort and flake8...")

    set_isort_profile(pyproject)
    set_flake8_config(pyproject)


def add_gitignore(pyproject: PyProject):
    print("Adding gitignore...")

    gitignore_template = Path(__file__).parent / "templates" / ".gitignore.template"
    gitignore_file = pyproject.path / ".gitignore"

    shutil.copyfile(gitignore_template, gitignore_file)
