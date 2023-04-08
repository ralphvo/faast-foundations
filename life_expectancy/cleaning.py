''' All modules used '''
from pathlib import Path
import pandas as pd


class Assignment01:
    ''' Class for assignment implementation '''

    FILE_NAME = 'eu_life_expectancy_raw.tsv'
    MAIN_PATH = Path('/mnt/c/Treinamentos/faast-foundations/life_expectancy')


    def load_data(self):
        '''
            This function read data from eu_life_expectancy_raw.tsv
        '''

        return pd.read_csv(f"{self.MAIN_PATH}/data/{self.FILE_NAME}", delimiter = '\t')


    def clean_data(self, df_to_clean):
        ''' 
            This functio unpivot data to long format, so that it have the following columns:
            unit, sex, age, region, year, value.
            
        '''

        eu_life_expectancy_raw = pd.melt(
            df_to_clean,
            id_vars = 'unit,sex,age,geo\\time',

            var_name = 'year',

            value_name = 'value'
        )


        eu_life_expectancy_raw = eu_life_expectancy_raw[
            eu_life_expectancy_raw['unit,sex,age,geo\\time'].str.split(',').str[-1] == 'PT'
        ]
        eu_life_expectancy_raw = eu_life_expectancy_raw.rename(
            columns={'unit,sex,age,geo\\time': 'unit,sex,age,region'}
        )
        eu_life_expectancy_raw = eu_life_expectancy_raw[
            eu_life_expectancy_raw['value'].str.strip() != ':'
        ]
        eu_life_expectancy_raw['value'] = eu_life_expectancy_raw['value'].str.split(' ').str[0]

        cast_dic = {'year': int, 'value': float}
        eu_life_expectancy_raw = eu_life_expectancy_raw.astype(cast_dic)

        eu_life_expectancy_raw['unit'] = eu_life_expectancy_raw['unit,sex,age,region'].str.split(',').str[0]

        new_columns = eu_life_expectancy_raw.columns[0].split(',')

        for column_intex, column in enumerate(new_columns):
            column_value = eu_life_expectancy_raw['unit,sex,age,region'].str.split(',').str[column_intex]
            eu_life_expectancy_raw[column] = column_value
        eu_life_expectancy_raw = eu_life_expectancy_raw.drop(['unit,sex,age,region'], axis=1)

        new_order = ['unit','sex','age','region','year','value']
        eu_life_expectancy_raw = eu_life_expectancy_raw.reindex(columns=new_order)

        return eu_life_expectancy_raw
    

    def save_data(self, df_to_save):
        '''
            This function save the data frame cleaned to the data folder
        '''

        df_to_save.to_csv(
            f"{self.MAIN_PATH}/data/pt_life_expectancy.csv",
            index=False,

            escapechar=''
        )
    

    def main(self):
        ''' Function to call clean_data() '''

        df_pt_life_expectancy = self.load_data()
        df_pt_life_expectancy_cleaned = self.clean_data(df_pt_life_expectancy)
        self.save_data(df_pt_life_expectancy_cleaned)


if __name__ == "__main__":

    ass = Assignment01()

    ass.main()
