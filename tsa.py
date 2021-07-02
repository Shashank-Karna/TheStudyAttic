from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from functools import partial
import mysql.connector
from tkinter import messagebox
import re
import webbrowser as wb
import smtplib
from email.message import EmailMessage
import math, random

global_name = 'Akash'
global_year = ''
global_branch = ''
global_type = ''
global_sem = 0
global_sub = ''
OTP = ""
change_pass_email = ''

class hoverButton(Frame):
    def __init__(self, master, **kw):
        Button.__init__(self, master, **kw)
        self.defaultbackground = self["bg"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["bg"] = self["activebackground"]

    def on_leave(self, e):
        self["bg"] = self.defaultbackground


def openBranch(button, win):
    if global_name == '':
        messagebox.showerror('Login', 'Action not Allowed!\nPlease Login first to access the resources.')
    else:
        if win == 'home':
            home.withdraw()
        elif win == 'syllabus':
            syllabus.withdraw()
        elif win == 'contact':
            contact.withdraw()
        elif win == 'branch':
            branch.withdraw()
        elif win == 'pdfs':
            pdfs.withdraw()

        brw.eb_btn.configure(fg="salmon4")
        brw.qp_btn.configure(fg="salmon4")
        branch.deiconify()
        global global_type
        if button == 'eb':
            brw.eb_btn.configure(fg="black")
            global_type = 'Ebook'
        elif button == 'qp':
            brw.qp_btn.configure(fg="black")
            global_type = 'Qpaper'


def openHome(win):
    if win == 'branch':
        branch.withdraw()
    elif win == 'contact':
        contact.withdraw()
    elif win == 'syllabus':
        syllabus.withdraw()
    elif win == 'pdfs':
        pdfs.withdraw()
    home.deiconify()


def openLogin():
    home.withdraw()
    login.deiconify()


def openRegister():
    login.withdraw()
    reg.deiconify()


def openSyllabus(win):
    if global_name == '':
        messagebox.showerror('Login', 'Action not Allowed!\nPlease Login first to access the resources.')
    else:
        global global_type
        if win == 'home':
            home.withdraw()
        elif win == 'contact':
            contact.withdraw()
        elif win == 'branch':
            branch.withdraw()
        elif win == 'pdfs':
            pdfs.withdraw()
        syllabus.deiconify()
        global_type = 'Syllabus'


def go_back(win):
    if win == 'reg':
        reg.withdraw()
        home.deiconify()
    elif win == 'login':
        login.withdraw()
        home.deiconify()


def openContact(win):
    if win == 'home':
        home.withdraw()
    elif win == 'branch':
        branch.withdraw()
    elif win == 'syllabus':
        syllabus.withdraw()
    elif win == 'pdfs':
        pdfs.withdraw()
    contact.deiconify()


def openPdf(name):
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="rosemary@21", database="tsa")
        cursor = con.cursor()
        sql_query = "select pdf_link from syllabus where pdf_name = '%s'"
        cursor.execute(sql_query % (name))
        plink = cursor.fetchone()
        wb.open_new(plink[0])

    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()


def openPdfT(name):
    global global_sem, global_sub, global_branch
    print(global_branch)
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="rosemary@21", database="tsa")
        cursor = con.cursor()
        if global_year == 'FE':
            sql_query = "select pdf_link from FE where (pdf_name = '%s' and sem = %d and sub = '%s')"
        else:
            sql_query = "select pdf_link from " + global_branch + " where (pdf_name = '%s' and sem = %d and sub = '%s')"
        cursor.execute(sql_query % (name, global_sem, global_sub))
        plink = cursor.fetchone()
        wb.open_new(plink[0])

    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()


def showSyllabus(event):
    global global_branch
    global_branch = event.widget.get()
    con = None
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="rosemary@21", database="tsa")
        cursor = con.cursor()
        sql_query_fe = "select pdf_name from syllabus where branch = 'FE'"
        cursor.execute(sql_query_fe)
        datafe = cursor.fetchone()

        sql_query_ex = "select pdf_name from syllabus where branch = '%s'"
        cursor.execute(sql_query_ex % (global_branch))
        dataex = cursor.fetchall()
        dataex1 = [dataex[0][0], dataex[1][0], dataex[2][0]]
        syllabus_pdf = list(datafe) + dataex1

        x = 50
        y = 300 - 70
        for i in range(len(syllabus_pdf)):
            if i % 2 == 0:
                x = 50
                y = y + 70
            else:
                x = x + 500
            bt = hoverButton(syllabus, text=syllabus_pdf[i], fg='black', bd=2, activebackground='salmon',
                             relief='groove', font=('Constantia', 15, 'bold'),
                             command=partial(openPdf, syllabus_pdf[i])).place(x=x, y=y, width=450, height=60)

    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()


