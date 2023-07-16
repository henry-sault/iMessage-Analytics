import pandas as pd
import polars as pl


class Messages():
    def __init__(self, messages: pd.DataFrame, reactions: pd.DataFrame):
        self.all_messages: pl.Dataframe = pl.from_pandas(messages)
        self.all_reactions: pl.Dataframe = pl.from_pandas(reactions)

    def get_handles_from_groupchat(self):
        print('moe')

    def attach_names_to_handle(self):
        print('moe')

    def parse_messages_into_words(self):
        words_list = self.all_messages.select(
            words=pl.col("text").str.split(by=" "),
            id=pl.col('id'),
        )
        lf = words_list.lazy()
        # clean up empty word strings
        lf = lf.explode('words')
        lf = lf.drop_nulls('words')
        lf = lf.filter(pl.col('words') != '')

        words_df = lf.collect()

        return words_df

    def join_words_with_messages(self, words):
        words = words.join(self.all_messages, on='id',
                           how='inner')
        words = words.select(
            id=pl.col('id'),
            word=pl.col('words'),
            handle=pl.col('handle_id'),
            date=pl.col('datetime'))
        words = words.unique(keep='any')
        return words
