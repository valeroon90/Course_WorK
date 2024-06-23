import os
from utils import get_vacancies, create_database, save_data_to_database, get_employer, getEmployers
from config import config

def main():
    api_hh_ru = 'https://api.hh.ru/vacancies'
    company_ids = [
        '1473866',
        '205',
        '4219',
        '23040',
        '740',
        '3838',
        '1057',
        '1180',
        '208707',
        '1740'
    ]

    params = config()
    #employers = getEmployers()
    data = get_vacancies(205)
    date_2 = get_employer(205)
   # print(get_vacancies(3421))
   # create_database('hh_data', params)
   # save_data_to_database(data, 'hh_data', params)

if __name__ == '__main__':
    main()