def saveDetails():
    con = None
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="rosemary@21", database="tsa")
        cursor = con.cursor()
        sql_query = "insert into student (fname, lname, college, branch, year, email, phone_no, password) values(%s,%s,%s,%s,%s,%s,%s,%s)"

        fname = rw.firstName_entry.get()
        lname = rw.lastName_entry.get()
        clg = rw.college_entry.get()
        branch = rw.branch_entry.get()
        year = rw.year_entry.get()
        email = rw.email_entry.get()
        phone = rw.phone_entry.get()
        passw = rw.pass_entry.get()

        em_check = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        result = re.search(em_check, email)

        details = (fname, lname, clg, branch, year, email, phone, passw)
        all_ok = True
        for info in details:
            if len(info) == 0:
                all_ok = False
                break

        if all_ok:
            if result is None:
                messagebox.showerror('Incorrect Credentials', 'Please enter VALID Email address.')
                rw.email_entry.delete(0, 'end')
                rw.email_entry.focus()
            else:
                cursor.execute(sql_query, details)
                con.commit()
                messagebox.showinfo('Registeration Successful',
                                    'Welcome ' + fname + '.\nPlease Login now to proceed further.')
                reg.withdraw()
                login.deiconify()

        else:
            messagebox.showwarning('Incomplete Details', 'Please enter all the details correctly to proceed further.')

    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()


def verifyDetails():
    con = None
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="rosemary@21", database="tsa")
        cursor = con.cursor()
        username = lw.text_email.get()
        password = lw.text_pass.get()
        sql_query = "select fname,password from student where email = '%s'"
        cursor.execute(sql_query % (username))
        data = cursor.fetchone()

        em_check = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        result = re.search(em_check, username)
        if result is not None:
            if data is None:
                messagebox.showwarning('Login Unsuccessful', 'Could not find account with this email address.')
            elif data[1] != password:
                messagebox.showerror('Incorrect Credentials', 'Please check your password.')
            else:
                global global_name
                global_name = data[0]
                login.withdraw()
                home.deiconify()
                hw.login_btn.configure(text=data[0], fg='black', command='')
                brw.login_btn.configure(text=data[0], fg='black')
                cw.login_btn.configure(text=data[0], fg='black', command='')
                sw.login_btn.configure(text=data[0], fg='black')
                hw.logout_btn.place(x=220, y=470, width=120)
                lw.text_email.delete(0, END)
                lw.text_pass.delete(0, END)
        else:
            messagebox.showerror('Incorrect Email', 'Please enter a valid Email Address.')
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()


def sendMsg():
    name = cw.name_entry.get()
    email = cw.email_entry.get()
    text = cw.text_entry.get("1.0", 'end-1c')

    em_check = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    result = re.search(em_check, email)

    msg_details = (name, email, text)
    all_ok = True
    for info in msg_details:
        if len(info) == 0:
            all_ok = False
            break

    if all_ok:
        if result is not None:
            msg = EmailMessage()
            msg.set_content(text)

            msg['Subject'] = 'Contact Request from ' + name
            msg['From'] = "thestudyattic705@gmail.com"
            msg['To'] = "thestudyattic705@gmail.com"

            # Send the message via our own SMTP server.
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("thestudyattic705@gmail.com", "tsa705@sar")
            server.send_message(msg)
            server.quit()
            messagebox.showinfo('Successful', 'Your Request has been sent successfully.\nThank you for contacting!')
        else:
            messagebox.showerror('Incorrect Email', 'Please enter a valid Email Address.')
        cw.name_entry.delete(0, END)
        cw.email_entry.delete(0, END)
        cw.text_entry.delete("1.0", 'end')
    else:
        messagebox.showwarning('Incomplete Details', 'Please enter all the details correctly to proceed further.')


def logoutf():
    global global_name, global_sub, global_year, global_branch, global_type, global_sem
    global_name = ''
    global_year = ''
    global_branch = ''
    global_type = ''
    global_sem = 0
    global_sub = ''
    messagebox.showinfo('Logout', 'Logout Successful!')
    hw.login_btn.configure(text='Login', fg='salmon4', command=openLogin)
    hw.logout_btn.place_forget()


def forgotPassword():
    forget.deiconify()


