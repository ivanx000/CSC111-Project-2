"""CSC111 Project 2"""
from __future__ import annotations

import csv
import random
from typing import Any, Optional
import os
import platform
import webbrowser

import matplotlib.pyplot as plt
import graphviz
import mpld3

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
            self._subtrees.append(Tree(0, []))
        else:
            for subtree in self._subtrees:
                subtree.add_leafs()

    def edit_leafs(self, data: list) -> None:
        """Mutates the leafs of our tree.
        In our case, it is the number shots the player made or missed of a specific shot type.
        """
        if len(data) == 1:
            if data[0]:
                self._subtrees[0]._root += 1
            else:
                self._subtrees[1]._root += 1
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
        filepath = os.path.abspath(f"{filename}.png")
        dot.render(filename, format='png', cleanup=True)

        # Open in Chrome (make sure Chrome is the default or specify path)
        system_name = platform.system()
        if system_name == "Windows":
            chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"  # For Windows
        else:   # macOS
            chrome_path = "open -a Google\\ Chrome %s"  # For macOS

        webbrowser.get(chrome_path).open(filepath)

    def map_shot_percentages(self, shot_path: list) -> dict[str, float]:
        """Returns a dictionary mapping each shot percentage to its path in the tree."""
        all_percentages = {}
        if is_actual_int(self._subtrees[0]._root) and is_actual_int(self._subtrees[1]._root):
            made_shots = self._subtrees[0]._root
            missed_shots = self._subtrees[1]._root
            total_shots = made_shots + missed_shots

            if total_shots == 0:
                percent = 0
            else:
                percent = round((made_shots / total_shots) * 100, 2)

            all_percentages[identify_shot(shot_path)] = percent
            return all_percentages
        else:
            for subtree in self._subtrees:
                all_percentages.update(subtree.map_shot_percentages(shot_path + [subtree._root]))

            return all_percentages

    def map_best_shot_percentages(self) -> list:
        """Maps each shot to its best percentage"""
        all_best_percentages = {"Layup": None, "Mid-Range": None, "3-pointer": None}

        for subtree in self._subtrees:
            best_percentage, best_path = subtree.best_shot_percentage([subtree._root])
            best_path = [identify_shot(best_path)]

            for shot in list(all_best_percentages.keys()):
                if shot.lower() in best_path[0].lower() and (all_best_percentages[shot] is None or best_percentage
                                                             > all_best_percentages[shot]):
                    all_best_percentages[shot] = (best_percentage, best_path)

        return list(all_best_percentages.values())

    def best_shot_percentage(self, shot_path: list) -> tuple:
        """Returns the maximum shot percentage and its path.
        If there is a tie-breaker, it returns the left-most shot
        """
        if is_actual_int(self._subtrees[0]._root) and is_actual_int(self._subtrees[1]._root):
            made_shots = self._subtrees[0]._root
            missed_shots = self._subtrees[1]._root
            total_shots = made_shots + missed_shots

            if total_shots == 0:
                percent = 0
            else:
                percent = round((made_shots / total_shots) * 100, 2)

            return percent, shot_path
        else:
            best_percentage = -1
            best_path = []

            for subtree in self._subtrees:
                curr_percentage, curr_path = subtree.best_shot_percentage(shot_path + [subtree._root])

                if curr_percentage > best_percentage:
                    best_percentage = curr_percentage
                    best_path = curr_path

            return best_percentage, best_path

    def map_worst_shot_percentages(self) -> list:
        """Maps each shot to its worst percentage"""
        all_worst_percentages = {"Layup": None, "Mid-Range": None, "3-pointer": None}

        for subtree in self._subtrees:
            worst_percentage, worst_path = subtree.worst_shot_percentage([subtree._root])
            worst_path = [identify_shot(worst_path)]

            for shot in list(all_worst_percentages.keys()):
                if shot.lower() in worst_path[0].lower() and (all_worst_percentages[shot] is None or worst_percentage
                                                              < all_worst_percentages[shot]):
                    all_worst_percentages[shot] = (worst_percentage, worst_path)

        return list(all_worst_percentages.values())

    def worst_shot_percentage(self, shot_path: list) -> tuple:
        """Returns the lowest shot percentage (for each shot type) and its path.
        If there is a tie-breaker, it returns the left-most shot
        """
        if is_actual_int(self._subtrees[0]._root) and is_actual_int(self._subtrees[1]._root):
            made_shots = self._subtrees[0]._root
            missed_shots = self._subtrees[1]._root
            total_shots = made_shots + missed_shots

            if total_shots == 0:
                percent = 0
            else:
                percent = round((made_shots / total_shots) * 100, 2)

            return percent, shot_path
        else:
            worst_percentage = 101
            worst_path = []

            for subtree in self._subtrees:
                curr_percentage, curr_path = subtree.worst_shot_percentage(shot_path + [subtree._root])

                if curr_percentage < worst_percentage:
                    worst_percentage = curr_percentage
                    worst_path = curr_path

            return worst_percentage, worst_path


