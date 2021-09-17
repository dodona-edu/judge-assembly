import bs4
from validators.css_validator import Rules, Rule


def prep_render(html_content: str) -> str:
    """prepares the html for randering:
        a body and a style tag must be present, if not returns the input html
        if both are present:
        * wraps the contents of body in a div with id='solution_rendering'
        * prepends '#solution_rendering ' to every css rule, so that every rule applies to descendants of the div"""
    try:
        soup = bs4.BeautifulSoup(html_content, "html.parser")

        # wrap div around the contents of body
        body = soup.find("body")
        div = soup.new_tag("div", attrs={"id": "solution_rendering"})
        body.wrap(div)
        attrs = body.attrs
        body.unwrap()
        div.wrap(soup.new_tag("body", attrs=attrs))

        # edit the css-rules
        style = soup.find("style")
        # print(style.string)
        rs = Rules(style.string)
        x: Rule
        for x in rs.rules:
            x.selector_str = f"#solution_rendering {x.selector_str}"

        new_style = ""
        for r in rs.rules:
            new_style += f"{r.selector_str}" + "{" + f"{r.name}:{r.value_str}{'!important' if r.important else ''}" + ";}\n   "

        style.string = new_style

        return str(soup.prettify())
    except Exception:
        return html_content