def send_otp():
    email = fpw.email_ent.get()
    em_check = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    result = re.search(em_check, email)

    con = None
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="rosemary@21", database="tsa")
        cursor = con.cursor()
        sql_query = "select email from student where email = '%s'"
        cursor.execute(sql_query % (email))
        data = cursor.fetchone()

        if result is not None:
            if data is None:
                messagebox.showwarning('Unsuccessful',
                                       'Could not find account with this email address.\n Please Register first.')
            else:
                global change_pass_email
                change_pass_email = email
                fpw.root.geometry("400x280+450+200")
                fpw.otp_lbl.place(x=155, y=140)
                fpw.otp_ent.place(x=100, y=170, width=200)
                digits = "0123456789"
                global OTP
                # for a 4 digit OTP we are using 4 in range
                for i in range(4):
                    OTP += digits[math.floor(random.random() * 10)]
                messagebox.showinfo('Successful', 'OTP has been sent to your registered email id.')
                msg = EmailMessage()
                msg.set_content('Your One Time Password (OTP) for changing the password is ' + OTP)
                msg['Subject'] = 'Change Password Request'
                msg['From'] = "thestudyattic705@gmail.com"
                msg['To'] = data[0]

                # Send the message via our own SMTP server.
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login("thestudyattic705@gmail.com", "tsa705@sar")
                server.send_message(msg)
                server.quit()

        else:
            messagebox.showerror('Incorrect Email', 'Please enter a valid Email Address.')

    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()


def confirmOTP():
    otp = fpw.otp_ent.get()
    global OTP
    if otp == OTP:
        forget.withdraw()
        new_pass.deiconify()
    else:
        messagebox.showerror('Incorrect OTP', 'Please enter correct OTP.')

def change_pass():
    password = npw.new_pass_ent.get()
    rpassword = npw.rpass_ent.get()

    con = None
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="rosemary@21", database="tsa")
        cursor = con.cursor()
        sql_query = "update student set password = '%s' where email = '%s'"
        if password == rpassword:
            cursor.execute(sql_query % (rpassword,change_pass_email))
            con.commit()
            messagebox.showinfo('Password Changed', 'Password changed successfully. \nPlease login with new password.')
            new_pass.withdraw()
        else:
            messagebox.showerror('Mismatch','Passwords did not match. \nRe-enter passwords.')
            npw.new_pass_ent.delete(0, END)
            npw.rpass_ent.delete(0, END)
    except Exception as e:
        print(e)
    finally:
        if con is not None:
            con.close()

def selectBranch(event):
    global global_branch
    global_branch = event.widget.get()
    brw.yearcombo['state'] = "normal"


def selectYear(event):
    global global_year
    global_year = event.widget.get()
    if global_year == 'FE':
        sem = ['Semester 1', 'Semester 2']
    elif global_year == 'SE':
        sem = ['Semester 3', 'Semester 4']
    elif global_year == 'TE':
        sem = ['Semester 5', 'Semester 6']
    elif global_year == 'BE':
        sem = ['Semester 7', 'Semester 8']
    brw.semcombo['value'] = sem
    brw.semcombo['state'] = "normal"


def selectSem(event):
    global global_sem
    sem = event.widget.get()
    global_sem = int(sem[9])
    print(global_sem)
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="rosemary@21", database="tsa")
        cursor = con.cursor()
        if global_year == 'FE':
            sql_query = "select distinct sub from FE where sem = %d and typ = '%s'"
        else:
            sql_query = "select distinct sub from " + global_branch + " where sem = %d and typ = '%s'"
        subjects = []
        cursor.execute(sql_query % (global_sem, global_type))
        while True:
            row = cursor.fetchone()
            if row == None:
                break
            subjects.append(row[0])

        brw.subcombo['value'] = subjects
        brw.subcombo['state'] = "normal"

    except:
        print('Connection unsuccessful')
    finally:
        if con is not None:
            con.close()


def selectSub(event):
    global global_sub
    global_sub = event.widget.get()


def searchPdf():
    search_filter = (global_type, global_branch, global_sub, global_year)
    print(global_branch)
    all_ok = True
    for info in search_filter:
        if len(info) == 0:
            all_ok = False
            break
    else:
        if global_sem == 0:
            all_ok = False

    if all_ok:
        try:
            con = mysql.connector.connect(host="localhost", user="root", password="rosemary@21", database="tsa")
            cursor = con.cursor()
            if global_year == 'FE':
                sql_query = "select pdf_name from FE where (typ = '%s' and sem = %d and sub = '%s')"
            else:
                sql_query = "select pdf_name from " + global_branch + " where (typ = '%s' and sem = %d and sub = '%s')"
            pdf_lst = []
            cursor.execute(sql_query % (global_type, global_sem, global_sub))
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                pdf_lst.append(row[0])

            x = 50
            y = 220 - 70
            for i in range(len(pdf_lst)):
                if i % 2 == 0:
                    x = 50
                    y = y + 70
                else:
                    x = x + 500
                bt = hoverButton(pdfs, text=pdf_lst[i], fg='black', bd=2, activebackground='salmon',
                                 relief='groove', font=('Ebrima', 15, 'bold'),
                                 command=partial(openPdfT, pdf_lst[i])).place(x=x, y=y, width=450, height=60)

            branch.withdraw()
            pdfs.deiconify()

        except:
            print('Connection unsuccessful')
        finally:
            if con is not None:
                con.close()

    else:
        messagebox.showwarning('Incomplete Details', 'Please select all the fields to proceed further.')


