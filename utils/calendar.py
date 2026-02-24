from datetime import date, time, datetime
from typing import TypedDict, Required, NotRequired
from playwright.sync_api import Page


class SelectCalendarDateRangeOptions(TypedDict):
    page: Required[Page]
    trigger_placeholder: Required[str]
    start_date: Required[date]
    end_date: Required[date]
    start_time: NotRequired[time]
    end_time: NotRequired[time]


def select_calendar_date_range(**kwargs: SelectCalendarDateRangeOptions):
    """
    Selects a date range from a Shadcn UI dual-month Calendar (popover variant).
    Optionally sets start and end times if the calendar includes time inputs.

    Kwargs:
        page (Page): Playwright Page instance
        trigger_placeholder (str): Placeholder or visible text on the calendar trigger button
        start_date (date): Start date of the range (e.g. date(2026, 2, 16))
        end_date (date): End date of the range (e.g. date(2026, 2, 18))
        start_time (time): Optional start time (e.g. time(0, 0, 0))
        end_time (time): Optional end time (e.g. time(23, 59, 59))
    """
    page: Page = kwargs["page"]
    trigger_placeholder: str = kwargs["trigger_placeholder"]
    start_date: date = kwargs["start_date"]
    end_date: date = kwargs["end_date"]
    start_time: time | None = kwargs.get("start_time")
    end_time: time | None = kwargs.get("end_time")

    # Open the calendar popover
    page.get_by_role("button").filter(
        has=page.locator(f"span:has-text('{trigger_placeholder}')")
    ).click()

    calendar = page.locator("[data-slot='calendar']")
    calendar.wait_for(state="visible", timeout=10_000)

    # Navigate so start_date is visible in the left month panel
    _navigate_to_month(page, calendar, start_date.strftime("%B %Y"), panel="left")

    # Click start date then end date
    _click_day(calendar, start_date)
    _click_day(calendar, end_date)

    # Set times if provided
    if start_time is not None:
        _set_time_input(page, "Start Time", start_time)
    if end_time is not None:
        _set_time_input(page, "End Time", end_time)


def _click_day(calendar, target_date: date):
    """Clicks a day button in the visible calendar panels."""
    target_month_year = target_date.strftime("%B %Y")
    target_day = str(target_date.day)

    panel = calendar.locator("[data-slot='month']").filter(
        has=calendar.locator(
            f"[data-slot='caption-label']:has-text('{target_month_year}')"
        )
    )
    panel.get_by_role("gridcell").get_by_role(
        "button", name=target_day, exact=True
    ).click()


def _navigate_to_month(
    page: Page, calendar, target_month_year: str, panel: str = "left"
):
    """
    Navigates the calendar using prev/next buttons until the target month/year
    appears in the specified panel (left = first caption, right = second caption).
    """
    max_iterations = 24
    panel_index = 0 if panel == "left" else 1

    for _ in range(max_iterations):
        labels = calendar.locator("[data-slot='caption-label']").all()
        current_label = labels[panel_index].inner_text().strip()

        if current_label == target_month_year:
            break

        current = _parse_month_year(current_label)
        target = _parse_month_year(target_month_year)

        if target > current:
            calendar.get_by_role("button", name="Go to next month").click()
        else:
            calendar.get_by_role("button", name="Go to previous month").click()

        page.wait_for_timeout(300)


def _set_time_input(page: Page, label: str, t: time):
    """Sets a time input field found by its label text."""
    field = (
        page.locator(".filter-item")
        .filter(has=page.locator(f"label:has-text('{label}')"))
        .locator("input[type='time']")
    )

    if not field.count():
        field = (
            page.locator(f"text={label}").locator("..").locator("input[type='time']")
        )

    field.fill(t.strftime("%H:%M:%S"))


def _parse_month_year(label: str) -> date:
    """Parses a 'Month YYYY' string into a date for comparison."""

    return datetime.strptime(label, "%B %Y").date().replace(day=1)
