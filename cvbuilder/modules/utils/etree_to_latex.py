from xml.etree.ElementTree import Element

__all__ = ["to_latex_string"]


def _get_full_text(element: Element) -> str:
    text = "" if element.text is None else element.text
    for child in element:
        text += _to_latex(child)
        if child.tail is not None:
            text += child.tail
    return text


def _to_latex(element: Element) -> str:
    if element.tag in "p":
        return _get_full_text(element) + "\n"
    if element.tag == "a":
        return f"\\href{{{element.get('href')}}}{{{_get_full_text(element)}}}"
    if element.tag == "em":
        return f"\\emph{{{_get_full_text(element)}}}"
    if element.tag == "strong":
        return f"\\textbf{{{_get_full_text(element)}}}"
    if element.tag in ["ul", "ol"]:
        environment = "itemize" if element.tag == "ul" else "enumerate"
        inner = "\n".join(map(_to_latex, element))
        return f"\\begin{{{environment}}}\n{inner}\n\\end{{{environment}}}\n"
    if element.tag == "li":
        return f"\\item {_get_full_text(element)}"
    if element.tag in "div":
        return "".join(map(_to_latex, element))
    print(f"LaTeX serializer: unknown tag {element.tag}. Please open an issue on GitHub for this.")
    return ""


def to_latex_string(element: Element) -> str:
    return f"<div>{_to_latex(element)}</div>"
