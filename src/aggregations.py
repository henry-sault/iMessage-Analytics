import pandas as pd
import polars as pl
from PyDictionary import PyDictionary


class Messages():
    def __init__(self, messages: pd.DataFrame, reactions: pd.DataFrame, handle: pd.DataFrame):
        self.all_messages: pl.DataFrame = self.clean_messages(
            pl.from_pandas(messages))
        self.all_reactions: pl.DataFrame = self.clean_reactions(
            pl.from_pandas(reactions))
        self.handles: pl.DataFrame = self.clean_handles(pl.from_pandas(handle))
        self.SQL = pl.SQLContext()

    ################################
    # Clean inherent class DataFrames
    ################################

    def clean_handles(self, handles):
        user = {"handles": ["User"]}
        df = pl.DataFrame(user)
        handles = pl.concat([handles, df])

        return handles

    def clean_messages(self, messages):
        messages = messages.select(
            id=pl.col("id"),
            datetime=pl.col("datetime"),
            text=pl.col("text"),
            handle_id=pl.when(pl.col("is_from_me") == 1).then("User").otherwise(pl.col("handle_id")))

        return messages

    def clean_reactions(self, reactions):
        reactions = reactions.select(
            id=pl.col("associated_message_id").str.slice(4),
            reaction_type=pl.col("reaction_type"),
            datetime=pl.col("datetime"),
            handle_id=pl.when(pl.col("is_from_me") == 1).then("User").otherwise(pl.col("handle_id")))

        return reactions

    def replace_column_with_series(self, df: pl.DataFrame, column: str, series: pl.Series) -> pl.DataFrame:
        df.replace(column, series)

        return df

    def replace_handles_with_names(self, mapping_dict: dict):
        handle_dict = {}
        for key, value in mapping_dict.items():
            handle_dict[self.handles.item(key, 0)] = value
        self.handles = self.handles.select(
            handles=pl.col(
                "handles").map_dict(handle_dict).alias("handles")
        )
        messages_series = self.all_messages.select(
            handle_id=pl.col(
                "handle_id").map_dict(handle_dict).alias("handle_id"))\
            .to_series()
        reactions_series = self.all_reactions.select(
            handle_id=pl.col(
                "handle_id").map_dict(handle_dict).alias("handle_id"))\
            .to_series()
        self.all_messages = self.replace_column_with_series(
            self.all_messages, 'handle_id', messages_series)
        self.all_reactions = self.replace_column_with_series(
            self.all_reactions, 'handle_id', reactions_series)

    def parse_messages_into_words(self):
        words_list = self.all_messages.select(
            words=pl.col("text").str.split(by=" "),
            id=pl.col('id'),
            handle=pl.col('handle_id'),
            date=pl.col('datetime')
        )
        lf = words_list.lazy()
        # clean up empty word strings
        lf = lf.explode('words')
        lf = lf.drop_nulls('words')
        lf = lf.filter(pl.col('words') != '')

        words_df = lf.collect()

        return words_df

    def group_by_most_common_words(self):
        # explode messages into words
        words_df = self.parse_messages_into_words()
        lf = words_df.lazy()
        grouped_lf = lf.groupby()

    def get_top_ten_messages_by_reaction(self, reaction_type: str) -> pl.DataFrame:

        # lazy_reactions = pl.LazyFrame(self.all_reactions)
        # lazy_messages = pl.LazyFrame(self.all_messages)
        df = self.all_messages.join(
            other=self.all_reactions,
            how='left',
            on='id'
        )
        print(df)
        df = df.groupby("id").agg(
            pl.col("reaction_type").where(pl.col("reaction_type") == reaction_type).sum().alias(f"num_reactions")
        ).sort("num_reactions", descending=True)
        df = df
        print(df)
        
        return df

        
