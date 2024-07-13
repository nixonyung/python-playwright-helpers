from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from playwright.async_api import (
    BrowserContext,
    ViewportSize,
    async_playwright,
)


@asynccontextmanager
async def get_browser_context(
    traces_output_path: Path | None = None,
) -> AsyncIterator[BrowserContext]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-gpu", "--single-process"],
        )
        browser_context = await browser.new_context(
            screen=ViewportSize(width=1920, height=1080),
        )

        if traces_output_path is not None:
            await browser_context.tracing.start(snapshots=True, screenshots=True, sources=True)

        try:
            yield browser_context
        finally:
            if traces_output_path is not None:
                await browser_context.tracing.stop(path=traces_output_path)
            await browser_context.close()
