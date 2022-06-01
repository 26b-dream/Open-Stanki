from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal

# Standard Library
import time

# Third Party
# Imported just to export
from playwright.sync_api import sync_playwright  # type: ignore # noqa
from playwright.sync_api._generated import ElementHandle, Page


def click_if_exists(self: Page, selector: str) -> bool:
    if self.query_selector(selector):
        self.click(selector)
        return True
    else:
        return False


def click_while_exists(self: Page, selector: str, sleep_time: int = 5) -> None:
    while True:
        element = self.query_selector(selector)
        if element:
            self.click(selector)
            time.sleep(sleep_time)
        else:
            break


def strict_query_selector(self: Page, selector: str) -> ElementHandle:
    output = self.query_selector(selector)
    if output:
        return output
    else:
        raise ValueError(f"Could not find element with selector: {selector}")


# wait_for_url has a type problem so put a wrapper around it
def fixed_wait_for_url(
    self: Page, url: str, wait_until: Literal["commit", "domcontentloaded", "load", "networkidle"] = "networkidle"
) -> None:
    self.wait_for_url(url, wait_until=wait_until)  # type: ignore - wait_until has bad typing, this is just a wrapper around it


# Actually add functions to Tag
# Because the type hints say the return type is Tag the type hints need to be added to .venv\Lib\site-packages\playwright\sync_api\_generated.py
# ! For these to work properly type hints need to be added to element.pyi in
# Page ElementHandle:
#   def click_if_exists(self: Page, selector: str) -> bool: ...
#   def def click_while_exists(self: Page, selector: str, sleep_time: int = 5) -> None: ...
#   def strict_query_selector(self: Page, selector: str) -> ElementHandle: ...
#   def def fixed_wait_for_url(self: Page, url: str, wait_until: Literal["commit", "domcontentloaded", "load", "networkidle"] = "networkidle") -> None: ...
Page.click_if_exists = click_if_exists
Page.click_while_exists = click_while_exists
Page.strict_query_selector = strict_query_selector
Page.fixed_wait_for_url = fixed_wait_for_url


def strict_get_attribute(self: ElementHandle, name: str) -> str:
    output = self.get_attribute(name)
    if output:
        return output
    else:
        raise ValueError(f"Could not find attribute with name: {name}")


def strict_text_content(self: ElementHandle) -> str:
    output = self.text_content()
    if output:
        return output
    else:
        raise ValueError("Could not find text content")


# Actually add functions to Tag
# Because the type hints say the return type is Tag the type hints need to be added to .venv\Lib\site-packages\playwright\sync_api\_generated.py
# ! For these to work properly type hints need to be added to element.pyi in
# class ElementHandle:
#   def strict_get_attribute(self, name: str) -> str: ...
#   def def strict_text_content(self) -> str: ...
ElementHandle.strict_get_attribute = strict_get_attribute
ElementHandle.strict_text_content = strict_text_content
