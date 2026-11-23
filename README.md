# rooms_students_practice
PROJECT TITLE:
rooms_students_practice

TASK DESCRIPTION:
Problem statement
Using MySQL database (or other relational database, for example, PostgreSQL) to create a data schema corresponding to the files in the attachment (many-to-one relationship)
Write a script to load these two files and write data to the database.
Necessary queries to the database
List of rooms and the number of students in each of them
5 rooms with the smallest average age of students
5 rooms with the largest difference in the age of students
List of rooms where different-sex students live
Requirements and comments
Propose options for optimizing queries using indexes
As a result we need to generate a SQL query that adds the required indexes.
Unload the result in JSON or XML format
All the “math” should be done at the database level
The command interface should support the following input parameters
5.1. students (path to students file)
5.2. rooms (path to the rooms file)
5.3. format (output format: xml or json)
5.4. use OOP and SOLID
5.5. no ORM (use SQL)
Before you begin the task 
Make sure you have understood the condition correctly 
Created and configured the virtual environment 
Designed the architecture 

TECH STACK:
Python, MS SQL Server, T-SQL

PROJECT STRUCTURE: 
main.py -- coordination of all structure units
loaders.py -- read data from json files
repository.py -- creation and processing db tables 
database.py -- connect to local db 
exporters.py -- load results of sql queries into xml/json files
input -- folder with task files
output -- folder with result files

CHALLENGES & LEARNINGS:
It was the first project with db connection, so i had to learn how to work with sql in python, read and write tables, work with json and xml formats 

AUTHOR:
ivanlukhtsin-prog

