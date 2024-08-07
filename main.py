import json
import tkinter as tk
from tkinter import messagebox, ttk



class LoginGUI:
    def __init__(self, data, root):
        self.root = root
        self.data = data
        self.root.title("Login GUI")
        self.root.geometry("300x600")
        self.current_user = "CUserHolder"

        self.create_widgets()

    def create_widgets(self):
        # username label and entry
        self.username_label = tk.Label(self.root, text="Username")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        # password label and entry
        self.password_label = tk.Label(self.root, text="Password")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        # login button
        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack(pady=20)

    def login(self):
        inputUsername = self.username_entry.get()
        inputPassword = self.password_entry.get()

        for user in self.data["allUser"]:
            if user['username'] == inputUsername and user['password'] == inputPassword:
                self.current_user = inputUsername
                if not user['isEmployee']:
                    self.open_renter_GUI()
                else:
                    self.open_employee_GUI()
                return
        return messagebox.showerror("Login", "Invalid Credentials")

    def open_renter_GUI(self):
        current_user = self.current_user
        self.root.destroy() 

        with open('cars.json', 'r') as f:
            data = json.load(f)

        root = tk.Tk()
        app = renterGUI(root, current_user)
        root.mainloop()

    def open_employee_GUI(self):
        current_user = self.current_user
        self.root.destroy() 
    
        with open('cars.json', 'r') as f:
            data = json.load(f)
    
        root = tk.Tk()
        app = employeeGUI(root, current_user)
        root.mainloop()





class renterGUI:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("logged in as : {}".format(current_user))
        self.root.geometry("300x600")
        
        self.create_widgets()

    def create_widgets(self):

        # rent button
        self.login_button = tk.Button(self.root, text="rent a car", command=self.open_car_rental_GUI)
        self.login_button.pack(pady=20)

        # return button
        self.login_button = tk.Button(self.root, text="return a car", command=self.open_car_return_GUI)
        self.login_button.pack(pady=20)

    def open_car_rental_GUI(self):
        current_user = self.current_user
        self.root.destroy() 

        with open('cars.json', 'r') as f:
            data = json.load(f)
            
        root = tk.Tk()
        app = CarRentalGUI(root, data, current_user)
        root.mainloop()
        
    def open_car_return_GUI(self):
        current_user = self.current_user
        self.root.destroy() 

        with open('cars.json', 'r') as f:
            data = json.load(f)

        root = tk.Tk()
        app = CarReturnGUI(root, data, current_user)
        root.mainloop()




class CarRentalGUI:
        def __init__(self, root, data, current_user):
            self.root = root
            self.data = data
            self.current_user = current_user
            self.root.title("Car Rental Service")

            # Create and configure the frame
            self.frame = ttk.Frame(self.root)
            self.frame.pack(fill=tk.BOTH, expand=True)

            # Create and configure the treeview
            self.tree = ttk.Treeview(self.frame, columns=("carName", "carAge", "pricePerMonth"), show="headings")
            self.tree.heading("carName", text="Car Name")
            self.tree.heading("carAge", text="Car Age")
            self.tree.heading("pricePerMonth", text="Price Per Month")
            self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

            # Add the available cars to the table
            self.populate_table()

            # Create and configure the scrollbar
            self.vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
            self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
            self.tree.configure(yscrollcommand=self.vsb.set)

            self.tree.pack(fill=tk.BOTH, expand=True)

            # Rent the Car button
            self.rent_button = tk.Button(self.root, text="Rent the Car", command=self.rent_car)
            self.rent_button.pack(pady=10)
            self.rent_button.pack_forget()  # Initially hide the button

        def populate_table(self):
            for car in self.data['cars']:
                if not car['rented'] and car['requestedForRent'] == "":
                    self.tree.insert("", tk.END, values=(car["carName"], car["carAge"], car["pricePerMonth"]))

        def on_tree_select(self, event):
            selected_item = self.tree.selection()
            if selected_item:
                self.selected_car = self.tree.item(selected_item)["values"][0]
                self.rent_button.pack()  # Show the button when a car is selected

        def rent_car(self):
            for car in self.data['cars']:
                if car["carName"] == self.selected_car:
                    car["requestedForRent"] = self.current_user
                    break
            with open('cars.json', 'w') as f:
                json.dump(self.data, f, indent=4)
            messagebox.showinfo("Success", f"You have requested to rent {self.selected_car}.")
            self.tree.delete(*self.tree.get_children())
            self.populate_table()
            self.rent_button.pack_forget()  # Hide the button after renting the car





