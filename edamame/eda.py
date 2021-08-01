import pandas as pd
import pandas_profiling as pdp

def read_csv_to_df(file_name):
    try:
        df = pd.read_csv(file_name)
        df.info()
        return df
    except:
        try:
            df = pd.read_csv(file_name, encoding='shift-jis')
            print('shift-jisで読み込みました')
            df.info()
            return df
        except:
            try:
                df = pd.read_csv(file_name, encoding='cp932')
                print('cp932で読み込みました')
                df.info()
                return df
            except:
                print('utf-8, shift-jis, cp932で読み込み失敗しました')
                return None

def profile_report(df, output_file=''):
    profile = pdp.ProfileReport(df)
    if (type(output_file) == str) & (len(output_file) > 0):
        profile.to_file(output_file=output_file+'_profile.html')
    return profile

def describe(df, output_file=''):
    percentiles = [.005, .01, .025, .05, .1,.25, .5, .75, .9, .95, .975, .99, .995]
    describe = pd.concat([pd.DataFrame(df.dtypes, columns=[ 'dtypes']).T, df.describe(percentiles=percentiles, include='all')])
    if (type(output_file) == str) & (len(output_file) > 0):
        describe.to_csv(output_file+'_describe.csv')
    return describe

def distribution_sheet(df, output_file='', max_unique=1000, bins=100, gss=False):
    if gss:
        import string
        uppercase = string.ascii_uppercase
    df_lst = []
    for n, c in enumerate(df):
        cols = [c]
        len_unique = len(df[c].unique())
        cols += [str(len_unique) + '(' + c + ')']
        if ((df[c].dtype == int) | (df[c].dtype == float))  & (len_unique > max_unique):
            tmp_df = df[c].value_counts(sort=False, bins=bins, dropna=True).sort_index(ascending=True, na_position='first').reset_index()
        else:
            tmp_df = df[c].value_counts(sort=False, dropna=True).sort_index(ascending=True, na_position='first').reset_index()
        tmp_df.columns = cols
        if gss:
            m = (n * 3) + 1
            q = m // 26
            r = m % 26
            address = uppercase[r]
            if q > 0:
                tensplace = uppercase[q-1]
                address = tensplace + address
            len_rows = tmp_df.shape[0]
            bar_max = tmp_df[str(len_unique) + '(' + c + ')'].max()
            sl_lst = ['=SPARKLINE('+address+str(i+2)+',{"charttype","bar";"max",'+str(bar_max)+'})' for i in range(len_rows)]
            sl_s = pd.Series(sl_lst, name='bar_' + c)
            tmp_df = pd.concat([tmp_df, sl_s], axis=1)
        df_lst += [tmp_df]
    concat_df  = pd.concat(df_lst, axis=1)
    if (type(output_file) == str) & (len(output_file) > 0):
        concat_df.to_csv(output_file + '_destribution.csv', index=False)
    return concat_df

if __name__ == '__main__':
    file_name = 'input.csv'
    output_file = 'output'
    df = csv_df(file_name)
    describe = describe(df, output_file)
    max_unique = 1000
    bins = 100
    sheet = distribution_sheet(df, output_file, max_unique=max_unique, bins=bins, gss=True)
    profile = profile_report(df, output_file)
