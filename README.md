# flac-mp3-converter
__Note:__ This script deletes flac files after a successful conversion of the flac file to mp3.
In the script, a 'successful conversion' is considered to have take place when:
1. The mp3 file exists. 
2. The mp3 file is non-empty. 
3. The mp3's tag data sucessfully loads, implying that the file is not corrupt. 

This is all done in a single for loop and the check / create / delete logic might need to be changed depending on the use case. Use with caution. 
