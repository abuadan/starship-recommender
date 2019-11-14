"""

"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from request_maker import collect_info, request_builder
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import logging
import swapi
import json
from databaseTables import StartShip

# Global Variables

logging.basicConfig(level=logging.INFO)
module_logger = logging.getLogger("starship-recommendation.database_setup")

SQLITE = "sqlite"
Session = sessionmaker(autoflush=False)


class MyDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        SQLITE: 'sqlite:///memory'
    }

    # Main DB Connection Ref Obj
    db_engine = None

    def __init__(self, dbtype, username=None, password=None, dbname=''):
        self.logger = logging.getLogger("starship-recommendation.database_setup.MyDatabase")
        self.logger.setLevel(logging.INFO)
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            self.logger.info(self.db_engine)

        else:
            self.logger.warning("DBType of {0} is not found in DB_ENGINE".format(dbtype))

    def create_db_tables(self):
        metadata = MetaData()

        try:
            metadata.create_all(self.db_engine)
            self.logger.info("Tables created")
        except Exception as e:
            self.logger.error("Error occurred during Table creation!", exc_info=e)

    def __session_maker__(self):
        session = Session.configure(bind=self.db_engine)
        return session

    def session_scope(self, session):
        """Provide a transactional scope around a series of operations."""
        try:
            yield session
            session.commit()
            self.logger.info("session successfully committed ")
        except Exception as e:
            session.rollback()
            self.logger.exception("Encountered error session is rolling back")
            raise
        finally:
            session.close()
            self.logger.info("Closing session")


class UpdateDB(collect_info.ParseInfo, MyDatabase):

    """
    """

    def __init__(self, category):
        super().__init__(category)
        self.logger = logging.getLogger("starship-recommendation.database_setup.UpdateDB")
        self.logger.setLevel(logging.INFO)

    def __initial_db__(self):
        pass

    def __parse_data__(self, starship_response):
        data = self.parse_starship_info(starship_response)
        return data

    @staticmethod
    def __create_database_objects__(data):
        db_objects = [
            StartShip(starship_id=item["starship_id"],
                      name=item["name"],
                      model=item["model"],
                      manufacturer=item["manufacturer"],
                      cost_in_credits=item["cost_in_credits"],
                      length=item["length"],
                      crew=item["crew"],
                      passengers=item["passengers"],
                      cargo_capacity=item["cargo_capacity"],
                      consumables=item["consumables"],
                      hyperdrive_rating=item["hyperdrive_rating"],
                      mglt=item["MGLT"],
                      starship_class=item["starship_class"],
                      in_film_one=item["in_film_one"],
                      in_film_two=item["in_film_two"],
                      in_film_three=item["in_film_three"],
                      in_film_four=item["in_film_four"],
                      in_film_five=item["in_film_five"],
                      in_film_six=item["in_film_six"],
                      in_film_seven=item["in_film_seven"],
                      in_film_eight=item["in_film_eight"],
                      number_of_pilots=item["number_of_pilots"]
                      ) for item in data
        ]
        return db_objects

    def __update_database__(self, session):
        try:
            session.commit()
            self.logger.info("successfully committed data ")
        except Exception as e:
            session.rollback()
            self.logger.exception("Something went wrong")
            raise
        finally:
            session.close()
            self.logger.info("Closing session")

    def run(self):
        raise NotImplementedError
        # request_starships = self.__request_all_starships__()
        # clean_data = self.__parse_data__(request_starships)
        # db_objects = self.__create_database_objects__(clean_data)
        # session = self.__session_maker__()
        # try:
        #     session.add_all(db_objects)
        #     self.__update_database__(session)
        #     self.logger.info("successfully updated DB")
        # except Exception as e:
        #     self.logger.exception("An error was encountered")
        #     raise e


if __name__ == "__main__":
    # stuff = UpdateDB.__request_all_starships__()
    # stuff2 = UpdateDB(category="starships").__parse_data__(stuff)
    UpdateDB(category="starships").run()
    # print(stuff2)
