from tkinter import *

from tkinter.filedialog import asksaveasfile


class Stream:

	def __init__(self):
		self.buttonFont = ("Helvetica", 15, "bold")
		self.textFieldFont = ("Georgia", 15, "normal")
		self.titleFont = ("Helvetica", 28, "bold")
		# variable for indicating if typing has started
		self.started = False
		# variable for indicating if
		# target amount of characters has been typed
		self.target_reached = False
		# initialize window
		self.window = Tk()
		# simplifies the title bar
		self.window.attributes("-toolwindow", 1)
		self.window.configure(bg="#83a95c")
		# for fade-out of text
		self.fade_scale = ["#202020", "#303030", "#404040", "#505050", "#606060", "#707070", "#808080", "#909090",
		                   "#A0A0A0", "#B0B0B0", "#e9c496"]
		# incrementer for fade
		self.fade_inc = 0

	def UI(self):
		self.window.title("Stream of Consciousness Typist")
		self.header = Label(self.window, width=28, font=self.titleFont, text="Stream of Consciousness Typist", bg="#83a95c", fg="#944e6c", pady=10)
		self.instructions = Label(self.window, width=35,font=self.textFieldFont, text="If you stop typing for 5 seconds, all will be lost", bg="#83a95c", fg="#433d3c")
		self.text = Text(self.window, width=60, height=15, font=self.textFieldFont, padx=10, pady=5)
		self.text.configure(bg="#e9c496")
		self.save_button = Button(self.window, text="Save", font=self.buttonFont, fg="#83a95c",bg="#944e6c", activebackground="#83a95c", activeforeground="#944e6c", relief=FLAT, command=self.save)
		# button initially disabled until minimum characters are typed
		self.save_button["state"] = "disabled"
		self.header.grid(column=0, row=0, columnspan=3)
		self.instructions.grid(column=1, row=1, columnspan=3, pady=10)
		self.text.grid(column=1, row=2)
		self.save_button.grid(column=1, row=4, pady=10)
		# activate keypress detection
		self.keypress = self.window.bind("<Key>", self.keydown)
		self.start_text = self.text.insert(END, "Start typing...")
		# focus cursor in text field
		self.text.focus_set()
		self.window.mainloop()

	def countdown(self, remaining=None):
		if remaining is not None:
			self.remaining = remaining
		if self.remaining <= 0:
			self.reset()
		elif not self.target_reached:
			self.remaining = self.remaining - 1
			self.window.after(1000, self.countdown)
		if self.remaining == 1:
			self.fade_out()


	def keydown(self, e):
		# resets countdown each time a key is pressed
		self.remaining = 5
		self.change_color("black")
		if self.started == False:
			self.instructions.configure(text="If you type 1000 characters, you can save it.")
			# starts countdown
			self.countdown(5)
			# deletes 'Start typing...' message
			self.text.delete("1.0", END)
			# reinserts first typed character which was deleted by previous line
			self.text.insert(END, e.char)
			self.started = True
		# if 1000 characters are typed, activate save function
		if len(self.text.get("1.0", END)) > 1000:
			self.target_reached = True
			self.save_button["state"] = "normal"


	def change_color(self, color):
			# changes text color
			self.text.tag_add("start", "1.0", END)
			self.text.tag_config("start", foreground=color)

	def save(self):
		#saves typed text as text file
		try:
			files = [('Text Document', '*.txt')]
			file = asksaveasfile(filetypes=files, defaultextension=files, mode='w')
			file.write(self.text.get("1.0", END))
			file.close()
		# handles cancel of save
		except AttributeError:
			pass
		#reset text field after save or cancel
		finally:
			self.reset()

	def reset(self):
		# resets text field to start conditions
		self.target_reached = False
		self.started = False
		self.instructions.configure(text="If you stop typing for 5 seconds, all will be lost")
		# disables the save button
		self.save_button["state"] = "disabled"
		self.text.delete("1.0", END)
		self.text.insert(END, "Start typing...")
		# restores black text color after fading to background color
		self.change_color("black")

	def fade_out(self):
		# fades out text 1 second before reset
		if self.fade_inc <= 10:
			self.change_color(self.fade_scale[self.fade_inc])
			self.fade_inc += 1
			self.window.after(100, self.fade_out)
		else:
			# reset incrementer for next time round
			self.fade_inc = 0
			return
