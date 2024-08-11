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

        # register button
        self.register_button = tk.Button(self.root, text="Register", command=self.open_register_gui)
        self.register_button.pack(pady=10)

        #shortcut used for test, delete them later
        self.btn1 = tk.Button(self.root, text="Test_renter", command=self.SC_R)
        self.btn1.pack(pady=20)
        self.btn2 = tk.Button(self.root, text="Test_employee", command=self.SC_E)
        self.btn2.pack(pady=20)

    def open_register_gui(self):
        self.root.destroy()
        root = tk.Tk()
        app = RegisterGUI(self.data, root)
        root.mainloop()

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
        app = renterGUI(data, root, current_user)
        root.mainloop()

    def open_employee_GUI(self):
        current_user = self.current_user
        self.root.destroy() 
    
        with open('cars.json', 'r') as f:
            data = json.load(f)
    
        root = tk.Tk()
        app = employeeGUI(data, root, current_user)
        root.mainloop()

    #delete the below later
    def SC_R(self):
        self.current_user = "renter"
        self.open_renter_GUI()

    def SC_E(self):
        self.current_user = "employee"
        self.open_employee_GUI()

class RegisterGUI:
    def __init__(self, data, root):
        self.root = root
        self.data = data
        self.root.title("Register")
        self.root.geometry("300x300")

        self.create_widgets()

    def create_widgets(self):
        # Username label and entry
        self.username_label = tk.Label(self.root, text="Username")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        # Password label and entry
        self.password_label = tk.Label(self.root, text="Password")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        # User type selection
        self.user_type = tk.StringVar(value="renter")
        self.renter_radio = tk.Radiobutton(self.root, text="Renter", variable=self.user_type, value="renter")
        self.renter_radio.pack()
        self.employee_radio = tk.Radiobutton(self.root, text="Employee", variable=self.user_type, value="employee")
        self.employee_radio.pack()

        # Register button
        self.register_button = tk.Button(self.root, text="Register", command=self.register)
        self.register_button.pack(pady=20)

        # Back to Login button
        self.back_button = tk.Button(self.root, text="Back to Login", command=self.back_to_login)
        self.back_button.pack(pady=10)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        is_employee = self.user_type.get() == "employee"

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return

        new_user = {
            "username": username,
            "password": password,
            "isEmployee": is_employee
        }

        self.data["allUser"].append(new_user)

        with open('user.json', 'w') as f:
            json.dump(self.data, f, indent=2)

        messagebox.showinfo("Success", "User registered successfully")
        self.back_to_login()

    def back_to_login(self):
        self.root.destroy()
        root = tk.Tk()
        app = LoginGUI(self.data, root)
        root.mainloop()

class renterGUI:
    def __init__(self, data, root, current_user):
        self.root = root
        self.current_user = current_user
        self.data = data
        self.root.title("logged in as : {}".format(current_user))
        self.root.geometry("300x600")
        
        self.create_widgets()

    def create_widgets(self):

        # rent button
        self.login_button = tk.Button(self.root, text="Rent a car", command=self.open_car_rental_GUI)
        self.login_button.pack(pady=20)

        # return button
        self.login_button = tk.Button(self.root, text="Return a car", command=self.open_car_return_GUI)
        self.login_button.pack(pady=20)

        # logout button
        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        self.logout_button.pack(pady=20)

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        with open('user.json', 'r') as users:
            UserData = json.load(users)
        app = LoginGUI(UserData, root)
        root.mainloop()

    def open_car_rental_GUI(self):
        current_user = self.current_user
        data = self.data
        self.root.destroy() 
            
        root = tk.Tk()
        app = CarRentalGUI(data, root, current_user)
        root.mainloop()
        
    def open_car_return_GUI(self):
        current_user = self.current_user
        data = self.data
        self.root.destroy() 

        root = tk.Tk()
        app = CarReturnGUI(data, root, current_user)
        root.mainloop()

