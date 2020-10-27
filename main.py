import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from PIL import Image, ImageTk
import os
import os.path

class MainWindow(tk.Frame):
	def __init__(self, root):
		super().__init__(root)
		self.init_main()

	def init_main(self):
		toolbar = tk.LabelFrame(text='Панель управления', bg='#d7d8e0', bd=2)
		toolbar.pack(fill=tk.X)

		btn_choose_image = tk.Button(toolbar, text='Выбрать изображение', command=self.choose_image, bg='#d7d8e0', bd=1)
		btn_choose_image.pack(side=tk.LEFT)

		btn_choose_image = tk.Button(toolbar, text='Обучение', command=self.open_training_dialog, bg='#d7d8e0', bd=1)
		btn_choose_image.pack(side=tk.LEFT)

		btn_auto_teach = tk.Button(toolbar, text='Автообучение', command=self.auto_teach, bg='#d7d8e0', bd=1)
		btn_auto_teach.pack(side=tk.LEFT)

		btn_read_image = tk.Button(toolbar, text='Распознать', command=self.read_image, bg='#d7d8e0', bd=1)
		btn_read_image.pack(side=tk.LEFT)

		btn_delete_image = tk.Button(toolbar, text='Очистить', command=self.delete_image, bg='#d7d8e0', bd=1)
		btn_delete_image.pack(side=tk.LEFT)

		self.img = tk.Canvas(self, bg='#ffffff') # Поле для отображения изображения
		self.img.pack(fill = tk.X)

		self.show_result = tk.Text() # Поле для вывода результата
		self.show_result.config(state = tk.NORMAL)
		self.show_result.bind("<Key>", lambda e: "break") # Блокирование ввода текста в поле
		self.show_result.pack(after = self.img)

		for i in range (10):
			w_file_name = 'w_' + str(i) + '.txt'
			if os.path.isfile('w/'+w_file_name) == False:
				w_file = open('w/'+w_file_name, 'w')
				a = ""
				w = []
				for i in range(901):
					w.append(0)
					a += str(w[i]) + " "
				a = a.rstrip()
				w_file.write(a)
				w_file.close()

	def choose_image(self):
		image_name = fd.askopenfilename() # Выбор изображения
		if image_name == '':
			return
		image = Image.open(image_name)  # Открываем изображение.
		image_showed = image.resize((250, 250)) # Увеличение изображения для отображения
		self.width = image.size[0]  # Определяем ширину.
		self.height = image.size[1]  # Определяем высоту.
		self.pix = image.load()  # Выгружаем значения пикселей.
		self.img.background = ImageTk.PhotoImage(image_showed)
		self.img.create_image(200, 135, image=self.img.background)
		image.close()

	def delete_image(self):
		self.img.delete("all")
		self.show_result.delete(1.0, tk.END)

	def open_training_dialog(self):
		Training()

	def auto_teach(self):
		pictures = os.listdir('Samples/') # Загружаем список изображений из папки с примерами для обучения
		mistake_counter = 0
		cycle_counter = 0
		stop_requirement = 0
		while stop_requirement == 0:
			for i in range (len(pictures)):
				image_name = 'Samples/' + str(pictures[i])  # Выбор изображения
				pic_number = int(pictures[i][7])
				image = Image.open(image_name)  # Открываем изображение.
				width = image.size[0]  # Определяем ширину.
				height = image.size[1]  # Определяем высоту.
				pix = image.load()  # Выгружаем значения пикселей.
				image.close()

				for j in range (10):
					neuron = j
					w_file_name = 'w_' + str(neuron) + '.txt'

					if pic_number == j:
						y_desired = 1
					else:
						y_desired = -1

					x = [1]

					# Проверяем наличие файла для записи коэффициентов, если файла нет, он создается с w = 0
					if os.path.isfile('w/' + w_file_name) == False:
						w_file = open('w/' + w_file_name, 'w')
						a = ""
						w = []
						for i in range(901):
							w.append(0)
							a += str(w[i]) + " "
						a = a.rstrip()
						w_file.write(a)
						w_file.close()

					for i in range(width):
						for j in range(height):
							a = pix[i, j][0]
							b = pix[i, j][1]
							c = pix[i, j][2]
							if ((a < 230) or (b < 230) or (c < 230)):
								x.append(1)
							else:
								x.append(-1)

					w_file = open('w/' + w_file_name, 'r')
					w = []
					c = w_file.read()
					w_file.close()
					c = c.split(" ")
					for i in range(len(c)):
						w.append(int(c[i]))

					S = 0
					for i in range(1, 901):
						S += x[i] * w[i]
					S += w[0]

					if S > 0:
						y_real = 1
					else:
						y_real = -1

					if y_real == y_desired:
						None
					else:
						mistake_counter += 1
						for i in range(901):
							w[i] += x[i] * y_desired

						w_file = open('w/' + w_file_name, 'w')
						a = ""
						for i in range(901):
							a += str(w[i]) + " "
						a = a.rstrip()
						w_file.write(a)
						w_file.close()

			if mistake_counter == 0:
				stop_requirement = 1
			else:
				None
			cycle_counter += 1
			print("Номер цикла - ", cycle_counter)
			print("Количество ошибок - ", mistake_counter)
			print("Условие останова - ", stop_requirement)
			mistake_counter = 0
		self.show_result.delete(1.0, tk.END)
		text = "Обучение нейронов завершено, кол-во циклов - " + str(cycle_counter)
		self.show_result.insert(1.0, text)


	def read_image(self):
		self.show_result.delete(1.0, tk.END)
		width = self.width
		height = self.height
		pix = self.pix

		counter = 0
		for i in range (10):
			neuron = i
			w_file_name = 'w_' + str(i) + '.txt'
			x = [1]

			for i in range(width):
				for j in range(height):
					a = pix[i, j][0]
					b = pix[i, j][1]
					c = pix[i, j][2]
					if ((a < 230) or (b < 230) or (c < 230)):
						x.append(1)
					else:
						x.append(-1)

			w_file = open('w/' + w_file_name, 'r')
			w = []
			c = w_file.read()
			w_file.close()
			c = c.split(" ")
			for i in range(len(c)):
				w.append(int(c[i]))

			S = 0
			for i in range(1, 901):
				S += x[i] * w[i]
			S += w[0]

			if S > 0:
				y_real = 1
				counter += 1
				digit = neuron
				text = "Нейрон " + str(neuron) + " распознает цифру, S = " + str(S) + " , y = " + str(y_real) + "\n"
				self.show_result.insert(1.0, text)
			else:
				y_real = -1
				text = "Нейрон " + str(neuron) + " не распознает цифру, S = " + str(S) + " , y = " + str(y_real) + "\n"
				self.show_result.insert(1.0, text)

		if counter == 0:
			self.show_result.insert(1.0, "\n")
			text_final = "Цифра не определена" + "\n"
			self.show_result.insert(1.0, text_final)
		elif counter > 1:
			self.show_result.insert(1.0, "\n")
			text_final = "У меня есть несколько вариантов..." + "\n"
			self.show_result.insert(1.0, text_final)
		else:
			self.show_result.insert(1.0, "\n")
			text_final = "Думаю, что это цифра - " + str(digit) + "\n"
			self.show_result.insert(1.0, text_final)



