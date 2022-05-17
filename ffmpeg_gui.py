import os
import subprocess
import tkinter as tk
import tkinter.filedialog

class MainMenu(tk.Frame):

	bg_color = '#2D2A2E'
	bg_color2 = '#181719'
	primary_color = '#FFD866'
	secondary_color = '#AB9DF2'
	attention_color = '#FF6188'
	title_color = '#FC9867'
	main_font = 'Courier'
	title_size = 20
	text_size = 15

	# default_PATH = os.getenv('USERPROFILE')+'/Videos'  #windows
	default_PATH = os.getenv('HOME')+'/Videos' #linux
	default_input_PATH = None
	default_start_time = '00:00:00'
	default_stop_time = '00:00:01'
	default_rezW = 0
	default_rezH = 0
	default_aspect_ratio = None		# W/H
	default_reencode = True
	default_compression = 25
	default_compression_MB = 0
	default_compression_perc = 100
	vcodec = 'libx265'
	# default_command = f'ffmpeg -ss {default_start_time} -to {default_stop_time} -vcodec libx265 -crf {default_compression} -i'

	file_PATH = None
	filetypes = (('video files',"*.mp4 *.mkv"),("all files","*"),("mp4 files","*.mp4"),("mkv files","*.mkv"))

	def __init__(self):
		# root settings:
		self.root_window = tk.Tk()
		self.root_window.title("ffmpeg Bad UI")
		self.root_window.minsize(600, 300)
		self.root_window.configure(bg=self.bg_color)
		self.menus_buttons = [0,1,2,3,4]

		# title settings:
		self.title = tk.Label(self.root_window,text='ffmpeg Bad UI 3.1', font=(self.main_font, self.title_size), fg=self.title_color ,bg=self.bg_color)

		# packing e main loop:
		self.title.pack(pady=(0, 30))
		self.main_frame_init()

		self.root_window.mainloop()


	def main_frame_init(self):
		if hasattr(self, 'main_frame'):
			self.main_frame.destroy()

		# self.main_frame = tk.LabelFrame(self.root_window, borderwidth=0, highlightthickness=0,bd=0)
		self.main_frame = tk.LabelFrame(self.root_window, fg=self.primary_color,bg=self.bg_color, padx=10, pady=10, borderwidth=0, highlightthickness=0,bd=0)

		self.file_frame(0,0)
		self.file_info_frame_init(1,0)
		self.cut_frame_init(2,0)
		self.rez_frame_init(3,0)
		self.compress_frame_init(4,0)
		self.presset_frame_init(5,0)
		self.reencode_frame_init(6,0)
		self.save_frame_init(7,0)

		# self.show_command()

		self.main_frame.pack()

	def file_frame(self,row,column):
		file_frame = tk.LabelFrame(self.main_frame, fg=self.primary_color,bg=self.bg_color, borderwidth=0, highlightthickness=0,bd=0)
		fileTitle_text = tk.Label(file_frame,text='File:', font=(self.main_font, self.text_size), fg=self.primary_color,bg=self.bg_color)		
		self.filePATH_text = tk.Entry(file_frame,text='', font=(self.main_font, self.text_size), fg=self.secondary_color,bg=self.bg_color)		
		search_button = tk.Button(file_frame,text='Search', command = self.getFilePATH, width=10, fg=self.primary_color,bg=self.bg_color)

		file_frame.grid(row=row,column=column, pady=5)
		fileTitle_text.grid(row=0,column=0)
		self.filePATH_text.grid(row=0,column=1,columnspan=3)
		search_button.grid(row=0,column=4)

	def file_info_frame_init(self,row,column):
		File_info_frame = tk.LabelFrame(self.main_frame, fg=self.primary_color,bg=self.bg_color, borderwidth=0, highlightthickness=0,bd=0)
		
		self.fileSize_text = tk.Label(File_info_frame,text='', font=(self.main_font, self.text_size), fg=self.attention_color,bg=self.bg_color)		

		File_info_frame.grid(row=row,column=column)
		self.fileSize_text.grid(row=0,column=0)


	def cut_frame_init(self,row,column): 
		# cut_frame = tk.LabelFrame(self.main_frame, fg=self.primary_color,bg=self.bg_color, padx=10, pady=10, borderwidth=0, highlightthickness=0,bd=0)

		self.cut_frame = tk.LabelFrame(self.main_frame, fg=self.primary_color,bg=self.bg_color, borderwidth=0, highlightthickness=0,bd=0)
		self.start_text = tk.Label(self.cut_frame,text='start:', font=(self.main_font, self.text_size), fg=self.primary_color,bg=self.bg_color)		
		self.start_entry = tk.Entry(self.cut_frame, width=8,fg=self.secondary_color,bg=self.bg_color,font=(self.main_font, self.text_size)) #state='disabled'
		self.start_entry.insert(0,self.default_start_time)
		self.stop_text = tk.Label(self.cut_frame,text='stop:', font=(self.main_font, self.text_size), fg=self.primary_color,bg=self.bg_color)		
		self.stop_entry = tk.Entry(self.cut_frame, width=8,fg=self.secondary_color,bg=self.bg_color,font=(self.main_font, self.text_size))
		self.stop_entry.insert(0,self.default_stop_time)
		self.cut_frame_pack(row,column)

	def cut_frame_pack(self,row,column): 
		self.cut_frame.grid(row=row,column=column, pady=5)
		self.start_text.grid(row=0,column=0)
		self.start_entry.grid(row=0,column=1)
		self.stop_text.grid(row=0,column=2)
		self.stop_entry.grid(row=0,column=3)

	def rez_frame_init(self,row,column):
		rez_frame = tk.LabelFrame(self.main_frame, fg=self.primary_color,bg=self.bg_color, borderwidth=0, highlightthickness=0,bd=0)
		rez_text = tk.Label(rez_frame,text='Resolution:', font=(self.main_font, self.text_size), fg=self.primary_color,bg=self.bg_color)		

		self.rezW = tk.IntVar()
		self.rezW.trace("w", self.refresh_rez)
		self.rezW_entry = tk.Entry(rez_frame, textvariable=self.rezW, width=5,fg=self.secondary_color,bg=self.bg_color,font=(self.main_font, self.text_size))
		self.rezW.set(self.default_rezW)

		x_text = tk.Label(rez_frame,text='x', font=(self.main_font, self.text_size), fg=self.primary_color,bg=self.bg_color)		

		self.rezH = tk.IntVar()
		self.rezH.trace("w", self.refresh_rez)
		self.rezH_entry = tk.Entry(rez_frame, textvariable=self.rezH, width=5,fg=self.secondary_color,bg=self.bg_color,font=(self.main_font, self.text_size))
		self.rezH.set(self.default_rezH)

		rez_frame.grid(row=row,column=column, pady=5)
		rez_text.grid(row=0,column=0)
		self.rezW_entry.grid(row=0,column=1)
		x_text.grid(row=0,column=2)
		self.rezH_entry.grid(row=0,column=3)

	def refresh_rez(self, *args):
		if(self.default_aspect_ratio):
			try: # é só pra n dar ruim quando vc colocar algo q n seja int
				if(args[0]=='PY_VAR0'): # PY_VAR0 é o W, troca o H
					if(self.root_window.focus_get()==self.rezW_entry):
						novo = int(self.rezW.get()/self.default_aspect_ratio)
						self.rezH.set(novo)

				elif (args[0]=='PY_VAR1'): # PY_VAR1 é o H, troca o W
					if(self.root_window.focus_get()==self.rezH_entry):
						ovo = int(self.rezH.get()*self.default_aspect_ratio)
						self.rezW.set(ovo)
			except:
				pass


	def compress_frame_init(self,row,column):
		compress_frame = tk.LabelFrame(self.main_frame, fg=self.primary_color,bg=self.bg_color, borderwidth=0, highlightthickness=0,bd=0)
		compression_text = tk.Label(compress_frame,text='Compression:', font=(self.main_font, self.text_size), fg=self.primary_color,bg=self.bg_color)		

		self.compression_MB = tk.StringVar()
		self.compression_MB.trace("w", self.refresh_compression_perc)
		self.compression_MB_entry = tk.Entry(compress_frame, textvariable=self.compression_MB, width=5,fg=self.secondary_color,bg=self.bg_color,font=(self.main_font, self.text_size))
		self.compression_MB.set(self.default_compression_MB)
		MB_text = tk.Label(compress_frame,text='MB', font=(self.main_font, self.text_size), fg=self.primary_color,bg=self.bg_color)		

		self.compression_perc = tk.StringVar()
		self.compression_perc.trace("w", self.refresh_compression_MB)
		self.compression_perc_entry = tk.Entry(compress_frame, textvariable=self.compression_perc, width=5,fg=self.secondary_color,bg=self.bg_color,font=(self.main_font, self.text_size))
		self.compression_perc.set(self.default_compression_perc)
		perc_text = tk.Label(compress_frame,text='%', font=(self.main_font, self.text_size), fg=self.primary_color,bg=self.bg_color)		

		compress_frame.grid(row=row,column=column, pady=5)

		compression_text.grid(row=0,column=0)
		self.compression_MB_entry.grid(row=0,column=1)
		MB_text.grid(row=0,column=2)

		self.compression_perc_entry.grid(row=1,column=1)
		perc_text.grid(row=1,column=2)

		# self.compression_entry

	def refresh_compression_MB(self, *args):
		try:
			if(self.root_window.focus_get()==self.compression_perc_entry):
				new_MB = (float(self.compression_perc.get())*self.file_size/100000000)
				self.compression_MB.set(new_MB)
		except:
			pass

	def refresh_compression_perc(self, *args):
		try:
			if(self.root_window.focus_get()==self.compression_MB_entry):
				new_perc = (float(self.compression_MB.get())*100000000/self.file_size)
				self.compression_perc.set(new_perc)
		except:
			pass

	def presset_frame_init(self,row,column):
		presset_options = [
			'N/A',
			'veryslow',
			'slower',
			'slow',
			'medium',
			'fast',
			'faster',
			'veryfast',
			'superfast',
			'ultrafast'
		]
		self.presset_clicked = tk.StringVar()
		presset_frame = tk.LabelFrame(self.main_frame, fg=self.primary_color,bg=self.bg_color, borderwidth=0, highlightthickness=0,bd=0)
		presset_text = tk.Label(presset_frame,text='Velocidade:', font=(self.main_font, self.text_size), fg=self.primary_color,bg=self.bg_color)		
		presset_dropdown = tk.OptionMenu( presset_frame , self.presset_clicked , *presset_options)
		
		presset_dropdown.configure(fg=self.secondary_color,bg=self.bg_color,font=(self.main_font, self.text_size),borderwidth=0, highlightthickness=0,bd=0)
		self.presset_clicked.set('N/A')

		presset_frame.grid(row=row,column=column, pady=5)
		presset_text.grid(row=0,column=0)
		presset_dropdown.grid(row=0,column=1)

	def reencode_frame_init(self,row,column):
		reencode_frame = tk.LabelFrame(self.main_frame, fg=self.primary_color,bg=self.bg_color, borderwidth=0, highlightthickness=0,bd=0)
		self.re_encode = tk.BooleanVar()
		re_encode_text = tk.Label(reencode_frame,text='re-encode:', font=(self.main_font, self.text_size), fg=self.primary_color,bg=self.bg_color)		
		re_encode_check = tk.Checkbutton(reencode_frame, variable= self.re_encode, onvalue=True, offvalue=False,bg=self.bg_color)
		
		if self.default_reencode:
			re_encode_check.select()
		else:
			re_encode_check.deselect()

		reencode_frame.grid(row=row,column=column)
		re_encode_text.grid(row=0,column=0)
		re_encode_check.grid(row=0,column=1)

	def save_frame_init(self,row,column):
		save_frame = tk.LabelFrame(self.main_frame, fg=self.primary_color,bg=self.bg_color, borderwidth=0, highlightthickness=0,bd=0)
		save_button = tk.Button(save_frame,text='Save', command = self.save_video, width=10, fg=self.primary_color,bg=self.bg_color)

		save_frame.grid(row=row,column=column, pady=(50,0))
		save_button.pack()

	def getFilePATH(self):
		self.file_PATH = tk.filedialog.askopenfilename(initialdir=self.default_PATH, filetypes=self.filetypes, title="Select a File")
		

		self.filePATH_text.delete(0, tk.END)
		self.filePATH_text.insert(0, self.file_PATH)
		self.filePATH_text.grid(row=0,column=1)

		if len(self.file_PATH):
			self.get_info(self.file_PATH)

	def get_info(self,file_PATH):
		if file_PATH!='':
			self.file_NAME = file_PATH.split('/')[-1]
			self.file_format = self.file_NAME.split('.')[-1]
			self.file_size = os.path.getsize(f'{file_PATH}')

		# Size info:
		file_size_MB = self.file_size/1000000
		self.fileSize_text.configure(text=f'File size: {file_size_MB}MB')
		self.compression_MB.set(file_size_MB)
		self.compression_perc.set(100)

		# length info:
		self.input_lenght = self.get_length(file_PATH, formatar=True, plusOne=True)
		self.input_adio_rate = self.get_adio_rate(file_PATH, KiB_s=True)

		if 'file' not in self.input_lenght:
			self.default_stop_time = self.input_lenght
			self.default_stop_time = self.input_lenght
		self.cut_frame_init(2,0)

		# rez info:
		self.default_rezW,self.default_rezH = self.get_rez(file_PATH)
		self.default_aspect_ratio = self.default_rezW/self.default_rezH
		self.rezW_entry.delete(0,tk.END)
		self.rezW_entry.insert(0,self.default_rezW)
		self.rezH_entry.delete(0,tk.END)
		self.rezH_entry.insert(0,self.default_rezH)

	def bitrateOfSize(self,size,duration): #bit rate in bit/s
		return size/duration

	def get_length(self,filename, formatar=False, plusOne=False):
		result = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{filename}"],
								stdout=subprocess.PIPE,
								stderr=subprocess.STDOUT
								)

		try:
			lenght = float(result.stdout)
		except:
			try:
				return str(result.stdout)
			except:
				return result.stdout

		if formatar:
			if(plusOne):
				lenght+=1
			return f'{int(lenght//(60*60)):02d}:{int(lenght//60):02d}:{int(lenght%60):02d}'
		else:
			return lenght

	def get_adio_rate(self,filename, KiB_s=True, default_rate = 96.0):
		''' Retorna audio bitrate em KiB/s (caso KiB_s==True) '''
		result = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=bit_rate", "-of", "csv=p=0", f"{filename}"],
								stdout=subprocess.PIPE,
								stderr=subprocess.STDOUT)
		try:
			adio_rate = float(result.stdout)
		except:
			if KiB_s:
				return default_rate 
			else:
				return default_rate * 1024

		if KiB_s:
			return adio_rate / 1024
		else:
			return adio_rate

	def calculate_Vbitrate(self,input_file_name,target,mode=0):		
		'''
			retorna video bitrate em kb (kbits)
			mode = 0: target em MB (Mega Bytes); mode = 1: target em %
		'''

		input_lenght = self.get_length(input_file_name)
		# output_video_rate = ( ( float(target_size) * 8192.0 ) / ( 1.048576 * input_lenght ) - input_adio_rate)
		# output_video_rate = ( float(target_size) * 8192.0 ) / ( 1.048576 * input_lenght )

		if mode==0:
			target_size = target
			return ( float(target_size) * 8000 ) / ( input_lenght )
		elif mode==1:
			file_size = os.path.getsize(f'd:{input_file_name}')
			target_size = target*file_size
			return ( float(target_size) * 8000 ) / ( input_lenght )


	def twopass_compression(self,input_file_name,output_video_rate,output_audio_rate,output_file_name): # -f mp4 
		os.system(f"ffmpeg -y -i \"{input_file_name}\" -c:v libx264 -b:v {output_video_rate}k -pass 1 -an -f null /dev/null && ffmpeg -i \"{input_file_name}\" -c:v libx264 -b:v {output_video_rate}k -pass 2 -c:a aac -b:a {output_audio_rate}k \"{output_file_name}\"")

	def get_rez(self,input_file_name):
		result = subprocess.run(["ffprobe","-v","error","-select_streams","v","-show_entries","stream=width,height","-of","csv=p=0:s=x",f"{input_file_name}"],
								stdout=subprocess.PIPE,
								stderr=subprocess.STDOUT
								)
		# return [int(s) for s in str(result.stdout).split() if s.isdigit()]
		# return [int(s) for s in result.stdout.decode().split('x') if s.isdigit()]
		# return result.stdout.decode().strip().split('x')
		return [int(x) for x in result.stdout.decode().strip().split('x')]

	def save_video(self):
		if(self.file_PATH):
			PATH = self.file_PATH.split('/')[:-1]
			fileName = self.file_NAME.split('.')[0]
			# output_file_path = f"{'.'.join(self.file_PATH.split('.')[:-1])}-crf{self.default_compression}.{self.file_PATH.split('.')[-1]}" # filename out
			start_time = self.start_entry.get()
			stop_time = self.stop_entry.get()
			video_bitrate = self.calculate_Vbitrate(self.file_PATH,self.compression_MB.get())
			rezW = self.rezW_entry.get()
			rezH = self.rezH_entry.get()

			self.save_PATH = tk.filedialog.asksaveasfilename(initialdir=PATH, initialfile=f"{fileName}-output", defaultextension='.'+self.file_format,title="Save File", filetypes=self.filetypes)

			if len(self.save_PATH):
				# ffmpeg [input options] -i input [output options] output
				command = 'ffmpeg'

				#[input options]:
				if start_time != self.default_start_time or stop_time != self.default_stop_time:
					command += f' -ss {start_time} -to {stop_time}'

				#[-i input]:
				command += f' -i \"{self.file_PATH}\"'

				#[output options]:
				command += f' -vcodec {self.vcodec}'

				if(self.compression_perc.get()!='100'):
					command += f' -b {video_bitrate}k'

				if rezW != self.default_rezW or rezH != self.default_rezH:
					command += f' -s {rezW}x{rezH}'						

				if not self.re_encode.get():
					command += ' -c copy'

				if 'N/A' != self.presset_clicked.get():
					command += ' -preset ' + self.presset_clicked.get()
				
				#[output]
				command += f' \"{self.save_PATH}\"'

				# print(command,end='\n'*3)
				os.system(command)
			else:
				pass
		else:
			tk.messagebox.showinfo('Erro','Nenhuma file selecionada')

def main():
	root = MainMenu()

if __name__ == '__main__':
	main()