class CarRentalGUI:
    def __init__(self, data, root, current_user):
        self.root = root
        self.data = data
        self.current_user = current_user
        self.root.title("Car Rental Service")

        # Create and configure the frame
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create and configure the treeview
        self.tree = ttk.Treeview(self.frame, columns=("id", "carName", "carAge", "pricePerMonth"), show="headings")
        self.tree.heading("carName", text="Car Name")
        self.tree.heading("carAge", text="Car Age")
        self.tree.heading("pricePerMonth", text="Price Per Month")
        self.tree.column("id", width=0, stretch=tk.NO)
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

        # Back button
        self.back_button = tk.Button(self.root, text="Back", command=self.back_to_renter_gui)
        self.back_button.pack(pady=10)

    def back_to_renter_gui(self):
        self.root.destroy()
        root = tk.Tk()
        app = renterGUI(self.data, root, self.current_user)
        root.mainloop()

    def populate_table(self):
        for car in self.data['cars']:
            if not car['rented'] and car['requestedForRent'] == "":
                self.tree.insert("", tk.END, values=(car["id"], car["carName"], car["carAge"], car["pricePerMonth"]))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_car = self.tree.item(selected_item)["values"][0]
            print(self.selected_car)
            self.rent_button.pack()  # Show the button when a car is selected

    def rent_car(self):
        for car in self.data['cars']:
            if car["id"] == self.selected_car:
                car["requestedForRent"] = self.current_user
                break
        with open('cars.json', 'w') as f:
            json.dump(self.data, f, indent=4)
        messagebox.showinfo("Success", f"You have requested to rent {self.selected_car}.")
        self.tree.delete(*self.tree.get_children())
        self.populate_table()
        self.rent_button.pack_forget()  # Hide the button after renting the car

class CarReturnGUI:
    def __init__(self, data, root, current_user):
        self.root = root
        self.data = data
        self.current_user = current_user
        self.root.title("Car Return Service")

        # Create and configure the frame
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create and configure the treeview
        self.tree = ttk.Treeview(self.frame, columns=("id", "carName", "carAge", "pricePerMonth"), show="headings")
        self.tree.heading("carName", text="Car Name")
        self.tree.heading("carAge", text="Car Age")
        self.tree.heading("pricePerMonth", text="Price Per Month")
        self.tree.column("id", width=0, stretch=tk.NO)
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

        # Back button
        self.back_button = tk.Button(self.root, text="Back", command=self.back_to_renter_gui)
        self.back_button.pack(pady=10)

    def back_to_renter_gui(self):
        self.root.destroy()
        root = tk.Tk()
        app = renterGUI(self.data, root, self.current_user)
        root.mainloop()

    def populate_table(self):
        for car in self.data['cars']:
            if car['rented'] and car['renter'] == self.current_user:
                self.tree.insert("", tk.END, values=(car["id"], car["carName"], car["carAge"], car["pricePerMonth"]))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_car = self.tree.item(selected_item)["values"][0]
            self.return_button.pack()  # Show the button when a car is selected

    def return_car(self):
        for car in self.data['cars']:
            if car["id"] == self.selected_car:
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
    def __init__(self, data, root, current_user):
        self.root = root
        self.current_user = current_user
        self.data = data
        self.root.title("logged in as : {}".format(current_user))
        self.root.geometry("300x600")

        self.create_widgets()

    def create_widgets(self):

        # rent button
        self.editDB_button = tk.Button(self.root, text="Edit database", command=self.open_edit_DB_GUI)
        self.editDB_button.pack(pady=20)

        # return button
        self.decision_button = tk.Button(self.root, text="Accept/reject request", command=self.open_decision_GUI)
        self.decision_button.pack(pady=20)

        # logout button
        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        self.logout_button.pack(pady=20)

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        with open('user.json', 'r') as users:
            UserData = json.load(users)
        app = LoginGUI(UserData, root)
        root.mainloop()

    def open_edit_DB_GUI(self):
        current_user = self.current_user
        data = self.data
        self.root.destroy() 

        root = tk.Tk()
        app = editDBGUI(data, root, current_user)
        root.mainloop()

    def open_decision_GUI(self):
        current_user = self.current_user
        data = self.data
        self.root.destroy() 

        root = tk.Tk()
        app = DecisionGUI(data, root, current_user)
        root.mainloop()

