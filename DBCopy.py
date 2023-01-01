import tkinter as tk;
import mysql.connector

size = '900x400+25+25'
window = tk.Tk() 
login_frame = tk.Frame(window, bg="grey")
username_label  = tk.Label(login_frame, text="Username:", bg="grey")
password_label = tk.Label(login_frame, text="Password:", bg="grey")
username_input = tk.Entry(login_frame, bg='white', width=30, fg= 'black', highlightbackground="grey")
password_input = tk.Entry(login_frame, bg='white', width=30, fg= 'black', show="*", highlightbackground="grey")
under_text = tk.Label(login_frame, bg='grey')
under_text.grid(row=100,column=0)
login_frame.grid(row=0, column=0)

### TO RUN INSTRUCTIONS
# Before you run the file, go to line 23 and 24 and update the username and password to your root user.
# Create a new user to simulate non-admin user and code should work.


## Make admin connection and cursor at application start
# Connection global to be used everywhere in application
global admin
admin = mysql.connector.connect(
    host = 'localhost',
    user = "root",
    password = "root",
    database = "databaseMGMT_database"
)
global cursor
# Creating cursor, dictionary meaning we can access data using row names instead of indexs
# Buffered is ensuring all records are in before reading
cursor = admin.cursor(dictionary=True, buffered=True)   



# Takes in place (tk.TK() window) and destroy's it
# Makes new window and configs it and passes it to mainmenu_screen function
def create_mainmenu_screen(place):

    place.destroy()

    # Making and configuring file
    mainmenu = tk.Tk()
    mainmenu.title('Main Menu')
    mainmenu.geometry(size)
    mainmenu.config(bg="#85929E")

    mainmenu_screen(mainmenu)


# Establishing connection with input given from user
def checkCredentials():
    # Storing input from user.
    username = username_input.get()
    password = password_input.get()

    
    # Checking for valid inputs
    if username == "" or password == "":
        under_text.config(text="Please provide credentials")
    else:
        # If valid, try to establish connection
        try:
            global this_con
            this_con = mysql.connector.connect (
                host = "localhost",
                user = username,
                passwd = password,
                database = "databaseMGMT_database"
            )  
            global normal_cursor
            # Creating normal non-admin cursor for application use
            normal_cursor = this_con.cursor(buffered = True)

            # Query to get user_Id for global use
            cursor.execute(f'SELECT User_ID FROM Users WHERE Username = "{username}"')

            # Get user id by parsing through the result returned from query
            for row in cursor:
                global user_id
                user_id = row["User_ID"]

            # Update database
            admin.commit()

            # After connection is successful we go to the main menu
            create_mainmenu_screen(window)
        except Exception as e:
            # If connection fails, because username and password are invalid, show error message
            under_text.config(text="Access Denied")


# Get and create user input
def create_user(uname_input, pword_input, fname_input, lname_input, error_text, checkbox, window):
    # Get all inputs from text boxes
    uname = uname_input.get()
    pword = pword_input.get()
    fname = fname_input.get()
    lname = lname_input.get()
    isAdmin = checkbox.get()

    # Reseting all the inputs
    uname_input.delete(0, 'end')
    pword_input.delete(0, 'end')
    fname_input.delete(0, 'end')
    lname_input.delete(0, 'end')


    # Normal Query to check if user with username given from input exists
    cursor.execute(f"SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = '{uname}') as 'check'")

    # store value in exists, which will be 0(doesn't exist) and 1(exists)
    for row in cursor:
        exists = row["check"]

    # Send information to databse
    admin.commit()

    # Check for all empty
    if (uname == "" or pword == "" or fname == "" or lname == ""):
        error_text.config(text ="Please fill out all fields")
    # Check for username too long
    elif(len(uname) > 32):
        error_text.config(text="Username has to be no longer than 32 characters")
    # Check if username given already exists
    elif(exists > 0):
        error_text.config(text="User already exists")
    # information passes tests, create user and grant permissions
    else:
        try:
            ## Create user 
            cursor.execute(f'CREATE USER "{uname}"@"localhost" IDENTIFIED BY "{pword}"')
            if (not isAdmin):
                # Grant permissions 
                cursor.execute(f'GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT on databaseMGMT_database.diary_management to "{uname}"@"localhost"')
                cursor.execute(f'GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT on databaseMGMT_database.entry_management to "{uname}"@"localhost"')
                cursor.execute(f'GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT on databaseMGMT_database.entry_log to "{uname}"@"localhost"')
                # Add user information to user table
                cursor.execute(f'INSERT INTO users(Username, Password, First_Name, Last_Name) value ("{uname}", "{pword}", "{fname}", "{lname}")')

                # Submit changes to database
                admin.commit()
            else:
                cursor.execute(f'GRANT ALL PRIVILEGES ON databaseMGMT_database.* TO "{uname}"@"localhost"')
            # Update text on the screen
            error_text.config(text="User created ! Please login on main screen")

            window.after(1000, window.destroy())
        except Exception as e:
            print("Error", e.args)

