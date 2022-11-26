import sqlite3
from sqlite3 import Error
from pathlib import Path
from datetime import datetime
import time
import os
import unicodedata
import re

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
def format_entry(name, sent_at, received_at, type, 
      hasAttachments, hasFileAttachments, hasVisualMediaAttachments, body):
  sender= name if type=="incoming" else "You" #vectorizeable
  attachmentText=""
  if hasAttachments:
    attachmentText = ", has attachments"
  if hasFileAttachments:
    attachmentText = ", has file attachments"
  if hasVisualMediaAttachments:
    attachmentText = ", has visual media attachments"

  sent_str = datetime.fromtimestamp(int(sent_at/1000))
  received_str = datetime.fromtimestamp(int(received_at/1000))
  res = f"{sender} sent at [{sent_str}], received at [{received_str}]{attachmentText}:\n{body}\n"
  return res
def format_and_write(id,name, conv, output_dir):
  print(name)
  conv_file = output_dir / (slugify(name)+".txt")
  print(conv_file)
  with open(conv_file, "w", encoding='utf-8') as f:
    f.write(f"Conversation with {name}\nSignal conversation backup as of {datetime.today().date()}\n")
    for s,r,t,h,hf,hv,b in conv:
      f.write(format_entry(name,s,r,t,h,hf,hv,b))
  
def format_and_write_all(ids,names,conversations, output_dir):
  print("===FORMAT===")
  for id,name,conv in zip(ids,names,conversations):
    format_and_write(id,name,conv, output_dir)

def select_messages(conn, id):
  """
  Query all rows in the tasks table
  :param conn: the Connection object
  :return:
  """
  
  cur = conn.cursor()
  cur.execute(f"SELECT sent_at, received_at, type, hasAttachments, hasFileAttachments, hasVisualMediaAttachments, body FROM messages WHERE conversationId='{id}'")

  rows = cur.fetchall()

  return rows #ids, name

def select_all_messages(conn, ids):
  conversations=list()
  for id in ids:
    conversations.append(select_messages(conn,id))
  return conversations

def select_conversations(conn):
  """
  Query all rows in the tasks table
  :param conn: the Connection object
  :return:
  """
  cur = conn.cursor()
  cur.execute("SELECT id, name FROM conversations")

  rows= cur.fetchall()
  ids,names=zip(*[row for row in rows if row[1]])
  
  return ids,names    


def main():
  # assume everything is unencrypted for the moment
  # sqlite does not support encryption it seems
  sigDir = Path.home() / "AppData/Roaming/Signal"
  dbfile = str(sigDir / "sql" / "db_unencrypted.sqlite")
  #keyFile = sigDir / "config.json"
  dt = datetime.now()
  ts = datetime.timestamp(dt)
  str_time = datetime.fromtimestamp(int(ts))

  output_dir=Path.home()/f"{datetime.today().date()}-Signal_Backup"

  os.makedirs(output_dir,exist_ok=True)
  # create a database connection
  conn = create_connection(dbfile)
  with conn:
      ids, names = select_conversations(conn)
      conversations = select_all_messages(conn, ids)
      format_and_write_all(ids,names,conversations,output_dir)

if __name__ == '__main__':
    main()