class HomeW:
    def __init__(self, root):
        self.root = root
        self.root.title("The Study Attic")
        self.root.geometry("1100x600+100+20")
        p1 = ImageTk.PhotoImage(file='images/university_cap.ico')
        self.root.iconphoto(False, p1)
        self.root.resizable(False, False)

        frame = Frame(self.root, bd=1)
        frame.place(x=0, y=0, width=1100, height=38)

        f = ("Rockwell", 15)
        home_btn = Button(frame, text='Home', font=f, bd=0, fg='black').place(x=20, y=2)
        eb_btn = Button(frame, text='EBooks', font=f, bd=0, fg='salmon4',
                        command=partial(openBranch, 'eb', 'home')).place(x=99, y=2)
        qp_btn = Button(frame, text='QPapers', font=f, bd=0, fg='salmon4',
                        command=partial(openBranch, 'qp', 'home')).place(x=191, y=2)
        sy_btn = Button(frame, text='Syllabus', font=f, bd=0, fg='salmon4',
                        command=partial(openSyllabus, 'home')).place(x=300, y=2)
        contact_btn = Button(frame, text='Contact Us', font=f, bd=0, fg='salmon4',
                             command=partial(openContact, 'home')).place(x=406, y=2)

        self.bg_img = ImageTk.PhotoImage(file='images/person.png')
        lbl = Label(frame, image=self.bg_img).place(x=960, y=2)
        self.login_btn = Button(frame, text='Login', font=f, bd=0, fg='salmon4', command=openLogin)
        self.login_btn.place(x=1000, y=2)

        c = Canvas(self.root)
        c.place(x=0, y=40, width=1100, height=600)
        self.myimg = Image.open('images/globe-graduation-cap.jpg')
        self.myimg = self.myimg.resize((1100, 565), Image.ANTIALIAS)
        '''myimg = myimg.resize((1400, 750), Image.ANTIALIAS)'''
        self.image = ImageTk.PhotoImage(self.myimg)
        c.create_image(550, 280, image=self.image)

        f1 = ("Rockwell", 45)
        c.create_text(300, 200, text="THE STUDY ATTIC", fill="black", font=f1)
        c.create_text(230, 270, text="Study Hard ,", fill="black",
                      font=('Lucida Handwriting', 31, 'italic', 'overstrike'))
        c.create_text(300, 325, text="Study SMART !", fill="black", font=('Lucida Handwriting', 31, 'italic'))
        self.logout_btn = Button(root, text='Logout', font=('Cambria', 18), bg='black', fg='white', command=logoutf)


class LoginW:
    def __init__(self, root):
        self.root = root
        self.root.title("The Study Attic")
        self.root.geometry("1100x600+100+20")
        p1 = ImageTk.PhotoImage(file='images/university_cap.ico')
        self.root.iconphoto(False, p1)
        self.root.resizable(False, False)

        self.bg = ImageTk.PhotoImage(file="images/register_bg.webp")
        self.bf_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        Login_frame = Frame(self.root, bg="white")
        Login_frame.place(x=350, y=80, height="450", width="400")

        title = Label(Login_frame, text="Login", font=("constantia", 32, 'bold'), bg="white", fg="salmon3").place(x=145,
                                                                                                                  y=15)

        back_btn = Button(self.root, text="< Back", font=("constantia", 15, "bold"), bg="white", fg="black", width=10,
                          bd=0, command=partial(go_back, 'login')).place(x=40, y=15)
        lbl_email = Label(Login_frame, text="Email ID", font=("constantia", 15), bg="white").place(x=50, y=100)
        self.text_email = Entry(Login_frame, font=("Arial", 14), bg="light gray")
        self.text_email.place(x=50, y=130, width=300, height=35)

        lbl_pass = Label(Login_frame, text="Password", font=("constantia", 15), bg="white").place(x=50, y=185)
        self.text_pass = Entry(Login_frame, show='*', font=("constantia", 15), bg="light gray")
        self.text_pass.place(x=50, y=215, width=300, height=35)

        forgot_btn = Button(Login_frame, text="Forgot Password?", font=("constantia", 12, 'bold', 'underline'),
                            bg="white", fg=("salmon3"), bd=0, cursor='hand2', command=forgotPassword).place(x=50, y=255)

        self.Login_btn = Button(self.root, text="Login", font=("constantia", 15), fg="white", bg=("salmon3"),
                                cursor='hand2', command=verifyDetails)
        self.Login_btn.place(x=450, y=395, width=200)

        new_btn = Button(Login_frame, text="Don't have an account? Register now", font=("constantia", 12, "bold"),
                         bg="white", fg=("salmon3"), bd=0, cursor='hand2', command=openRegister).place(x=50, y=370)