# Creates the "Create new user" window with all inputs, buttons, and labels
def create_new_user():
    # Creating the window
    create_user_window = tk.Tk()

    # Inputs
    make_uname_input = tk.Entry(create_user_window, bg="white", fg="black")
    make_pword_input = tk.Entry(create_user_window, bg='white', fg="black", show="*")
    make_fname_input = tk.Entry(create_user_window, bg='white', fg="black")
    make_lname_input = tk.Entry(create_user_window, bg='white', fg="black")

    status_var = tk.IntVar()
    make_admin_checkbox = tk.Checkbutton(create_user_window, text="Admin?", variable=status_var)

    # Labels
    make_uname_label = tk.Label(create_user_window, text="Username:")
    make_pword_label = tk.Label(create_user_window, text="Password:")
    make_fname_label = tk.Label(create_user_window, text="First Name:")
    make_lname_label = tk.Label(create_user_window, text="Last Name:")
    create_user_under_txt = tk.Label(create_user_window)
    create_user_button = tk.Button(create_user_window, text="Create User", command= lambda: create_user(make_uname_input, make_pword_input,
    make_fname_input, make_lname_input, create_user_under_txt, status_var, create_user_window))

    # Configuring window
    create_user_window.title("Create New User")
    create_user_window.geometry("500x300+800+0")
    create_user_under_txt.grid(row = 50, column = 1)
    
    # Placing everything on the screen
    make_uname_label.grid(row = 0, column = 0, pady=10)
    make_uname_input.grid(row = 0, column = 1, pady=10)
    make_pword_label.grid(row = 1, column = 0, pady=10)
    make_pword_input.grid(row = 1, column = 1, pady=10)
    make_fname_label.grid(row = 2, column = 0, pady=10)
    make_fname_input.grid(row = 2, column = 1, pady=10)
    make_lname_label.grid(row = 3, column = 0, pady=10)
    make_lname_input.grid(row = 3, column = 1, pady=10)
    make_admin_checkbox.grid(row = 4, column= 0)
    create_user_button.grid(row = 5)
            
# Creating all the buttons for the Initial window
enter_button = tk.Button(login_frame, bg='grey', text="Enter", command=checkCredentials, highlightbackground="grey")
new_user_button = tk.Button(login_frame, text="Create Account", command=create_new_user, highlightbackground="grey")
 
# Configuring initial window
window.title('Login Page')
window.geometry(size)
window.config(bg="grey")

# Placing everything on the screen
username_label.grid(row=1,column=0, padx= 10, pady = 20)
password_label.grid(row=2, column=0, padx= 10,pady = 20)
username_input.grid(row=1, column=1,pady = 20)
password_input.grid(row=2,column=1,pady = 20)
enter_button.grid(row=3, column=0, padx=5)
new_user_button.grid(row=3, column=1)


# Creates the Main menu screen by puttin the buttons the window
def mainmenu_screen(menutk):

    # Creating all the buttons
    add_button = tk.Button(menutk, text="Add", command=lambda: add_screen(menutk), highlightbackground="#85929E")
    delete_button = tk.Button(menutk, text="Delete", command=lambda: delete_screen(menutk), highlightbackground="#85929E")
    modify_button = tk.Button(menutk, text="Modify", command=lambda: modify_screen(menutk), highlightbackground="#85929E")
    search_button = tk.Button(menutk, text="Search", command=lambda: search_screen(menutk), highlightbackground="#85929E")
    print_button = tk.Button(menutk, text="Print", command=lambda: print_screen(menutk), highlightbackground="#85929E")

    # Putting all the buttons on the screen
    add_button.pack(pady=10)
    delete_button.pack(pady=10)
    modify_button.pack(pady=10)
    search_button.pack(pady=10)
    print_button.pack(pady=10)

