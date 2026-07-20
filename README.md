<img width="420" height="303" alt="image" src="https://github.com/user-attachments/assets/482b5d11-6492-4f59-8ed6-19e93ea68d05" />
<img width="517" height="465" alt="image" src="https://github.com/user-attachments/assets/438efbfd-a231-46fb-9504-49ba3bc314b1" />
<img width="517" height="232" alt="image" src="https://github.com/user-attachments/assets/7baecbd4-7d70-4616-974d-311dfa9c9853" />

Python script to convert  UTF8 ISO text file from ASCII chars to Umlaute and vive versa. Other characters mixed in (like cyrillic) should not disturb and don't get touched.

uses following Converion table: 

NORMAL_MAP = {
    'ae': 'ä', 'oe': 'ö', 'ue': 'ü',
    'AE': 'Ä', 'OE': 'Ö', 'UE': 'Ü',
    'Ae': 'Ä', 'Oe': 'Ö', 'Ue': 'Ü'
}

REVERSE_MAP = {
    'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
    'Ä': 'AE', 'ß': 'ss', 'ẞ': 'SS'

If you omit target file during launch a file dialog pops ups 
and let's you choose a txt file to view before processing. 

Chosse conversion direction to start conversion. 

The file dialog writes the last used directory to a readable and editable .txt file, reading it back next start.
That means you can launch the script from any r/w directory youlike. 

It remembers the dir where you picked the last file from.
Avoiding click orgies to numerous drives and dirs when you just want to choose the next file from the previous dir.

Have fun. 
Live long and prosper.
