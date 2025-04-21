import asyncio
import importlib.util
import inspect
import pathlib
import sys
import uuid
from typing import Optional, Type

import rich
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from fastcrawl.base_crawler import BaseCrawler

app = typer.Typer(name="FastCrawl", help="FastCrawl CLI for running crawlers.", add_completion=False)


@app.command("list", help="List all available crawlers.")
def list_crawlers(
    path: pathlib.Path = typer.Argument(
        default_factory=pathlib.Path.cwd,
        exists=True,
        file_okay=False,
        resolve_path=True,
        help="Path to the directory containing crawlers. If not provided, defaults to the current working directory.",
    )
) -> None:
    """Shows all available crawlers in the specified directory.

    Args:
        path (pathlib.Path): Path to the directory containing crawlers.
            If not provided, current working directory is used.

    """
    crawlers = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Scanning files...", total=None)

        for file_path in path.rglob("*.py"):
            for crawler in get_crawlers_from_file(file_path):
                line_number = inspect.getsourcelines(crawler)[1]
                crawlers.append((crawler.__name__, file_path, line_number))

    if crawlers:
        crawlers_length = len(crawlers)
        rich.print(f"[bold green]Found {crawlers_length} crawler{'s' if crawlers_length > 1 else ''}[/bold green]\n")
        for name, file_path, line_number in crawlers:
            rich.print(f"[bold blue]{name}[/bold blue] -> {file_path}:{line_number}")
    else:
        rich.print("[bold red]No crawlers found[/bold red]")


@app.command("run", help="Run a specific crawler.")
def run_crawler(
    path: pathlib.Path = typer.Argument(
        exists=True,
        dir_okay=False,
        resolve_path=True,
        help="Path to python file containing the crawler to run.",
    ),
    crawler_name: Optional[str] = typer.Option(
        default=None,
        help=(
            "Name of the crawler class to run. Provide it if the file contains multiple crawlers. "
            "But if the file contains only one crawler, this argument is optional."
        ),
    ),
) -> None:
    """Runs a specific crawler from the provided python file.

    Args:
        path (pathlib.Path): Path to the python file containing the crawler.
        crawler_name (Optional[str]): Name of the crawler class to run. Default is None.

    """
    if path.suffix != ".py":
        raise typer.BadParameter(
            f"File '{path}' is not a python file. Please provide a valid python file.",
            param_hint="path",
        )

    crawlers = get_crawlers_from_file(path)

    if not crawlers:
        raise typer.BadParameter(
            f"File '{path}' does not contain any crawlers.",
            param_hint="path",
        )

    crawler_to_run = None
    if crawler_name:
        for crawler in crawlers:
            if crawler.__name__ == crawler_name:
                crawler_to_run = crawler
                break

        if not crawler_to_run:
            raise typer.BadParameter(
                f"Crawler '{crawler_name}' not found in file '{path}'.",
                param_hint="--crawler-name",
            )
    else:
        if len(crawlers) > 1:
            crawler_names = ", ".join([f"'{c.__name__}'" for c in crawlers])
            raise typer.BadParameter(
                (
                    f"You must specify a crawler name because '{path}' contains multiple crawlers. "
                    f"Crawlers found: {crawler_names}."
                ),
                param_hint="--crawler-name",
            )
        crawler_to_run = crawlers[0]

    rich.print(f"[bold green]Running {crawler_to_run.__name__}...[/bold green]")
    asyncio.run(crawler_to_run().run())


def get_crawlers_from_file(file_path: pathlib.Path) -> list[Type[BaseCrawler]]:
    """Returns a list of crawlers from the provided python file.

    Args:
        file_path (pathlib.Path): Path to the python file.

    """
    crawlers = []
    identifier = uuid.uuid4().hex

    spec = importlib.util.spec_from_file_location(identifier, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load file '{file_path}'")
    module = importlib.util.module_from_spec(spec)
    sys.modules[identifier] = module
    spec.loader.exec_module(module)

    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, type) and issubclass(attr, BaseCrawler) and not inspect.isabstract(attr):
            crawlers.append(attr)

    return crawlers


if __name__ == "__main__":
    app()