# Submits info to database
def submit_info(ename_input, econtent_input, status_txt, diname, all_d_list, is_dnew):
    # Get inputs
    ename = ename_input.get()
    econtent = econtent_input.get("1.0",'end-1c')

    # Clear input boxes
    ename_input.delete(0, 'end')
    econtent_input.delete(1.0, tk.END)

    # Check for valid inputs
    if (ename == '' or econtent == ''):
        status_txt.config(text="Please enter all fields")
    elif (len(ename) > 45):
        status_txt.config(text="Entry Name is too long")
    elif(len(econtent) > 200):
        status_txt.config(text="Content is too long")
    else:
        # Normal query to get values for last diary_id and entry_id (add 1 to last id)
        normal_cursor.execute ('SELECT max(diary_id) FROM diary_management')

        # Get the result given from the query and save it to diary_num
        result = normal_cursor.fetchone()
        diary_num = result[0] 
        
        # Normal query to get the id of the last entry in the entry_management table
        normal_cursor.execute('SELECT max(Entry_ID) FROM Entry_Management')

        # Get the result given from the query and save it to entry_num
        result = normal_cursor.fetchone()
        entry_num = result[0]

        # Increment entry Id becuase of new entry but find index of diary for diary ID
        diary_num = all_d_list.index(diname) + 1
        entry_num += 1


        # Disable foreign key checks before insert
        normal_cursor.execute('SET foreign_key_checks = 0')
        cursor.execute('SET foreign_key_checks = 0')

        # NORMAL USER QUERIES
        # Normal query to add diary info to diary management table only if new diary was made
        if (is_dnew):
            normal_cursor.execute(f'INSERT INTO Diary_Management VALUE ({diary_num}, "{diname}", "{ename}", CURRENT_TIME, {entry_num})')

        # Normal Query to add entry info to entry management table 
        normal_cursor.execute(f'INSERT INTO Entry_Management VALUE ({entry_num}, "{diname}", "{ename}", CURRENT_TIME, {diary_num})')

        # Normal Query to add entry info to entry log table
        normal_cursor.execute(f'INSERT INTO Entry_Log VALUE ({entry_num}, "{econtent}", {diary_num})')

        # ADMIN QUERIES
        # Admin Query to add info to databases management table
        cursor.execute(f'INSERT INTO Databases_Management VALUE ({user_id}, "{diname}", {diary_num}, {entry_num}, CURRENT_TIME)')

        # Admin Query to add info to server table
        cursor.execute(f'INSERT INTO Server VALUE ({user_id}, "{econtent}", {diary_num}, {entry_num}, CURRENT_TIME)')

        # Re-enable foreign key checks
        normal_cursor.execute('SET foreign_key_checks = 1')
        cursor.execute('SET foreign_key_checks = 1')

        # Update status text on window
        status_txt.config(text="Entry Submitted")

        # Send all the data to the database
        this_con.commit() 
        admin.commit()   

# Removes everything from the window but the main meny buttom
def remove(place):
    
    # For each child widget in the grid of the window,
    for child in place.grid_slaves():
        # Check if child is of type (tk.Button) and if it is , check if the text says "Back to main menu"
        if (not (type(child) is tk.Button and child.cget('text') == 'Back to main menu')):

            # If true, destroy the child lol
            child.destroy()
        

# Shows page to enter entry and entry name
def next_step(dname, frame, all_ds, is_new):
    # Clear Screen
    remove(frame)

    name_input_label = tk.Label(frame, text="Entry Name:", bg="black")
    name_input = tk.Entry(frame, textvariable=name_input_label, width=30, highlightbackground="black", bg="grey")
    content_input_label = tk.Label(frame, text = "Entry:", bg="black")
    content_input = tk.Text(frame, height= 4, width= 50, highlightbackground="black", bg="grey")
    info_text = tk.Label(frame, bg="black")
    submit_info_button = tk.Button(frame, text="Submit", command=lambda: submit_info(name_input, content_input, info_text, dname, all_ds, is_new),
    highlightbackground="black")

    submit_info_button.grid(row = 3, column = 1)
    
    # Adding the name portion to screen
    name_input_label.grid(row = 1, column = 0, pady= 10)
    name_input.grid(row = 1, column = 1, pady = 10)

    # Adding the content portion to screen
    content_input_label.grid(row = 2, column = 0)
    content_input.grid(row = 2, column = 1);
    
    # Adding info text to screen
    info_text.grid(row=10, column=1)





def create_new_diary(diary, text, screen, list_d):
    dname = diary
    text.config(text="Diary Created.")
    list_d.append(dname)

    ## Delete All widgets from screen
    screen.after(1500, lambda: remove(screen))
    screen.after(2000, lambda: next_step(diary, screen, list_d, True))

    