class editDBGUI:
    def __init__(self, data, root, current_user):
        self.root = root
        self.data = data
        self.current_user = current_user
        self.root.title("Car Return Service")

        # Create and configure the frame
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create and configure the treeview
        self.tree = ttk.Treeview(self.frame, columns=("id", "carName", "carAge", "pricePerMonth"), show="headings")
        self.tree.heading("carName", text="Car Name")
        self.tree.heading("carAge", text="Car Age")
        self.tree.heading("pricePerMonth", text="Price Per Month")
        self.tree.column("id", width=0, stretch=tk.NO)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Add the rented cars to the table
        self.populate_table()

        # Create and configure the scrollbar
        self.vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.vsb.set)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Add New Car button
        self.ADN_button = tk.Button(self.root, text="Add New", command=self.Open_add_new_GUI)
        self.ADN_button.pack(pady=10)

        # Delete the Car button
        self.EC_button = tk.Button(self.root, text="Edit Information", command=self.Open_edit_current_GUI)
        self.EC_button.pack(pady=10)
        self.EC_button.pack_forget()  # Initially hide the button

        # Edit the Car button
        self.Del_button = tk.Button(self.root, text="Delete", command=self.Delete_current)
        self.Del_button.pack(pady=10)
        self.Del_button.pack_forget()  # Initially hide the button

        # Back Button
        self.back_button = tk.Button(self.root, text="Back", command=self.back_to_employee_gui)
        self.back_button.pack(pady=10)

    def back_to_employee_gui(self):
        self.root.destroy()
        root = tk.Tk()
        app = employeeGUI(self.data, root, self.current_user)
        root.mainloop()

    def populate_table(self):
        for car in self.data['cars']:   
             self.tree.insert("", tk.END, values=(car["id"], car["carName"], car["carAge"], car["pricePerMonth"]))

    def refresh_table(self, event=None):
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Reload data
        with open('cars.json', 'r') as f:
            self.data = json.load(f)
        print("car list refreshed")
        self.populate_table()

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_car = self.tree.item(selected_item)["values"][0]
            self.Del_button.pack()
            self.EC_button.pack()  # Show the button when a car is selected

    def Open_add_new_GUI(self):
        current_user = self.current_user
        data = self.data

        new_root = tk.Toplevel(self.root)
        new_root.bind("<Destroy>", self.refresh_table)
        app = addOrEditGUI(data, new_root, current_user, False, len(self.data['cars'])+1, "", 0, 0)
        new_root.mainloop()

    def Open_edit_current_GUI(self):
        current_user = self.current_user
        data = self.data

        for car in self.data['cars']:
            if car["id"] == self.selected_car:
                self.carID = car["id"]
                self.carName = car["carName"]
                self.carAge = car["carAge"]
                self.PPM = car["pricePerMonth"]
                break

        new_root = tk.Toplevel(self.root)
        new_root.bind("<Destroy>", self.refresh_table)
        app = addOrEditGUI(data, new_root, current_user, True, self.carID, self.carName, self.carAge, self.PPM)
        new_root.mainloop()

    def Delete_current(self):
        response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?")
        if response:
            for car in self.data['cars']:
                if car["id"] == self.selected_car:
                    self.data['cars'].remove(car)
                    with open('cars.json', 'w') as f:
                        json.dump(self.data, f, indent=4) 
                    self.refresh_table()
                    break
        else:
            print("Item not deleted")

class addOrEditGUI:
    def __init__(self, data, root, current_user, isEdit, carID, carName, carAge, pricePerMonth):
        self.root = root
        self.data = data
        self.root.title("Add New")
        self.root.geometry("300x600")
        self.current_user = current_user
        self.carId = carID
        self.carNameHolder = carName
        self.carAgeHolder = carAge
        self.PPMHolder = pricePerMonth
        self.isEdit = isEdit

        if isEdit:
            self.root.title("Edit")

        self.create_widgets()

    def create_widgets(self):
        # labels and entries
        self.CarName_label = tk.Label(self.root, text="Car Name")
        self.CarName_label.pack(pady=5)
        self.CarName_entry = tk.Entry(self.root)
        self.CarName_entry.pack(pady=5)
        self.CarName_entry.insert(0, self.carNameHolder)

        self.CarAge_label = tk.Label(self.root, text="Car age")
        self.CarAge_label.pack(pady=5)
        self.CarAge_entry = tk.Entry(self.root)
        self.CarAge_entry.pack(pady=5)
        self.CarAge_entry.insert(0, str(self.carAgeHolder))

        self.PPM_label = tk.Label(self.root, text="$/Month")
        self.PPM_label.pack(pady=5)
        self.PPM_entry = tk.Entry(self.root)
        self.PPM_entry.pack(pady=5)
        self.PPM_entry.insert(0, str(self.PPMHolder))

        # Save button
        self.login_button = tk.Button(self.root, text="Save", command=self.check_value_type)
        self.login_button.pack(pady=20)

    def check_value_type(self):
        try:
            int(self.CarAge_entry.get())
            float(self.PPM_entry.get())
        except:
            return messagebox.showerror("Error", "Invalid value type. Please enter a valid value.")
        else:
            self.save_data()

    def save_data(self):
        if self.isEdit:
            for car in self.data['cars']:
                if car["id"] == self.carId:
                    car["carName"] = self.CarName_entry.get()
                    car["carAge"] = int(self.CarAge_entry.get())
                    car["pricePerMonth"] = float(self.PPM_entry.get())
                    break
        else:
            new_car = {
                "id": self.carId,
                "carName": self.CarName_entry.get(),
                "carAge": int(self.CarAge_entry.get()),
                "pricePerMonth": float(self.PPM_entry.get()),
                "rented": False,
                "renter": "",
                "requestedForRent": ""
            }
            self.data["cars"].append(new_car)
        with open('cars.json', 'w') as f:
            json.dump(self.data, f, indent=4) 
        messagebox.showinfo("Success", f"Change Saved." if self.isEdit else f"Car added successfully.")
        self.root.destroy() 

