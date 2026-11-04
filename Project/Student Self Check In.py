# Import all classes and constants from the tkinter module
from tkinter import *
from datetime import datetime
from tkinter import messagebox
from os import write
import csv
from PIL import ImageTk  
import time
from tkinter import simpledialog
import firebase_admin
from firebase_admin import credentials, db


#OpenAI. (2026). ChatGPT (GPT-5) [Large language model]. Retrieved January 2, 2026, from https://chat.openai.com/

cred = credentials.Certificate("api.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://student-a5554-default-rtdb.firebaseio.com/'
        
    })
#OpenAI. (2026). ChatGPT (GPT-5) [Large language model]. Retrieved January 2, 2026, from https://chat.openai.com/



#-------------------------------------
attempt = 0
max_attempt = 4
LATE_HOUR = 7
LATE_MINUTE = 00

def login():
    global attempt
    student_ids = []
    student_names = []
    if attempt == max_attempt:
        messagebox.showerror('Error', 'You have exceeded maximum number of attempts')
        userid_input.config(state="disabled")
        enter_button.config(state="disabled")
        code.config(state="disabled")
        enter_button.config(state="disabled")
        
        
    with open('student_checkin_updated.csv', 'r') as obj:
        reader = csv.reader(obj)
        next(reader)  # skip header

        for row in reader:
            student_ids.append(int(row[1]))
            student_names.append(row[0])

    student_dict = {student_ids[i]: student_names[i] for i in range(len(student_ids))}

    try:
        #OpenAI. (2026). ChatGPT (GPT-5) [Large language model]. Retrieved January 2, 2026, from https://chat.openai.com/
        user_input = userid_input.get().strip()
        entered_code = code.get().strip()
        #OpenAI. (2026). ChatGPT (GPT-5) [Large language model]. Retrieved January 2, 2026, from https://chat.openai.com/
        #----------------------------------------------------------------------------------

        if user_input == '' or entered_code == " ":
            messagebox.showerror('Error', 'Please fill out both feilds')
            attempt+=1

        if int(user_input) not in student_dict:    
            messagebox.showerror("Error", "Invalid Student ID")
            attempt += 1
            return
        


        #OpenAI. (2026). ChatGPT (GPT-5) [Large language model]. Retrieved January 2, 2026, from https://chat.openai.com/
        correct_code = db.reference("checkin_code").get()
        if correct_code is None:
            messagebox.showerror("Error", "Attendance has not started yet.")
            return

        if entered_code != correct_code:
            messagebox.showerror("Error", "Invalid Check-in Code")
            attempt += 1
            return
        #OpenAI. (2026). ChatGPT (GPT-5) [Large language model]. Retrieved January 2, 2026, from https://chat.openai.com/

        # Success: ID exists and code matches, disbales the input feild is both id and code are correct to prevent multipl logings
            # Logic assisted by ChatGPT (OpenAI, 2026) for Firebase Realtime Database usage

        messagebox.showinfo("Success", f"Welcome {student_dict[int(user_input)]}")
        # ---------------- Firebase Attendance Node ----------------
   
       
        now = datetime.now()
        cutoff_time = now.replace(hour=LATE_HOUR, minute=LATE_MINUTE, second=0, microsecond=0)

       

        status="Present"
        late_pass = None

        if now > cutoff_time:
            conf = messagebox.askyesno("Late", "You are late. Do you have a late pass?")
    

            if conf:
                late_pass = simpledialog.askstring(
            "Late Pass",
            "1 attempt only, make sure to type the correct code"
            "Enter late pass code:",
        
        )     
                    

            correct_late_pass = db.reference("late_pass_code").get()
            


            if (late_pass) == correct_late_pass:
                status = "Excused "
            elif late_pass != correct_late_pass:
                messagebox.showerror("Invalid input, your lare tardy")
                status = "Tardy"
        
    
            
       

        student_id = user_input
        student_name = student_dict[int(user_input)]



        attendance_data = {
            "id": student_id,
            "name": student_name,
            "time": now.strftime("%H:%M:%S"),
            "date": now.strftime("%m/%d/%Y"),
            "status": status
           
            
        }

        db.reference("attendance").child(student_id).set(attendance_data)
        userid_input.config(state="disabled")
        enter_button.config(state="disabled")
        code.config(state="disabled")
        enter_button.config(state="disabled")
        #home.after(500, home.destroy)  # destroy after 0.5 seconds

        
  #--------------------------------------------------------------------      
        
    except ValueError:
        messagebox.showerror('Error', "ID must be a number.")
        attempt += 1
        


home = Tk()
home.title("Student")
home.configure(background="#0B2AA6")

home.geometry('1280x700+50+50')



logFrame = Frame(home, bg = "#0B2AA6")
logFrame.place(x=600,y=150)

logoImage=PhotoImage(file='mill.png')

logo_label = Label(logFrame, image = logoImage, bg="#0B2AA6")
logo_label.grid(row=0,column=0, columnspan=2, pady=10)

user_img=PhotoImage(file = 'id.png' )

user_id = Label(logFrame, image =user_img , text=" Student ID", compound=LEFT, font = ('times new roman', 20),bg="#0B2AA6")

user_id.grid(row=1,column=0, pady=10, padx=10)


userid_input = Entry(logFrame, font =("Verdana",10,"italic"))

userid_input.grid(row=1,column=1, pady=10,padx=10)

enter_button = Button(logFrame, text="Sign In",width=10,font =("Segoe UI",10,"italic"),fg='white',bg='cornflowerblue', activebackground='cornflowerblue', activeforeground='white',cursor='hand2', command=login, 
                relief="raised",
                borderwidth=1)
enter_button.grid(row=4,column=1)

#--------------------------------------------------------------------------


codeimg=PhotoImage(file="code.png")

code_id = Label(logFrame, image = codeimg, text = "Enter Code", compound=LEFT,font = ('times new roman', 20),bg="#0B2AA6")
code_id.grid(row=2,column=0,pady=10,padx=10)

code = Entry(logFrame, font = ("Verdana",10,"italic"))
code.grid(row=2, column=1,pady=10,padx=10)





excused_id = Label(logFrame, image = codeimg, text = "Enter late pass code", compound=LEFT,font = ('times new roman', 20),bg="#0B2AA6")
excused_id.grid(row=3,column=0,pady=10,padx=10)

excused = Entry(
    logFrame,
    font=("Verdana", 10, "italic"),
    state=DISABLED
)
excused.grid(row=3, column=1, pady=10, padx=10)




des = Label(
    logFrame,
    text="Welcome to Millbrook High School",
    font=("Times New Roman", 20),
    bg="#0B2AA6",
    fg="white"
)

des.grid(row=5, column=0, columnspan=2, pady=20)

des2 = Label(
    logFrame,
    text= "Home of the Pioneers",
    font = ("Times New Roman",20),
    bg="#0B2AA6",
    fg = "white"

)

des2.grid(row = 7, column=0, columnspan=2,pady=20 )

after_id = None

def clock():
    global after_id
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%m/%d/%Y")
    time_label.config(text=f"Time: {current_time}\nDate: {current_date}")
    after_id = time_label.after(1000, clock)


time_label = Label(home, font=("Courier", 20, "bold"),fg="white",bg="#0B2AA6", justify=LEFT)
time_label.place(x=5, y=7)
clock()


home.mainloop()
home.after(500, home.destroy)
