import duckdb
import sqlite3
import pandas as pd
con = sqlite3.connect("chat.db")

cur = con.cursor()


# execute a query
cur.execute('''SELECT
    datetime (message.date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") AS message_date,
    message.text,
    message.is_from_me,
    chat.chat_identifier,
    handle.id
FROM
    chat
    LEFT JOIN chat_message_join ON chat. "ROWID" = chat_message_join.chat_id
    LEFT JOIN message ON chat_message_join.message_id = message. "ROWID"
    LEFT JOIN handle ON handle. "ROWID"  = message.handle_id
WHERE
    chat.chat_identifier = "chat783632288714701473"
ORDER BY
    message_date ASC;''')


# fetch the results
results = cur.fetchall()
df = pd.DataFrame(results, columns=(
    'date', 'text', 'is_from_me', 'chat.identifier', 'person_id'))
# print the results

df = df.fillna(value={'person_id': '+18087538953'})
# df = df.fillna("moe")
# df.assign(Laughed= [1 if df['text'].startswith('Laughed at ') else 0])
# df['Love'] = 0
# df['Like'] = 0

# for index, row in df.iterrows():
#     # print(row['text'])
#     row['Laugh'] = [1 if row['text'].startswith('Laughed at ') else 0]
#     row['Love'] = [1 if row['text'].startswith('Loved') else 0]
#     row['Like'] = [1 if row['text'].startswith('Liked') else 0]

# liked = df[df['Laugh'] == 1]
# df.groupby('id')
# df.to_csv('dtfl.csv')
# close the connection
# print(liked)
con.close()

grouped_df = df.groupby('person_id').agg('count')
print(grouped_df)
