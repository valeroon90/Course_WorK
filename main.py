import os
from utils import create_database, save_data_to_database, get_employer, getEmployers, get_hh_ru_data
from config import config

def main():

    company_ids = [
        '4307',
        '4787018',
        '4219',
        '23040',
        '1579449',
        '2180',
        '1057',
        '1180',
        '208707',
        '205'
    ]

    params = config()
    #employers = getEmployers()

    data = get_hh_ru_data(company_ids)
    #print(data)
    date_2 = get_employer(2180)
    print(date_2)
   # create_database('hh_data', params)
   # save_data_to_database(data, 'hh_data', params)

if __name__ == '__main__':
    main()