class Forget_passW:
    def __init__(self, root):
        self.root = root
        self.root.title("Change Password")
        self.root.geometry("400x180+450+200")
        p1 = ImageTk.PhotoImage(file='images/university_cap.ico')
        self.root.iconphoto(False, p1)
        self.root.resizable(False, False)

        email_lbl = Label(root, text='Email ID:', font=("constantia", 13)).place(x=155, y=20)
        self.email_ent = Entry(root, font=("Arial", 12), bg="white")
        self.email_ent.place(x=30, y=50, width=330)
        otp_btn = Button(root, text='Send OTP', font=("Cambria", 11, 'bold'), fg='white', bg='black',
                         command=send_otp).place(x=140, y=90, width=120)

        self.otp_lbl = Label(root, text='Enter OTP:', font=("constantia", 13))
        self.otp_ent = Entry(root, font=("Arial", 12), bg="white")
        confirm_btn = Button(root, text='Confirm', font=("Cambria", 11, 'bold'), fg='white', bg='black',
                             command=confirmOTP).place(x=140, y=210, width=120)


class New_passW:
    def __init__(self, root):
        self.root = root
        self.root.title("Change Password")
        self.root.geometry("400x240+450+240")

        p1 = ImageTk.PhotoImage(file='images/university_cap.ico')
        self.root.iconphoto(False, p1)
        self.root.resizable(False, False)
        new_pass_lbl = Label(self.root, text = "New password: ", font = ("constantia", 13)).place(x=30, y=20)
        self.new_pass_ent = Entry(self.root, show = "*", font = ("constantia", 13))
        self.new_pass_ent.place(x=30, y=50, width=330)
        rpass_lbl = Label(self.root, text="Re-enter New password: ", font=("constantia", 13)).place(x=30, y=100)
        self.rpass_ent = Entry(self.root, show="*", font=("constantia", 13))
        self.rpass_ent.place(x=30, y=130, width=330)
        ok_btn = Button(self.root, text="OK", font=("Cambria", 11, 'bold'), fg='white', bg='black', command=change_pass).place(x=140,y=180, width=120)


class Register_wd:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("1100x600+100+20")
        p1 = ImageTk.PhotoImage(file='images/university_cap.ico')
        self.root.iconphoto(False, p1)
        self.root.resizable(False, False)

        self.bg = ImageTk.PhotoImage(file="images/register_bg.webp")
        self.bf_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        Register_frame = Frame(self.root, bg="white")
        Register_frame.place(x=220, y=60, height="480", width="670")

        title = Label(Register_frame, text="Register", font=("constantia", 32, 'bold'), bg="white", fg="salmon3").place(
            x=250, y=8)

        back_btn = Button(self.root, text="< Back", font=("constantia", 15, "bold"), bg="white", fg="black", width=10,
                          bd=0, command=partial(go_back, 'reg')).place(x=40, y=15)

        firstName_lbl = Label(Register_frame, text="First Name", font=("constantia", 15), bg="white").place(x=40, y=90)
        self.firstName_entry = Entry(Register_frame, font=("constantia", 15), bg="white", fg="grey")
        self.firstName_entry.place(x=40, y=120)

        lastName_lbl = Label(Register_frame, text="Last Name", font=("constantia", 15), bg="white").place(x=400, y=90)
        self.lastName_entry = Entry(Register_frame, font=("constantia", 15), bg="white", fg="grey")
        self.lastName_entry.place(x=400, y=120)

        college_lbl = Label(Register_frame, text="College", font=("constantia", 15), bg="white").place(x=40, y=160)
        self.college_entry = Entry(Register_frame, font=("constantia", 15), bg="white", fg="grey", width="53")
        self.college_entry.place(x=40, y=190)

        branch_lbl = Label(Register_frame, text="Branch", font=("constantia", 15), bg="white").place(x=40, y=230)
        self.branch_entry = Entry(Register_frame, font=("constantia", 15), bg="white", fg="grey")
        self.branch_entry.place(x=40, y=260)

        year_lbl = Label(Register_frame, text="Year", font=("constantia", 15), bg="white").place(x=400, y=230)
        self.year_entry = Entry(Register_frame, font=("constantia", 15), bg="white", fg="grey")
        self.year_entry.place(x=400, y=260)

        email_lbl = Label(Register_frame, text="Email", font=("Contantia", 15), bg="white").place(x=40, y=300)
        self.email_entry = Entry(Register_frame, font=("Arial", 14), bg="white", fg="grey", width="53")
        self.email_entry.place(x=40, y=330)

        phone_lbl = Label(Register_frame, text="Phone", font=("constantia", 15), bg="white").place(x=40, y=370)
        self.phone_entry = Entry(Register_frame, font=("Arial", 13), bg="white", fg="grey")
        self.phone_entry.place(x=40, y=400)

        pass_lbl = Label(Register_frame, text="Password", font=("constantia", 15), bg="white").place(x=400, y=370)
        self.pass_entry = Entry(Register_frame, show='*', font=("constantia", 15), bg="white", fg="grey")
        self.pass_entry.place(x=400, y=400)
        reg_button = Button(self.root, text="Register", font=("constantia", 15, "bold"), bg="salmon3", fg="white",
                            width=15, bd=0, command=saveDetails).place(x=450, y=520)


