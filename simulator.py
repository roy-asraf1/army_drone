import csv
import math
import threading
import time
import tkinter as tk
from tkinter import ttk
from location import Location
from indication import Indication
from attacker import Attacker
import drone

MINIMUM = 100000
MAXIMUM = 999999

# Constants
my_speed_kmh = 120  # our speed in km/h
my_speed_mps = my_speed_kmh * 1000 / 3600  # our speed in meters per second
max_time_seconds = 300  # Maximum time to reach the attacker in seconds (e.g., 5 minutes)

# Time since indication for the thread
indication_time_seconds = 0

def update_time_since_indication(): # Update the time since indication
    global indication_time_seconds # Use the global variable
    while True:
        indication_time_seconds += 1 # Increment the time since indication
        time.sleep(1) # Sleep for 1 second

def start_calculations(): # Start the calculations
    try:
        x = float(miz_entry.get()) # Get the x value
        y = float(north_entry.get()) # Get the y value
        direction = float(direction_entry.get()) # Get the direction value
    except ValueError:
        result_label.config(text="Invalid input. Please enter numeric values.") # Display an error message
        return

    if x < MINIMUM or x > MAXIMUM or y < MINIMUM or y > MAXIMUM or direction < 0 or direction > 360: # Check if the values are out of range
        result_label.config(text="There was an error, please try again.") # Display an error message
        return

    z = 1500 # Set the z value to 1500
    first_location = Location(x, y, z) # Create a new location object for the attacker
    direction_rad = math.radians(direction) # Convert the direction to radians
    indication = Indication(first_location, direction) # Create a new indication object
    attacker = Attacker(indication)  # Attacker object

    with open('road.csv', mode='w', newline='') as file: # Open the road.csv file
        writer = csv.writer(file) # Create a CSV writer
        writer.writerow(['time', 'x', 'y', 'height']) # Write the header row

        time_seconds = 0 # Set the time to 0
        current_x = x # Set the current x value
        current_y = y # Set the current y value

        for _ in range(attacker.duration_seconds): # Loop through the duration of the attacker
            current_x += attacker.speed_mps * math.cos(direction_rad) # Update the x value
            current_y += attacker.speed_mps * math.sin(direction_rad) # Update the y value
            current_z = attacker.height # Set the z value to the attacker's height
            writer.writerow([time_seconds, current_x, current_y, current_z]) 
            time_seconds += 1 

    print("road.csv created successfully :)")

    # Start the thread to update the time since indication
    time_thread = threading.Thread(target=update_time_since_indication) # Create a new thread
    time_thread.daemon = True # Set the thread as a daemon
    time_thread.start() # Start the thread

    try:
        x_myLocation = float(x_location_entry.get()) # Get the x value
        y_myLocation = float(y_location_entry.get()) # Get the y value
        height = float(height_entry.get()) # Get the height value
    except ValueError:
        result_label.config(text="Invalid input. Please enter correct values.")
        return

    myLocation = Location(x_myLocation, y_myLocation, height) # Create a new location object for the drone
    myDrone = drone.drone(myLocation) # Create a new drone object

    def update_reach_status(): # Update the reach status
        while True:
            distances_between_att_drone = [] 
            angles_between_drone_to_att = []
            angles_vertical_between_drone_to_att = []
            time_for_att = []
            can_reach = []

            with open('road.csv', mode='r') as file:
                reader = csv.DictReader(file) 
                for row in reader:
                    x_attacker = float(row['x'])
                    y_attacker = float(row['y'])
                    z_attacker = float(row['height'])

                    distance = math.sqrt((x_attacker - myLocation.x)**2 + 
                                         (y_attacker - myLocation.y)**2 + 
                                         (z_attacker - myLocation.z)**2)
                    distances_between_att_drone.append(distance) 

                    dx = x_attacker - myLocation.x 
                    dy = y_attacker - myLocation.y
                    angle_horizontal = math.degrees(math.atan2(dy, dx)) 
                    
                    if angle_horizontal < 0:
                        angle_horizontal += 360

                    angles_between_drone_to_att.append(angle_horizontal)

                    dz = z_attacker - myLocation.z
                    distance_horizontal = math.sqrt(dx**2 + dy**2)  # horizontal distance
                    angle_vertical = math.degrees(math.atan2(dz, distance_horizontal)) # vertical angle

                    angles_vertical_between_drone_to_att.append(angle_vertical)

                    time_required = distance / my_speed_mps
                    time_for_att.append(time_required)

                    time_attacker_reaches_point = int(row['time'])
                    remaining_time = time_attacker_reaches_point - indication_time_seconds
                    if time_required <= remaining_time:
                        can_reach.append(True)
                    else:
                        can_reach.append(False)

            with open('results.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['time', 'distance', 'angle_horizontal', 'angle_vertical', 'time_required', 'remaining_time', 'can_reach'])

                time_seconds = 0
                for distance, angle_horizontal, angle_vertical, time_required, reach in zip(distances_between_att_drone, angles_between_drone_to_att, angles_vertical_between_drone_to_att, time_for_att, can_reach):
                    time_attacker_reaches_point = time_seconds
                    remaining_time = time_attacker_reaches_point - indication_time_seconds
                    reach = time_required <= remaining_time
                    writer.writerow([time_seconds, distance, angle_horizontal, angle_vertical, time_required, remaining_time, reach])
                    time_seconds += 1

            time.sleep(1)

    results_thread = threading.Thread(target=update_reach_status)
    results_thread.daemon = True
    results_thread.start()

    print("results.csv created successfully and will be updated in real-time.")
    result_label.config(text="Calculations complete, results.csv created and updated in real-time.")
    display_possible_solutions()
    display_results()

def display_possible_solutions():
    possible_solutions = []
    with open('results.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['can_reach'] == 'True' and int(row['remaining_time']) >= 10:
                possible_solutions.append(row)

    if len(possible_solutions) == 0:
        solutions_label.config(text="No solutions can reach the attacker in time.")
    else:
        solutions_text = "Possible solutions (10 with at least 10 seconds remaining):\n"
        for solution in possible_solutions[:10]:
            solutions_text += f"Time: {solution['time']}, Distance: {solution['distance']}, Angle degrees: {solution['angle_horizontal']}, Angle Vertical: {solution['angle_vertical']}, Time Required: {solution['time_required']}, Remaining Time: {solution['remaining_time']}\n"
        print(solutions_text)
        solutions_label.config(text=solutions_text)

def display_results():
    results_window = tk.Toplevel(app)
    results_window.title("Results")
    results_window.geometry("800x600")

    results_text = tk.Text(results_window, font=("Segoe UI", 12))
    results_text.pack(expand=True, fill='both')

    def update_results_text():
        while True:
            if not results_text.winfo_exists():
                break
            try:
                results_text.config(state='normal')
                results_text.delete('1.0', tk.END)
                with open('results.csv', mode='r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if int(row['remaining_time']) >= 10:
                            results_text.insert('end', f"Time: {row['time']}, Distance: {row['distance']}, Angle Horizontal: {row['angle_horizontal']}, Angle Vertical: {row['angle_vertical']}, Time Required: {row['time_required']}, Remaining Time: {row['remaining_time']}\n", 'bold')
                        else:
                            results_text.insert('end', f"Time: {row['time']}, Distance: {row['distance']}, Angle Horizontal: {row['angle_horizontal']}, Angle Vertical: {row['angle_vertical']}, Time Required: {row['time_required']}, Remaining Time: {row['remaining_time']}\n")
                results_text.config(state='disabled')
            except tk.TclError:
                break
            time.sleep(1)

    results_text_thread = threading.Thread(target=update_results_text)
    results_text_thread.daemon = True
    results_text_thread.start()

    scroll = tk.Scrollbar(results_window, command=results_text.yview)
    scroll.pack(side='right', fill='y')
    results_text.config(yscrollcommand=scroll.set)

    results_window.mainloop()

app = tk.Tk()
app.title("Attacker Tracker")
app.geometry("800x600")
app.configure(bg='#f0f0f0')

style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 12), background='#f0f0f0')
style.configure("TEntry", font=("Segoe UI", 12))
style.configure("TButton", font=("Segoe UI", 12, "bold"), foreground='#ffffff', background='#0078d7')

# Attacker Frame
attacker_frame = tk.LabelFrame(app, text="Attacker", bg='#0078d7', fg='#ffffff', font=("Segoe UI", 14, "bold"), bd=5)
attacker_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.35, anchor='n')

