from tkinter import *
import time
import ttkthemes
from tkinter import ttk
import random
import firebase_admin
from firebase_admin import credentials, db


from tkinter import messagebox
manage = Tk()

manage.configure(background="#0B2AA6")

manage.geometry("1280x700+50+50")
manage.title("Teacher")


#OpenAI. (2026). ChatGPT (GPT-5) [Large language model]. Retrieved January 2, 2026, from https://chat.openai.com/

cred = credentials.Certificate("api.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://student-a5554-default-rtdb.firebaseio.com/'
})

#OpenAI. (2026). ChatGPT (GPT-5) [Large language model]. Retrieved January 2, 2026, from https://chat.openai.com/










# --- Clock ---
after_id = None




def clock():
    global after_id
    current_time = time.strftime("%I:%M %p")
    current_date = time.strftime("%m/%d/%Y")
    time_label.config(text=f"Time: {current_time}\nDate: {current_date}")
    after_id = time_label.after(1000, clock)

time_label = Label(manage, font=("Courier", 20, "bold"), justify=LEFT,bg="#0B2AA6",pady=20)
time_label.place(x=5, y=-7)
clock()

# --- Student slider ---
student = "Students"
count = 0
text = ""

def slider():
    global count, text
    if count == len(student):
        count = 0
        text = ""
    text += student[count]
    studentslider.config(text=text)
    count += 1
    studentslider.after(600, slider)

studentslider = Label(manage, text="", font=("Courier", 40, "italic bold"), width=30,bg='#0B2AA6',fg='white')
studentslider.place(x=300, y=50)  # moved y down to avoid overlap
slider()


lframe = Frame(
    manage,
    bg="#162A5C",
    bd=3,
    relief=RIDGE
)
lframe.place(x=0, y=100, width=300, height=600)


logo=PhotoImage(file="mill.png")
logo_label = Label(lframe,image=logo,bg='#162A5C')
logo_label.grid(row=0,column=0)



style = ttk.Style()
style.theme_use('clam')


style.configure(
    "Tech.TButton",
    font=("Segoe UI", 11, "bold"),
    padding=10,
    background="#1f6aa5",
    foreground="white",
    borderwidth=0
)

style.map(
    "Tech.TButton",
    background=[("active", "#155a8a")]
)


def pass_gen():
    pas_code = str(random.randint(100 , 500))  # Uses the random function to generate random numbers 1000 - 2000, I converted it to a string because th code input box is a str
    db.reference("late_pass_code").set(pas_code)#Stores the generated code in that node, If the node does not exist → Firebase creates it,If it exists → Firebase replaces the old code
    messagebox.showinfo("Code Generated", f"Pass Code: {pas_code}")


pas = ttk.Button(lframe, text = 'Generate Pass', style = "Tech.TButton", command=pass_gen)# Teacher can add students having trouble getting in

pas.grid(row = 1, column = 0, pady = 20)


def end(): #This function resets/ends the attendance
        # Logic assisted by ChatGPT (OpenAI, 2026) for Firebase Realtime Database usage

    conf = messagebox.askyesno( "End Attendance", "Do you want to end the attendance for today?") # End or dont end

    if conf: # if yes this lines exectues, if not, nothing heppens
        db.reference("attendance").delete() #Goes to the fire base node and deletes everything there
        table_info.delete(*table_info.get_children()) #Deletes everthing shown on the table
        messagebox.showinfo("Attendance", "You have reset the attendance") #Confrimation box



end_attendance = ttk.Button(lframe, text = 'End Attendance', style = "Tech.TButton",command=end)# Teacher can add students having trouble getting in

end_attendance.grid(row = 2, column = 0, pady = 20)


#OpenAI. (2026). ChatGPT (GPT-5) [Large language model]. Retrieved January 2, 2026, from https://chat.openai.com/

def generate_code():
    code = str(random.randint(1000 , 2000))  # Uses the random function to generate random numbers 1000 - 2000, I converted it to a string because th code input box is a str
    db.reference("checkin_code").set(code)#Stores the generated code in that node, If the node does not exist → Firebase creates it,If it exists → Firebase replaces the old code


    messagebox.showinfo("Code Generated", f"Check-in Code: {code}")


gen_code = ttk.Button(lframe, text = 'Generate Code', style = "Tech.TButton", command= generate_code)# Teacher can add students having trouble getting in

gen_code.grid(row = 3, column = 0, pady = 20)
#OpenAI. (2026). ChatGPT (GPT-5) [Large language model]. Retrieved January 2, 2026, from https://chat.openai.com/


export = ttk.Button(lframe, text="Export Students",style = "Tech.TButton")
export.grid(row=4, column=0,pady=20)




rframe=Frame(manage,bg="#155a8a")
rframe.place(x=450,y=190,width=800,height=600)

scrollx = Scrollbar(rframe,orient=HORIZONTAL)
scrolly = Scrollbar(rframe,orient=VERTICAL)

scrollx.pack(side=BOTTOM,fill=X)

scrolly.pack(side=RIGHT,fill=Y)



table_info = ttk.Treeview(rframe,columns=('ID','Name','Time','Date','Status'),xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
scrollx.config(command=table_info.xview)
scrolly.config(command=table_info.yview)

table_info.pack(fill=BOTH,expand=1)

table_info.heading('ID', text = "Student ID")
table_info.heading('Name', text = "Student Name")
table_info.heading('Time', text = "Time")
table_info.heading('Date', text = "Date",)
table_info.heading('Status', text = "Status",)





table_info.config(show="headings")


def load_attendance():
    # Clear the table first
    table_info.delete(*table_info.get_children())

    attendance = db.reference("attendance").get()

    if attendance:
        for student_id, info in attendance.items():
            table_info.insert(
                "",
                END,
                values=(
                    info["id"],
                    info["name"],
                    info["time"],
                    info["date"],
                    info.get("status", "Unknown")
                    


                )
            )
def refresh_attendance():
    load_attendance()
    manage.after(3000, refresh_attendance)  # refresh every 3 seconds

refresh_attendance()





manage.mainloop()
