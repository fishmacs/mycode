def add_to_tree(root, value_string):
    """Given a string of characters `value_string`, create or update a
    series of dictionaries where the value at each level is a dictionary of
    the characters that have been seen following the current character.

    Example:
    >>> my_string = 'abc'
    >>> tree = {}
    >>> add_to_tree(tree, my_string)
    >>> print(tree['a']['b'])
    {'c': {}}
    >>> add_to_tree(tree, 'abd')
    >>> print(tree['a']['b'])
    {'c': {}, 'd': {}}
    >>> print(tree['a']['d'])
    KeyError 'd'
    """

    for character in value_string:
        root = root.setdefault(character, {})