miz_label = ttk.Label(attacker_frame, text="Attacker's Miz:")
miz_label.grid(row=0, column=0, padx=10, pady=5, sticky='e')
miz_entry = ttk.Entry(attacker_frame)
miz_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

north_label = ttk.Label(attacker_frame, text="Attacker's North:")
north_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')
north_entry = ttk.Entry(attacker_frame)
north_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

direction_label = ttk.Label(attacker_frame, text="Direction (in degrees):")
direction_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
direction_entry = ttk.Entry(attacker_frame)
direction_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

attacker_height_label = ttk.Label(attacker_frame, text="Attacker's Height:")
attacker_height_label.grid(row=3, column=0, padx=10, pady=5, sticky='e')
attacker_height_entry = ttk.Entry(attacker_frame)
attacker_height_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')

# Drone Frame
drone_frame = tk.LabelFrame(app, text="Drone", bg='#0078d7', fg='#ffffff', font=("Segoe UI", 14, "bold"), bd=5)
drone_frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.35, anchor='n')

x_location_label = ttk.Label(drone_frame, text="Your x location:")
x_location_label.grid(row=0, column=0, padx=10, pady=5, sticky='e')
x_location_entry = ttk.Entry(drone_frame)
x_location_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

y_location_label = ttk.Label(drone_frame, text="Your y location:")
y_location_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')
y_location_entry = ttk.Entry(drone_frame)
y_location_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

height_label = ttk.Label(drone_frame, text="Your height location:")
height_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
height_entry = ttk.Entry(drone_frame)
height_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

start_button = ttk.Button(app, text="Start Calculations", command=start_calculations)
start_button.place(relx=0.5, rely=0.9, anchor='center')

result_label = ttk.Label(app, text="", background='#f0f0f0', font=("Segoe UI", 12, "bold"))
result_label.place(relx=0.5, rely=0.95, anchor='center')

solutions_label = ttk.Label(app, text="", background='#f0f0f0', font=("Segoe UI", 12))
solutions_label.place(relx=0.5, rely=1, anchor='center')

app.mainloop()

