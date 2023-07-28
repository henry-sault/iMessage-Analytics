import sqlite3
import pandas as pd
con = sqlite3.connect("chat.db")

cursor = con.cursor()


def get_reaction_messages_from_chat_identifier(chat_identifier):
    cursor.execute(f'''
       SELECT  m.associated_message_guid, 
        CASE 
            WHEN m.associated_message_type = 2000
            THEN 'loved'
            WHEN m.associated_message_type = 2001
            THEN 'liked'
            WHEN m.associated_message_type = 2002
            THEN 'disliked'
            WHEN m.associated_message_type = 2003
            THEN 'laughed'
            WHEN m.associated_message_type = 2004
            THEN 'emphasized'
            WHEN m.associated_message_type = 2005
            THEN 'questioned'
            ELSE m.associated_message_type
        END AS reaction_type,
        datetime(m.date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") AS message_date,
        m.is_from_me,
        h.id
        FROM chat c
        LEFT JOIN chat_message_join j
        ON c.ROWID = j.chat_id
        LEFT JOIN message m
        ON m.ROWID = j.message_id
        LEFT JOIN chat_handle_join hj
        ON hj.chat_id = c.ROWID
        LEFT JOIN handle h
        ON h.ROWID = hj.handle_id

        where chat_identifier = '{chat_identifier}'
        and associated_message_type IN (2000, 2001, 2002, 2003, 2004, 2005);

                   ''')

    results = cursor.fetchall()

    df = pd.DataFrame(results, columns=('associated_message_id',
                      'reaction_type', 'datetime', 'is_from_me', 'handle_id'))

    return df


def get_original_messages_from_chat_identifier(chat_identifier) -> pd.DataFrame:
    cursor.execute(f'''
        SELECT  m.guid, 
                datetime (m.date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") AS message_date,
                m.text,
                m.is_from_me,
                h.id
        from chat c
        join chat_message_join j
        on c.ROWID = j.chat_id
        join message m
        on m.ROWID = j.message_id
        join chat_handle_join hj
        on hj.chat_id = c.ROWID
        join handle h
        on h.ROWID = hj.handle_id

        where chat_identifier = '{chat_identifier}'
        and associated_message_type = 0
                   ''')

    results = cursor.fetchall()

    df = pd.DataFrame(results, columns=('id', 'datetime',
                      'text', 'is_from_me', 'handle_id'))

    return df


def get_all_groupchat_identifiers() -> pd.DataFrame:

    cursor.execute('''
        SELECT display_name, 
                chat_identifier
        FROM chat
        WHERE display_name is not null and display_name != '';
                ''')

    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=('display_name', 'chat_identifier'))

    return df


def get_handles_for_groupchat_identifiers(chat_identifier) -> pd.DataFrame:

    cursor.execute(f'''
        SELECT h.id
        FROM chat_handle_join j
        LEFT JOIN chat chat ON j.chat_id = chat.ROWID
        LEFT JOIN handle h on h.ROWID = j.handle_id
        WHERE chat.chat_identifier = '{chat_identifier}'
                   ''')
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=["handles"])

    return df


def get_all_non_groupchat_identifiers() -> pd.DataFrame:

    cursor.execute('''
        SELECT display_name, 
                chat_identifier
        FROM chat
        WHERE display_name is null or display_name = '';
                ''')

    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=('display_name', 'chat_identifier'))

    return df
