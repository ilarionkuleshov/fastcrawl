import asyncio

from pydantic import BaseModel
from fastcrawl import FastCrawl, Request, Response, AppSettings, LogSettings


class TitleItem(BaseModel):
    title: str


app = FastCrawl(
    settings=AppSettings(
        log=LogSettings(
            level="DEBUG",
        )
    )
)

@app.handler("http://example.com")
def parse_example(response: Response) -> TitleItem | None:
    title = response.selector.xpath(".//h1/text()").get()
    if title:
        return TitleItem(title=title)
    return None


@app.pipeline()
def process_title(item: TitleItem) -> None:
    print(f"Title found: {item.title}")


# asyncio.run(app.run())
