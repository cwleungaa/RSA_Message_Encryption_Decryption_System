from tkinter import *
import tkinter as tk 
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter.messagebox import askokcancel
import csv
import sqlite3 as sqlite
import random
import math

con = sqlite.connect("database.db")

LARGEFONT =("Verdana", 15)
LARGEFONT2 =("Verdana", 10) 
LARGEFONT3 =("Verdana", 20) 

sender = ""

#Two prime number
p = 11
q = 17

#Two variable using in RSA
n = p * q
k = (p-1) * (q-1)


class tkinterApp(tk.Tk): 
	
	# __init__ function for class tkinterApp ,variable, dict
	def __init__(self, *args, **kwargs): 
		
		# __init__ function for class Tk 
		tk.Tk.__init__(self, *args, **kwargs) 
		
		# creating a container 
		container = tk.Frame(self) 
		container.pack(side = "top", fill = "both", expand = True) 

		container.grid_rowconfigure(0, weight = 1) 
		container.grid_columnconfigure(0, weight = 1) 

		# initializing frames to an empty array 
		self.frames = {} 

		# iterating through a tuple consisting of the different page layouts 
		for F in (LoginPage, RegisterPage, EncryPage): 

			frame = F(container, self) 

			# initializing frame of that object from startpage, page1, page2 respectively with for loop 
			self.frames[F] = frame 

			frame.grid(row = 0, column = 0, sticky ="nsew") 

		self.show_frame(LoginPage) 

	# Display the current frame
	def show_frame(self, cont): 
		frame = self.frames[cont] 
		frame.tkraise()
		frame.postupdate()  # For focus the input label

class LoginPage(tk.Frame): 
	def __init__(self, parent, controller): 
		tk.Frame.__init__(self, parent) 

		global usernameinput, passwordinput


		def login(self):
			usernameinput1 = usernameinput.get()

			passwordinput1 = passwordinput.get()

			dnamespws = con.execute("SELECT name,password from data1")

			for name, password in dnamespws:
				if name == usernameinput1 and password == passwordinput1:
					global sender
					sender = usernameinput1
					controller.show_frame(EncryPage)
					break
			else:
				showinfo("Alert", "Login info is not correct!!!")
				return

		
		# label of LoginPage
		self.loginlabel = ttk.Label(self, text ="Loginpage", font = LARGEFONT) 
		
		self.usernamelabel = ttk.Label(self, text ="Username:", font = LARGEFONT)

		usernameinput = ttk.Entry(self, font = LARGEFONT)

		self.passwordlabel = ttk.Label(self, text = "Password:", font = LARGEFONT) 

		passwordinput = ttk.Entry(self, show = "*", font = LARGEFONT)

		self.button1 = Button(self, text = "Login", font = LARGEFONT2, width = 20, height = 5,
		command = lambda : login(self)) 


		self.button2 = Button(self, text ="Register", font = LARGEFONT2, width = 20, height = 5,
		command = lambda : controller.show_frame(RegisterPage)) 


		self.loginlabel.pack(pady = 20)
		self.usernamelabel.pack(pady = 20)
		usernameinput.pack(pady = 20)
		self.passwordlabel.pack(pady = 20)
		passwordinput.pack(pady = 20)
		self.button1.pack(padx = 120, pady = 20, side = LEFT)
		self.button2.pack(pady = 20, side = LEFT)

	# Focus the input label
	def postupdate(self):
		usernameinput.focus()

     
