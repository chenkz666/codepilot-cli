from __future__ import annotations

from codepilot.commands.completion import CompletionPopup


def test_completion_popup_scrolls_selection_into_view() -> None:
    popup = CompletionPopup()
    pairs = [(f"command {index}", f"/command-{index}") for index in range(25)]

    popup.show_pairs(pairs)
    for _ in range(24):
        popup.move_down()

    assert popup.get_selected() == "/command-24"
    assert popup._window_start == 5


def test_completion_popup_resets_window_for_new_results() -> None:
    popup = CompletionPopup()
    popup.show_pairs([(str(index), str(index)) for index in range(20)])
    for _ in range(18):
        popup.move_down()

    popup.show_pairs([("new", "/new")])

    assert popup._window_start == 0
    assert popup.get_selected() == "/new"
