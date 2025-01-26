from typing import Type, List
from sqlalchemy import create_engine, Engine, text, ForeignKey, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
import os


Base = declarative_base()


def configure() -> None:
    load_dotenv()


class Person(Base):
    __tablename__ = 'people'

    people_id = Column("people_id", Integer, primary_key=True)
    ssn = Column("ssn", String)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    gender = Column("gender", String)
    age = Column("age", Integer)

    def __init__(self, people_id: Column[int], ssn: Column[str], firstname: Column[str], lastname: Column[str], gender: Column[str], age: Column[int]):
        super().__init__()
        self.people_id = people_id
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"{self.people_id} {self.ssn} {self.firstname} {self.lastname} {self.gender} {self.age}"


class Thing(Base):
    __tablename__ = 'things'
    thing_id = Column("thing_id", Integer, primary_key=True)
    description = Column("description", String)
    owner = Column("owner", String, ForeignKey("people.ssn"))

    def __init__(self, thing_id:Column[int], description: Column[str], owner: Column[str]):
        super().__init__()
        self.thing_id = thing_id
        self.description = description
        self.owner = owner

    def __repr__(self):
        return f"{self.thing_id} {self.description} owned by {self.owner}"


def postgres_get_engine() -> Engine:
    # Define the PostgreSQL URL
    postgresql_url = f"postgresql+psycopg2://{os.getenv('username')}:{os.getenv('password')}@{os.getenv('host')}:{os.getenv('port')}/{os.getenv('database')}"

    # Create an engine
    # Can also use create_engine(postgresql_url, echo=True) for more information for debugging purposes.
    p_engine = create_engine(postgresql_url)
    print(f"engine: {p_engine}")
    print(f"engine type: {type(p_engine)}")
    print(f"engine url: {p_engine.url}")

    return p_engine


def add_person(p_session: Session, in_person: Person) -> None:
    p_person = in_person
    p_session.add(p_person)


def add_things(p_session: Session, in_thing: Thing) -> None:
    p_thing = in_thing
    p_session.add(p_thing)


def commit(p_session: Session) -> None:
    p_session.commit()


def query_all_person(p_session: Session) -> list[Type[Person]]:
    p_person: list[Type[Person]] = p_session.query(Person).all() # filter(Person.people_id==1).first()
    # print(f"person type: {type(p_person)}")
    return p_person


def query_all_person_by_column(p_session: Session, filter_column: str, find: str) -> List[Type[Person]]:
    # Dynamically construct the filter condition
    filter_condition: bool = getattr(Person, filter_column) == find
    # Apply the filter
    p_person: list[Type[Person]] = p_session.query(Person).filter(filter_condition).all()
    # p_person = p_session.query(Person).filter_by(getattr(column)=find).all()
    # p_person = p_session.query(Person).filter_by(column=column).all()
    # print(f"person type: {type(p_person)}")
    return p_person


def query_all_person_using_in(p_session: Session, filter_column: str, filter_value: List) -> List[Type[Person]]:
    # Dynamically construct the filter condition
    filter_condition: bool = getattr(Person, filter_column).in_(filter_value)
    # Apply the filter
    p_person: list[Type[Person]] = p_session.query(Person).filter(filter_condition).all()
    return p_person


# This function needs to be more generic/dynamic regardless of the query statement
def query_person_using_statement(p_session: Session, statement: str) -> str:
    value: str = "-1"
    # res type: <class 'sqlalchemy.engine.cursor.CursorResult'>
    res = p_session.execute(text(statement))
    for val in res:
        value: str = f"{val[0]}"
        # print(f"value type: {type(value)}")
    # print(f"res: {res}")
    # print(f"[item[0] for item in res]: {[item[0] for item in res]}")
    # print(f"res type: {type(res)}")
    return value #f"{[item[0] for item in res]}"


def main() -> None:
    configure()
    engine = postgres_get_engine()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # add_person(session, Person(1, 12345, 'Mike', 'Smith', 'M', 35))
    # add_person(session, Person(2, 48288, 'Anna', 'Blue', 'F', 40))
    # add_person(session, Person(3, 63684, 'Bob', 'Blue', 'M', 32))
    # add_person(session, Person(4, 79493, 'Angela', 'Cold', 'F', 22))
    # commit(session)

    print(query_all_person(session))
    print(query_all_person_by_column(session, "ssn", "12345"))
    print(query_all_person_using_in(session, "firstname", ["Angela", "Mike"]))
    # people_l = query_all_person_using_in(session, "firstname", ["Mike"])
    # print(f"people_l type: {type(people_l)}")
    # print(f"item 1: {[item[1] for item in people_l]}")

    # ssn = query_person_using_statement(session, "SELECT ssn FROM people where firstname = 'Mike'")
    # print(f"ssn: {ssn}")
    # print(f"ssn type: {type(ssn)}")
    # add_things(session, Thing(1, "Car", query_person_using_statement(session, "SELECT ssn FROM people where firstname = 'Mike'")))
    # add_things(session, Thing(2, "Laptop", query_person_using_statement(session, "SELECT ssn FROM people where firstname = 'Mike'")))
    # add_things(session, Thing(3, "PS5", query_person_using_statement(session, "SELECT ssn FROM people where firstname = 'Anna'")))
    # add_things(session, Thing(4, "Tools", query_person_using_statement(session, "SELECT ssn FROM people where firstname = 'Bob'")))
    # add_things(session, Thing(5, "Book", query_person_using_statement(session, "SELECT ssn FROM people where firstname = 'Angela'")))
    # commit(session)

    print(session.query(Thing, Person).filter(Thing.owner == Person.ssn).filter(Person.firstname == "Anna").all())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
