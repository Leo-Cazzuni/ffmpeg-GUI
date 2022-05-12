import os
import subprocess

def bitrateOfSize(size,duration): #bit rate in bit/s
	return size/duration

def get_length(filename, formatar=False, plusOne=False):
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

def get_adio_rate(filename, KiB_s=True, default_rate = 96.0):
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

def calculate_Vbitrate(input_file_name,target,mode=0):		
	'''
		retorna video bitrate em kb (kbits)
		mode = 0: target em MB (Mega Bytes); mode = 1: target em %
	'''

	input_lenght = get_length(input_file_name)
	# output_video_rate = ( ( float(target_size) * 8192.0 ) / ( 1.048576 * input_lenght ) - input_adio_rate)
	# output_video_rate = ( float(target_size) * 8192.0 ) / ( 1.048576 * input_lenght )

	if mode==0:
		target_size = target
		return ( float(target_size) * 8000 ) / ( input_lenght )
	elif mode==1:
		file_size = os.path.getsize(f'd:{input_file_name}')
		target_size = target*file_size
		return ( float(target_size) * 8000 ) / ( input_lenght )


def twopass_compression(input_file_name,output_video_rate,output_audio_rate,output_file_name): # -f mp4 
	os.system(f"ffmpeg -y -i \"{input_file_name}\" -c:v libx264 -b:v {output_video_rate}k -pass 1 -an -f null /dev/null && ffmpeg -i \"{input_file_name}\" -c:v libx264 -b:v {output_video_rate}k -pass 2 -c:a aac -b:a {output_audio_rate}k \"{output_file_name}\"")

def get_rez(input_file_name):
	result = subprocess.run(["ffprobe","-v","error","-select_streams","v","-show_entries","stream=width,height","-of","csv=p=0:s=x",f"{input_file_name}"],
							stdout=subprocess.PIPE,
							stderr=subprocess.STDOUT
							)
	# return [int(s) for s in str(result.stdout).split() if s.isdigit()]
	# return [int(s) for s in result.stdout.decode().split('x') if s.isdigit()]
	# return result.stdout.decode().strip().split('x')
	return [int(x) for x in result.stdout.decode().strip().split('x')]