use databaseMGMT_database;
set foreign_key_checks = 0;
set sql_safe_updates = 0;


insert into Admin values(1,"Justin","Sterlacci","JSterlacci","Password1234"),
(2,"Brenden","Cabrera ","BCabrera","Pass10312022"),
(3,"Nicholas","Psaras","NPsaras","Password03032000"),
(4,"Kyra","Paddock","KPaddock","lil_Peep95"),
(5,"Chase","Evans","CEvans","Phonk1023$"),
(6,"Brady","Young","BYoung","BallCap1923"),
(7,"Fredrick","Berbrich","FBerbrich","Frilly$102"),
(8,"Abby","Castonguay","ACastonguay","Pass102847"),
(9,"Racheal","Oksa","ROksa","Password10848"),
(10,"Lillian","McPadden","LMcPadden","Password$567839");
				
insert into Databases_Management values(1,"Notes",01,01,CURRENT_TIME),
(1,"Homework",02,01,CURRENT_TIME),
(3,"Personal",01,05,CURRENT_TIME),
(5,"Homework",07,35,CURRENT_TIME),
(10,"Study Guide",15,2,CURRENT_TIME),
(7,"Fantasy Lineup",03,01,CURRENT_TIME),
(2,"Roommate Meeting",03,03,CURRENT_TIME),
(9,"Housing Issues",01,01,CURRENT_TIME),
(8,"Schedule",02,02,CURRENT_TIME),
(4,"Notes",01,01,CURRENT_TIME);

insert into Diary_Catalog values
(1, 1, "School", CURRENT_TIME, "Homework"),
(2, 2, "Personal", CURRENT_TIME, "Personal"),
(3, 3, "Work", CURRENT_TIME, "Schedule"),
(4, 4, "Dorm", CURRENT_TIME, "Housing Issues"),
(5, 5, "Hobby", CURRENT_TIME, "Fantasy Lineup"),
(6, 6, "To-Do", CURRENT_TIME, "Study Guide"),
(7, 7, "School", CURRENT_TIME, "Notes"),
(8, 8, "Dorm", CURRENT_TIME, "Roommate Meeting"),
(9, 9, "School", CURRENT_TIME, "Schedule"),
(10,10, "Personal", CURRENT_TIME, "Notes");

insert into Diary_Management values
(1, "Homework", "Tuesday Class", CURRENT_TIME, 3),
(2, "Personal", "Groceries", CURRENT_TIME, 4),
(3, "Schedule", "Fantasy Game", CURRENT_TIME, 7),
(4, "Housing Issues", "Bathroom Fix", CURRENT_TIME, 1),
(5, "Fantasy Lineup", "Player Performance", CURRENT_TIME, 9),
(6, "Study Guide", "Midterm", CURRENT_TIME, 2),
(7, "Notes", "Wednesday Class", CURRENT_TIME, 5),
(8, "Roomate Meeting", "Friday Meeting", CURRENT_TIME, 8),
(9, "Homework", "Thursday Class", CURRENT_TIME, 6),
(10, "Notes", "Friday Class", CURRENT_TIME, 10);

insert into Edit_Log values
("Homework", 6, 9, CURRENT_TIME, "Finished Homework"),
("Notes", 10, 10, CURRENT_TIME, "Added more notes"),
("Roommate Meeting", 8, 8, CURRENT_TIME, "Added new rules"),
("Notes", 5, 7, CURRENT_TIME, "Added more information"),
("Housing Issues", 1, 4, CURRENT_TIME, "Removed problems"),
("Personal", 4, 2, CURRENT_TIME, "Finished groceries"),
("Homework", 3, 1, CURRENT_TIME, "Removed diagrams"),
("Schedule", 7, 3, CURRENT_TIME, "Added rest of games"),
("Fantasy Lineup", 9, 5, CURRENT_TIME, "Added new stats"),
("Study Guide", 2, 6, CURRENT_TIME, "Removed new test");

insert into Entry_Catalog values
(1, 3, "Removing", CURRENT_TIME, "Tuesday Class"),
(2, 6, "Done", CURRENT_TIME, "Thursday Class"),
(1, 1, "Removing", CURRENT_TIME, "Bathroom Fix"),
(2, 4, "Done", CURRENT_TIME, "Groceries"),
(3, 10, "Adding", CURRENT_TIME, "Friday Class"),
(1, 2, "Removing", CURRENT_TIME, "Midterm"),
(3, 5, "Adding", CURRENT_TIME, "Wednesday Class"),
(3, 8, "Adding", CURRENT_TIME, "Friday Meeting"),
(3, 9, "Adding", CURRENT_TIME, "Player Performance"),
(3, 7, "Adding", CURRENT_TIME, "Fantasy Game");