class CarReturnGUI:
    def __init__(self, root, data, current_user):
        self.root = root
        self.data = data
        self.current_user = current_user
        self.root.title("Car Return Service")

        # Create and configure the frame
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create and configure the treeview
        self.tree = ttk.Treeview(self.frame, columns=("carName", "carAge", "pricePerMonth"), show="headings")
        self.tree.heading("carName", text="Car Name")
        self.tree.heading("carAge", text="Car Age")
        self.tree.heading("pricePerMonth", text="Price Per Month")
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Add the rented cars to the table
        self.populate_table()

        # Create and configure the scrollbar
        self.vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.vsb.set)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Return the Car button
        self.return_button = tk.Button(self.root, text="Return the Car", command=self.return_car)
        self.return_button.pack(pady=10)
        self.return_button.pack_forget()  # Initially hide the button

    def populate_table(self):
        for car in self.data['cars']:
            if car['rented'] and car['renter'] == self.current_user:
                self.tree.insert("", tk.END, values=(car["carName"], car["carAge"], car["pricePerMonth"]))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_car = self.tree.item(selected_item)["values"][0]
            self.return_button.pack()  # Show the button when a car is selected

    def return_car(self):
        for car in self.data['cars']:
            if car["carName"] == self.selected_car:
                car["rented"] = False
                car["renter"] = ""
                car["requestedForRent"] = ""
                break
        with open('cars.json', 'w') as f:
            json.dump(self.data, f, indent=4)
        messagebox.showinfo("Success", f"You have returned {self.selected_car}.")
        self.tree.delete(*self.tree.get_children())
        self.populate_table()
        self.return_button.pack_forget()  # Hide the button after returning the car




class employeeGUI:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("logged in as : {}".format(current_user))
        self.root.geometry("300x600")

        self.create_widgets()

    def create_widgets(self):

        # rent button
        self.login_button = tk.Button(self.root, text="edit database", command=self.open_edit_DB_GUI)
        self.login_button.pack(pady=20)

        # return button
        self.login_button = tk.Button(self.root, text="accept/reject request", command=self.open_car_return_GUI)
        self.login_button.pack(pady=20)

    def open_edit_DB_GUI(self):
        current_user = self.current_user
        self.root.destroy() 

        with open('cars.json', 'r') as f:
            data = json.load(f)

        root = tk.Tk()
        app = editDBGUI(root, data, current_user)
        root.mainloop()

    def open_car_return_GUI(self):
        current_user = self.current_user
        self.root.destroy() 

        with open('cars.json', 'r') as f:
            data = json.load(f)

        root = tk.Tk()
        app = CarReturnGUI(root, data, current_user)
        root.mainloop()






class editDBGUI:
    def __init__(self, root, data, current_user):
        self.root = root
        self.data = data
        self.current_user = current_user
        self.root.title("Car Return Service")

        # Create and configure the frame
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create and configure the treeview
        self.tree = ttk.Treeview(self.frame, columns=("carName", "carAge", "pricePerMonth"), show="headings")
        self.tree.heading("carName", text="Car Name")
        self.tree.heading("carAge", text="Car Age")
        self.tree.heading("pricePerMonth", text="Price Per Month")
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Add the rented cars to the table
        self.populate_table()

        # Create and configure the scrollbar
        self.vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.vsb.set)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Add New Car button

        self.return_button = tk.Button(self.root, text="Add New", command=self.return_car)
        self.return_button.pack(pady=10)
        
        # Delete the Car button
        self.return_button = tk.Button(self.root, text="Delete", command=self.return_car)
        self.return_button.pack(pady=10)
        self.return_button.pack_forget()  # Initially hide the button

        # Edit the Car button
        self.return_button = tk.Button(self.root, text="Edit Information", command=self.return_car)
        self.return_button.pack(pady=10)
        self.return_button.pack_forget()  # Initially hide the button

    def populate_table(self):
        for car in self.data['cars']:
            self.tree.insert("", tk.END, values=(car["carName"], car["carAge"], car["pricePerMonth"]))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_car = self.tree.item(selected_item)["values"][0]
            self.return_button.pack()  # Show the button when a car is selected





if __name__ == "__main__":
    
    with open('user.json', 'r') as users:
        UserData = json.load(users)
        
    root = tk.Tk()
    app = LoginGUI(UserData, root)
    root.mainloop()