def diary_chosen(text, diary_input, dlist, window):
    diary = diary_input.get().lower()

    if (diary == ''):
        text.config(text="Fill out field.")
    elif (len(diary) > 45):
        text.config(text="Name is too long")
    elif (diary not in dlist):
        text.config(text="Diary Doesn't Exist. Create New ?")
        create_button = tk.Button(window, text="Create", command=lambda: create_new_diary(diary, text, window, dlist), highlightbackground="black")
        create_button.grid(row = 0, column=100)
    else:
        next_step(diary, window, dlist, False)
    
def get_diaries():

    normal_cursor.execute('SELECT Diary_Name AS names FROM Diary_Management')
    this_con.commit()
    
    all_ds = []

    # Adding all diary names to diaries array
    for result in normal_cursor:
        all_ds.append(result[0].lower())

    return all_ds


def add_screen(mainmenu):
    mainmenu.destroy()
    
    # Creating all buttons, labels and the window
    frame = tk.Tk()

    # Config the window
    frame.config(bg="black")

    #Query for existing diary names, then fill up array with names
    normal_cursor.execute('SELECT Diary_Name AS names FROM Diary_Management')
    this_con.commit()
    
    diaries = get_diaries()

    choose_d_label = tk.Label(frame, text= "Enter Diary Name:", bg="black")
    choose_d_input = tk.Entry(frame, bg="grey", highlightbackground="black")
    result_text = tk.Label(frame, bg="black")
    enter_d_button = tk.Button(frame, text="Choose", command=lambda: diary_chosen(result_text, choose_d_input, diaries,
    frame), highlightbackground="black")
    add_back_button = tk.Button(frame, text="Back to main menu", command=lambda: create_mainmenu_screen(frame), highlightbackground="black")

    # Configuring the window
    frame.title("Add")
    frame.geometry(size)

    # Adding everything to the screen
    choose_d_label.grid(row = 0, column= 0)
    choose_d_input.grid(row = 0, column = 1)
    result_text.grid(row = 0, column= 50)
    enter_d_button.grid(row = 0, column = 2)
    

    
    add_back_button.grid(row = 4, column = 0, pady= 10)

def remove_diary(label, button1, button2 ,window, num_diary):

    # Disable foriegn key checks
    cursor.execute('SET foreign_key_checks = 0')
    # Admin Queries to remove diary from all tables referenced in
    cursor.execute(f'DELETE FROM Databases_Management WHERE Diary_ID = {num_diary}')
    cursor.execute(f'DELETE FROM Diary_Management WHERE Diary_ID = {num_diary}')
    cursor.execute(f'DELETE FROM Server WHERE Diary_ID = {num_diary}')
    cursor.execute(f'DELETE FROM Entry_Management WHERE Diary_ID = {num_diary}')
    cursor.execute(f'DELETE FROM Diary_Catalog WHERE Diary_ID = {num_diary}')
    cursor.execute(f'DELETE FROM Edit_Log WHERE Diary_ID = {num_diary}')
    cursor.execute(f'DELETE FROM Entry_Log WHERE Diary_ID = {num_diary}')


    # Re-enable foreign key checks
    cursor.execute('SET foreign_key_checks = 1')

    admin.commit()


    label.config(text="Diary Deleted.")
    button1.destroy()
    button2.config(command=None)
    window.after(1000, lambda: create_mainmenu_screen(window))



