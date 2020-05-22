import pandas as pd
import us
import holidays

# read csv
df = pd.read_csv('data/recipe/epirecipes/epi_r.csv')

class column_collector(object):
    outputs = []
    def __init__(self, f):
        self.f = f()
        print(self.f)
        try:
            self.outputs.extend(self.f)
        except Exception as e:
            print(e)

    def __call__(self):
        pass


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


    @column_collector
    def input_cols():
        if len(columns)>0:
            return columns
        else:
            return None

    @column_collector
    def create_states():
        states = [s.name.lower() for s in us.states.STATES]
        return states

    @column_collector
    def create_cities():
        return None

    @column_collector
    def create_holidays():
        us_holidays = holidays.UnitedStates(years=2020).values()
        return [h.lower() for h in us_holidays]


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
    cols_to_drop = column_collector.outputs
    print(cols_to_drop)
    # cols_to_drop = create_cols(cols=columns)
    indices_to_drop = range(1,13)

    # drop the columns
    df = drop_the_columns(df, cols_to_drop, indices_to_drop)
    return df


def write_file(df, f):
    df.to_csv(f)

df = drop_columns(df)
columns_list = list(df.columns)
print(columns_list)