class Training(tk.Toplevel):
	def __init__(self):
		super().__init__(root)
		self.init_training()
		self.main_window = app_main_window

	def init_training(self):
		self.title('Параметры обучения')
		self.geometry('300x100+530+400')
		self.resizable(False, False)

		label_digit = tk.Label(self, text='Выберите нейрон для обучения')
		label_digit.place(x=10, y=10)

		label_digit = tk.Label(self, text='Нейрон должен узнавать это число?')
		label_digit.place(x=10, y=40)

		self.combobox_neuron = ttk.Combobox(self, values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
		self.combobox_neuron.current(0)
		self.combobox_neuron.place(x=240, y=10, width=50)

		self.combobox_y = ttk.Combobox(self)
		self.combobox_y['values'] = ['Да', 'Нет']
		self.combobox_y.current(0)
		self.combobox_y.place(x=240, y=40, width=50)

		self.button_teach = ttk.Button(self, text = "Обучить", command = self.teach)
		self.button_teach.place(x = 115, y = 70)

		self.grab_set()
		self.focus_set()

	def teach(self):
		width = self.main_window.width
		height = self.main_window.height
		pix = self.main_window.pix

		neuron = int(self.combobox_neuron.get())
		w_file_name = 'w_' + str(neuron) + '.txt'

		if self.combobox_y.get() == 'Да':
			y_desired = 1
		elif self.combobox_y.get() == 'Нет':
			y_desired = -1

		x = [1]

		# Проверяем наличие файла для записи коэффициентов, если файла нет, он создается с w = 0
		if os.path.isfile('w/'+w_file_name) == False:
			w_file = open('w/'+w_file_name, 'w')
			a = ""
			w = []
			for i in range(901):
				w.append(0)
				a += str(w[i]) + " "
			a = a.rstrip()
			w_file.write(a)
			w_file.close()

		for i in range(width):
			for j in range(height):
				a = pix[i, j][0]
				b = pix[i, j][1]
				c = pix[i, j][2]
				if ((a < 230) or (b < 230) or (c < 230)):
					x.append(1)
				else:
					x.append(-1)

		w_file = open('w/' + w_file_name, 'r')
		w = []
		c = w_file.read()
		w_file.close()
		c = c.split(" ")
		for i in range (len(c)):
			w.append(int(c[i]))

		S = 0

		for i in range(901):
			w[i] += x[i] * y_desired

		for i in range(1, 901):
			S += x[i] * w[i]

		S += w[0]
		if S > 0:
			y_real = 1
		else:
			y_real = -1

		w_file = open('w/' + w_file_name, 'w')
		a = ""
		for i in range(901):
			a += str(w[i]) + " "
		a = a.rstrip()
		w_file.write(a)
		w_file.close()

		self.main_window.show_result.delete(1.0, tk.END)
		text = "Обучение нейрона " + str(neuron) + " завершено, S = " + str(S) + " y = " + str(y_real)
		self.main_window.show_result.insert(1.0, text)
		self.destroy()

if __name__ == "__main__":
	root = tk.Tk()
	app_main_window = MainWindow(root)
	app_main_window.pack()
	root.title("Нейросеть Хебба")
	root.geometry("422x530+480+110")
	root.resizable(False, False)
	root.mainloop()