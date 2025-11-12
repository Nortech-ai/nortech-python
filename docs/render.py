from __future__ import annotations

import shutil
from pathlib import Path

from docspec import ApiObject, Docstring, HasMembers, Module
from pydoc_markdown import PydocMarkdown
from pydoc_markdown.contrib.loaders.python import PythonLoader
from pydoc_markdown.contrib.processors.crossref import CrossrefProcessor
from pydoc_markdown.contrib.processors.filter import FilterProcessor
from pydoc_markdown.contrib.processors.google import GoogleProcessor
from pydoc_markdown.contrib.renderers.docusaurus import (
    CustomizedMarkdownRenderer,
    DocusaurusRenderer,
)
from pydoc_markdown.interfaces import Processor, Resolver

DOCS_PATH = Path(__file__).parent
REPO_ROOT = DOCS_PATH.parent / "nortech"
EXAMPLES_PATH = DOCS_PATH / "examples"
BASE_FILE = "index.md"


def add_examples_to_modules(modules: list[ApiObject], examples_path: Path = EXAMPLES_PATH):
    for path in examples_path.iterdir():
        if path.is_file() and path.name == "__init__.py":
            module = modules[0].parent
            if module and module.name == path.parent.name and module.docstring:
                module.docstring = Docstring(
                    location=module.docstring.location,
                    content=module.docstring.content.rstrip()
                    + "\n\n**Example**:\n\n```python\n"
                    + path.read_text()
                    + "\n```",
                )

        else:
            module = next((m for m in modules if m.name == path.stem), None)
            if not module:
                continue

            if path.is_file():
                if module and module.docstring:
                    module.docstring = Docstring(
                        location=module.docstring.location,
                        content=module.docstring.content.rstrip()
                        + "\n\n**Example**:\n\n```python\n"
                        + path.read_text()
                        + "\n```",
                    )
            else:
                if isinstance(module, HasMembers):
                    add_examples_to_modules(list(module.members), path)


class ExampleProcessor(Processor):
    def process(self, modules: list[Module], resolver: Resolver | None = None) -> None:
        add_examples_to_modules(list(modules))


def render_doc():
    config = PydocMarkdown(
        loaders=[PythonLoader(search_path=[str(REPO_ROOT)])],
        processors=[
            FilterProcessor(skip_empty_modules=True),
            CrossrefProcessor(),
            GoogleProcessor(),
            ExampleProcessor(),
        ],
        renderer=DocusaurusRenderer(
            docs_base_path=str(DOCS_PATH),
            relative_output_path=str(DOCS_PATH),
            relative_sidebar_path=str(DOCS_PATH / "sidebar.json"),
            sidebar_top_level_module_label="Docs",
            sidebar_top_level_label="Reference",
            markdown=CustomizedMarkdownRenderer(
                classdef_code_block=False,
                escape_html_in_docstring=False,
                add_module_prefix=True,
                render_module_header_template="",
                descriptive_class_title=False,
                data_code_block=True,
                header_level_by_type={
                    "Module": 2,
                    "Class": 3,
                    "Method": 4,
                    "Function": 4,
                    "Variable": 4,
                },
            ),
        ),
    )

    modules: list[Module] = config.load_modules()
    config.process(modules)
    config.render(modules)


def format_files():
    for path in DOCS_PATH.rglob("*"):
        if path.is_dir() and path.name == "__init__":
            init_file = path / "__init__.md"
            if init_file.exists():
                init_file.rename(path.parent / BASE_FILE)
                path.rmdir()
        elif path.is_file() and path.name == "__init__.md":
            path.rename(path.parent / BASE_FILE)


def format_md_contents():
    for path in DOCS_PATH.rglob("*.md"):
        content = path.read_text()
        content = content.replace("#### \\_\\_init\\_\\_", "#### constructor")
        content = content.replace("# \\_\\_init\\_\\_", "")
        path.write_text(content)


def group_files(file_order: list[str] | None = None):
    """Append contents of files to BASE_FILE in specified order."""
    index_path = DOCS_PATH / BASE_FILE

    # Get all markdown files
    md_files = list(DOCS_PATH.rglob("*.md"))

    # Filter out BASE_FILE in root docs path only
    md_files = [f for f in md_files if not (f.parent == DOCS_PATH and f.name == BASE_FILE)]

    if file_order:
        # Sort files according to specified order
        ordered_files: list[Path] = []
        remaining_files = md_files.copy()

        for ordered_path in file_order:
            for file in md_files:
                if str(file.relative_to(DOCS_PATH)) == ordered_path:
                    ordered_files.append(file)
                    remaining_files.remove(file)
                    break

        # Add any remaining files not in the order list
        md_files = ordered_files + remaining_files

    # Append each file's contents
    for file in md_files:
        content = file.read_text()
        with open(index_path, "a") as index:
            index.write("\n\n" + content)


def delete_extra_files():
    for item in DOCS_PATH.iterdir():
        if item in [EXAMPLES_PATH, DOCS_PATH / BASE_FILE, Path(__file__)]:
            continue
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)


def main():
    DOCS_PATH.mkdir(exist_ok=True, parents=True)
    render_doc()
    format_files()
    format_md_contents()
    group_files(
        [
            "metadata/index.md",
            "datatools/index.md",
            "derivers/index.md",
            "metadata/values/time_window.md",
            "metadata/values/pagination.md",
            "metadata/values/workspace.md",
            "metadata/values/asset.md",
            "metadata/values/division.md",
            "metadata/values/unit.md",
            "metadata/values/signal.md",
            "derivers/values/schema.md",
            "derivers/values/instance.md",
            "derivers/values/physical_units_schema.md",
        ],
    )
    delete_extra_files()


if __name__ == "__main__":
    main()
