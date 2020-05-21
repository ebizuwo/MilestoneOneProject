import pandas as pd
import us

# read csv
df = pd.read_csv('data/recipe/epirecipes/epi_r.csv')


def drop_columns(df, columns=[]):
    """
    Were going to drop columns based on slicing here because there is no reason to get too logical about
    it. The goal here is to chop off useless columns.
    Were also going to drop the states because that makes no
    sense.
    :param df:
    :param columns: (optional)
    :return:
    """


    def create_cols(cols=[]):
        # we add the states in here as well
        states = [s.name.lower() for s in us.states.STATES]
        cities = []
        return cols+states

    def drop_the_columns(df, cols, ind):
        df = df.drop(index=ind)
        for c in cols:
            try:
                df = df.drop(columns=c)
            except Exception as e:
                print(e)
                continue
        return df
    # create some stuff to use
    cols_to_drop = create_cols(cols=columns)
    indices_to_drop = range(1,13)

    # drop the columns
    df = drop_the_columns(df, cols_to_drop, indices_to_drop)
    return df



df = drop_columns(df)
print(list(df.columns))