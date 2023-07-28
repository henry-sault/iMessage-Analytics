
import sqlite3
import pandas as pd
from queries import (
    get_all_groupchat_identifiers,
    get_original_messages_from_chat_identifier,
    get_reaction_messages_from_chat_identifier,
    get_handles_for_groupchat_identifiers)
con = sqlite3.connect("chat.db")


# Moe

# execute a query
df = get_handles_for_groupchat_identifiers('chat328831580126696185')
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
