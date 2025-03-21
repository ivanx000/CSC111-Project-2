"""CSC111 Project 2"""
from __future__ import annotations

import csv
from typing import Any, Optional
import graphviz

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
        if not data:
            self._subtrees[0]._root += 1
        else:
            for subtree in self._subtrees:
                temp = data[0]
                if subtree._root == temp:
                    subtree.edit_leafs(data[1:])

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

    def best_shot_percentage_helper(self) -> tuple[float, list]:
        """Returns the maximum shot percentage and the path to achieve it.

        - The percentage is calculated **pairwise** (1 & 2, 3 & 4, etc.).
        - If multiple paths yield the same percentage, the **leftmost (odd) path is chosen**.
        - Path is a list of node labels (e.g., ["3-pointer", True, False, True]).
        """
        if not self._subtrees:  # Leaf node case
            return self._root, []  # Return the leaf value (either `made` or `miss`)

        max_percentage = -1
        best_path = []

        # Process subtrees in pairs (we assume they are structured correctly)
        for i in range(0, len(self._subtrees), 2):
            made, path_made = self._subtrees[i].best_shot_percentage_helper()
            miss, path_miss = self._subtrees[i + 1].best_shot_percentage_helper()

            if miss != 0:  # Compute percentage
                percentage = made / miss
                if percentage > max_percentage:  # Update best if greater
                    max_percentage = percentage
                    best_path = [self._root] + path_made  # Store node label
                elif percentage == max_percentage:  # Tie-breaker: favor leftmost
                    best_path = [self._root] + path_made

        return max_percentage, best_path


def modify_rows(row: list) -> list:
    """Takes in a row of data and returns a list with the values that we want from the csv file"""

    if float(row[12]) == 3:
        shot_type = "3-pointer"
    elif float(row[11]) >= 10:
        shot_type = "Mid-Range"
    else:
        shot_type = "Layup"

    touch_time = (float(row[10]) < 6)
    dribbles = (float(row[9]) < 6)
    make_or_miss = (row[13] == 'made')

    return [shot_type, touch_time, dribbles, make_or_miss]


@check_contracts
def build_decision_tree(file: str, player: str) -> Tree:
    """Build a decision tree storing the animal data from the given file.

    Preconditions:
        - file is the path to a csv file in the format of the provided animals.csv
    """
    tree = Tree(player, [Tree("3-pointer", []), Tree("Mid-Range", []), Tree("Layup", [])])
    tree.add_tree_body()
    tree.add_tree_body()
    tree.add_tree_body()
    tree.add_leafs()

    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # skip the header row

        for row in reader:
            if row[19] == player:  # row[19] is the player's name in the csv file
                data = modify_rows(row)
                tree.edit_leafs(data)

    return tree


def read_names(file: str) -> set:
    """Returns a set of all the players from our data"""
    all_player_names = set()

    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            all_player_names.add(row[19])

    return all_player_names


def identify_shot(path: list) -> str:
    """Identifies the type of shot the player made"""

    shot_profile = [path[0]]

    if path[1]:
        shot_profile.append("Touch Time: >6 seconds")
    else:
        shot_profile.append("Touch Time: 6+ seconds")

    if path[2]:
        shot_profile.append('0-5 Dribbles')
    else:
        shot_profile.append('6 + Dribbles')

    for element in shot_profile:
        print(f'- {element}')


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    player_names = read_names("shot_logs[1].csv")

    name = input("\nChoose an NBA Player that played in the 2014-15 season (full name): ").lower().strip()

    while all(player_names):
        print(f"{name} did not play in the 2014-15 season.")
        name = input("\nEnter a different player: ").lower().strip()

    my_tree = build_decision_tree("shot_logs[1].csv", name)
    my_tree.visualize(name)