def is_actual_int(value: Any) -> bool:
    """To fix isinstance(True, int) returning True"""
    return isinstance(value, int) and not isinstance(value, bool)


def modify_rows(row: list) -> list:
    """Takes in a row of data and returns a list with the values that we want from the csv file"""

    if float(row[12]) == 3:
        shot = "3-pointer"
    elif float(row[11]) >= 10:
        shot = "Mid-Range"
    else:
        shot = "Layup"

    time = float(row[10]) < 6
    num_dribbles = float(row[9]) < 6
    make_or_miss = row[13] == 'made'

    return [shot, time, num_dribbles, make_or_miss]


@check_contracts
def build_decision_tree(file: str, player: str) -> Tree:
    """Build a decision tree storing the animal data from the given file.

    Preconditions:
        - file is the path to a csv file in the format of the provided animals.csv
    """
    tree = Tree(player, [Tree("3-pointer", []), Tree("Mid-Range", []), Tree("Layup", [])])
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


def identify_shot(shot_path: list) -> str:
    """Identifies the type of shot the player made"""

    shot_classification = shot_path[0]

    if shot_path[1]:
        shot_classification += ", >6 seconds"
    else:
        shot_classification += ", 6+ seconds"

    if shot_path[2]:
        shot_classification += ", 0-5 dribbles"
    else:
        shot_classification += ", 6+ dribbles"

    return shot_classification


def display_pie_chart(data: dict[str, float], player_name: str) -> None:
    """Displays a pie chart of all the shot percentages in a web browser."""
    labels = list(data.keys())
    sizes = list(data.values())

    colours = [
        "#FF5733", "#FFBD33", "#DBFF33", "#75FF33", "#33FF57",
        "#33FFBD", "#33DBFF", "#3375FF", "#5733FF", "#BD33FF",
        "#FF33A8", "#FF3385", "#FF3366", "#FF6633", "#FF9933",
        "#FFFF33", "#A8FF33", "#85FF33", "#66FF33", "#33FF66",
        "#33FFA8", "#33FFFF", "#33A8FF", "#3385FF", "#3366FF"
    ]
    random_number = random.randint(0, 13)
    all_colours = colours[random_number:random_number + len(labels)]

    # Create pie chart
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=all_colours, startangle=140)
    ax.set_title(f"{player_name.title()}'s Shot Distribution")

    # Display the pie chart in the browser using mpld3
    html_content = mpld3.fig_to_html(fig)

    # Save to file
    filename = "pie_chart.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Get the current platform
    system_name = platform.system()

    # Open the HTML file in the default browser based on the platform
    filepath = os.path.abspath(filename)

    if system_name == "Windows":
        try:
            os.startfile(filepath)  # Opens in the default browser on Windows
        except AttributeError:
            print("Error: 'os.startfile' is not supported on your system.")
            print(f"Please manually open {filepath}")
    elif system_name == "Darwin":  # macOS
        os.system(f"open {filepath}")
    elif system_name == "Linux":
        os.system(f"xdg-open {filepath}")
    else:
        print(f"Unsupported platform: {system_name}. Please open {filepath} manually.")


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

    while name not in player_names:
        print(f"{name} did not play in the 2014-15 season.")
        name = input("\nEnter a different player: ").lower().strip()

    my_tree = build_decision_tree("shot_logs[1].csv", name)

    my_tree.visualize(name)

    shot_percentages = my_tree.map_shot_percentages([])

    display_pie_chart(shot_percentages, name)

    best_shots = my_tree.map_best_shot_percentages()

    print(f"\033[1;97m{name.title()}\033[0m should \033[32mTAKE MORE\033[0m...")

    for shot_description in best_shots:
        percentage, path = shot_description

        shot_type, touch_time, dribbles = path[0].split(',')

        print(f"\t- \033[35m{shot_type.lower()}s\033[0m with {dribbles} & a touch time of {touch_time} "
              f"(\033[33m{percentage}%\033[0m)")

    worst_shots = my_tree.map_worst_shot_percentages()

    print("\nand \033[31mAVOID\033[0m...")

    for shot_description in worst_shots:
        percentage, path = shot_description

        shot_type, touch_time, dribbles = path[0].split(',')

        print(f"\t- \033[35m{shot_type.lower()}s\033[0m with {dribbles} & a touch time of {touch_time} "
              f"(\033[33m{percentage}%\033[0m)")
