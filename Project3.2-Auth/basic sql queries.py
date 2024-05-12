### Basic SQL Queries

INSERT INTO todos (title, description, priority, completed) 
VALUES ('Go to store', 'To pick up eggs', 4, False);
# don't need to specify id

SELECT * FROM todos;
# * means all rows and columns in todos table

SELECT title FROM todos;
# only return title column

SELECT title, description FROM todos;
# return title and description columns

SELECT * FROM todos WHERE priority = 5;
# return all rows and columns where priority is 5

SELECT * FROM todos WHERE title = 'Feed dog';
SELECT * FROM todos WHERE id=2;

SELECT * FROM todos WHERE priority > 3 AND completed = False;
SELECT * FROM todos WHERE priority > 3 OR completed = False;
# from github copilot 

UPDATE todos SET completed = True WHERE id=5;
# set completed to True where id is 5

DELETE FROM todos WHERE id=5;
DELETE FROM todos WHERE completed = 0;



### sqlite3
cd Project3-Todo
sqlite3 todos.db


.schema

insert into todos (title, description, priority, completed) values ('go to the store', 'Pick up eggs', 5, False);

select * from todos;

.mode column # change the output format
# also try .mode markdown, .mode box, .mode table
select * from todos;

delete from todos where id=4;