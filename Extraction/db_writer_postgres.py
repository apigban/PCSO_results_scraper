#!/usr/bin/env python3.7

import re
from datetime import datetime as dt

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.exc import SQLAlchemyError
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
    composite = Column('composite', String)

    def __init__(self, datedrawn, game, game_result, jackpot, winners, composite):
        # self.id = id
        self.datedrawn = datedrawn
        self.game = game
        self.game_result = game_result
        self.jackpot = jackpot
        self.winners = winners
        self.composite = composite
        print(f'A {__name__} object has been created')

    def __repr__(self):
        return f'{object.__repr__(self)}, ({str(self)})'


Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def db_check_last_update():
    """
    Checks last db entry
    returns an object
    """

    try:
        latest_db_entry = session.query(Combination).order_by(Combination.id.desc()).first()
        return latest_db_entry
    except SQLAlchemyError as error_sql:
        print(error_sql)
        latest_db_entry = None
    return latest_db_entry


def db_update_from_last_entry():
    start_date = dt.strptime('2008-01-01', '%Y-%m-%d')
    end_date = None
    # print(db_recent_entry_date)
    # db_recent_entry_date

    if db_recent_entry_date == None:
        print('\nNo Entry on Table. Dumping all rows to DB')
        # start_date = dt.strftime(start_date, '%B/%A/%Y')
        end_date = date_now
        return start_date, end_date

    elif db_recent_entry_date.datedrawn < date_now:
        print(f'\nSome entries are missing, last entry is {db_recent_entry_date.datedrawn}. TODAY is {date_now}')
        start_date = db_recent_entry_date.datedrawn
        end_date = date_now
        return start_date, end_date

    else:  # Use for exception handling
        print('\nNo Commits to DB')


def fetch_recent_composite():
    """
    search db table for composite column and limit only to last 40 rows
    result 'composite' is a list
    if no table is present from db, return an empty list

    ###SQL QUERY:
    SELECT composite FROM table
    ORDER BY id DESC
    LIMIT 40
    """

    composite = []

    db_composite = session.query(Combination).order_by(Combination.id.desc()).limit(100).all()

    for item in db_composite:
        composite.append(item.composite)

    return composite

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

    for element in range(1, len(parsed_table)):

        datedrawn = dt.strftime(dt.strptime(parsed_table[element][2], "%m/%d/%Y"), "%Y-%m-%d")
        game = parsed_table[element][0]
        game_result = parsed_table[element][1]
        jackpot = int(float(re.sub('[, ]', '', parsed_table[element][3])))
        winners = int(parsed_table[element][4])
        composite = f'{datedrawn}|{game}|{game_result}'

        draw = Combination(datedrawn, game, game_result, jackpot, winners, composite)

        recent_composite_list = fetch_recent_composite()

        if draw.composite in recent_composite_list:
            print(f'Game {draw.game} drawn on {draw.datedrawn} with combination {draw.game_result} is already in DB.')

        else:
            print(
                f'Game {draw.game} drawn on {draw.datedrawn} with combination {draw.game_result} is a NEW RECORD.\n Committing draw object to DB...')
            session.add(draw)
            session.commit()
            session.close()
            print(f'Commit Success. Session Closed.')


db_recent_entry_date = db_check_last_update()

if __name__ == '__main__':
    print('Module Executed Independently.')
