"""CSC111 Project 2"""
from __future__ import annotations

import graphviz
import csv
from typing import Any, Optional

from python_ta.contracts import check_contracts


class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.

    Representation Invariants:
        - self._root is not None or self._subtrees == []
        - all(not subtree.is_empty() for subtree in self._subtrees)
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item.
    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            size = 1  # count the root
            for subtree in self._subtrees:
                size += subtree.__len__()  # could also write len(subtree)
            return size

    def __contains__(self, item: Any) -> bool:
        """Return whether the given is in this tree.

        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> t.__contains__(1)
        True
        >>> t.__contains__(5)
        True
        >>> t.__contains__(4)
        False
        """
        if self.is_empty():
            return False
        elif self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if subtree.__contains__(item):
                    return True
            return False

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return self._str_indented(0).rstrip()

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            str_so_far = '  ' * depth + f'{self._root}\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                str_so_far += subtree._str_indented(depth + 1)
            return str_so_far

    def remove(self, item: Any) -> bool:
        """Delete *one* occurrence of the given item from this tree.

        Do nothing if the item is not in this tree.
        Return whether the given item was deleted.
        """
        if self.is_empty():
            return False
        elif self._root == item:
            self._delete_root()  # delete the root
            return True
        else:
            for subtree in self._subtrees:
                deleted = subtree.remove(item)
                if deleted and subtree.is_empty():
                    # The item was deleted and the subtree is now empty.
                    # We should remove the subtree from the list of subtrees.
                    # Note that mutate a list while looping through it is
                    # EXTREMELY DANGEROUS!
                    # We are only doing it because we return immediately
                    # afterward, and so no more loop iterations occur.
                    self._subtrees.remove(subtree)
                    return True
                elif deleted:
                    # The item was deleted, and the subtree is not empty.
                    return True

            # If the loop doesn't return early, the item was not deleted from
            # any of the subtrees. In this case, the item does not appear
            # in this tree.
            return False

    def _delete_root(self) -> None:
        """Remove the root item of this tree.

        Preconditions:
            - not self.is_empty()
        """
        if not self._subtrees:
            self._root = None
        else:
            # Strategy: Promote a subtree (the rightmost one is chosen here).
            # Get the last subtree in this tree.
            last_subtree = self._subtrees.pop()

            self._root = last_subtree._root
            self._subtrees.extend(last_subtree._subtrees)

    def add_tree_body(self) -> None:
        """Builds our tree. True and False values that our answered through questions"""
        if not self._subtrees:
            self._subtrees = [Tree(True, []), Tree(False, [])]
        else:
            for subtree in self._subtrees:
                subtree.add_tree_body()

    def add_leafs(self) -> None:
        """Adds the leafs of our tree"""
        if not self._subtrees:
            self._subtrees.append(Tree(0, []))
        else:
            for subtree in self._subtrees:
                subtree.add_leafs()

    def edit_leafs(self, data: list) -> None:
        """Mutates the leafs of our tree.
        In our case, it is the number shots the player made or missed of a specific shot type.
        """

    def visualize(self, filename: str = 'tree') -> None:
        """Visualize this tree using Graphviz."""
        dot = graphviz.Digraph()

        def _add_nodes(tree: Tree, node_id: str) -> None:
            if tree.is_empty():
                return

            # Add the current node
            dot.node(node_id, str(tree._root))

            # Add child nodes and edges
            for i, subtree in enumerate(tree._subtrees):
                child_id = f'{node_id}_{i}'
                dot.node(child_id, str(subtree._root))
                dot.edge(node_id, child_id)
                _add_nodes(subtree, child_id)

        _add_nodes(self, 'root')

        # Save the visualization
        dot.render(filename, format='png', cleanup=True)


def modify_rows(row: list) -> list:
    """Takes in a row of data and returns a list with the values that we want from the csv file"""

    shot_profile = []

    if row[12] == '3':
        shot_profile.append("3-pointer")
    elif int(row[11]) >= 10:
        shot_profile.append("Mid-Range")
    else:
        shot_profile.append("Layup")

    if int(row[10]) >= 6:
        shot_profile.append(True)
    else:
        shot_profile.append(False)

    if int(row[8]) < 12:
        shot_profile.append(True)
    else:
        shot_profile.append(False)

    if row[13] == "made":
        shot_profile.append(True)
    else:
        shot_profile.append(False)

    return shot_profile


@check_contracts
def build_decision_tree(file: str, player: str) -> Tree:
    """Build a decision tree storing the animal data from the given file.

    Preconditions:
        - file is the path to a csv file in the format of the provided animals.csv
    """
    tree = Tree(player, [Tree("Three", []), Tree("Mid-range", []), Tree("Layup", [])])
    [tree.add_tree_body() for _ in range(3)]  # Runs add_tree_body() 3 times
    tree.add_leafs()

    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # skip the header row

        for row in reader:
            if row[19] == player:  # row[19] is the player's name in the csv file
                data = modify_rows(row)
                tree.edit_leafs(data)

    return tree


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    # User Input
