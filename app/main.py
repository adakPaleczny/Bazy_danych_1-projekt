import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2

class DatabaseViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("FS Poland Database Viewer")

        # Create and place widgets for connection
        self.create_connection_widgets()

        # Create and place widgets for data display
        self.create_teams_display_widgets()
        self.create_members_display_widgets()
        self.create_member_insert()

    def create_connection_widgets(self):
        # Connect Button
        self.teams_button = tk.Button(self.root, text="TEAMS", command=self.display_team)
        self.members_button = tk.Button(self.root, text="MEMBERS", command=self.display_member)

        # Grid layout for connection widgets
        self.teams_button.grid(row=5, column=0, columnspan=2, pady=10)
        self.members_button.grid(row=5, column=1, columnspan=2, pady=10)

    def create_teams_display_widgets(self):
        # Treeview for displaying data
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("Nazwa", "Uczelnia", "Kraj")  # Replace with your actual column names

        # Configure columns
        self.tree.column("#0", width=0, stretch=tk.NO)  # Hidden ID column
        self.tree.column("Nazwa",anchor=tk.W, width=200)  # Hidden ID column
        self.tree.column("Uczelnia", anchor=tk.W, width=300)
        self.tree.column("Kraj", anchor=tk.W, width=100)

        # Add column headings
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("Nazwa", text="Team", anchor=tk.W)
        self.tree.heading("Uczelnia", text="Uczelnia", anchor=tk.W)
        self.tree.heading("Kraj", text="Kraj", anchor=tk.W)

        # Grid layout for Treeview
        self.tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    def create_members_display_widgets(self):
        # Treeview for displaying data
        self.tree_team_members = ttk.Treeview(self.root)
        self.tree_team_members["columns"] = ("Imie", "Nazwisko", "TEAM", "Rola")

        # Configure columns
        self.tree_team_members.column("#0", width=0, stretch=tk.NO)  # Hidden MemberID column
        self.tree_team_members.column("Imie", anchor=tk.W, width=150)
        self.tree_team_members.column("Nazwisko", anchor=tk.W, width=150)
        self.tree_team_members.column("TEAM", anchor=tk.W, width=200)
        self.tree_team_members.column("Rola", anchor=tk.W, width=300)

        # Add column headings
        self.tree_team_members.heading("#0", text="", anchor=tk.W)
        self.tree_team_members.heading("Imie", text="Imie", anchor=tk.W)
        self.tree_team_members.heading("Nazwisko", text="Nazwisko", anchor=tk.W)
        self.tree_team_members.heading("TEAM", text="TEAM", anchor=tk.W)
        self.tree_team_members.heading("Rola", text="Rola", anchor=tk.W)


        # Grid layout for Treeviews
        self.tree_team_members.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.tree_team_members.grid_forget()

    
    def create_member_insert(self):
        # Entry Widgets for data insertion
        self.member_id_label = tk.Label(self.root, text="Member ID")
        self.member_id_entry = tk.Entry(self.root)
        self.member_name_label = tk.Label(self.root, text="Imie")
        self.member_name_entry = tk.Entry(self.root)
        self.member_surname_label = tk.Label(self.root, text="Nazwisko")
        self.member_surname_entry = tk.Entry(self.root)
        self.member_team_label = tk.Label(self.root, text="TEAM")
        self.member_team_entry = tk.Entry(self.root)
        self.member_role_label = tk.Label(self.root, text="Rola: ")
        self.member_role_entry = tk.Entry(self.root)


        # Insert Button
        self.insert_button = tk.Button(self.root, text="Insert Member", command=self.insert_member)

        # Grid layout for data insertion widgets
        self.member_id_label.grid(row=8, column=0, padx=5, pady=5)
        self.member_id_entry.grid(row=8, column=1, padx=5, pady=5)
        self.member_name_label.grid(row=9, column=0, padx=5, pady=5)
        self.member_name_entry.grid(row=9, column=1, padx=5, pady=5)
        self.member_surname_label.grid(row=10, column=0, padx=5, pady=5)
        self.member_surname_entry.grid(row=10, column=1, padx=5, pady=5)
        self.member_team_label.grid(row=11, column=0, padx=5, pady=5)
        self.member_team_entry.grid(row=11, column=1, padx=5, pady=5)
        self.member_role_label.grid(row=12, column=0, padx=5, pady=5)
        self.member_role_entry.grid(row=12, column=1, padx=5, pady=5)
        self.insert_button.grid(row=13, column=3, padx=5, pady=5)

        

    def insert_member(self):
        # Retrieve values from entry widgets
        id = self.member_id_entry.get()
        name = self.member_name_entry.get()
        surname = self.member_surname_entry.get()
        role = self.member_role_entry.get()
        team_name = self.member_team_entry.get()
        self.connect_to_database()

        if not all([id, name, surname,  team_name]):
            messagebox.showerror("Error", "Wszystkie pola poza 'Rola' muszą być wypełnione!")
            return
        
        # Execute a query to insert data into the table (replace with your query)
        try:
            self.cursor.execute("SELECT team_id FROM projekt.zespoly WHERE nazwa = %s", (team_name,))
            team_id = self.cursor.fetchone()[0] 
            self.cursor.execute("INSERT INTO projekt.czlonkowie VALUES (%s, %s, %s, %s, %s);", (id, name, surname, role,team_id))
            self.connection.commit()
            messagebox.showinfo("Info", "Członek dodany!")

        except Exception as e:
            messagebox.showerror("Error", f"Wystąpił błąd przy dodawaniu członka: {e}")

        # # Clear entry fields
        self.member_id_entry.delete(0, tk.END)
        self.member_name_entry.delete(0, tk.END)
        self.member_surname_entry.delete(0, tk.END)
        self.member_team_entry.delete(0, tk.END)
        self.member_role_entry.delete(0, tk.END)


        self.close_database_connection()

    def display_member(self):
        self.tree.grid_forget()
        self.tree_team_members.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.connect_to_database()
         # Execute a query to retrieve data from the table (replace with your query)
        self.cursor.execute("select c.imie, c.nazwisko, z.nazwa, c.rola from projekt.czlonkowie c join projekt.zespoly z on c.team_id = z.team_id")

        rows = self.cursor.fetchall()

        # Clear existing data in the Treeview
        for item in self.tree_team_members.get_children():
            self.tree_team_members.delete(item)

        # Insert retrieved data into the Treeview
        for row in rows:
            self.tree_team_members.insert("", "end", values=row)

        self.close_database_connection()

    def close_database_connection(self):
        # Close the cursor and connection
        self.cursor.close()
        self.connection.close()

    def display_team(self):
        self.tree_team_members.grid_forget()
        self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.connect_to_database()
         # Execute a query to retrieve data from the table (replace with your query)
        self.cursor.execute("SELECT nazwa, uczelnia, kraj FROM projekt.zespoly")
        rows = self.cursor.fetchall()

        # Clear existing data in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert retrieved data into the Treeview
        for row in rows:
            self.tree.insert("", "end", values=row)

        self.close_database_connection()

    def connect_to_database(self):
        try:
            # Establish a connection to the PostgreSQL database
            self.connection = psycopg2.connect(
                host='peanut.db.elephantsql.com',
                database='jminsjkl',
                user='jminsjkl' ,
                password='UFJogNQVmyM9lpboburJF6yaqPq5LauU',
                port=5432
            )

            # Create a cursor object to interact with the database
            self.cursor = self.connection.cursor()

        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Error", f"Error while connecting to PostgreSQL: {error}")

        

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseViewer(root)
    root.mainloop()