class BranchW:
    def __init__(self, root):
        self.root = root
        self.root.title("The Study Attic")
        self.root.geometry("1100x600+100+20")
        p1 = ImageTk.PhotoImage(file='images/university_cap.ico')
        self.root.iconphoto(False, p1)
        self.root.resizable(False, False)

        frame = Frame(self.root, bd=1)
        frame.place(x=0, y=0, width=1100, height=38)

        f = ("Rockwell", 15)
        home_btn = Button(frame, text='Home', font=f, bd=0, fg='salmon4', command=partial(openHome, 'branch')).place(
            x=20, y=2)
        self.eb_btn = Button(frame, text='EBooks', font=f, bd=0, fg='salmon4',
                             command=partial(openBranch, 'eb', 'branch'))
        self.eb_btn.place(x=99, y=2)
        self.qp_btn = Button(frame, text='QPapers', font=f, bd=0, fg='salmon4',
                             command=partial(openBranch, 'qp', 'branch'))
        self.qp_btn.place(x=191, y=2)
        self.sy_btn = Button(frame, text='Syllabus', font=f, bd=0, fg='salmon4',
                             command=partial(openSyllabus, 'branch'))
        self.sy_btn.place(x=300, y=2)
        contact_btn = Button(frame, text='Contact Us', font=f, bd=0, fg='salmon4',
                             command=partial(openContact, 'branch')).place(x=406, y=2)

        self.bg_img = ImageTk.PhotoImage(file='images/person.png')
        lbl = Label(frame, image=self.bg_img).place(x=962, y=2)
        self.login_btn = Button(frame, text='Login', font=f, bd=0, fg='salmon4')
        self.login_btn.place(x=1000, y=2)

        self.bg = ImageTk.PhotoImage(file="images/bookcases.jpg")
        bf_image = Label(self.root, image=self.bg).place(x=0, y=38, relwidth=1, relheight=1)
        Brframe = Frame(self.root, bg="white")
        Brframe.place(x=250, y=80, height="480", width="580")
        f1 = ("Constantia", 15)
        branch_lbl = Label(Brframe, text="Branch", font=f1, bg='white').place(x=40, y=40)
        branches = ['Computer', 'IT', 'EXTC', 'Chemical', 'Mechanical']
        self.brcombo = ttk.Combobox(Brframe, value=branches, font=f1)
        self.brcombo.place(x=40, y=80, width=500, height=30)
        self.brcombo.bind("<<ComboboxSelected>>", selectBranch)
        Brframe.option_add('*TCombobox*Listbox.font', ("Calibri", 15))

        year_lbl = Label(Brframe, text="Year", font=f1, bg='white').place(x=40, y=130)
        years = ['FE', 'SE', 'TE', 'BE']
        self.yearcombo = ttk.Combobox(Brframe, value=years, state="disabled", font=f1)
        self.yearcombo.place(x=40, y=170, width=500, height=30)
        self.yearcombo.bind("<<ComboboxSelected>>", selectYear)

        sem_lbl = Label(Brframe, text="Semester", font=f1, bg='white').place(x=40, y=220)
        self.semcombo = ttk.Combobox(Brframe, state="disabled", font=("Calibri", 15))
        self.semcombo.place(x=40, y=260, width=500, height=30)
        self.semcombo.bind("<<ComboboxSelected>>", selectSem)

        sub_lbl = Label(Brframe, text="Subject", font=f1, bg='white').place(x=40, y=310)
        self.subcombo = ttk.Combobox(Brframe, state="disabled", font=("Calibri", 15))
        self.subcombo.place(x=40, y=350, width=500, height=30)
        self.subcombo.bind("<<ComboboxSelected>>", selectSub)

        self.submit = Button(self.root, text='Submit', font=f1, bg='salmon3', fg='white', command=searchPdf).place(
            x=450, y=500, width=200)


