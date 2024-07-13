import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator, Literal

from playwright.async_api import (
    BrowserContext,
    Page,
)
from playwright_stealth import stealth_async  # type:ignore


@asynccontextmanager
async def get_page(browser_context: BrowserContext) -> AsyncIterator[Page]:
    page = await browser_context.new_page()
    await stealth_async(page)

    try:
        yield page
    finally:
        await page.close()


async def page_goto(
    page: Page,
    url: str,
    wait_until: Literal["load", "domcontentloaded"] = "load",
    timeout_sec: int = 30,
    num_scrolls: int = 10,
):
    await page.goto(
        url=url,
        timeout=timeout_sec * 1000,
        wait_until=wait_until,
    )

    # (ref.) [Playwright auto-scroll to bottom of infinite-scroll page](https://stackoverflow.com/questions/69183922/playwright-auto-scroll-to-bottom-of-infinite-scroll-page)
    for _ in range(num_scrolls):
        await page.mouse.wheel(0, 1_000)
        await asyncio.sleep(0.1)
