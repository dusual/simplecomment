from sqlalchemy import *

db = create_engine('sqlite:///test.db')

db.echo = False  # Try changing this to True and see what happens

metadata = MetaData(db)

chapter = Table('Chapter', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(40)),
)
chapter.create()

i = chapter.insert()
i.execute(name='basic_func')

