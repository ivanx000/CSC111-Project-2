🏀 NBA Shot Analyzer

NBA Shot Analyzer is a Python-based data analysis tool that builds and visualizes decision trees from NBA shot log data. It allows users to analyze a player’s shooting tendencies, calculate shot percentages, and visualize their best and worst shot scenarios using decision trees and interactive charts.

📘 Project Overview

This project reads NBA shot log data (2014–2015 season) from a CSV file and builds a decision tree model representing shot outcomes based on three main factors:

Shot Type → Layup, Mid-Range, or 3-pointer

Touch Time → Whether the player took the shot within 6 seconds or longer

Dribbles → Whether the player took 5 or fewer dribbles before shooting

The program then calculates:

Each shot’s make/miss percentage

The best and worst shot scenarios for the player

A pie chart visualization of shot distributions

A decision tree graph using Graphviz

⚙️ Installation
1. Clone the Repository
git clone https://github.com/<your-username>/nba-shot-analyzer.git
cd nba-shot-analyzer

2. Set Up a Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows

3. Install Dependencies

Make sure you have Python 3.10+ installed, then run:

pip install -r requirements.txt


If you don’t have a requirements.txt file yet, create one with the following contents:

graphviz
matplotlib
mpld3
python-ta


⚠️ macOS users: You may need to install Graphviz separately:

brew install graphviz


Windows users: Download Graphviz from graphviz.org/download
 and add it to your PATH.

▶️ Usage

Make sure the file shot_logs[1].csv is in the same directory as your script.

Run the main program:

python tree_analyzer.py

When prompted, enter a player’s full name (e.g., LeBron James, Stephen Curry).

The program will:

Generate a decision tree visualization (.png file)

Create a pie chart of shot distributions (opens in your browser)

Print the best and worst shots in the terminal

🧠 Example Output
Choose an NBA Player that played in the 2014-15 season (full name): stephen curry

Stephen Curry should TAKE MORE...
    - 3-pointers with 0-5 dribbles & a touch time of 0-5 seconds (58.3%)

and AVOID...
    - Mid-Range shots with 6+ dribbles & a touch time of 6+ seconds (21.7%)

Example Visuals

Decision Tree: Displays shooting outcomes as a hierarchical tree.

Pie Chart: Interactive browser-based chart (via mpld3).

🧩 Key Functions

Function	Description
build_decision_tree(file, player)	Builds a recursive tree from shot log data
edit_leafs(data)	Updates made/missed shot counts for each condition
map_shot_percentages()	Calculates shot success percentages
visualize()	Generates a .png decision tree graph
display_pie_chart()	Creates an interactive HTML pie chart visualization

🧰 Technologies Used

Python 3.10+

Graphviz – Decision tree visualization

Matplotlib + mpld3 – Interactive chart visualization

Python-TA – Code contract checking (used for testing and validation)

CSV module – Data handling

🚀 Future Improvements

Add player comparison mode (e.g., Curry vs. Thompson)

Integrate modern datasets (2020+)

Include GUI interface using Tkinter or Streamlit

Export visualizations as interactive dashboards