def choose_entry(num_input, text, all_ids, all_labels, all_entries):

    
    # Check for valid inputs
    try:
        id = int(num_input.get())
        num_input.delete(0, 'end')
    except Exception as e:
        text.config(text="Please enter a number")
        return
    if (id not in all_ids or id <= 0):
        text.config(text="ID doesn't exist.")
    else:
        text.config(text="")

        for label in all_labels:
            info = label.cget('text')[8:10]
            info = int(info)

            if (info == id):
                # Get the id to remove the data from the arrays
                rmv_id = all_ids.index(id)

                # Remove foreign key constraint
                cursor.execute('SET foreign_key_checks = 0')

                cursor.execute(f'DELETE FROM Databases_Management WHERE Entry_ID = {id}')

                # If it is not the only one, update table to show other entry if
                if (len(all_ids) != 1):
                    all_ids.pop(rmv_id)
                    
                    new_point = all_ids[0]
                    ## GET the date of that entry
                    cursor.execute(f'SELECT Entry_Date, Entry_Name, Diary_ID FROM Entry_Management WHERE Entry_ID = {new_point}')
                    
                    result = cursor.fetchall()
                    for row in result:
                        date = row["Entry_Date"]
                        name = row["Entry_Name"]
                        id_of_parent = row["Diary_ID"]

                    cursor.execute(f'UPDATE Diary_Management SET Entry_Name = "{name}", Entry_Date = "{date}" WHERE Diary_ID = {id_of_parent}')
                else:
                    # If it is the only one, remove diary
                    cursor.execute(f'DELETE FROM Diary_Management WHERE Entry_ID = {id}')

                # Admin Queries to remove entry from every table it is referenced in.
                cursor.execute(f'DELETE FROM Server WHERE Entry_ID = {id}')
                cursor.execute(f'DELETE FROM Entry_Management WHERE Entry_ID = {id}')
                cursor.execute(f'DELETE FROM Entry_Catalog WHERE Entry_ID = {id}')
                cursor.execute(f'DELETE FROM Edit_Log WHERE Entry_ID = {id}')
                cursor.execute(f'DELETE FROM Entry_Log WHERE Entry_ID = {id}')

                cursor.execute('SET foreign_key_checks = 1')
                admin.commit()
                label.destroy()
                all_labels.remove(label)
                text.config(text=f'Entry {id} removed.')
                
                try:
                    all_ids.pop(rmv_id)
                except:
                    print("X")
                all_entries.pop(rmv_id)


                
        






        

    

def remove_options(place, d_id):
    remove(place)

    # Warning for deleting the only entry of a diary
    warning_label = tk.Label(place, text="WARNING! Deleting the only entry in the diary will result in the removal of the diary.")
    warning_label.grid(row = 1000, column = 0, pady=20)


    normal_cursor.execute(f'SELECT Entry_ID, Entry_Content from Entry_log where diary_Id = {d_id}')
    this_con.commit()

    entry_ids = []
    entries = []
    results = normal_cursor.fetchall()

    for row in results:
        entry_ids.append(row[0])
        entries.append(row[1])

    
    i = 1
    entries_displayed = []

    for entry in entries:
        index = entry_ids[entries.index(entry)]
        temp_label = tk.Label(place, text=f'EntryID:{index}   Entry: {entry}', bg="white", fg="black")
        entries_displayed.append(temp_label)
        temp_label.grid(row = i, column = 0, padx=50)

        i += 1
    

    
    choice_label = tk.Label(place, text="Enter an Entry ID.")
    choice_input = tk.Entry(place)
    problem_label = tk.Label(place)
    choice_button = tk.Button(place, text="Enter", command=lambda: choose_entry(choice_input, problem_label, entry_ids, entries_displayed, entries))

    
    choice_label.grid(row = 0, column = 0)
    choice_input.grid(row = 0, column = 1)
    choice_button.grid(row = 0, column = 2)
    problem_label.grid(row = 0, column = 3)



    

def find_diary(text, diary_entry, screen):
    name = diary_entry.get().lower()
 
    diary_entry.delete(0, 'end')

    ds = get_diaries()
    

    if (name == ''):
        text.config(text="Please fill out field.")
    elif (len(name) > 45):
        text.config(text="Diary Name is too long.")
    elif (name not in ds):
        text.config(text="Diary does not exist.")
    else:
        index = ds.index(name) + 1
        text.config(text="")
        remove(screen)
        
        rmvd_text = tk.Label(screen)
        rmv_e_button = tk.Button(screen, text="Remove an Entry", command=lambda: remove_options(screen, index))
        rmv_d_button = tk.Button(screen, text="Remove Diary", command=lambda: remove_diary(rmvd_text, rmv_d_button, rmv_e_button, screen, index))
        
        

        rmv_d_button.grid(row = 0, column = 0, padx= 20, pady = 50)
        rmv_e_button.grid(row = 0, column = 1, padx= 20)
        rmvd_text.grid(row = 0, column = 20)


    

def delete_screen(mainmenu):
    mainmenu.destroy()
    
    # Window and window configuration
    delete_window = tk.Tk()
    delete_window.title("Delete")
    delete_window.geometry(size)

    # Creating widgets
    find_d_label = tk.Label(delete_window, text="Diary Name")
    find_d_input = tk.Entry(delete_window)
    outcm_text = tk.Label(delete_window)
    find_d_button = tk.Button(delete_window, text="Enter", command=lambda: find_diary(outcm_text, find_d_input, delete_window))

    

    # Back to main menu button
    delete_back_button = tk.Button(delete_window, text="Back to main menu", command=lambda: create_mainmenu_screen(delete_window))
    delete_back_button.grid(row = 100, column = 0)

    # Adding widgets to screen
    find_d_label.grid(row = 0, column = 0)
    find_d_input.grid(row = 0, column = 1)
    find_d_button.grid(row = 0, column = 2)
    outcm_text.grid(row = 0, column = 6)

