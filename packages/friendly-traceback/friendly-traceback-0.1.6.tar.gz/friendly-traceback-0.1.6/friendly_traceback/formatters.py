"""formatters.py

Default formatters showing all or only part of the available information.
"""
from .my_gettext import current_lang

RICH_HEADER = False

default_items_in_order = [  # This list excludes three traceback items
    "header",
    "message",
    "suggest",
    "generic",
    "parsing_error",
    "parsing_error_source",
    "cause_header",
    "cause",
    "last_call_header",
    "last_call_source",
    "last_call_variables_header",
    "last_call_variables",
    "exception_raised_header",
    "exception_raised_source",
    "exception_raised_variables_header",
    "exception_raised_variables",
]


def tb_items_to_show(level=1):
    """Given a verbosity level, returns a list of traceback items to show."""
    selector = {
        1: _traceback_before_default,  # for running script in non-interactive mode
        2: _default,  # used to be level 1
        3: _traceback_after_default,
        4: _traceback_before_no_generic,
        5: _no_generic_explanation,
        6: _traceback_after_no_generic,
        7: _tb_plus_suggest,  # shortened traceback, default for console
        8: _advanced_user,
        9: _shortened_python_traceback,
        0: _simulated_python_traceback,
        -1: _original_python_traceback,
        11: _what,
        12: _where,
        13: _why,
        14: _suggest,
    }
    return selector[level]()


def pre(info, level=1):
    """Default formatter, primarily for console usage.

    It also  produces an output that is suitable for
    insertion in a RestructuredText (.rst) code block,
    with pre-formatted indentation.

    The only change made to the content of "info" is
    some added indentation.
    """
    pre_items = {
        "header": "single",
        "message": "double",
        "suggest": "double",
        "generic": "single",
        "parsing_error": "single",
        "parsing_error_source": "none",
        "cause_header": "single",
        "cause": "double",
        "last_call_header": "single",
        "last_call_source": "none",
        "last_call_variables_header": "double",
        "last_call_variables": "double",
        "exception_raised_header": "single",
        "exception_raised_source": "none",
        "exception_raised_variables_header": "double",
        "exception_raised_variables": "double",
        "simulated_python_traceback": "single",
        "original_python_traceback": "single",
        "shortened_traceback": "single",
    }

    items_to_show = tb_items_to_show(level=level)
    spacing = {"single": " " * 4, "double": " " * 8, "none": ""}
    result = [""]
    for item in items_to_show:
        if item in info:
            indentation = spacing[pre_items[item]]
            for line in info[item].split("\n"):
                result.append(indentation + line)

    if result == [""]:
        return _no_result(info, level)

    return "\n".join(result)


def markdown(info, level=1):
    """Traceback formatted with with markdown syntax.

    Some minor changes of the traceback info content are done,
    for nicer final display when the markdown generated content
    if further processed.
    """
    result = _markdown(info, level=level)
    if result == [""]:
        return _no_result(info, level)
    return "\n\n".join(result)


def markdown_docs(info, level=1):
    """Traceback formatted with with markdown syntax, where each
    header is shifted down by 2 (h1 -> h3, etc.) so that they
    can be inserted in a document, without creating artificial
    top headers.

    Some minor changes of the traceback info content are done,
    for nicer final display when the markdown generated content
    is further processed.
    """
    result = _markdown(info, level=level, docs=True)
    if result == [""]:
        return _no_result(info, level)

    return "\n\n".join(result)


def rich_markdown(info, level=1):
    """Traceback formatted with with markdown syntax suitable for
    printing in color in the console using Rich.

    Some minor changes of the traceback info content are done,
    for nicer final display when the markdown generated content
    if further processed.
    """
    result = _markdown(info, level=level, rich=True)
    if result == [""]:
        return _no_result(info, level)
    return "\n\n".join(result)


def _no_result(info, level):
    """Should only be called if no result is available from either
    suggest() or why()
    """
    _ = current_lang.translate
    if level == 13:  # why()
        return _("I do not know.")
    elif level == 14:  # suggest()
        if info["cause"]:
            return _("I have no suggestion to offer; try `why()`.")
        else:
            return _("I have no suggestion to offer.")
    else:
        return f"Internal error: level = {level} in formatters._no_result()"


