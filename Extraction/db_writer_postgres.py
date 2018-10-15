#!/usr/bin/env python3.7

import re
import Log.log as log
from datetime import datetime as dt

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from Extraction import db_config

db_logger = log.get_logger(__name__)

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
        db_logger.info(f'An {__name__} object has been created')



Base.metadata.create_all(bind=engine)
db_logger.info(f'Table {Combination.__tablename__} created on {db_config.host} using the {db_config.database} database')
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
        db_logger.error(f'{error_sql}')
        latest_db_entry = None
    return latest_db_entry


def db_update_from_last_entry():
    start_date = dt.strptime('2008-01-01', '%Y-%m-%d')

    if db_recent_entry_date is None:
        db_logger.info(f'No Entry on table {Combination.__tablename__}.')

        end_date = date_now
        return start_date, end_date

    elif db_recent_entry_date.datedrawn < date_now:
        db_logger.info(f'Continuing read from {db_recent_entry_date.datedrawn}. TODAY is {date_now}.')

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
            db_logger.warn(
                f'DUPLICATE ENTRY:    Game {draw.game} drawn on {draw.datedrawn} with combination {draw.game_result} is already in DB.')
        else:
            db_logger.info(
                f'NEW ENTRY: Game {draw.game} drawn on {draw.datedrawn} with combination {draw.game_result} is a NEW RECORD. Committing draw object to DB...')
            session.add(draw)
            session.commit()
            db_logger.info(f'Commit Done. Draw date:  {draw.datedrawn} Draw game: {draw.game}')
            session.close()
            db_logger.info(f'Session Closed')


db_recent_entry_date = db_check_last_update()

if __name__ == '__main__':
    print('Module Executed Independently.')
