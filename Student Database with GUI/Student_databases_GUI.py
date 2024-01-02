from tkinter import Tk, Entry, Text, END, font, Label, Button, BOTH
import sqlite3
from tkinter.messagebox import showinfo
from datetime import datetime
import pandas as pd

# Create the main application window
app = Tk()
app.title('cool title') #title
app.geometry('800x800') #size of the window

# Create a custom font with your desired size and other attributes
custom_font = font.nametofont("TkDefaultFont")  # Start with the default font
custom_font.configure(size=18)  # Set the desired font size

# Set the custom font as the default font for the application
app.option_add("*Font", custom_font)

# Connect to the SQLite database and create a cursor
conn = sqlite3.connect('records.db')
cursor = conn.cursor()

# Create a 'students' table in the database if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS students (pantherid INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
conn.commit()

#creating labels for the panther id, name, and email
pantherid_label = Label(master=app, text='PantherId')
pantherid_label.grid(row=0,column=0)
name_label = Label(master=app, text='name') 
name_label.grid(row=1, column=0)
email_label = Label(master=app, text='Email')
email_label.grid(row=2, column=0)

#creating a place entry widgets for the labels above
pantherid_entry = Entry(master=app)
pantherid_entry.grid(row=0, column=1)
name_entry = Entry(master=app)
name_entry.grid(row=1, column=1)
email_entry = Entry(master=app)
email_entry.grid(row=2, column=1)

#function to add students
def on_add_student_button_clicked():
    #step 1 obtain info from entry widgets
    try:
        pantherid = int(pantherid_entry.get()) #gets the information from widgets
        name = name_entry.get()
        email = email_entry.get()
        cursor.execute('INSERT INTO Students (PantherID, Name, Email) Values (?,?,?)', (pantherid, name, email))
        #insert information into database
        conn.commit()

        #clear the entry fields
        pantherid_entry.delete(0, END)
        name_entry.delete(0, END)
        email_entry.delete(0, END)

        #show an information message
        showinfo(message='Student record added to the database...')
    except:
        print("Entry is either empty or has an invalid value")

#function to show the record on the text box
def on_list_student_button_clicked():
    try:
        cursor.execute('SELECT * from Students')
        records = cursor.fetchall()
        txt.delete(0.0, END)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        txt.insert(END, f'----- Student list as of {timestamp} -----\n')
        for record in records:
            txt.insert(END, f"PantherID: {record[0]} Name: {record[1]} Email: {record[2]}\n")
    except:
        print("Entry is either empty or has an invalid value")

#this function searches a student by its pantherID
def on_search_student_button():
    try:
        #if that student exists in the database then the search code will execute else a message will show that the student is not in the database
        cursor.execute(f"SELECT * FROM Students WHERE PantherID ='{pantherid_entry.get()}'")
        conn.commit()
        searched = cursor.fetchall()

        if pantherid_entry.get() == '':
            showinfo(message="Please enter a PantherID to search for a record")
        else:
            #if student is on database then show the student's info on the text box
            if searched:
                txt.insert(END, f"\nStudent found: \nPantherID: {searched[0][0]} Name: {searched[0][1]} Email: {searched[0][2]}")

                #clear the entry fields
                pantherid_entry.delete(0, END)
                name_entry.delete(0, END)
                email_entry.delete(0, END)

            else:
                #show message if record not found
                showinfo(message=f"No record was found for #{pantherid_entry.get()}")
                #clear the entry fields
                pantherid_entry.delete(0, END)
                name_entry.delete(0, END)
                email_entry.delete(0, END)
                
                

        
    except:
        print("Entry is either empty or has an invalid value")

#this function updates the information of the student using the pantherID
def on_update_student_record():
    try:
        #check if student is on the database
        cursor.execute(f"SELECT * FROM Students WHERE PantherID ='{pantherid_entry.get()}'")
        conn.commit()
        searched = cursor.fetchall()

        #check that entry box for pantherID is not empty
        if pantherid_entry.get() == '':
            showinfo(message="Please enter PantherID, Name and Email to update a record.")
        else:
            #update students information and save it to the database
            if searched:
                pantherid = int(pantherid_entry.get()) #gets the information from widgets
                name = name_entry.get()
                email = email_entry.get()

                cursor.execute(f"UPDATE Students SET Email='{email}' where PantherID={pantherid}")
                cursor.execute(f"UPDATE Students SET Name='{name}' where PantherID={pantherid}")
                conn.commit()

                #clear the entry fields
                pantherid_entry.delete(0, END)
                name_entry.delete(0, END)
                email_entry.delete(0, END)

                showinfo(message="Database has been updated") #name and email needs to be updated
            else:

                showinfo(message=f"No record was found for #{pantherid_entry.get()}")
                #clear the entry fields
                pantherid_entry.delete(0, END)
                name_entry.delete(0, END)
                email_entry.delete(0, END)           
    except:
        print("Entry is either empty or has an invalid value")

def on_delete_student_record():
    try:
        #check if student is on database
        cursor.execute(f"SELECT * FROM Students WHERE PantherID ='{pantherid_entry.get()}'")
        conn.commit()
        searched = cursor.fetchall()

        #check panterID entry box is not empty
        if pantherid_entry.get() == '':
            showinfo(message=f"Please enter PantherID")
        else:
            #if student exists on database then delete its information
            if searched:
                pantherid = int(pantherid_entry.get()) #gets the information from widgets             
                cursor.execute(f"DELETE FROM Students WHERE PantherID={pantherid}")
                conn.commit()

                #clear the entry fields
                pantherid_entry.delete(0, END)
                name_entry.delete(0, END)
                email_entry.delete(0, END)

                showinfo(message=f"{pantherid} Has been deleted from the database")
            else:
                
                showinfo(message=f"No record was found for #{pantherid_entry.get()}")
                #clear the entry fields
                pantherid_entry.delete(0, END)
                name_entry.delete(0, END)
                email_entry.delete(0, END)
    except:
        print("An error has occurred")
    
def on_export_database_to_CSV():
    #saving sqlite into a dataframe
    exporting = pd.read_sql('SELECT * FROM Students', conn)

    #write it into a CSV file
    exporting.to_csv('records.csv', index=False)
    txt.insert(END, 'File has been exported to csv')

#create buttons for adding student
button_add = Button(master=app, text='Add student', command=on_add_student_button_clicked)
button_add.grid(row=3, column=0, columnspan=2, sticky='w')

#button to show what students are currently on the database
button_list = Button(master=app, text='List Students', command=on_list_student_button_clicked)
button_list.grid(row=4, column=0, columnspan=2, sticky='w')

#creating a button to search for a student
button_search = Button(master=app, text='Search Record', command=on_search_student_button)
button_search.grid(row=3, column=1, columnspan=2)

#button for deleting a record
button_delete_record = Button(master=app, text='Delete record', command=on_delete_student_record)
button_delete_record.grid(row=4, column=1, columnspan=2)

#button for updating record
button_update_record = Button(master=app, text='Update Record', command=on_update_student_record)
button_update_record.grid(row=3, column=2, columnspan=2)

#button to export to csv
button_export_to_csv = Button(master=app, text='Export to CSV', command=on_export_database_to_CSV)
button_export_to_csv.grid(row=4, column=2, columnspan=2)

#create a text widget to display sutdent records
txt = Text(master=app, height=10, width=40)
txt.grid(row=5, column=0, columnspan=2)

app.mainloop()