# Signal_Chat_Extractor
Extracts chat messages from signal

### Usage:
4) WIN+R and paste  
   `cp %HOMEPATH%\AppData\Roaming\Signal\sql\db.sqlite %HOMEPATH%\AppData\Roaming\Signal\sql\db_unencrypted.sqlite`
5) Download [DB Browser for SQLite](https://sqlitebrowser.org/dl/)
6) Choose zip (64-bit or 32-bit, whatever runs on your machine) 
7) unzip it
8) go in and run DB Browser for SQLCipher
9)  File -> Open Database -> Paste this in the bar and select `db_unencrypted.sqlite`:
`%HOMEPATH%\AppData\Roaming\Signal\sql`. Another window will open, don't close it.
1) WIN+R and paste `notepad.exe %HOMEPATH%\AppData\Roaming\Signal\config.json`, copy (CTRL+C) the key but leave out the " 
2) back to DB browser: change passphrase to raw, enter `0x` in the bar, then paste (CTRL+V) the key you just copied, press Ok
3) Tools -> Set Encryption -> leave all blank and select Ok, you can now quit the DB Browser
4) open a terminal where extract.py is
5) `python extract.py`

It will automatically extract all your messages into a moderately nicely formatted text file. You can find your files in
`%HOMEPATH%\[date]-Signal_Backup`

### What we are doing:
1) Copy the database, we don't work on the live database
2) open the database with the config file
3) decrypt the database
4) run the script

The script only uses plain python, as sqlite is already included.

If you want to have a new backup, you can run the steps again, everytime you use signal, the database is updated so we need to copy it again, decrypt it, then run the script.
