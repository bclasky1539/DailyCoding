# This is a sample Python script.
# from importlib.metadata import metadata

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from sqlalchemy import create_engine, Connection, Engine, text, Table
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
import os

Base = declarative_base()  # same declarative_base() as usual


def configure() -> None:
    load_dotenv()


def print_hi(name) -> None:
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def postgres_get_engine() -> Engine:
    # Define the PostgreSQL URL
    postgresql_url = f"postgresql+psycopg2://{os.getenv('username')}:{os.getenv('password')}@{os.getenv('host')}:{os.getenv('port')}/{os.getenv('database')}"

    # Create an engine
    p_engine = create_engine(postgresql_url)
    print(f"engine: {p_engine}")
    print(f"engine type: {type(p_engine)}")
    print(f"engine url: {p_engine.url}")

    return p_engine


def postgres_connect(p_engine:  Engine) -> Connection:
    # Establish a connection
    print(f"Connecting to PostgreSQL...")
    p_connection = p_engine.connect()
    print(f"connection: {p_connection}")
    print(f"connection type: {type(p_connection)}")
    print(f"Connected to PostgreSQL")

    return p_connection


def postgres_create_tables() -> None:
    pass


def postgres_drop_tables() -> None:
    pass


def postgres_get_session(p_engine: Engine) -> Session:
    # Bind the engine to the session
    p_session = sessionmaker(bind=p_engine) ()
    print(f"session: {p_session}")
    print(f"session type: {type(p_session)}")

    return p_session


def postgres_create_session():
    pass


def postgres_close(p_connection: Connection) -> None:
    # Close the connection
    print(f"Disconnecting to PostgreSQL...")
    p_connection.close()


# Press the green button in the gutter to run the script.
def main() -> None:
    configure()
    engine = postgres_get_engine()
    # connection = postgres_connect(engine)

    Base.metadata.create_all(engine)
    error_table = Table("error_log",  Base.metadata, autoload_with=engine)
    print(f"error_table: {error_table}")
    print(f"error_table type: {type(error_table)}")
    sql_stmt = text(f"select source_system,key_column_value from public.error_log")
    # print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print(f"!!!!!!!!! Before first with !!!!!!!!!")
    with engine.connect() as connection:
        result1 = connection.execute(sql_stmt)
        for row in result1:
            print(f"row: {row}")
            print(f"row type: {type(row)}")
            print(f"source_system: {row.source_system}, key_column_value: {row.key_column_value}")
            # row_as_dict = row._mapping

        # print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(f"!!!!!!!!!! After first with !!!!!!!!!")
        # print(f"connection: {connection}")
        # print(f"connection type: {type(connection)}")

        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"Now insert new record...")
        # with engine.connect() as connection:
        connection.execute(error_table.insert(), {'source_system': 'Vulnerabilities', 'key_column_value': 'Column 4 value', 'parsed_column': 'Column 4 value parsed',
                                                  'actual_column_value': 'Column 4 value actual', 'description': 'Column 4 value description',
                                                  'adt_ins_tstmp': '2014-12-26 18:06:00'})
        connection.commit()  # commit the transaction

        # List of dicts
        errors = [
            {'source_system': 'Vulnerabilities', 'key_column_value': 'Column 5 value',
             'parsed_column': 'Column 5 value parsed', 'actual_column_value': 'Column 5 value actual',
             'description': 'Column 5 value description', 'adt_ins_tstmp': '2014-12-31 09:55:00'},
            {'source_system': 'Vulnerabilities', 'key_column_value': 'Column 6 value',
             'parsed_column': 'Column 6 value parsed', 'actual_column_value': 'Column 6 value actual',
             'description': 'Column 6 value description', 'adt_ins_tstmp': '2014-12-31 09:55:00'},
        ]
        print(f"errors: {errors}")
        print(f"errors type: {type(errors)}")
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"Now insert bulk of records...")
        # with engine.connect() as connection:
        connection.execute(error_table.insert().values(errors))
        connection.commit()  # commit the transaction

        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"!!!!!!!!! After new records !!!!!!!!!")
        # with engine.connect() as connection:
        result2 = connection.execute(sql_stmt)
        for row in result2:
            print(f"row: {row}")
            print(f"row type: {type(row)}")
            print(f"source_system: {row.source_system}, key_column_value: {row.key_column_value}")
            # row_as_dict = row._mapping

        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"!!!!!!!!!!! Get sequence !!!!!!!!!!!!")
        # with engine.connect() as connection:
        result3 = connection.execute(text("select COALESCE(MAX(errlog_id),0) errorlog_id_max from public.error_log"))
        for row in result3:
            print(f"row: {row}")
            print(f"row type: {type(row)}")
            print(f"errorlog_id_max: {row.errorlog_id_max}")
            # row_as_dict = row._mapping

    '''
    with engine.begin() as connection:
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"!!!!!!!!! Update record 6 !!!!!!!!!!!")
        sql_stmt_update = f"update(error_log).where(error_log.c.errorlog_id == bindparam('errorlog_id')).values(description=bindparam('newdescription'))"
        print(f"sql_stmt_update: {sql_stmt_update}")
        print(f"sql_stmt_update type: {type(sql_stmt_update)}")
        errors_update = [
            {'errorlog_id': 5, 'newdescription': 'Column 55 value description'},
            {'errorlog_id': 6, 'newdescription': 'Column 66 value description'},
        ]
        print(f"errors_update: {errors_update}")
        print(f"errors_update type: {type(errors_update)}")
        connection.execute(error_table.update(), errors_update)
    '''

    session = postgres_get_session(engine)

    postgres_close(connection)


if __name__ == '__main__':
    main()
