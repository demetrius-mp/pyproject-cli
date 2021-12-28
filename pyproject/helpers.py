from pathlib import Path

from tomlkit import dumps, parse
from tomlkit.toml_document import TOMLDocument


class PyProject:
    def __init__(self, project_name: str, package_name: str) -> None:
        self.project_name = project_name
        self.package_name = package_name
        self.path = Path.cwd() / self.package_name
        self.toml_path = self.path / "pyproject.toml"

    @property
    def toml_doc(self):
        with open(self.toml_path, "r") as f:
            content = f.read()
            doc = parse(content)

        return doc

    def save_toml_doc(self, doc: TOMLDocument):
        dumped_doc = dumps(doc)
        with open(self.toml_path, "w") as f:
            f.write(dumped_doc)
