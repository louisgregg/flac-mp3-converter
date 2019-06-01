from pathlib import Path
import sys
import os
import re
# from pydub import AudioSegment
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
import mutagen

from pydub import AudioSegment
from pydub.utils import mediainfo

# for strange filenames
# reload(sys)
# sys.setdefaultencoding('utf-8')

def get_list_of_filetype(path,filetype):
	list_of_files =[]

	filetype = filetype.replace('.','')

	for filename in Path(path).glob('**/*.'+filetype.lower()):
		list_of_files.append(filename.as_posix())
	for filename in Path(path).glob('**/*.'+filetype.upper()):
		list_of_files.append(filename.as_posix())		
	return(list_of_files)	


def check_if_file_exists(path):
	config = Path(path)
	if config.is_file():
	    return(True)
	else:
	    return(False)

def check_if_file_empty(path):
	return(os.stat(path).st_size == 0)



def convert_flac_to_mp3(flac_path,mp3_path):
			# AudioSegment.from_file(flac_path).export(
			# mp3_path, format='mp3', bitrate="320k",
			# parameters=["-map_metadata", "0", "-id3v2_version", "3","-write_id3v1", "1"]
			# )
			seg = AudioSegment.from_file(flac_path)
			seg.export(mp3_path, format='mp3', bitrate="320k", tags=mediainfo(flac_path).get('TAG', {}))

def check_audio_file_has_info(path):
	check_file = mediainfo(path)
	if check_file:
		return(True)
	else:
		return(False)

def main(folder_path):

	list_of_flacs = get_list_of_filetype(folder_path, 'flac')
	list_of_mp3s = []
	for flac_path in list_of_flacs:
		mp3_path = re.sub('\.flac$','.mp3', flac_path,flags=re.IGNORECASE)
		print('-----------------------')
		print(flac_path)
		if check_if_file_exists(mp3_path):
			if check_if_file_empty(mp3_path):
				print('mp3 exists and is empty\t:\t'+mp3_path)
				print('Converting:\t'+flac_path)
				convert_flac_to_mp3(flac_path,mp3_path)
			else:
				print('mp3 exists and is non-empty\t:\t'+mp3_path)
				print('Skipping conversion.')
				# print('Deleting flac file.')
				# os.remove(flac_path)
				# continue # skips to next flac in loop
		else: 
			print('mp3 file does not exist\t:\t'+mp3_path)
			print('Converting\t:\t'+flac_path)
			convert_flac_to_mp3(flac_path,mp3_path)

		# if mp3 exists and is non-empty
		# # delete flac file
		# print('flac tags:')
		# for key in mutagen.File(flac_path).keys():
		# 	print(key+'\t:\t'+mutagen.File(flac_path)[key][0])

		# # delete flac file
		# print('mp3 tags:')
		# for key in mutagen.File(mp3_path).keys():

		# 	print(key)
		# 	print(mutagen.File(mp3_path)[key][0])
		# print('\n')

		if check_if_file_exists(mp3_path) and not check_if_file_empty(mp3_path) and check_audio_file_has_info(mp3_path):
			print('mp3 exists, is non-empty and has functioning tags\t:\t'+mp3_path)
			print('Deleting\t'+flac_path)
			os.remove(flac_path)
		print('-----------------------')
		print('\n')
if __name__ == '__main__':
	try:
		main(str(sys.argv[1]))
	except IndexError as e:
		print('Usage: \n python3 convert_1.py "path/to/music/folder" ')    