class DecisionGUI:
    def __init__(self, data, root, current_user):
        self.root = root
        self.data = data
        self.current_user = current_user
        self.root.title("Car Return Service")

        # Create and configure the frame
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create and configure the treeview
        self.tree = ttk.Treeview(self.frame, columns=("id", "carName", "carAge", "pricePerMonth", "requestor"), show="headings")
        self.tree.heading("carName", text="Car Name")
        self.tree.heading("requestor", text="Requestor")
        self.tree.column("id", width=0, stretch=tk.NO)
        self.tree.column("carAge", width=0, stretch=tk.NO)
        self.tree.column("pricePerMonth", width=0, stretch=tk.NO)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Add the rented cars to the table
        self.populate_table()

        # Create and configure the scrollbar
        self.vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.vsb.set)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Accept button
        self.Accept_button = tk.Button(self.root, text="Accept", command=self.Accept)
        self.Accept_button.pack(pady=10)
        self.Accept_button.pack_forget() 

        # Reject button
        self.Reject_button = tk.Button(self.root, text="Reject", command=self.Reject)
        self.Reject_button.pack(pady=10)
        self.Reject_button.pack_forget()  # Initially hide the button

        # Check Detail button
        self.Detail_button = tk.Button(self.root, text="Check Detail", command=self.Check_Detail)
        self.Detail_button.pack(pady=10)
        self.Detail_button.pack_forget() # Initially hide the button

        # Back Button
        self.back_button = tk.Button(self.root, text="Back", command=self.back_to_employee_gui)
        self.back_button.pack(pady=10)

    def back_to_employee_gui(self):
        self.root.destroy()
        root = tk.Tk()
        app = employeeGUI(self.data, root, self.current_user)
        root.mainloop()

    def populate_table(self):
        for car in self.data['cars']:   
            if not car["rented"] and car["requestedForRent"] != "":
             self.tree.insert("", tk.END, values=(car["id"], car["carName"], car["carAge"], car["pricePerMonth"], car["requestedForRent"]))

    def refresh_table(self, event=None):
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Reload data
        with open('cars.json', 'r') as f:
            self.data = json.load(f)
        print("car list refreshed")
        self.populate_table()

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_car = self.tree.item(selected_item)["values"][0]
            self.Accept_button.pack()
            self.Reject_button.pack()
            self.Detail_button.pack()  # Show the button when a car is selected

    def Accept(self):
        for car in self.data['cars']:
            if car["id"] == self.selected_car:
                car["renter"] = car["requestedForRent"]
                car["requestedForRent"] = ""
                car["rented"] = True
                self.Inform_renter("Congratulations!", "You have successfully rented the " + car["carName"] + ".")
                
                with open('cars.json', 'w') as f:
                    json.dump(self.data, f, indent=4) 
                self.refresh_table()
            
    def Reject(self):
        for car in self.data['cars']:
            if car["id"] == self.selected_car:
                car["requestedForRent"] = ""
                self.Inform_renter("Sorry!", "You request to rent the " + car["carName"] + " has been rejected.")
                
                with open('cars.json', 'w') as f:
                    json.dump(self.data, f, indent=4) 
                self.refresh_table()

    def Check_Detail(self):
        headers = ["Car ID","Car Name", "Car Age", "Price Per Month", "Requestor"]
        Detail_str = ""
        selected_item = self.tree.selection()
        
        if selected_item:
            item = self.tree.item(selected_item)
            values = item['values']

            # Iterate through all elements (values) in the selected item
            for index, value in enumerate(values):
                heading = headers[index]
                Detail_str += "{}: {}\n".format(heading, value)
        messagebox.showinfo("Request Details", Detail_str)

    def Inform_renter(self, title, message):
        pass
        #acknowledge the renter the next time they login in a messagebox


if __name__ == "__main__":
    
    with open('user.json', 'r') as users:
        UserData = json.load(users)
        
    root = tk.Tk()
    app = LoginGUI(UserData, root)
    root.mainloop()


