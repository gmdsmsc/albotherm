import pandas as pd


''' This will load each of the different trials data. We may want to add additional data cleaning steps in here if necessary. 
    One example would be to have better names for the supplementary data columns. '''


def combine_date_times(df):
    df['DateTime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str), dayfirst=True)
    return df.drop(columns=['Date', 'Time'])

def load_supplementary_file(file_path, **kwargs):
    with open(file_path) as f:
        line1 = f.readline()
        name = '_'.join(line1.split(',')[2:6])
    df = pd.read_csv(file_path, skiprows=2, usecols=[0, 1, 2], **kwargs)
    df.columns = ['Date', 'Time', name]
    df = df.dropna(subset=['Date', 'Time'])
    return combine_date_times(df)

def load_vitacress_supplementary_data():
    df2 = pd.read_csv('csv/vitacress_supplementary_data2.csv', parse_dates=[0])
    df2.columns = [f'{column_name}_2' if column_name != 'DateTime' else 'DateTime' for column_name in df2.columns]
    df3 = pd.read_csv('csv/vitacress_supplementary_data3.csv', parse_dates=[0])
    df3.columns = [f'{column_name}_3' if column_name != 'DateTime' else 'DateTime' for column_name in df3.columns]
    df_sup = df2.merge(df3, on='DateTime')
    drop_columns = ['radiation_sum:_measurement_-_2', 'radiation_sum:_measurement_-_3',
                    'outside_temperature:_measurement_-_3',
                    'radiation:_measurement_-_W/mｲ\n_3', 'lee_side_vent_position:_3']
    df_sup.drop(columns=drop_columns, inplace=True)
    col_names = {'greenhouse_temperature_climate:_measurement_2': 'Greenhouse Temp 2',
    'lee_side_vent_position:_2': 'Lee Side Vent',
    'wind_side_vent_position:_2': 'Wind Side Vent 2',
    'radiation:_measurement_-_W/mｲ\n_2': 'Radiation',
    'outside_temperature:_measurement_-_2': 'Outside Temperature',
    'greenhouse_temperature_climate:_measurement_3': 'Greenhouse Temp 3',
    'wind_side_vent_position:_3': 'Wind Side Vent 3',}
    df_sup.rename(columns=col_names, inplace=True)
    return df_sup


def load_vitacress_1():
    df = pd.read_csv('csv/vitacress_1.csv')
    df.rename(columns={'Unnamed: 1': 'Time'}, inplace=True)
    df = combine_date_times(df)
    df_sup = load_vitacress_supplementary_data()
    return df.merge(df_sup, how='left', on='DateTime')

def load_vitacress_2():
    df = pd.read_csv('csv/vitacress_2.csv')
    df.rename(columns={'Unnamed: 1': 'Time'}, inplace=True)
    df = combine_date_times(df)
    df_sup = load_vitacress_supplementary_data()
    return df.merge(df_sup, how='left', on='DateTime')

def load_flavourfresh_1():
    df = pd.read_csv('csv/flavourfresh_1.csv', parse_dates=[0])
    df.rename(columns={'Date': 'DateTime'}, inplace=True)
    df_temp = pd.read_csv('csv/flavourfresh_1_temperature.csv', parse_dates=[0])
    df_temp.rename(columns={'Date': 'DateTime'}, inplace=True)
    return df.merge(df_temp, how='left', on='DateTime')

def load_flavourfresh_2():
    df = pd.read_csv('csv/flavourfresh_2.csv', parse_dates=[0])
    df.rename(columns={'Date': 'DateTime'}, inplace=True)
    df_temp = pd.read_csv('csv/flavourfresh_2_temperature.csv', parse_dates=[0])
    df_temp.rename(columns={'Date': 'DateTime'}, inplace=True)
    return df.merge(df_temp, how='left', on='DateTime')
