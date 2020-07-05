from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


def today_tasks():
    today = datetime.today()
    # print(today.day) - the day of a current month.
    # print(today.strftime('%b'))  # the short name of the current month. I.e 'Apr'
    print()
    print(f'Today {today.day} {today.strftime("%b")}:')
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    if len(rows):  # In case rows list is not empty
        for row in rows:
            print(f"{row.id}. {row.task}")
        print()
    else:
        print("Nothing to do!")
        print()


def week_tasks():
    today = datetime.today()
    # print(today.day) - the day of a current month.
    # print(today.strftime('%b'))  # the short name of the current month. I.e 'Apr'
    print()
    for shift in range(7):  # Prints all tasks for 7 days from today.
        print(f'{(today + timedelta(days=shift)).strftime("%A")} {(today + timedelta(days=shift)).day}'
              f' {(today + timedelta(days=shift)).strftime("%b")}:')
        rows = session.query(Table).filter(Table.deadline == (today + timedelta(days=shift)).date()).all()
        if len(rows):  # In case rows list is not empty
            for row in rows:
                print(f"{row.id}. {row.task}")
            print()
        else:
            print("Nothing to do!")
            print()


def all_tasks():
    print()
    print('All tasks:')
    rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows):  # In case rows list is not empty
        for row in rows:
            print(f"{row.id}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        print()
    else:
        print("Nothing to do!")
        print()


def add_task():
    print()
    print("Enter task")
    new_task = input("> ")
    new_deadline = datetime.strptime(input("Enter deadline\n> "), '%Y-%m-%d')
    new_row = Table(task=new_task, deadline=new_deadline)
    session.add(new_row)
    session.commit()
    print("The task has been added!")
    print()


def missed_tasks():
    print()
    print('Missed tasks:')
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    if len(rows):  # In case rows list is not empty
        for row in rows:
            print(f"{row.id}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        print()
    else:
        print("Nothing is missed!")
        print()


def delete_task():
    print()
    print('Choose the number of the task you want to delete:')
    rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows):  # In case rows list is not empty
        for row in rows:
            print(f"{row.id}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        print()
    else:
        print("Nothing to do!")
        print()
    task_to_delete = int(input('> '))
    session.query(Table).filter(Table.id == task_to_delete).delete()
    session.commit()
    print("The task has been deleted!")
    print()


def print_menu():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    print("> ", end='')


def main():
    while True:
        print_menu()
        command = input()
        if command == "1":
            today_tasks()
        elif command == "2":
            week_tasks()
        elif command == "3":
            all_tasks()
        elif command == "4":
            missed_tasks()
        elif command == "5":
            add_task()
        elif command == "6":
            delete_task()
        elif command == "0":
            print()
            print("Bye!")
            break
        else:
            print("Error!")
            continue


if __name__ == '__main__':
    engine = create_engine('sqlite:///todo.db?check_same_thread=False')

    Base = declarative_base()


    class Table(Base):
        __tablename__ = 'task'
        id = Column(Integer, primary_key=True)
        task = Column(String, default='Nothing to do!')
        deadline = Column(Date, default=datetime.today().date())

        def __repr__(self):
            return self.task


    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    main()
