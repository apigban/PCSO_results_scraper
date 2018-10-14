#!/usr/bin/env python3.7

import re
from datetime import datetime as dt

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from Extraction import db_config

date_now = dt.now().date()

Base = declarative_base()
engine = create_engine(
    f'postgresql://{db_config.username}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}',
    echo=False)


class Combination(Base):
    __tablename__ = 'lotto'

    id = Column('id', Integer, primary_key=True)
    datedrawn = Column('datedrawn', Date)
    game = Column('game', String)
    game_result = Column('result', String)
    jackpot = Column('jackpot', Integer)
    winners = Column('winners', Integer)


def db_check_last_update():
    """
    get draw information from passed list
    initialize db engine, commit drawinfo from parsed list
    List Structure: [
        ELEMENT 0: ['LOTTO GAME', 'COMBINATIONS', 'DRAW DATE', 'JACKPOT', 'WINNERS'],
        ELEMENT 1: ['Megalotto 6/45', '41-05-21-31-45-03', '10/8/2018', '56,250,597.00', '0'],
                    ...
                    ]
    """
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()


    try:
        latest_db_entry = session.query(Combination).order_by(Combination.id.desc()).first()
        return latest_db_entry.datedrawn
    except TypeError as error_type:
        print('f{error_type}')
        latest_db_entry = None
    return latest_db_entry


def db_update_from_last_entry():
    db_recent_entry_date = db_check_last_update()
    start_date = dt.strptime('2008-01-01', '%Y-%m-%d')
    end_date = None

    if db_recent_entry_date == None:
        print('\nNo Entry on Table. Dumping all rows to DB')
        # start_date = dt.strftime(start_date, '%B/%A/%Y')
        end_date = date_now
        return start_date, end_date

    elif db_recent_entry_date < date_now:
        print(f'\nSome entries are missing, last entry is {db_recent_entry_date}. TODAY is {date_now}')
        start_date = db_recent_entry_date
        end_date = date_now
        return start_date, end_date

    else:  # Use for exception handling
        print('\nNo Commits to DB')


def db_commit(parsed_table):
    """
    get draw information from passed list
    initialize db engine, commit drawinfo from parsed list
    List Structure: [
        ELEMENT 0: ['LOTTO GAME', 'COMBINATIONS', 'DRAW DATE', 'JACKPOT', 'WINNERS'],
        ELEMENT 1: ['Megalotto 6/45', '41-05-21-31-45-03', '10/8/2018', '56,250,597.00', '0'],
                    ...
                    ]
    """
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    #    try:
    for element in range(1, len(parsed_table)):
        draw = Combination()

        draw.datedrawn = dt.strftime(dt.strptime(parsed_table[element][2], "%m/%d/%Y"), "%Y-%m-%d")
        draw.game = parsed_table[element][0]
        draw.game_result = parsed_table[element][1]
        draw.jackpot = int(float(re.sub('[, ]', '', parsed_table[element][3])))
        draw.winners = int(parsed_table[element][4])

        session.add(draw)
        session.commit()

        session.close()


#    except ValueError as wrong_datatype:
#        print(f'{wrong_datatype}')
#        pass

if __name__ == '__main__':
    print('Module Executed Independently.')