def update_name(place, edit_entry, elabel, dnum):
    updated = edit_entry.get().strip()

    # Check for valid inputs
    if (updated == ''):
        elabel.config(text="Fill out field")
    elif (len(updated) > 45):
        elabel.config(text="Name is too long")
    else:
        elabel.config(text="")
        # Admin Queries to change all instances where diary name and id is
        cursor.execute(f'UPDATE Databases_Management SET Diary_Name = "{updated}" WHERE Diary_ID = {dnum}')
        cursor.execute(f'UPDATE Diary_Management SET Diary_Name = "{updated}" WHERE Diary_ID = {dnum}')
        cursor.execute(f'UPDATE Entry_Management SET Diary_Name = "{updated}" WHERE Diary_ID = {dnum}')
        cursor.execute(f'UPDATE Diary_Catalog SET Diary_Name = "{updated}" WHERE Diary_ID = {dnum}')
        cursor.execute(f'UPDATE Edit_Log SET Diary_Name = "{updated}" WHERE Diary_ID = {dnum}')

        admin.commit()
        elabel.config(text = 'Diary Updated')
        place.after(1000, lambda: create_mainmenu_screen(place))


def change_dname(window, name, value):
    # Display an input, enter button, and text for error
    edit_input = tk.Entry(window, highlightbackground="#154360", bg="grey")
    edit_input.insert(0, name)

    etext = tk.Label(window, bg="#154360")    
    edit_button = tk.Button(window, text="Enter", command=lambda:update_name(window, edit_input, etext, value),
    highlightbackground="#154360")
    
    etext.grid(row =1, column = 2)
    edit_input.grid(row = 1, column = 0)
    edit_button.grid(row =1, column=1)

def update_entry(screen, textbox, show_text, num, dname, val):
    new_entry = textbox.get(1.0, "end-1c")

    if (new_entry == ''):
        show_text.config(text="Fill in field.")
    elif (len(new_entry) > 200):
        show_text.config(text="Entry is too long")
    else:
        # Databases Man.(UserID, Diary_Name, Diary_ID, Entry_ID, Entry_Date) []
        # Diary Man. (DiaryID, Diary_Name, Entry_Name, Entry_Date, Entry_ID) []
        # Server (User_ID, Diary_Entry, Diary_ID, Entry_ID, Entry_Date) [x]
        # Entry Man. (Entry_ID, Diary_Name, Entry_Name, Entry_Date, Diary_ID) [x]
        # Diary Catalog (Diary_Catalog_ID, Diary_ID, Diary_Catalog_Name, Diary_Catalog_Date, Diary_Name) []
        # Entry Catalog (Entry_Catalog_ID, Entry_ID, Entry_Catalog_Name, Entry_Catalog_Date, Entry_Name)
        # Edit_Log (Diary_Name,  Entry_ID, Diary_ID, Entry_Time, Edit_Comment) []
        # Entry_Log (Entry_ID, Entry_Content, Diary_ID) []
        # Admin Query to update entry entry log and edit log tables

        cursor.execute(f'UPDATE Entry_Log SET Entry_Content = "{new_entry}" WHERE Entry_ID = {num}')
        cursor.execute(f'INSERT INTO Edit_Log VALUE ("{dname}", {num}, {val}, CURRENT_TIME, "Edited")')

        admin.commit()

        screen.after(1000, create_mainmenu_screen(screen))


def send_num(num_input, place, txt, dict_of_e, dname, val):
    enum = num_input.get()

    try:
        enum = int(enum)
    except Exception as e:
        txt.config(text="Enter a number.")
    
    if (enum not in dict_of_e.keys()):
        txt.config(text="Entry doesn't exist")
    else:
        # Clear window
        remove(place)

        edit_text = tk.Text(place, height=10, highlightbackground="#154360", bg="grey")
        edit_text.insert("1.0", dict_of_e[enum])

        status_text = tk.Label(place, bg="#154360")
        submit_change = tk.Button(place, text="Enter", command=lambda: update_entry(place, edit_text, status_text, enum, dname, val),
        highlightbackground="#154360")

        edit_text.grid(row = 0, column= 0)
        submit_change.grid(row = 0, column= 1)
        status_text.grid(row = 0, column=3)



