import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pathlib import Path
import psycopg2

class DatabaseViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Formuła Student Polska System Informacji")

        self.create_button_widgets()
        self.create_teams_display_widgets()
        self.create_members_display_widgets()
        self.create_member_insert()
        self.create_search_widgets()
        self.create_results_widgets()

    def create_button_widgets(self):
        # Connect Button
        self.teams_button = tk.Button(self.root, text="ZESPOŁY", command=self.display_team)
        self.members_button = tk.Button(self.root, text="CZŁONKOWIE", command=self.display_member)
        self.cv_button = tk.Button(self.root, text="CV", command=self.display_cv_results)
        self.ev_button = tk.Button(self.root, text="EV", command=self.display_ev_results)
        self.overall_button = tk.Button(self.root, text="OVERALL", command=self.display_results)
        self.config_button = tk.Button(self.root, text="Załaduj przykładowe dane", command=self.load_example_data)
    
        self.overall_test = tk.Label(self.root, text="WYNIKI ZAWODÓW")
        self.overall_test.config(font=('Helvatical bold',15))

        self.info_label = tk.Label(self.root, text="INFORMACJE O ZESPOŁACH I CZŁONKACH")
        self.info_label.config(font=('Helvatical bold',15))

        # Grid layout for connection widgets
        self.config_button.grid(row=4, column=1, columnspan=1, pady=10)
        self.info_label.grid(row=4, column=0, columnspan=1, pady=10)
        self.teams_button.grid(row=5, column=0, columnspan=1, pady=10)
        self.members_button.grid(row=5, column=1, columnspan=1, pady=10)
        self.overall_test.grid(row=4, column=15, columnspan=1, pady=1)
        self.cv_button.grid(row=5, column=15, columnspan=1, pady=1)
        self.ev_button.grid(row=5, column=16, columnspan=1, pady=1)
        self.overall_button.grid(row=5, column=17, columnspan=1, pady=1)

    def create_teams_display_widgets(self):
        # Treeview for displaying data
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("Nazwa", "Uczelnia", "Kraj", "Liczba_czlonkow")  # Replace with your actual column names

        # Configure columns
        self.tree.column("#0", width=0, stretch=tk.NO)  # Hidden ID column
        self.tree.column("Nazwa",anchor=tk.W, width=300)
        self.tree.column("Uczelnia", anchor=tk.W, width=200)
        self.tree.column("Kraj", anchor=tk.W, width=100)
        self.tree.column("Liczba_czlonkow", anchor=tk.W, width=160) 

        # Add column headings
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("Nazwa", text="Team", anchor=tk.W)
        self.tree.heading("Uczelnia", text="Uczelnia", anchor=tk.W)
        self.tree.heading("Kraj", text="Kraj", anchor=tk.W)
        self.tree.heading("Liczba_czlonkow", text="Ilość członków", anchor=tk.W)

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
        self.tree_team_members.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

        # Hide grip to display empty rows
        self.tree_team_members.grid_forget()
  
    def create_member_insert(self):
        # Insertion Label
        self.insert_info_label =  tk.Label(self.root, text="Rejstracja nowych członków: ")
        self.insert_info_label.config(font=('Helvatical bold',20))
        
        # Entry Widgets for data insertion
        self.member_name_label = tk.Label(self.root, text="Imie")
        self.member_name_entry = tk.Entry(self.root)
        self.member_surname_label = tk.Label(self.root, text="Nazwisko")
        self.member_surname_entry = tk.Entry(self.root)
        self.member_team_label = tk.Label(self.root, text="TEAM")
        self.member_team_entry = tk.Entry(self.root)
        self.member_role_label = tk.Label(self.root, text="Rola: ")
        self.member_role_entry = tk.Entry(self.root)


        # Insert Button
        self.insert_button = tk.Button(self.root, text="Zarejstruj uczestnika", command=self.insert_member)
        self.delete_button = tk.Button(self.root, text="Usuń uczestnika", command=self.delete_member)

        # Grid layout for data insertion widgets
        self.insert_info_label.grid(row=7, column=0, columnspan=2, pady=10)
        self.member_name_label.grid(row=8, column=0, padx=5, pady=5)
        self.member_name_entry.grid(row=8, column=1, padx=5, pady=5)
        self.member_surname_label.grid(row=9, column=0, padx=5, pady=5)
        self.member_surname_entry.grid(row=9, column=1, padx=5, pady=5)
        self.member_team_label.grid(row=10, column=0, padx=5, pady=5)
        self.member_team_entry.grid(row=10, column=1, padx=5, pady=5)
        self.member_role_label.grid(row=11, column=0, padx=5, pady=5)
        self.member_role_entry.grid(row=11, column=1, padx=5, pady=5)
        self.insert_button.grid(row=12, column=0, padx=5, pady=5)
        self.delete_button.grid(row=12, column=1, padx=5, pady=5)

    def create_search_widgets(self):
        # Search Label 
        self.search_info_label =  tk.Label(self.root, text="Wyszkuja informacja dla członka:")
        self.search_info_label.config(font=('Helvatical bold',20))
        self.name_label = tk.Label(self.root, text="Wprowadź imie uczestnika: ")
        self.name_entry = tk.Entry(self.root)
        self.surname_label = tk.Label(self.root, text="Wprowadź nazwisko uczestnika: ")
        self.surname_entry = tk.Entry(self.root)    

        self.get_info_button = tk.Button(self.root, text="Nocleg", command=self.get_info_sleeping)

        # Grid layout for data insertion widgets
        self.search_info_label.grid(row=14, column=0, columnspan=2, pady=10)   
        self.name_label.grid(row=15, column=0, padx=5, pady=5)
        self.name_entry.grid(row=15, column=1, padx=5, pady=5)
        self.surname_label.grid(row=16, column=0, padx=5, pady=5)
        self.surname_entry.grid(row=16, column=1, padx=5, pady=5)
        self.get_info_button.grid(row=17, column=0, padx=5, pady=5)

        self.tree_member = ttk.Treeview(self.root)
        self.tree_member["columns"] = ("Ulica", "Numer", "Numer pola namiotowego", "Lokatorzy")  # Replace with your actual column names

        # Configure columns
        self.tree_member.column("#0", width=0, stretch=tk.NO)  # Hidden MemberID column
        self.tree_member.column("Ulica",anchor=tk.W, width=150)  # Hidden ID column
        self.tree_member.column("Numer", anchor=tk.W, width=80)
        self.tree_member.column("Numer pola namiotowego", anchor=tk.W, width=130)
        self.tree_member.column("Lokatorzy", anchor=tk.W, width=380) 

        # Add column headings
        self.tree_member.heading("#0", text="", anchor=tk.W)
        self.tree_member.heading("Ulica", text="Ulica", anchor=tk.W)
        self.tree_member.heading("Numer", text="Numer", anchor=tk.W)
        self.tree_member.heading("Numer pola namiotowego", text="Pole namiotowe", anchor=tk.W)
        self.tree_member.heading("Lokatorzy", text="Lokatorzy", anchor=tk.W)

        # Grid layout for Treeview
        self.tree_member.grid(row=18, column=0, columnspan=3, padx=10, pady=10)

    def create_results_widgets(self):
        # Treeview for displaying data
        self.tree_results = ttk.Treeview(self.root)
        self.tree_results["columns"] = ("Wynik", "Zespol", "Numer_startowy", "Nazwa_samochodu")

        # Configure columns
        self.tree_results.column("#0", width=0, stretch=tk.NO) 
        self.tree_results.column("Wynik", anchor=tk.W, width=150)
        self.tree_results.column("Zespol", anchor=tk.W, width=280)
        self.tree_results.column("Numer_startowy", anchor=tk.W, width=140)
        self.tree_results.column("Nazwa_samochodu", anchor=tk.W, width=200)

        # Add column headings
        self.tree_results.heading("#0", text="", anchor=tk.W)
        self.tree_results.heading("Wynik", text="Wynik", anchor=tk.W)
        self.tree_results.heading("Zespol", text="Zespół", anchor=tk.W)
        self.tree_results.heading("Numer_startowy", text="Numer startowy", anchor=tk.W)
        self.tree_results.heading("Nazwa_samochodu", text="Nazwa samochodu", anchor=tk.W)

        # Grid layout for Treeviews
        self.tree_results.grid(row=6, column=15, columnspan=3, padx=10, pady=10)

    def load_example_data(self):
        self.delete_all_data()

        self.execute_sql_script("table_create.sql")
        self.execute_sql_script("insert.sql")
        self.execute_sql_script("view.sql")
        self.execute_sql_script("trigger.sql")

        messagebox.showinfo("Info", "Przykładowe dane zostały załadowane!")
            
    def delete_all_data(self):
        self.connect_to_database()
        self.cursor.execute("DROP SCHEMA IF EXISTS projekt CASCADE")
        self.connection.commit()
        self.close_database_connection()

    def execute_sql_script(self, script_name):
        self.connect_to_database()

        # Read the SQL script from file
        path = Path(__file__).parent.absolute()
        with open(str(path) + "/../sql/" + script_name, "r") as file:
            sql_script = file.read()

        # Execute the SQL script
        self.cursor.execute(sql_script)
        self.connection.commit()
        self.close_database_connection()

    def insert_member(self):
        # Retrieve values from entry widgets
        name = self.member_name_entry.get()
        surname = self.member_surname_entry.get()
        role = self.member_role_entry.get()
        team_name = self.member_team_entry.get()
        self.connect_to_database()

        if not all([name, surname,  team_name]):
            messagebox.showerror("Error", "Wszystkie pola poza 'Rola' muszą być wypełnione!")
            return
        
        self.cursor.execute("SELECT MAX(czlonek_id) FROM projekt.czlonkowie")
        max_id = self.cursor.fetchone()[0]
        
        # Execute a query to insert data into the table (replace with your query)
        try:
            self.cursor.execute("SELECT team_id FROM projekt.zespoly WHERE nazwa = %s", (team_name,))
            team_id = self.cursor.fetchone()[0] 
            self.cursor.execute("INSERT INTO projekt.czlonkowie VALUES (%s, %s, %s, %s, %s);", (str(max_id+1), name, surname, role,team_id))
            self.connection.commit()
            messagebox.showinfo("Info", "Członek dodany!")

        except Exception as e:
            messagebox.showerror("Error", f"Wystąpił błąd przy dodawaniu członka: {e}")

        # # Clear entry fields
        self.member_name_entry.delete(0, tk.END)
        self.member_surname_entry.delete(0, tk.END)
        self.member_team_entry.delete(0, tk.END)
        self.member_role_entry.delete(0, tk.END)


        self.close_database_connection()

    def delete_member(self):
        # Checking if all important fields are filled
        if not self.member_name_entry.get() or not self.member_surname_entry.get():
            messagebox.showerror("Error", "Brak wypełnienia pola Imie i Nazwisko!")
            return
        
        self.connect_to_database()
        self.cursor.execute("SELECT czlonek_id FROM projekt.czlonkowie WHERE imie = %s AND nazwisko = %s", (self.member_name_entry.get(), self.member_surname_entry.get(),))

        czlonek_id = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT team_id from projekt.zespoly where szef_zespolu = %s", (czlonek_id,))
        if self.cursor.fetchone():
            messagebox.showerror("Error", "Nie można usunąć szefa zespołu!")
            return
        
        self.cursor.execute("SELECT team_id FROM projekt.czlonkowie WHERE imie = %s AND nazwisko = %s", (self.member_name_entry.get(), self.member_surname_entry.get(),))
        team_id = self.cursor.fetchone()[0]

        self.cursor.execute("DELETE FROM projekt.nocleg_czlonkow WHERE czlonek_id = %s", (czlonek_id,))
        self.cursor.execute("DELETE FROM projekt.czlonkowie WHERE czlonek_id = %s", (czlonek_id,))  # Fix: Use 'czlonek_id' instead of 'imie' and 'nazwisko'
        self.connection.commit()

        messagebox.showinfo("Info", "Członek usunięty!")

        self.cursor.execute("SELECT COUNT(czlonek_id) FROM projekt.czlonkowie WHERE team_id = %s", (team_id,))
        if self.cursor.fetchone()[0] == 0:
            messagebox.showinfo("Info", "Zespół został usunięty, za mało członków!")

        self.close_database_connection()

        # Clear entry fields
        self.member_name_entry.delete(0, tk.END)
        self.member_surname_entry.delete(0, tk.END)
        self.member_team_entry.delete(0, tk.END)
        self.member_role_entry.delete(0, tk.END)

    def display_member(self):
        # Hide the other Treeview
        self.tree.grid_forget()
        self.tree_team_members.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

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

    def display_team(self):
        # Hide the other Treeview
        self.tree_team_members.grid_forget()
        self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.connect_to_database()
         # Execute a query to retrieve data from the table (replace with your query)
        self.cursor.execute("SELECT z.nazwa, z.uczelnia, z.kraj, COUNT(c.czlonek_id) as ilosc_czlonkow FROM projekt.zespoly z JOIN projekt.czlonkowie c on c.team_id = z.team_id GROUP BY nazwa, uczelnia, kraj HAVING COUNT(c.czlonek_id) > 1;")
        rows = self.cursor.fetchall()

        # Clear existing data in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert retrieved data into the Treeview
        for row in rows:
            self.tree.insert("", "end", values=row)

        self.close_database_connection()

    def display_results(self):
        self.connect_to_database()

        # Execute a query that gets results from the table
        self.cursor.execute("SELECT wynik, zespol, numer, bolid from projekt.wyniki")
        rows = self.cursor.fetchall()

        for row in self.tree_results.get_children():
            self.tree_results.delete(row)

        for row in rows:
            self.tree_results.insert("", "end", values=row)

        self.close_database_connection()

    def display_cv_results(self):
        self.connect_to_database()

        # Execute a query that gets results from the table with "CV" class
        self.cursor.execute("SELECT ROW_NUMBER() OVER (ORDER BY wynik) as wynik, zespol, numer, bolid FROM projekt.wyniki where typ = 'CV';")

        for row in self.tree_results.get_children():
            self.tree_results.delete(row)

        for row in self.cursor.fetchall():
            self.tree_results.insert("", "end", values=row)
        
        self.close_database_connection()

    def display_ev_results(self):
        self.connect_to_database()

        # Execute a query that gets results from the table with "EV" class
        self.cursor.execute("SELECT ROW_NUMBER() OVER (ORDER BY wynik) as wynik, zespol, numer, bolid FROM projekt.wyniki where typ = 'EV';")

        for row in self.tree_results.get_children():
            self.tree_results.delete(row)

        for row in self.cursor.fetchall():
            self.tree_results.insert("", "end", values=row)
        
        self.close_database_connection()

    def get_info_sleeping(self):
        self.connect_to_database()
        # Getting nocleg_id from user that is needed to get information about sleeping
        self.cursor.execute("SELECT nocleg_ID from projekt.nocleg_czlonkow n join projekt.czlonkowie c on c.czlonek_ID = n.czlonek_ID where c.imie = %s and c.nazwisko = %s", (self.name_entry.get(),self.surname_entry.get(),)) 

        nocleg_id_result = self.cursor.fetchone()
        if not nocleg_id_result:
            messagebox.showerror("Error", "Nie znaleziono takiego członka!")
            return
        
        nocleg_id = nocleg_id_result[0]

        # Getting information people sleeping in the same place
        self.cursor.execute("SELECT c.imie, c.nazwisko from projekt.czlonkowie c join projekt.nocleg_czlonkow n on c.czlonek_ID = n.czlonek_ID WHERE nocleg_ID = %s", (nocleg_id,))
        czlonkowie = self.cursor.fetchall()

        # Getting information about sleeping place
        self.cursor.execute("SELECT ulica, numer, numer_pola_namiotowego FROM projekt.nocleg WHERE nocleg_id = %s", (nocleg_id,))
        ulica, numer, numer_pola_namiotowego = self.cursor.fetchone()
        
        nazwy_czlonkow_table = [ nazwa[0]+ " " + nazwa[1] + "\n"  for nazwa in czlonkowie]
        nazwy_czlonkow = "".join(nazwy_czlonkow_table)
        nazwy_czlonkow = nazwy_czlonkow[:-2]
        
        # Clear existing data in the Treeview
        for item in self.tree_member.get_children():
            self.tree_member.delete(item)

        # Insert retrieved data into the Treeview       
        self.tree_member.insert("", "end", values=[ulica, numer, numer_pola_namiotowego, nazwy_czlonkow])

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

    def close_database_connection(self):
        # Close the cursor and connection
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseViewer(root)
    root.mainloop()
