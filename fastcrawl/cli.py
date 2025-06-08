import asyncio
import importlib.util
import pathlib
import sys

import rich
import typer

from fastcrawl.core import FastCrawl

app = typer.Typer(name="FastCrawl", help="FastCrawl CLI for running crawlers.", add_completion=False)


@app.command("run", help="Run the FastCrawl application.")
def run_crawler(
    path: pathlib.Path = typer.Argument(
        exists=True,
        dir_okay=False,
        resolve_path=True,
        help="Path to python file containing the FastCrawl application to run.",
    ),
) -> None:
    # insert_cwd_to_sys_path()

    if path.suffix != ".py":
        raise typer.BadParameter(
            f"File '{path}' is not a python file. Please provide a valid python file.",
            param_hint="path",
        )

    app = import_app_from_module(path)

    rich.print(f"[bold green]Running app {app.name}...[/bold green]")
    asyncio.run(app.run())


def import_app_from_module(path: pathlib.Path) -> FastCrawl:
    module_name = path.stem
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load '{path}'")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    if not hasattr(module, "app"):
        raise AttributeError(f"Module '{module_name}' does not have attribute 'app'")
    app = getattr(module, "app")
    if not isinstance(app, FastCrawl):
        raise TypeError(f"Attribute 'app' in module '{module_name}' is not an instance of FastCrawl")
    return app


def insert_cwd_to_sys_path() -> None:
    current_dir = str(pathlib.Path.cwd())
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)


if __name__ == "__main__":
    app()