def change_ename(window, num, dname):
    remove(window)

    edict = {}
    normal_cursor.execute(f'SELECT Entry_ID, Entry_Content FROM Entry_Log WHERE Diary_ID = {num}')

    read = normal_cursor.fetchall()
    for row in read:
        edict[row[0]] = row[1]

    this_con.commit()
    
    # Show all entries by making labels and filling content
    a = 0;

    for entry in edict.keys():
        temp = tk.Label(window, text=f'EntryID: {entry}  Entry: {edict[entry]}', bg="#154360")
        temp.grid(row = a, column = 0)

        a += 1

    num_label = tk.Label(window, text="Enter an Entry Number:", bg="#154360")
    num_entry = tk.Entry(window, highlightbackground="#154360", bg="grey")
    ptext = tk.Label(window, bg="#154360")
    send_num_button = tk.Button(window, text="Enter", command=lambda: send_num(num_entry, window, ptext, edict, dname, num), highlightbackground="#154360")

    num_label.grid(row = 0, column=1)
    num_entry.grid(row = 0, column=2)
    send_num_button.grid(row = 0, column=3)
    ptext.grid(row = 0, column =4)

    

def get_num(label, text, ddict, screen):
    value = text.get()
    
    # Check if it is a number
    try:
        value = int(value)
    except Exception as e:
        label.config(text='Enter a number')
        return

    # Check if empty or not in diary nums list (dlist)
    if (value == ''):
        label.config(text="Fill out field")
    elif (value not in ddict.keys()):
        label.config(text="Diary doesn't exist")
    else:
        label.config(text="")
        
        remove(screen)

        # Two buttons to give choice on what to modify
        diary_name = ddict[value]
        diary_button = tk.Button(screen, text="Change Diary Name", command= lambda: change_dname(screen, diary_name, value), highlightbackground="#154360")
        entry_button = tk.Button(screen, text="Change Entry", command=lambda: change_ename(screen, value, diary_name), highlightbackground="#154360")

        diary_button.grid(row = 0, column = 0, pady = 20)
        entry_button.grid(row = 0, column = 1, pady = 20)





def modify_screen(mainmenu):
    mainmenu.destroy()
    
    modify_window = tk.Tk()
    modify_window.title("Modify")
    modify_window.geometry(size)
    modify_window.config(bg="#154360")

    # Fill screen with diaries
    normal_cursor.execute('SELECT Diary_ID, Diary_Name FROM Diary_Management')
    this_con.commit()

    diary_dict = {}
    results = normal_cursor.fetchall()
    for row in results:
        diary_dict[row[0]] = row[1]

    r = 0;
    for key in diary_dict.keys():
        temp = tk.Label(modify_window, text=f'DiaryID: {key}   Name: {diary_dict[key]}', fg="white", width=25, anchor=tk.W, bg="#154360")
        temp.grid(row = r, column = 0)

        r += 1

    # Label and text box for diary num input and label for errors
    input_label = tk.Label(modify_window, text="Enter Diary Number:", bg="#154360")
    input = tk.Entry(modify_window, highlightbackground="#154360")
    problem_text = tk.Label(modify_window, bg="#154360")
    input_label.grid(row = 0, column = 1)
    input.grid(row = 0, column = 2)
    problem_text.grid(row = 0, column = 10)

    # Button for num entry
    submit_num = tk.Button(modify_window, text="Enter", command=lambda: get_num(problem_text, input, diary_dict, modify_window),
    highlightbackground= "#154360")
    submit_num.grid(row = 0, column= 3)

    modify_back_button = tk.Button(modify_window, text="Back to main menu", command=lambda: create_mainmenu_screen(modify_window),
    highlightbackground="#154360")
    modify_back_button.grid(row = 50, column = 0)