class RegisterPage(tk.Frame): 

	# Only public key and secret key is missing	
	
	def __init__(self, parent, controller): 

		def reg(self):

			database_pset=[]

			public_key=0
			secret_key=0

			dnames = con.execute("SELECT name from data1")
			dpublic_keys = con.execute("SELECT public_key from data1")

			# Assign all public key in database to database_pset to check if the new generated key are duplicate or not
			for dpublic_key in dpublic_keys:
				database_pset.append(dpublic_key[0])

			# generate a random number a such that gcd(a,k) = 1
			while True:
				a = random.randint(2, k)
				if a in database_pset:
					continue
				else:
					if math.gcd(a,k) != 1:
						continue
					else:
						public_key = a
						break

			# print("The public key is: ", public_key)
		
			q = 0
			r = 0
			i = 0
			j = public_key
			self.kl, self.jl, self.ql, self.rl = [], [], [], []		

			# Extended GCD, first part:
			def find_gcd(self, k, j, i):
				q = k // j
				r = k % j

				self.kl.append(k)
				self.jl.append(j)
				self.ql.append(q)
				self.rl.append(r)
				i += 1
				if r == 1:
					# Only ql and i is required, others for calculation reference
					return i
				else:
					return find_gcd(self, j, r, i)
					
			i = find_gcd(self, k, j, i)

			# Extended GCD, second part:
			xlist = [1]
			ylist = [0]

			def inverse(x, y, i):
				if i != -1:
					ytemp = x
					xtemp = y - self.ql[i] * x
					xlist.append(xtemp)
					ylist.append(ytemp)
					i = i - 1
					return inverse(xtemp, ytemp, i)
				else:
					return

			inverse(1, 0, i-1)

			# print("The xlist is: ", xlist)
			# print("The multiple inverse is: ", xlist[i])
			# print("The ylist is: ", ylist)

			secret_key = xlist[i]

			# change secret key to positive
			# while secret_key <0:
			# 	secret_key = secret_key + k


			# Checking if the username is registered
			for dname in dnames:
				if dname[0] == self.regnameinput.get():
					showinfo("Alert", "Your name is registered")
					return

			# Checking if password equals to confirm password
			if self.regpasswordinput1.get() != self.regpasswordinput2.get():
				showinfo("Alert", "Your password and conirm password is not the same!")
				return	

			# Checking of input for username, password, password confirmation		
			elif self.regnameinput.get() == "":
				showinfo("Alert", "You must provide a username for registration!")
				return
			elif self.regpasswordinput1.get() == "":
				showinfo("Alert", "You must provide a password for registration!")
				return	
			elif self.regpasswordinput2.get() == "":
				showinfo("Alert", "You must provide a password confirmation for registration!")
				return				
			else:	
				name = self.regnameinput.get()
				password = self.regpasswordinput1.get()

				# SQL to insert data,using place-holder
				insert_data = '''insert into data1 values(?,?,?,?)'''
				x = (name, password, public_key, secret_key)

				# execute the insert_data
				con.execute(insert_data,x)
				# update the data in SQL file
				con.commit()

				#popup message of register sucessfully
				showinfo("Window", "You register successfully!!")
				controller.show_frame(LoginPage)

				self.regnameinput.focus()
				self.regnameinput.delete(0,'end')
				self.regpasswordinput1.delete(0,'end')
				self.regpasswordinput2.delete(0,'end')
				# results = con.execute("SELECT * from data1")
				# for result in results:
				# 	print(result[0])

				# con.close()	

		tk.Frame.__init__(self, parent) 
		
		# label of frame Layout 2 
		self.label = ttk.Label(self, text ="Register page", font = LARGEFONT) 

		self.usernamelabel = ttk.Label(self, text ="Username:", font = LARGEFONT)

		self.regnameinput = Entry(self, font = LARGEFONT)

		self.passwordlabel = ttk.Label(self, text ="Password:", font = LARGEFONT) 

		self.regpasswordinput1 = Entry(self, show = "*", font = LARGEFONT)

		self.passwordlabel2 = ttk.Label(self, text ="Confirm Password:", font = LARGEFONT) 

		self.regpasswordinput2 = Entry(self, show = "*", font = LARGEFONT)

		self.button1 = Button(self, text ="Register", font = LARGEFONT2, width = 20, height = 5,
		command = lambda: reg(self)) 

		self.button2 = Button(self, text ="Return", font = LARGEFONT2, width = 20, height = 5,
		command = lambda: controller.show_frame(LoginPage)) 

		self.label.pack(pady = 10)
		self.usernamelabel.pack(pady = 10)
		self.regnameinput.pack(pady = 10)
		self.passwordlabel.pack(pady = 10)
		self.regpasswordinput1.pack(pady = 10)
		self.passwordlabel2.pack(pady = 10)
		self.regpasswordinput2.pack(pady = 10)
		self.button1.pack(padx= 120, pady = 20,side = LEFT)
		self.button2.pack(pady = 20, side = LEFT)

	# For focus the input label
	def postupdate(self):
		self.regnameinput.focus_set()	

