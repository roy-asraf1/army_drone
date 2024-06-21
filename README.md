# Attacker Tracker Project
## Description
The Attacker Tracker project is designed to monitor and track an attacker’s position relative to a drone. The project calculates the distance and angles (both horizontal and vertical) between the drone and the attacker. It also determines if the drone can reach the attacker within a given time frame.

## Features
* Real-time calculations of distance and angles (horizontal and vertical) between the drone and attacker.
* Updates and writes results to CSV files in real-time.
* Displays possible solutions if the drone can reach the attacker in time.
* Provides a graphical user interface (GUI) for input and display.
## Files Included
* attacker.py: Defines the Attacker class and its behavior.
* drone.py: Defines the Drone class and its behavior.
* indication.py: Defines the Indication class and its behavior.
* location.py: Defines the Location class and its behavior.
* simulator.py: Main script that includes the logic for tracking and calculating the drone and attacker positions.
* dell.sh: Shell script to remove all CSV files generated during the program execution.

## Requirements
- Python 3.x
- Tkinter for GUI
- CSV module for handling CSV files
- Math module for mathematical calculations
- Threading module for concurrent tasks
### How to Run
Setup: Ensure you have Python 3.x installed on your machine. Install the required modules if they are not already available.

## Running the Script:

Navigate to the project directory.
python simulator.py

## Cleaning Up:
To remove all generated CSV files, execute the dell.sh script:
./dell.sh