def search_d(input, error_text, dict, place):
    diary = input.get()

    try:
        diary = int(diary)
    except Exception as e:
        error_text.config(text="Enter a Number")
    
    if (diary == ''):
        error_text.config(text="Fill out Field.")
    elif (diary not in dict.keys()):
        error_text.config(text="ID Doesn't Exist")
    else:
        remove(place)
        diary_name = dict[diary]
        diary_num = diary

        entry_dict = {}

        # Admin Query to get the entries for the diary
        cursor.execute(f'SELECT Entry_ID, Entry_Content FROM Entry_Log WHERE Diary_ID = {diary}')

        back = cursor.fetchall()
        for row in back:
            entry_dict[row["Entry_ID"]] = row["Entry_Content"]
        
        admin.commit()


        # Display all information
        did_label = tk.Label(place, text=f'DiaryID: {diary_num}', bg="#5E86D1")
        dname_label = tk.Label(place, text=f'Diary Name: {diary_name}', bg="#5E86D1")
        etitle = tk.Label(place, text="Entries", bg="#5E86D1")

        did_label.grid(row = 0, column = 0)
        dname_label.grid(row = 1, column = 0)
        etitle.grid(row = 2, column = 0)


        # loop to show all entries
        b = 3

        for e in entry_dict.keys():
            this_label = tk.Label(place, text=f"EntryID:{e}  Entry: {entry_dict[e]}", anchor=tk.W, bg="#5E86D1")
            this_label.grid(row = b, column = 0)

            b += 1


def search_screen(mainmenu):
    mainmenu.destroy()
    
    search_window = tk.Tk()
    search_window.title("Search")
    search_window.geometry(size)
    search_window.config(bg="#5E86D1")

    # Admin Query to get all the diaries and their id's
    cursor.execute('SELECT Diary_ID, Diary_Name From Diary_Management')

    results = cursor.fetchall()

    dict_of_d = {}

    for row in results:
        dict_of_d[row["Diary_ID"]] = row["Diary_Name"]

    admin.commit()


    j = 0

    for d in dict_of_d.keys():
        new_label = tk.Label(search_window, text=f'DiaryID:{d}  Diary:{dict_of_d[d]}', anchor=tk.W, bg="#5E86D1")
        new_label.grid(row = j, column = 0)

        j += 1

    # Input and enter button
    get_d_label = tk.Label(search_window, text="Enter an ID:", bg="#5E86D1")
    get_d = tk.Entry(search_window, highlightbackground="#5E86D1", bg="grey")
    bad_text = tk.Label(search_window, bg="#5E86D1")
    get_d_button = tk.Button(search_window, text="Enter", command=lambda: search_d(get_d, bad_text, dict_of_d, search_window),
    highlightbackground="#5E86D1")

    get_d_label.grid(row = 0, column = 1)
    get_d.grid(row = 0, column = 2)
    bad_text.grid(row = 0, column = 6)
    get_d_button.grid(row = 0, column = 3)

    search_back_button = tk.Button(search_window, text="Back to main menu", command=lambda: create_mainmenu_screen(search_window), highlightbackground="#5E86D1")
    search_back_button.grid(row = 100, column = 0)

def print_screen(mainmenu):
    mainmenu.destroy()

    print_window = tk.Tk()
    print_window.title("Print")
    print_window.geometry(size)
    print_window.config(bg="#38397E")


    all_diaries = {}

    # Admin Query to get all the diaries
    cursor.execute('SELECT Diary_ID, Diary_Name From Diary_Management')

    results = cursor.fetchall()
    admin.commit()
    # Fill up dict with all diaries
    for row in results:
        all_diaries[row["Diary_ID"]] = row["Diary_Name"]

    r = 0
    c = 0
    for diary in all_diaries.keys():

        
        name_label = tk.Label(print_window, text=f'Diary: {all_diaries[diary]} ID:{diary}', bg="#38397E")
        name_label.grid(row = r, column = c)
        
        entries_label = tk.Label(print_window, text='Entries', bg="#38397E")
        entries_label.grid(row = r + 1, column = c)

        # Admin Query to get entries
        cursor.execute(f'SELECT Entry_ID, Entry_Content FROM Entry_Log WHERE Diary_ID = {diary}')

        edict = {}
        back = cursor.fetchall()
        for row in back:
            edict[row["Entry_ID"]] = row["Entry_Content"]

        admin.commit()
        p = r + 2
        enum = 0
        # Put entries on the screen
        for e in edict.keys():
            enum += 1
            temp = tk.Label(print_window, text=f'EntryID: {e}  Entry: {edict[e]}', bg="#38397E")
            temp.grid(row = p, column = c)

            p += 1
        

        # Move to the next column
        c += 1

        if (c > 2):
            r = p + 1
            c = 0


    admin.commit()
    print_back_button = tk.Button(print_window, text="Back to main menu", command=lambda: create_mainmenu_screen(print_window),
    highlightbackground="#38397E")
    print_back_button.grid(row = 1000, column = 0)





        




window.mainloop()