class EncryPage(tk.Frame):
	def __init__(self, parent, controller): 
		tk.Frame.__init__(self, parent) 

		def submit(self):
			messages = []
			if self.myCombo.get() == "":
				showinfo("Alert", "Your must pick a person")
				return

			receiver = self.myCombo.get()	

			# Get the sender's secret key using placeholder

			select_sender = '''SELECT secret_key from data1 where name = ?'''

			sender_secret_obj = con.execute(select_sender, [sender])

			sender_secret_key_tuple = sender_secret_obj.fetchall()

			sender_secret_key = sender_secret_key_tuple[0][0]

			while sender_secret_key < 0:
				sender_secret_key = sender_secret_key + k

			# Get the receiver's public key using placeholder

			select_receiver = '''SELECT public_key from data1 where name = ?'''

			receiver_public_obj = con.execute(select_receiver, [receiver])

			receiver_public_key_tuple = receiver_public_obj.fetchall()

			receiver_public_key = receiver_public_key_tuple[0][0]

			# Get the message
			texts = self.texts.get("1.0", "end-1c")
			if texts != "":
			# encrypt each letter of text
				with open("message.csv", 'w', newline='') as csvfile:
					encrypted_asc2 = []
					for text in texts:
						ord_text = ord(text)

						encrypted_data = pow(ord_text, receiver_public_key * sender_secret_key, n)

						encrypted_asc2.append(encrypted_data)

					writer = csv.writer(csvfile)

					writer.writerow(encrypted_asc2)

				showinfo("Window", "Text is summited for encrypt!")	
			else:
				showinfo("Alert", "Your need to type something!")
				return

		def logout(self):
			sender = ""
			# clean the info of username, pw
			result = askokcancel("Logout", "Do you want to logout?")
			if result == True:
				sender = ""
				# clean the info of username,pw
				usernameinput.focus()
				usernameinput.delete(0, 'end')
				passwordinput.delete(0, 'end')
				controller.show_frame(LoginPage)
			else:
				return	



		self.label = ttk.Label(self, text = "Please pick a person:", font = LARGEFONT) 

		def updated_list_value(self):

			option_list = []

			dnames = con.execute("SELECT name from data1")

			for dname in dnames:
				option_list.append(dname)

			self.myCombo['values'] = option_list

		# Select name list from db 
		self.options = []

		dnames = con.execute("SELECT name from data1")

		for dname in dnames:
			self.options.append(dname)

		# Select menu, postcommand use for updating the newly registered user into the option list
		self.myCombo = ttk.Combobox(self, font=LARGEFONT3, width = 10, value = self.options, postcommand = lambda : updated_list_value(self))

		self.myCombo.current()

		# Change the font size of option
		self.myCombo.option_add('*TCombobox*Listbox.font', LARGEFONT)

		self.label.pack()
		self.myCombo.pack(pady = 50)

		# Add two frame contain the text part and button part
		self.frame = Frame(self)
		self.frame.pack()
		self.bframe = Frame(self)
		self.bframe.pack(side = BOTTOM)

		# Input box and scrollbar
		self.texts = Text(self.frame, height = 6, width = 35, font = ("Helvetica", 20))

		self.scrollbar = Scrollbar(self.frame)

		# Submit button
		self.submit_button = Button(self.bframe, text = "Submit", font = LARGEFONT2, width = 20, height = 5,
							command = lambda : submit(self)) 

		# logout button			
		self.logout_button = Button(self.bframe, text ="Logout", font = LARGEFONT2, width = 20, height = 5,
							command = lambda : logout(self)) 
	

		# Pack the textbox and scrollbar	
		self.texts.pack(side = LEFT, padx = (25, 0), pady = (0, 0))
		self.scrollbar.pack(side = LEFT, fill = Y)
		self.scrollbar.config(command = self.texts.yview)
		self.texts.config(yscrollcommand = self.scrollbar.set)

		# Pack the button
		self.submit_button.pack(padx= (0, 80), pady = 40, side = LEFT)
		self.logout_button.pack(pady = 40, side = LEFT)

	# For focus the input label		
	def postupdate(self):
		pass


# Create the database table

# create_table = '''Create table data1(
#     name TEXT,
# 	password TEXT,
# 	public_key INTEGER,
# 	secret_key INTEGER)'''

# printing the database

# results = con.execute("SELECT * from data1")
# for result in results:
# 	print(result[0])

# con.close()


app = tkinterApp() 
app.title("Encrypter")
app.geometry("800x600")

app.mainloop()
