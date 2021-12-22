from sqlalchemy.orm import relationship

import base
from sqlalchemy import Column, Integer, String, Date, ForeignKey


class Company(base.Base):
    __tablename__ = 'company'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', Text)
    adress = Column('adress', Text)

    def __repr__(self):
        return "<Company(id='{}', name='{}', adress='{}')>" \
            .format(self.id, self.name, self.adress)


class Department(base.Base):
    __tablename__ = 'department'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', Text)
    id_company = Column('id_company', Integer, ForeignKey('company.id'))

    def __repr__(self):
        return "<Department(id='{}', name='{}', id_company='{}')>" \
            .format(self.id, self.name, self.id_company)


class Employee(base.Base):
    __tablename__ = 'employee'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', Text)
    position = Column('position', Text)
    seniority = Column('seniority', Text)
    id_department = Column('id_department', Integer, ForeignKey('department.id'))

    def __repr__(self):
        return "<Employee(id='{}', name='{}', position='{}',seniority='{}', id_department='{}')>" \
            .format(self.id, self.name, self.position, self.seniority, self.id_department)


class Project(base.Base):
    __tablename__ = 'project'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', Text)
    income = Column('income', Integer)
    outcome = Column('outcome', Integer)

    def __repr__(self):
        return "<Employee(id='{}', name='{}', income='{}',outcome='{}')>" \
            .format(self.id, self.name, self.income, self.outcome)