class SyllabusW:
    def __init__(self, root):
        self.root = root
        self.root.title("The Study Attic")
        self.root.geometry("1100x600+100+20")
        p1 = ImageTk.PhotoImage(file='images/university_cap.ico')
        self.root.iconphoto(False, p1)
        self.root.resizable(False, False)

        frame = Frame(self.root, bd=1)
        frame.place(x=0, y=0, width=1100, height=38)

        f = ("Rockwell", 15)
        home_btn = Button(frame, text='Home', font=f, bd=0, fg='salmon4', command=partial(openHome, 'syllabus')).place(
            x=20, y=2)
        eb_btn = Button(frame, text='EBooks', font=f, bd=0, fg='salmon4',
                        command=partial(openBranch, 'eb', 'syllabus')).place(x=99, y=2)
        qp_btn = Button(frame, text='QPapers', font=f, bd=0, fg='salmon4',
                        command=partial(openBranch, 'qp', 'syllabus')).place(x=191, y=2)
        sy_btn = Button(frame, text='Syllabus', font=f, bd=0, fg='black').place(x=300, y=2)
        contact_btn = Button(frame, text='Contact Us', font=f, bd=0, fg='salmon4',
                             command=partial(openContact, 'syllabus')).place(x=406, y=2)

        self.bg_img = ImageTk.PhotoImage(file='images/person.png')
        lbl = Label(frame, image=self.bg_img).place(x=960, y=2)
        self.login_btn = Button(frame, text='Login', font=f, bd=0, fg='salmon4')
        self.login_btn.place(x=1000, y=2)

        c = Canvas(self.root)
        c.place(x=0, y=40, width=1100, height=150)
        self.image = ImageTk.PhotoImage(file='images/bss.png')
        c.create_image(570, 60, image=self.image)
        f1 = ("Rockwell", 45)
        c.create_text(170, 60, text="SYLLABUS", fill="white", font=f1)

        branch_lbl = Label(self.root, text='Select Branch :', fg='black', font=("constantia", 15, 'bold')).place(x=250,
                                                                                                                 y=190)
        branches = ['Computer', 'IT', 'EXTC', 'Chemical', 'Mechanical']
        self.brcombo = ttk.Combobox(self.root, value=branches, font=("constantia", 15))
        self.brcombo.place(x=410, y=190, width=370, height=30)
        self.brcombo.bind("<<ComboboxSelected>>", showSyllabus)
        self.root.option_add('*TCombobox*Listbox.font', ("constantia", 15))


