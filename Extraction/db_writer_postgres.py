#!/usr/bin/env python3.7

import re
from datetime import datetime as dt
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relation
from Extraction import db_config

Base = declarative_base()
engine = create_engine(
    f'postgresql://{db_config.username}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}',
    echo=True)


class Combination(Base):
    __tablename__ = 'lotto'

    id = Column('id', Integer, primary_key=True)
    datedrawn = Column('date', Date)
    game = Column('game', String)
    game_result = Column('result', String)
    jackpot = Column('jackpot', Integer)
    winners = Column('winners', Integer)


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

    for element in range(1, len(parsed_table)):
        draw = Combination()
        session = Session()

        draw.datedrawn = dt.strftime(dt.strptime(parsed_table[element][2], "%m/%d/%Y"), "%Y-%m-%d")
        draw.game = parsed_table[element][0]
        draw.game_result = parsed_table[element][1]
        draw.jackpot = int(float(re.sub('[, ]', '', parsed_table[element][3])))
        draw.winners = int(parsed_table[element][4])

        session.add(draw)
        session.commit()

        session.close()


if __name__ == '__main__':
    print('Module Executed Independently.')
