from __future__ import annotations

import shutil
from pathlib import Path

from pydoc_markdown import PydocMarkdown
from pydoc_markdown.contrib.loaders.python import PythonLoader
from pydoc_markdown.contrib.processors.crossref import CrossrefProcessor
from pydoc_markdown.contrib.processors.filter import FilterProcessor
from pydoc_markdown.contrib.processors.google import GoogleProcessor
from pydoc_markdown.contrib.renderers.docusaurus import (
    CustomizedMarkdownRenderer,
    DocusaurusRenderer,
)

DOCS_PREFIX = "docs"
BASE_FILE = "index.md"


def render_doc(path: Path, output_dir: Path):
    config = PydocMarkdown(
        loaders=[PythonLoader(search_path=[str(path)])],
        processors=[
            FilterProcessor(skip_empty_modules=True),
            CrossrefProcessor(),
            GoogleProcessor(),
        ],
        renderer=DocusaurusRenderer(
            docs_base_path=str(output_dir),
            relative_output_path=str(output_dir),
            relative_sidebar_path=str(output_dir / "sidebar.json"),
            sidebar_top_level_module_label=DOCS_PREFIX,
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
    modules = config.load_modules()
    config.process(modules)
    config.render(modules)


def format_files(docs_path: Path):
    for path in docs_path.rglob("*"):
        if path.is_dir() and path.name == "__init__":
            init_file = path / "__init__.md"
            if init_file.exists():
                init_file.rename(path.parent / BASE_FILE)
                path.rmdir()
        elif path.is_file() and path.name == "__init__.md":
            path.rename(path.parent / BASE_FILE)


def format_md_contents(docs_path: Path):
    for path in docs_path.rglob("*.md"):
        content = path.read_text()
        content = content.replace("#### \\_\\_init\\_\\_", "#### constructor")
        content = content.replace("# \\_\\_init\\_\\_", "")
        path.write_text(content)


def group_files(docs_path: Path, file_order: list[str] | None = None):
    """Append contents of files to BASE_FILE in specified order."""
    index_path = docs_path / BASE_FILE

    # Get all markdown files
    md_files = list(docs_path.rglob("*.md"))

    # Filter out BASE_FILE in root docs path only
    md_files = [f for f in md_files if not (f.parent == docs_path and f.name == BASE_FILE)]

    if file_order:
        # Sort files according to specified order
        ordered_files = []
        remaining_files = md_files.copy()

        for ordered_path in file_order:
            for file in md_files:
                if str(file.relative_to(docs_path)) == ordered_path:
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


def delete_extra_files(docs_path: Path):
    for path in docs_path.rglob("*"):
        if path.is_file() and path.name != BASE_FILE:
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)


def main():
    base_path = Path(__file__).parent
    repo_root = base_path / "nortech"
    docs_path = base_path / DOCS_PREFIX
    docs_path.mkdir(exist_ok=True, parents=True)
    render_doc(repo_root, docs_path)
    format_files(docs_path)
    format_md_contents(docs_path)
    group_files(
        docs_path,
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
            "metadata/values/device.md",
            "metadata/values/signal.md",
            "derivers/values/schema.md",
            "derivers/values/instance.md",
            "derivers/values/physical_units_schema.md",
        ],
    )
    delete_extra_files(docs_path)


if __name__ == "__main__":
    main()