class ContactW:
    def __init__(self, root):
        self.root = root
        self.root.title("The Study Attic")
        self.root.geometry("1100x600+100+20")
        p1 = ImageTk.PhotoImage(file='images/university_cap.ico')
        self.root.iconphoto(False, p1)
        self.root.resizable(False, False)

        frame = Frame(self.root, bd=1)
        frame.place(x=0, y=0, width=1100, height=38)

        f = ("Rockwell", 15)
        home_btn = Button(frame, text='Home', font=f, bd=0, fg='salmon4', command=partial(openHome, 'contact')).place(
            x=20, y=2)
        eb_btn = Button(frame, text='EBooks', font=f, bd=0, fg='salmon4',
                        command=partial(openBranch, 'eb', 'contact')).place(x=99, y=2)
        qp_btn = Button(frame, text='QPapers', font=f, bd=0, fg='salmon4',
                        command=partial(openBranch, 'qp', 'contact')).place(x=191, y=2)
        sy_btn = Button(frame, text='Syllabus', font=f, bd=0, fg='salmon4',
                        command=partial(openSyllabus, 'contact')).place(x=300, y=2)
        contact_btn = Button(frame, text='Contact Us', font=f, bd=0, fg='black').place(x=406, y=2)

        self.bg_img = ImageTk.PhotoImage(file='images/person.png')
        lbl = Label(frame, image=self.bg_img).place(x=960, y=2)
        self.login_btn = Button(frame, text='Login', font=f, bd=0, fg='salmon4', command=openLogin)
        self.login_btn.place(x=1000, y=2)

        c = Canvas(self.root)
        c.place(x=0, y=40, width=1100, height=150)
        self.image = ImageTk.PhotoImage(file='images/bss.png')
        c.create_image(570, 60, image=self.image)
        f1 = ("Rockwell", 45)
        c.create_text(200, 60, text="CONTACT US", fill="white", font=f1)

        framec = Frame(self.root, bg='white')
        framec.place(x=0, y=160, height=600, width=1100)
        name_lbl = Label(framec, text='Name :', font=("constantia", 15, 'bold'), bg='white', fg='black').place(x=280,
                                                                                                               y=40)
        self.name_entry = Entry(framec, font=("constantia", 15), bg="light gray", fg='black')
        self.name_entry.place(x=380, y=40, width=440)
        email_lbl = Label(framec, text='Email :', font=("constantia", 15, 'bold'), bg='white', fg='black').place(x=280,
                                                                                                                 y=90)
        self.email_entry = Entry(framec, font=("Arial", 15), bg="light gray", fg='black')
        self.email_entry.place(x=380, y=90, width=440)
        text_lbl = Label(framec, text='Any greviences or suggestions :', font=("constantia", 15, 'bold'), bg='white',
                         fg='black').place(x=280,
                                           y=140)
        self.text_entry = Text(framec, font=("constantia", 13), width=60, height=8, wrap=WORD, bg='light gray')
        self.text_entry.place(x=280, y=180)
        contact_btn = Button(framec, text='Submit', font=("constantia", 15), bg="black", fg='white',
                             comman=sendMsg).place(x=450, y=375, width=150, height=30)


class PdfsW:
    global global_type
    def __init__(self, root):
        self.root = root
        self.root.title("The Study Attic")
        self.root.geometry("1100x600+100+20")
        p1 = ImageTk.PhotoImage(file='images/university_cap.ico')
        self.root.iconphoto(False, p1)
        self.root.resizable(False, False)

        frame = Frame(self.root, bd=1)
        frame.place(x=0, y=0, width=1100, height=38)

        f = ("Rockwell", 15)
        home_btn = Button(frame, text='Home', font=f, bd=0, fg='salmon4', command=partial(openHome, 'pdfs')).place(x=20,
                                                                                                                   y=2)
        eb_btn = Button(frame, text='EBooks', font=f, bd=0, fg='salmon4',
                        command=partial(openBranch, 'eb', 'pdfs')).place(x=99, y=2)
        qp_btn = Button(frame, text='QPapers', font=f, bd=0, fg='salmon4',
                        command=partial(openBranch, 'qp', 'pdfs')).place(x=191, y=2)
        sy_btn = Button(frame, text='Syllabus', font=f, bd=0, fg='salmon4',
                        command=partial(openSyllabus, 'pdfs')).place(x=300, y=2)
        contact_btn = Button(frame, text='Contact Us', font=f, bd=0, fg='salmon4',
                             command=partial(openContact, 'pdfs')).place(x=406, y=2)

        self.bg_img = ImageTk.PhotoImage(file='images/person.png')
        lbl = Label(frame, image=self.bg_img).place(x=960, y=2)
        self.login_btn = Button(frame, text='Login', font=f, bd=0, fg='salmon4')
        self.login_btn.place(x=1000, y=2)

        c = Canvas(self.root)
        c.place(x=0, y=40, width=1100, height=150)
        self.image = ImageTk.PhotoImage(file='images/bss.png')
        c.create_image(570, 60, image=self.image)
        f1 = ("Rockwell", 45)
        c.create_text(170, 60, text=global_type.upper(), fill="white", font=f1)


home = Tk()
hw = HomeW(home)

login = Toplevel()
lw = LoginW(login)

forget = Toplevel()
fpw = Forget_passW(forget)

new_pass = Toplevel()
npw = New_passW(new_pass)

reg = Toplevel()
rw = Register_wd(reg)

branch = Toplevel()
brw = BranchW(branch)

contact = Toplevel()
cw = ContactW(contact)

syllabus = Toplevel()
sw = SyllabusW(syllabus)

pdfs = Toplevel()
pdfw = PdfsW(pdfs)

login.withdraw()
forget.withdraw()
new_pass.withdraw()
branch.withdraw()
reg.withdraw()
syllabus.withdraw()
contact.withdraw()
pdfs.withdraw()
home.mainloop()
