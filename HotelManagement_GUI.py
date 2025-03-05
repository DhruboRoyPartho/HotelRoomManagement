"""
Code Author: Dhrubo Roy Partho
Project: Hotel Management
Date: 06-03-2025
Version: 1.0v
"""

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

class Room:
    def __init__(self, room_no, room_type, price, status):
        self.room_no = room_no
        self.room_type = room_type
        self.price = price
        self.status = status
    
    # Get properties
    def getRoomNo(self):
        return self.room_no
    
    def getRoomType(self):
        return self.room_type
    
    def getPrice(self):
        return self.price
    
    def getStatus(self):
        return self.status
    
    # Set properties
    def setRoomNo(self, room_no):
        self.room_no = room_no
    
    def setRoomType(self, room_type):
        self.room_type = room_type
    
    def setPrice(self, price):
        self.price = price
    
    def setStatus(self, status):
        self.status = status


class Hotel:
    def __init__(self):
        self.rooms = []
    
    def searchRoom(self, room_no):
        for room in self.rooms:
            if room.getRoomNo() == room_no:
                return room
        return None
    
    def addRoom(self, room):
        if self.searchRoom(room.getRoomNo()):
            return False
        else:
            self.rooms.append(room)
            return True
        
    def deleteRoom(self, room_no):
        room = self.searchRoom(room_no)
        if room:
            self.rooms.remove(room)
            return True
        else:
            return False


class Manager:
    def __init__(self, root):
        self.hotel = Hotel()
        self.root = root
        self.root.title("Hotel Room Management System")
        self.root.geometry("800x600")

        # CSV file for data storage
        self.csv_file = "hotel_data.csv"
        self.load_data()  # Load data from CSV at startup

        # Title Label
        self.title_label = tk.Label(root, text="Hotel Room Management System", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)

        # Treeview to display rooms
        self.tree = ttk.Treeview(root, columns=("Room No", "Type", "Price", "Status"), show="headings")
        self.tree.heading("Room No", text="Room No")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons for actions
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add Room", command=self.addRoom, width=15)
        self.add_button.grid(row=0, column=0, padx=5)

        self.book_button = tk.Button(self.button_frame, text="Book Room", command=self.bookRoom, width=15)
        self.book_button.grid(row=0, column=1, padx=5)

        self.check_out_button = tk.Button(self.button_frame, text="Check Out", command=self.checkout, width=15)
        self.check_out_button.grid(row=0, column=2, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Room", command=self.deleteRoom, width=15)
        self.delete_button.grid(row=0, column=3, padx=5)

        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.exit, width=15)
        self.exit_button.grid(row=0, column=4, padx=5)

        # Initialize Treeview with loaded data
        self.update_treeview()

    # Update Treeview
    def update_treeview(self):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Insert new data
        for room in self.hotel.rooms:
            self.tree.insert("", tk.END, values=(
                room.getRoomNo(),
                room.getRoomType(),
                f"{room.getPrice()} BDT",  # Display price with BDT
                room.getStatus()
            ))

    # Add Room
    def addRoom(self):
        def save_room():
            room_no = room_no_entry.get()
            room_type = room_type_combobox.get()
            price = price_entry.get()
            status = status_combobox.get()

            # Validate inputs
            if not room_no or not room_type or not price or not status:
                messagebox.showwarning("Input Error", "Please fill all fields.")
                return
            
            try:
                price = float(price)  # Convert price to float
                if price <= 0:
                    messagebox.showwarning("Input Error", "Price must be greater than 0.")
                    return
            except ValueError:
                messagebox.showwarning("Input Error", "Price must be a valid number.")
                return

            # Checking if room already exists
            if self.hotel.searchRoom(room_no):
                messagebox.showwarning("Input Error", f"Room {room_no} already exists.")
                return

            # Adding room to hotel
            new_room = Room(room_no, room_type, price, status)
            self.hotel.addRoom(new_room)
            self.update_treeview()
            self.save_data()  # Save data to CSV
            add_window.destroy()

        # Create add room window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Room")
        add_window.geometry("300x200")

        tk.Label(add_window, text="Room No:").grid(row=0, column=0, padx=10, pady=5)
        room_no_entry = tk.Entry(add_window)
        room_no_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Type:").grid(row=1, column=0, padx=10, pady=5)
        room_type_combobox = ttk.Combobox(add_window, values=["Single", "Double", "Suite"], state="readonly")
        room_type_combobox.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Price:").grid(row=2, column=0, padx=10, pady=5)
        price_entry = tk.Entry(add_window)
        price_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Status:").grid(row=3, column=0, padx=10, pady=5)
        status_combobox = ttk.Combobox(add_window, values=["Available", "Booked"], state="readonly")
        status_combobox.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(add_window, text="Save", command=save_room).grid(row=4, column=0, columnspan=2, pady=10)

    # Room Booking
    def bookRoom(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a room to book.")
            return

        room_no = self.tree.item(selected_item, "values")[0]
        room = self.hotel.searchRoom(room_no)
        if room:
            if room.getStatus() == "Available":
                room.setStatus("Booked")
                self.update_treeview()
                self.save_data()  # Save data to CSV
                messagebox.showinfo("Success", f"Room {room_no} has been booked.")
            else:
                messagebox.showwarning("Booking Error", f"Room {room_no} is already booked.")
        else:
            messagebox.showwarning("Error", f"Room {room_no} not found.")

    # Check Out
    def checkout(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a room to check out.")
            return

        room_no = self.tree.item(selected_item, "values")[0]
        room = self.hotel.searchRoom(room_no)
        if room:
            if room.getStatus() == "Booked":
                room.setStatus("Available")
                self.update_treeview()
                self.save_data()  # Save data to CSV
                messagebox.showinfo("Success", f"Room {room_no} has been checked out.")
            else:
                messagebox.showwarning("Check Out Error", f"Room {room_no} is not booked.")
        else:
            messagebox.showwarning("Error", f"Room {room_no} not found.")

    # Delete Room
    def deleteRoom(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a room to delete.")
            return

        room_no = self.tree.item(selected_item, "values")[0]
        if self.hotel.deleteRoom(room_no):
            self.update_treeview()
            self.save_data()  # Save data to CSV
            messagebox.showinfo("Success", f"Room {room_no} has been deleted.")
        else:
            messagebox.showwarning("Error", f"Room {room_no} not found.")

    # Save data to CSV
    def save_data(self):
        with open(self.csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Room No", "Type", "Price", "Status"])  # Write header
            for room in self.hotel.rooms:
                writer.writerow([room.getRoomNo(), room.getRoomType(), room.getPrice(), room.getStatus()])

    # Load data from CSV
    def load_data(self):
        if os.path.exists(self.csv_file):
            with open(self.csv_file, mode="r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    room_no, room_type, price, status = row
                    self.hotel.addRoom(Room(room_no, room_type, float(price), status))

    # Exit
    def exit(self):
        self.save_data()  # Save data before exiting
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = Manager(root)
    root.mainloop()