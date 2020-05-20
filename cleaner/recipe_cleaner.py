import pandas as pd
import us

# read csv
df = pd.read_csv('data/recipe/epirecipes/epi_r.csv')
# print(df.columns[:30])
states = [us.states.STATES]
print(type(states[0]))



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
    states = us.states.STATES
    cols = []
    indices_to_drop = range(1,13)
    # df.columns

    df.drop(columns=cols, index=indices_to_drop)


