import random as random_module
from typing import TypedDict, Required, NotRequired
from playwright.sync_api import Page


class SelectComboboxOptions(TypedDict):
    page: Required[Page]
    label_text: Required[str]
    value: NotRequired[str]
    random: NotRequired[bool]


class SelectComboboxByPlaceholderOptions(TypedDict):
    page: Required[Page]
    placeholder: Required[str]
    value: NotRequired[str]
    random: NotRequired[bool]


def _pick_option(page: Page, value: str, use_random: bool):
    """Clicks an option from an open Radix/Shadcn listbox."""
    options = page.get_by_role("option")
    options.first.wait_for(state="visible", timeout=10_000)

    selected_options = options.filter(has=page.locator(f"span:has-text('{value}')"))

    if not value:
        options.first.click()
    elif use_random:
        count = options.count()
        options.nth(random_module.randint(0, count - 1)).click()
    elif selected_options.count() > 0:
        selected_options.first.click()
    else:
        page.get_by_role("option", name=value, exact=True).click()


def select_combobox_option(**kwargs: SelectComboboxOptions):
    """
    Selects an option from a Shadcn/Radix combobox by matching the label text.

    Kwargs:
        page (Page): Playwright Page instance
        label_text (str): The visible label text next to the combobox (e.g. "Cage:")
        value (str): The option text to select. Selects the first option if not provided.
        random (bool): If True, selects a random available option. Defaults to False.
    """
    page: Page = kwargs["page"]
    label_text: str = kwargs["label_text"]
    value: str = kwargs.get("value", "")
    use_random: bool = kwargs.get("random", False)

    field = page.locator(".filter-item").filter(
        has=page.locator(f"label:has-text('{label_text}')")
    )
    field.get_by_role("combobox").first.click()
    _pick_option(page, value, use_random)


def select_filter_combobox_option(**kwargs: SelectComboboxByPlaceholderOptions):
    """
    Selects an option from a Shadcn/Radix combobox by matching the combobox placeholder text.

    Kwargs:
        page (Page): Playwright Page instance
        placeholder (str): The placeholder text inside the combobox trigger (e.g. "Select a zone")
        value (str): The option text to select. Selects the first option if not provided.
        random (bool): If True, selects a random available option. Defaults to False.
    """
    page: Page = kwargs["page"]
    placeholder: str = kwargs["placeholder"]
    value: str = kwargs.get("value", "")
    use_random: bool = kwargs.get("random", False)

    page.get_by_role("combobox").filter(
        has=page.locator(f"span:has-text('{placeholder}')")
    ).click()
    _pick_option(page, value, use_random)
