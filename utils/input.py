from typing import TypedDict, Required, NotRequired
from playwright.sync_api import Page


class FillInputOptions(TypedDict):
    page: Required[Page]
    placeholder: Required[str]
    value: Required[str]
    clear: NotRequired[bool]


def fill_input(**kwargs: FillInputOptions):
    """
    Fills an input or textarea field located by its placeholder text.

    Kwargs:
        page (Page): Playwright Page instance
        placeholder (str): The placeholder text of the input (e.g. "Search...")
        value (str): The value to type into the input
        clear (bool): If True, clears the field before filling. Defaults to True.
    """
    page: Page = kwargs["page"]
    placeholder: str = kwargs["placeholder"]
    value: str = kwargs["value"]
    clear: bool = kwargs.get("clear", True)

    field = page.get_by_placeholder(placeholder)
    field.wait_for(state="visible", timeout=10_000)

    if clear:
        field.clear()

    field.fill(value)
