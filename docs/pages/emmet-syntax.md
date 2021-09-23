# Emmet Syntax

All `find_*` methods support `Emmet Syntax`, which allows you to perform search queries in a (**much**) shorter way. This comes in handy when you want to quickly find a deeply-nested element along a very specific path. This document aims to first explain this syntax, and then provide a few examples to show how it works (and to show how much shorter it can be). The methods will always display the character count, to show you that `Emmet Syntax` is always **almost twice** as compact (and for more complex cases, even more than that).

To indicate that a specific method supports this, all of them have the following line underneath their header in their respective documentation: 

_**This method supports Emmet Syntax through the [PARAMETER] parameter**_

### Note:

The `index` and `kwargs` parameters passed into the `find` methods are still allowed, but will only be applied to the _**last**_ element from the query. The path will always take priority when clashing, so if the query itself ends with an index (eg. `table>tr[3]`) then this index will be used instead of the parameter.

## Basics of Emmet Syntax

Before we dive in, a `tag` is still referenced by its name. `element("div")` is valid. If you want to include a tag name in your path, **it should _always_ be in the beginning**.

### Finding nested elements

To indicate that an element should contain another, use the `>` symbol (from left to right).

#### Example usage:

Problem: "Find the `<div>` inside of the `<td>` inside of the `<tr>` inside of the `<table>` inside of the `<div>` inside of the `<body>` starting from the root element (`<html>`)"

```python
# Without Emmet Syntax | 140 characters
div_element = suite.element("html", from_root=True)
    .get_child("body")
    .get_child("div")
    .get_child("table")
    .get_child("tr")
    .get_child("td")
    .get_child("div")

# With Emmet Syntax | 62 characters
div_element = suite.element("html>body>div>table>tr>td>div", from_root=True)
```

### Specifying indexes

By default, the first match will always be chosen for every step. To specify that the `n-th` match should be used, you may do so by adding the index between square brackets **at the end of the step**.

#### Example usage:

Problem: "Find the _third_ `<div>` inside of the _fourth_ `<td>` inside of the _first_ `<tr>` inside of the `<table>`"

```python
# Without Emmet Syntax | 97 characters
div_element = suite.element("table", from_root=False)
    .get_child("tr", 0)
    .get_child("td", 3)
    .get_child("div", 2)

# With Emmet Syntax | 58 characters
div_element = suite.element("table>tr[0]>td[3]>div[2]", from_root=False)

# The first is chosen by default, so [0] is always obsolete | 55 characters
div_element = suite.element("table>tr>td[3]>div[2]", from_root=False)
```

### Specifying id's

To filter down based on id's, you can specify an id by adding a hashtag (`#`) in front of it.

An id should only contain `letters`, `numbers`, `underscores` and `hyphens`, and should contain at least one character. In essence, they should match the following regex: `#([a-zA-Z0-9_-]+)`.

#### Example usage:

Problem: "Find the `<div>` with id `example` inside of the `<body>`"

```python
# Without Emmet Syntax | 52 characters
div_element = suite.element("body")
    .get_child("div", id="example")

# With Emmet Syntax | 33 characters
div_element = suite.element("body>div#example")

# With Emmet Syntax, only specifying the id and not the tag | 30 characters
div_element = suite.element("body>#example")

# With Emmet Syntax, using kwargs for the id as it is for the final step of the path | 39 characters
div_element = suite.element("body>div", id="example")
```

### Specifying class names

Class names can be specified by adding a dot (`.`) in front of them, and multiple class names in a row are **allowed**.

A class name should only contain `letters`, `numbers`, `underscores` and `hyphens`, and should contain at least one character. These are the same rules as for the `id`'s, so the same regex can be used to check: `\.[a-zA-z0-9_-]+`.

**However**, a class name can **not** start with:
- A `number`
- Two `hyphens`
- A `hyphen` followed by a `number`

This means your class name may **never** match the following regex: `\.([0-9]|--|-[0-9])`.

#### Example usage:

Problem: "Find the `<td>` with class names `ex-1` **and** `ex-2`, inside of the `<tr>` with class name `tr-example` inside of the `<table>`"

```python
# Without Emmet Syntax | 95 characters
div_element = suite.element("table")
    .get_child("tr", class_="tr-example")
    .get_child("td", class_="ex-1 ex-2")

# With Emmet Syntax | 49 characters
div_element = suite.element("table>tr.tr-example>td.ex-1.ex-2")
```