insert into Entry_Management values
(1, "Housing Issues", "Bathroom Fix", CURRENT_TIME, 4),
(2, "Study Guide", "Midterm", CURRENT_TIME, 6),
(3, "Homework", "Tuesday Class", CURRENT_TIME, 1),
(4, "Personal", "Groceries", CURRENT_TIME, 2),
(5, "Notes", "Wednesday Class", CURRENT_TIME, 7),
(6, "Homework", "Thursday Class", CURRENT_TIME, 9),
(7, "Schedule", "Fantasy Game", CURRENT_TIME, 3),
(8, "Roomate Meeting", "Friday Meeting", CURRENT_TIME, 8),
(9, "Fantasy Lineup", "Player Performance", CURRENT_TIME, 5),
(10, "Notes", "Friday Class", CURRENT_TIME, 10);

insert into Manager values(1,"Justin","Sterlacci","JSterlacci","Password1234"),
(2,"Brenden","Cabrera ","BCabrera","Pass10312022"),
(3,"Nicholas","Psaras","NPsaras","Password03032000"),
(4,"Kyra","Paddock","KPaddock","lil_Peep95"),
(5,"Chase","Evans","CEvans","Phonk1023$"),
(6,"Brady","Young","BYoung","BallCap1923"),
(7,"Fredrick","Berbrich","FBerbrich","Frilly$102"),
(8,"Abby","Castonguay","ACastonguay","Pass102847"),
(9,"Racheal","Oksa","ROksa","Password10848"),
(10,"Lillian","McPadden","LMcPadden","Password$567839");

insert into Server values 
(1, "Homework -> Done", 1, 3, CURRENT_TIME),
(4, "Bathroom work is done", 4,1, CURRENT_TIME),
(10, "Groceries are all done", 2,4, CURRENT_TIME),
(7, "We won our fantasy game", 3,7, CURRENT_TIME),
(2, "He scored no points", 5, 9, CURRENT_TIME),
(9, "We have a pop quiz tomorrow", 10,10, CURRENT_TIME),
(6, "Midterm is next week", 6,2, CURRENT_TIME),
(5, "All roommates are fine", 8,8, CURRENT_TIME),
(3, "Essay due tomorrow", 9,6, CURRENT_TIME),
(8, "History is fun", 7,5, CURRENT_TIME);


insert into users values(1,"Justin","Sterlacci","JSterlacci","Password1234"),
(2,"Brenden","Cabrera ","BCabrera","Pass10312022"),
(3,"Nicholas","Psaras","NPsaras","Password03032000"),
(4,"Kyra","Paddock","KPaddock","lil_Peep95"),
(5,"Chase","Evans","CEvans","Phonk1023$"),
(6,"Brady","Young","BYoung","BallCap1923"),
(7,"Fredrick","Berbrich","FBerbrich","Frilly$102"),
(8,"Abby","Castonguay","ACastonguay","Pass102847"),
(9,"Racheal","Oksa","ROksa","Password10848"),
(10,"Lillian","McPadden","LMcPadden","Password$567839");

insert into Works_For values 
(1,9),
(1,3),
(2,6),
(2,1),
(3,2),
(3,8),
(3,4),
(3,10),
(4,5),
(5,7);

insert into Entry_Log values 
(1, "We fixed the sink.", 4),
(2, "Midterm is tommorow @ 9.", 6),
(3, "Essay is due @ 11:59", 1),
(4, "Eggs, Cheese, Bacon", 2),
(5, "We did good on our project!", 7),
(6, "We have a project due Tuesday.", 9),
(7, "Game tommorow @ 10", 3),
(8, "Everything is great.", 8),
(9, "Star player did great.", 5),
(10, "Got a 90 on the test.", 10);



select * from entry_management;
select count(*) from Databases_Management where User_ID = 1;
select * from Diary_Catalog order by Diary_ID;
select distinct(Diary_ID) from Diary_Management;
select avg(Diary_ID) from Edit_Log;
select Entry_Catalog.Entry_ID, Entry_Management.Entry_ID
from Entry_Catalog
left join Entry_Catalog on Entry_Catalog.Entry_ID = Entry_Management.Entry_ID;
select Server.User_ID, users.User_ID
from Server
right join users on Server.User_ID = users.User_ID;
select Manager.Manager_ID, Works_For.Manager_ID
from Works_For
inner join Works_For on Manager.Manager_ID = Works_For.Manager_ID;



alter table users add column age int;
alter table users drop column age;
alter table Works_For rename column Manager_ID to ID_Manager;
alter table Edit_Log modify column Edit_Comment char(200);
alter table Admin add column age int;
alter table Admin drop column age;


update Server
set User_ID = 5
where Entry_ID = 3;

update Server
set Diary_Entry = "I just finished my homework"
where User_ID = 8;

update users
set First_Name = "Brody"
where User_ID = 2;

update users
set First_Name = "Jeff"
where User_ID REGEXP '$S';


select * from users;

select avg(10, 6);
show variables like '%default_storage_engine%';
alter table users auto_increment = 10;

INSERT INTO users(Username, Password, First_Name, Last_Name) value ("boofdoof", md5('hey'), "John", "Legend");








