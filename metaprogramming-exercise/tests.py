from unittest import TestCase
import unittest
from textwrap import dedent
from dataclasses import dataclass
from typing import Callable, Any, Dict
import os


@dataclass
class Field:
    """
    Defines a field with a label and preconditions
    """
    label: str
    precondition: Callable[[Any], bool] = None

# Record and supporting classes here
class RecordMeta(type):
    def __new__(cls, name, bases, attr):
        _class = super(RecordMeta, cls).__new__(cls, name, bases, attr)
        setattr(_class,"attr",cls.mro)
        return _class

# Set the metaclass of the Record class
class Record(metaclass=RecordMeta):
    pass

# Usage of Record
class Person(Record):
    """
    A simple person record
    """ 
    name: str = Field(label="The name") 
    age: int = Field(label="The person's age", precondition=lambda x: 0 <= x <= 150)
    income: float = Field(label="The person's income", precondition=lambda x: 0 <= x)

    def __init__(self,name,age,income):
        Person.name = name
        if 0<= age <=150:
            Person.age = age
        else:
            raise TypeError('Value must be in range ')
        
        if 0 <= income:
            Person.income = income
        else:
            raise TypeError('Value must be in range ')
        

    def __setattr__(self, key, value):

        if key == 'age':
            if  not isinstance(value,int):
                raise TypeError('')
        if key == 'name' and hasattr(self,'name'):
            raise AttributeError('The value for the name attribute has already been set, and can not be re-set')
        elif key == 'age' and hasattr(self,'age'):
            raise AttributeError('The value for the name attribute has already been set, and can not be re-set')
        elif key == 'income' and hasattr(self,'income'):
            raise AttributeError('The value for the name attribute has already been set, and can not be re-set')
        if key in 'age':
            self.__dict__[key] = int(value)
        if key in 'income':
            self.__dict__[key] = float(value)


        self.__dict__[key] = value



    def __str__(self):
        return dedent("""
                Person(
                  # The name
                  name='{self.name}'

                  # The person's age
                  age={self.age}

                  # The person's income
                  income={self.income}
                )
         """).strip().format(self=self)
    
    @property
    def name(self):
        # the name property
        return self.name
    @name.setter
    def name(self,name):
        self.name = name

    @property
    def age(self):
        return self.age

    @age.setter
    def age(self,age):
        if ( (age >=0) or (age <=150) ) and isinstance(age,int):
            self.age = age
        else:
            raise TypeError('Wrong type or invalid value')       
    @property
    def income(self):
        # the income property
        return self.income
    
    @income.setter
    def income(self,income):
        self.income = income

    
class Named(Record):
    """
    A base class for things with names
    """
    name: str = Field(label="The name") 
    def __init__(self,name):
        Named.name = name
        # Record.__init__()

    @property
    def name(self):
        return self.name

class Animal(Named):
    """
    An animal
    """
    habitat: str = Field(label="The habitat", precondition=lambda x: x in ["air", "land","water"])
    weight: float = Field(label="The animals weight (kg)", precondition=lambda x: 0 <= x)

    def __init__(self,habitat,weight,name):
        if habitat in ["air","land","water"]:
            Animal.habitat = habitat
        else:
            raise TypeError('value not int range')
        if 0 <= weight: 
            Animal.weight = weight
        else:
            raise TypeError('value not in range')
        # Named.__init__(self,name)

    @property
    def habitat(self):
        return self.habitat

    @property
    def weight(self):
        return self.weight
      
class Dog(Animal):
    """
    A type of animal
    """
    bark: str = Field(label="Sound of bark")

    def __init__(self,bark,name,habitat,weight):
        Dog.bark = bark
        Animal.__init__(self,habitat,weight,name)
        Named.__init__(self,name)

    @property 
    def bark(self):
        return self.bark
# Tests 
class RecordTests(TestCase):

    # __metaclass__ = RecordMeta

    # @classmethod
    # def setUpClass(cls):
    #     return super().setUpClass()

        
    def test_creation(self):
        Person(name="JAMES", age=110, income=24000.0)
        with self.assertRaises(TypeError): 
            Person(name="JAMES", age=160, income=24000.0)
        with self.assertRaises(TypeError): 
            Person(name="JAMES")
        with self.assertRaises(TypeError): 
            Person(name="JAMES", age=-1, income=24000.0)
        with self.assertRaises(TypeError): 
            Person(name="JAMES", age="150", income=24000.0)
        with self.assertRaises(TypeError): 
            Person(name="JAMES", age="150", wealth=24000.0)
    
    def test_properties(self):
        james = Person(name="JAMES", age=34, income=24000.0)
        self.assertEqual(james.age, 34)
        with self.assertRaises(AttributeError):
            james.age = 32
    
    def test_str(self):
        james = Person(name="JAMES", age=34, income=24000.0)
        correct = dedent("""
        Person(
          # The name
          name='JAMES'

          # The person's age
          age=34

          # The person's income
          income=24000.0
        )
        """).strip()
        self.assertEqual(str(james), correct)

    def test_dog(self):
        mike = Dog(name="mike", habitat="land", weight=50., bark="ARF")
        self.assertEqual(mike.weight, 50)
        
if __name__ == '__main__':
    unittest.main()