def _markdown(info, level, rich=False, docs=False):
    """Traceback formatted with with markdown syntax."""
    global RICH_HEADER
    RICH_HEADER = False
    result = []

    markdown_items = {
        "header": ("# ", ""),
        "message": ("", ""),
        "suggest": ("", "\n"),
        "generic": ("", ""),
        "parsing_error": ("", ""),
        "parsing_error_source": ("```python\n", "\n```"),
        "cause_header": ("### ", ""),
        "cause": ("", ""),
        "last_call_header": ("## ", ""),
        "last_call_source": ("```python\n", "\n```"),
        "last_call_variables_header": ("### ", ""),
        "last_call_variables": ("```python\n", "\n```"),
        "exception_raised_header": ("## ", ""),
        "exception_raised_source": ("```python\n", "\n```"),
        "exception_raised_variables_header": ("### ", ""),
        "exception_raised_variables": ("```python\n", "\n```"),
        "simulated_python_traceback": ("```pytb\n", "\n```"),
        "original_python_traceback": ("```pytb\n", "\n```"),
        "shortened_traceback": ("```pytb\n", "\n```"),
    }

    items_to_show = tb_items_to_show(level=level)
    result = [""]
    for item in items_to_show:
        if rich and item == "header":  # Skip it here; handled by session.py
            RICH_HEADER = True
            continue
        if item in info:
            # With normal markdown formatting, it does not make sense to have a
            # header end with a colon.
            # However, we style headers differently with Rich; see
            # Rich theme in file friendly_rich.
            content = info[item]
            if item.endswith("header"):
                if not rich:
                    content = content.rstrip(":")
                else:
                    if item not in [
                        "cause_header",
                        "last_call_variables_header",
                        "exception_raised_variables_header",
                    ]:
                        content = content.rstrip(":")
            if item == "message" and rich:
                # Ensure that the exception name is highlighted.
                content = content.split(":")
                content[0] = "`" + content[0] + "`"
                content = ":".join(content)

            prefix, suffix = markdown_items[item]
            if docs:
                if prefix.startswith("#"):
                    prefix = "##" + prefix
            result.append(prefix + content + suffix)
    return result


def _default():
    """Includes all the information processed by Friendly-traceback
    which does not include a traditional Python traceback
    """
    return default_items_in_order[:]


def _traceback_before_default():
    """Includes the simulated Python traceback before all the information
    processed by Friendly-traceback.
    """
    items = _default()
    # The traceback ends with the message; so we replace the message by the tb.
    items[1] = "shortened_traceback"
    return items


def _traceback_after_default():
    """Includes the simulated Python traceback after all the information
    processed by Friendly-traceback.
    """
    items = _default()
    items.append("shortened_traceback")
    return items


def _no_generic_explanation():
    """Similar to the default option except that it does not display the
    generic information about a given exception.
    """
    items = []
    for item in default_items_in_order:
        if item == "generic":
            continue
        items.append(item)
    return items


def _traceback_before_no_generic():
    """Includes the simulated Python traceback before all the information
    processed by Friendly-traceback.
    """
    items = ["shortened_traceback"]
    items.extend(_no_generic_explanation())
    return items


def _traceback_after_no_generic():
    """Includes the simulated Python traceback after all the information
    processed by Friendly-traceback.
    """
    items = _no_generic_explanation()
    items.append("shortened_traceback")
    return items


def _advanced_user():  # Not (yet) included by Thonny
    """Useful information for advanced users."""
    return [
        "header",
        "simulated_python_traceback",
        "suggest",
        "parsing_error_source",
        "cause",
        "last_call_header",
        "last_call_source",
        "last_call_variables",
        "exception_raised_header",
        "exception_raised_source",
        "exception_raised_variables",
    ]


def _tb_plus_suggest():
    """Shortened Python tracebacks followed by specific information."""
    return ["shortened_traceback", "parsing_error", "suggest"]


def _simulated_python_traceback():
    """Shows only the simulated Python traceback"""
    return ["simulated_python_traceback"]


def _shortened_python_traceback():
    """Shows only the simulated Python traceback"""
    return ["shortened_traceback"]


def _original_python_traceback():
    """Shows only the original Python traceback, which includes calls
    to friendly-traceback itself. It should only be used for diagnostic.
    """
    return ["original_python_traceback"]


def _what():
    """Shows the message and and the generic meaning.

    For example: A NameError means ...
    """
    return ["message", "generic"]


def _why():
    """Show only the likely cause"""
    return ["cause"]


def _suggest():
    """Show only the hint/suggestion if available"""
    return ["suggest"]


def _where():
    """Shows the locations where the program stopped and where the
    exception was raised, together with variable information
    at these locations.
    """
    return [
        "parsing_error",
        "parsing_error_source",
        "last_call_header",
        "last_call_source",
        "last_call_variables",
        "exception_raised_header",
        "exception_raised_source",
        "exception_raised_variables",
    ]
