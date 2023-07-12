
import sqlite3
import pandas as pd
from queries import (
    get_all_groupchat_identifiers,
    get_original_messages_from_chat_identifier,
    get_reaction_messages_from_chat_identifier)
con = sqlite3.connect("./chat.db")

cur = con.cursor()

# Moe

# execute a query
df = get_all_groupchat_identifiers(cur)
print(df)

# # fetch the results
# results = cur.fetchall()
# df = pd.DataFrame(results, columns=(
#     'date', 'text', 'is_from_me', 'chat.identifier', 'person_id'))
# # print the results

# df = df.fillna(value={'person_id': '+18087538953'})

# con.close()

# grouped_df = df.groupby('person_id').agg('count')
# print(grouped_df)
