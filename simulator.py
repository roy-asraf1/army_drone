import csv
import math
import threading
import time
import tkinter as tk
from tkinter import ttk
import random
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

def update_time_since_indication():
    global indication_time_seconds
    while True:
        indication_time_seconds += 1
        time.sleep(1)

def start_calculations():
    try:
        x = float(miz_entry.get())
        y = float(north_entry.get())
        direction = float(direction_entry.get())
    except ValueError:
        result_label.config(text="Invalid input. Please enter numeric values.")
        return

    if x < MINIMUM or x > MAXIMUM or y < MINIMUM or y > MAXIMUM or direction < 0 or direction > 360:
        result_label.config(text="There was an error, please try again.")
        return

    z = 1500
    first_location = Location(x, y, z)
    direction_rad = math.radians(direction)
    indication = Indication(first_location, direction)
    attacker = Attacker(indication)  # Attacker object

    with open('road.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'x', 'y', 'height'])

        time_seconds = 0
        current_x = x
        current_y = y

        for _ in range(attacker.duration_seconds):
            current_x += attacker.speed_mps * math.cos(direction_rad)
            current_y += attacker.speed_mps * math.sin(direction_rad)
            current_z = attacker.height
            writer.writerow([time_seconds, current_x, current_y, current_z])
            time_seconds += 1

    print("road.csv created successfully :)")

    # Start the thread to update the time since indication
    time_thread = threading.Thread(target=update_time_since_indication)
    time_thread.daemon = True
    time_thread.start()

    try:
        x_myLocation = float(x_location_entry.get())
        y_myLocation = float(y_location_entry.get())
        height = float(height_entry.get())
    except ValueError:
        result_label.config(text="Invalid input. Please enter numeric values.")
        return

    myLocation = Location(x_myLocation, y_myLocation, height)
    myDrone = drone.drone(myLocation)

    distances_between_att_drone = []
    angles_between_drone_to_att = []
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
            angle = math.degrees(math.atan2(dy, dx))
            
            if angle < 0:
                angle += 360
                
            angles_between_drone_to_att.append(angle)

            time_required = distance / my_speed_mps
            time_for_att.append(time_required)

            remaining_time = max_time_seconds - indication_time_seconds
            if time_required <= remaining_time:
                can_reach.append(True)
            else:
                can_reach.append(False)

    print("Distances, angles, and time_for_att calculated successfully.")

    # Continuously check remaining time and update the results file
    def update_results():
        while True:
            with open('results.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['time', 'distance', 'angle', 'time_required', 'remaining_time', 'can_reach'])

                time_seconds = 0
                for distance, angle, time_required, reach in zip(distances_between_att_drone, angles_between_drone_to_att, time_for_att, can_reach):
                    remaining_time = max_time_seconds - indication_time_seconds
                    reach = time_required <= remaining_time
                    writer.writerow([time_seconds, distance, angle, time_required, remaining_time, reach])
                    time_seconds += 1

            time.sleep(1)

    results_thread = threading.Thread(target=update_results)
    results_thread.daemon = True
    results_thread.start()

    print("results.csv created successfully and will be updated in real-time.")
    result_label.config(text="Calculations complete, results.csv created and updated in real-time.")

    # Display 10 random possible solutions
    def display_possible_solutions():
        possible_solutions = [i for i, reach in enumerate(can_reach) if reach]
        if len(possible_solutions) == 0:
            solutions_label.config(text="No solutions can reach the attacker in time.")
        else:
            random_solutions = random.sample(possible_solutions, min(10, len(possible_solutions)))
            solutions_text = "Possible solutions (random 10):\n"
            with open('results.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for i, row in enumerate(reader):
                    if i in random_solutions:
                        solutions_text += f"Time: {row['time']}, Distance: {row['distance']}, Angle: {row['angle']}, Time Required: {row['time_required']}, Remaining Time: {row['remaining_time']}\n"
            solutions_label.config(text=solutions_text)

    display_possible_solutions()

    display_results()

def display_results():
    results_window = tk.Toplevel(app)
    results_window.title("Results")
    results_window.geometry("800x600")

    results_text = tk.Text(results_window, font=("Segoe UI", 12))
    results_text.pack(expand=True, fill='both')

    def update_results_text():
        while True:
            results_text.config(state='normal')
            results_text.delete('1.0', tk.END)
            with open('results.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if int(row['remaining_time']) >= 20:
                        results_text.insert('end', f"Time: {row['time']}, Distance: {row['distance']}, Angle: {row['angle']}, Time Required: {row['time_required']}, Remaining Time: {row['remaining_time']}\n", 'bold')
                    else:
                        results_text.insert('end', f"Time: {row['time']}, Distance: {row['distance']}, Angle: {row['angle']}, Time Required: {row['time_required']}, Remaining Time: {row['remaining_time']}\n")
            results_text.config(state='disabled')
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

frame = tk.Frame(app, bg='#0078d7', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.7, anchor='n')

miz_label = ttk.Label(frame, text="Attacker's Miz:")
miz_label.grid(row=0, column=0, padx=10, pady=5, sticky='e')
miz_entry = ttk.Entry(frame)
miz_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

north_label = ttk.Label(frame, text="Attacker's North:")
north_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')
north_entry = ttk.Entry(frame)
north_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

direction_label = ttk.Label(frame, text="Direction (in degrees):")
direction_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
direction_entry = ttk.Entry(frame)
direction_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')



x_location_label = ttk.Label(frame, text="Your x location:")
x_location_label.grid(row=3, column=0, padx=10, pady=5, sticky='e')
x_location_entry = ttk.Entry(frame)
x_location_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')

y_location_label = ttk.Label(frame, text="Your y location:")
y_location_label.grid(row=4, column=0, padx=10, pady=5, sticky='e')
y_location_entry = ttk.Entry(frame)
y_location_entry.grid(row=4, column=1, padx=10, pady=5, sticky='w')

height_label = ttk.Label(frame, text="Your height location:")
height_label.grid(row=5, column=0, padx=10, pady=5, sticky='e')
height_entry = ttk.Entry(frame)
height_entry.grid(row=5, column=1, padx=10, pady=5, sticky='w')

start_button = ttk.Button(app, text="Start Calculations", command=start_calculations)
start_button.place(relx=0.5, rely=0.8, anchor='center')

result_label = ttk.Label(app, text="", background='#f0f0f0', font=("Segoe UI", 12, "bold"))
result_label.place(relx=0.5, rely=0.9, anchor='center')

solutions_label = ttk.Label(app, text="", background='#f0f0f0', font=("Segoe UI", 12))
solutions_label.place(relx=0.5, rely=0.95, anchor='center')

app.mainloop()
