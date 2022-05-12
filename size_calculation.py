import sys
import os
import subprocess
# os.system("@echo off")
# os.getcwd()

# Re-encode a video to a target size in MB. This script tries to mantain the same audio bitrate
# Example:
#    python this_script.py video.mp4 15

def get_length(filename):
    # ffprobe -v error -show_entries format=duration -of csv=p=0 {filename}
    result = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{filename}"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT
                            )
    try:
        return float(result.stdout)
    except:
        return result.stdout

def get_adio_rate(filename):
    # ffprobe -v error -select_streams a:0 -show_entries stream=bit_rate -of csv=p=0 {filename}
    result = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=bit_rate", "-of", "csv=p=0", f"{filename}"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    try:
        return float(result.stdout)
    except:
        return 96.0

def twopass_compression(input_file_name,output_video_rate,output_audio_rate,output_file_name): # -f mp4 
    os.system(f"ffmpeg -y -i \"{input_file_name}\" -c:v libx264 -b:v {output_video_rate}k -pass 1 -an -f null /dev/null && ffmpeg -i \"{input_file_name}\" -c:v libx264 -b:v {output_video_rate}k -pass 2 -c:a aac -b:a {output_audio_rate}k \"{output_file_name}\"")

def main():
    target_size = str(sys.argv[2]) # target size in MB
    input_file_name = str(sys.argv[1]) # filename in
    output_file_name = f"{'.'.join(input_file_name.split('.')[:-1])}-{target_size}MB.mp4" # filename out

    # print(input_file_name,type(input_file_name))
    # print(get_length(input_file_name))

    input_lenght = get_length(input_file_name)
    input_adio_rate = get_adio_rate(input_file_name) / 1024 # em KiB/s

    output_min_size = (input_adio_rate * input_lenght) / 8192

    output_audio_rate = input_adio_rate

    output_video_rate = ( ( float(target_size) * 8192.0 ) / ( 1.048576 * input_lenght ) - input_adio_rate)

    twopass_compression(input_file_name,output_video_rate,output_audio_rate,output_file_name)

    # print(f"ffmpeg -i \"{input_file_name}\" -c:v libx264 -b:v {output_video_rate}k -pass 1 -an /dev/null && ffmpeg -i \"{input_file_name}\" -c:v libx264 -b:v {output_video_rate}k -pass 2 -c:a aac -b:a {output_audio_rate}k \"{output_file_name}\"")

if __name__ == '__main__':
    main()