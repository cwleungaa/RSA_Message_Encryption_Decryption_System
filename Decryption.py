from tkinter import *
import tkinter as tk 
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter.messagebox import askokcancel
import csv
import sqlite3 as sqlite

con = sqlite.connect("database.db")

LARGEFONT =("Verdana", 15)
LARGEFONT2 =("Verdana", 10) 
LARGEFONT3 =("Verdana", 20) 

receiver = ""

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
		for F in (LoginPage, DecryptPage): 

			frame = F(container, self) 

			# initializing frame of that object from startpage, page1, page2 respectively with for loop 
			self.frames[F] = frame 

			frame.grid(row = 0, column = 0, sticky = "nsew") 

		self.show_frame(LoginPage) 

	# Display the current frame
	def show_frame(self, cont): 
		frame = self.frames[cont] 
		frame.tkraise()

class LoginPage(tk.Frame): 
	def __init__(self, parent, controller): 
		tk.Frame.__init__(self, parent) 

		global usernameinput, passwordinput

		def login(self):

			usernameinput1 = usernameinput.get()

			passwordinput1 = passwordinput.get()

			dnamespws = con.execute("SELECT name,password from data1")

			for name,password in dnamespws:
				if name == usernameinput1 and password == passwordinput1:
					global receiver
					receiver = usernameinput1
					controller.show_frame(DecryptPage)
					break
			else:
				showinfo("Alert", "Login info is not correct!!!")
				return

		
		# label of LoginPage
		self.login_label = ttk.Label(self, text = "Loginpage", font = LARGEFONT) 

		self.usernamelabel = ttk.Label(self, text = "Username:", font = LARGEFONT)

		usernameinput = ttk.Entry(self, font = LARGEFONT)

		self.passwordlabel = ttk.Label(self, text = "Password:", font = LARGEFONT) 

		passwordinput = ttk.Entry(self, show = "*", font = LARGEFONT)

		usernameinput.focus()

		self.login_button = Button(self, text = "Login", font = LARGEFONT2, width = 20, height = 5,
		command = lambda : login(self)) 

		self.login_label.pack(pady = 20)
		self.usernamelabel.pack(pady = 20)
		usernameinput.pack(pady = 20)
		self.passwordlabel.pack(pady = 20)
		passwordinput.pack(pady = 20)
		self.login_button.pack(pady = 20)
      

class DecryptPage(tk.Frame): 
	def __init__(self, parent, controller): 

		tk.Frame.__init__(self, parent) 

		def decrypt_message(self):
			messages=[]
			if self.myCombo.get() == "":
				showinfo("Alert", "Your must pick a person")
				return
			sender1 = self.myCombo.get()	

			# Get the sender's secret key using placeholder

			select_sender = '''SELECT public_key from data1 where name = ?'''

			sender_public_obj = con.execute(select_sender, [sender1])

			sender_public_key_tuple = sender_public_obj.fetchall()

			sender_public_key = sender_public_key_tuple[0][0]

			# Get the receiver's public key using placeholder

			select_receiver = '''SELECT secret_key from data1 where name = ?'''

			receiver_secret_obj = con.execute(select_receiver, [receiver])

			receiver_secret_key_tuple = receiver_secret_obj.fetchall()

			receiver_secret_key = receiver_secret_key_tuple[0][0]

			# Adjust receiver_secret_key to positive index
			while receiver_secret_key < 0:
				receiver_secret_key = receiver_secret_key + k

            # Decrypt each letter of text
			with open("message.csv") as csvfile:
				csvReader = csv.reader(csvfile)
				csvReader_list = list(csvReader)
				for texts in csvReader_list:
					for num in texts:
						num = int(num)
						temp = pow(num, receiver_secret_key * sender_public_key, n)
						ord_text = chr(temp)
						messages.append(ord_text)

				for message in messages:	
					self.texts.insert(END, message)

		def logout(self):
			result = askokcancel("Logout", "Do you want to logout?")
			if result == True:
				self.texts.delete("1.0", "end-1c")
				self.myCombo.current = self.myCombo.current()
				sender=""

				# Clean the info of username, password
				usernameinput.focus()
				usernameinput.delete(0,'end')
				passwordinput.delete(0,'end')
				controller.show_frame(LoginPage)
			else:
				return	

		def clear(self):
			self.texts.delete("1.0","end-1c")


		self.sender_label = ttk.Label(self, text ="Please pick your sender:", font = LARGEFONT) 

		self.options = []

		dnames = con.execute("SELECT name from data1")

		for dname in dnames:
			self.options.append(dname)

		# Code for select menu
		self.myCombo = ttk.Combobox(self, value = self.options, font=LARGEFONT3, width = 10)
		self.myCombo.current()

		# Change the font size of option
		self.myCombo.option_add('*TCombobox*Listbox.font', LARGEFONT)
		self.sender_label.pack()
		self.myCombo.pack(pady=50)

		#add two frame contain the text part and button part
		self.frame = Frame(self)
		self.frame.pack()
		self.bframe = Frame(self)
		self.bframe.pack(side = BOTTOM)

		# Output box and scrollbar
		self.texts = Text(self.frame, height = 6, width = 30, font=("Helvetica", 20))

		self.scrollbar = Scrollbar(self.frame)

		# Three buttons to show decrypt, clear, logout

		self.decrypt_button = Button(self.bframe, text = "Decrypt", font = LARGEFONT2, width = 20, height = 5,
							command = lambda : decrypt_message(self)) 

		self.clear_button = Button(self.bframe, text = "Clear", font = LARGEFONT2, width = 20, height = 5,
							command = lambda : clear(self)) 					
			
		self.logout_button = Button(self.bframe, text = "Logout", font = LARGEFONT2, width = 20, height = 5,
							command = lambda : logout(self)) 
	
		# Pack the textbox and scrollbar	
		self.texts.pack(side = LEFT, padx = (25, 0), pady=(0, 0))
		self.scrollbar.pack(side = LEFT, fill = Y)
		self.scrollbar.config(command = self.texts.yview)
		self.texts.config(yscrollcommand = self.scrollbar.set)

		# Pack the button
		self.decrypt_button.pack(padx = 20, pady = 30, side = LEFT)
		self.clear_button.pack(padx = 10, pady = 30, side = LEFT)
		self.logout_button.pack(padx =20, pady = 30, side = RIGHT)

app = tkinterApp() 
app.title("Decrypter")
app.geometry("800x600")

app.mainloop()
