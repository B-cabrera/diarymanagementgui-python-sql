drop database if exists databaseMGMT_database;
create database databaseMGMT_database;
use databaseMGMT_database;

drop table if exists users;
drop table if exists Admin;
drop table if exists Manager;
drop table if exists Databases_Management;
drop table if exists Diary_Management;
drop table if exists Server;
drop table if exists Entry_Management;
drop table if exists Diary_Catalog;
drop table if exists Entry_Catalog;
drop table if exists Edit_Log;
drop table if exists Works_For;
drop table if exists Entry_log;
 

create table if not exists users(
User_ID int primary key not null,
First_Name varchar(45),
Last_Name varchar(45),
Username varchar(45),
Password varchar(45));

create table if not exists Admin(
Admin_ID int primary key not null,
First_Name varchar(45),
Last_Name varchar(45),
Username varchar(45),
Password varchar(45));

create table if not exists Manager(
Manager_ID int primary key not null,
First_Name varchar(45),
Last_Name varchar(45),
Username varchar(45),
Password varchar(45));

create table if not exists Databases_Management(
User_ID int,
Diary_Name varchar(45),
Diary_ID int,Entry_ID int,
Entry_Date datetime, 
foreign key (User_ID) references users(User_ID), 
foreign key (Diary_ID) references Diary_Management(Diary_ID), 
foreign key (Entry_ID) references Entry_Management(Entry_ID));

create table if not exists Diary_Management(
Diary_ID int not null primary key , 
Diary_Name varchar(45) not null,
Entry_Name varchar(45),
Entry_Date datetime,
Entry_ID int,
foreign key (Entry_ID) references Entry_Management(Entry_ID));

create table if not exists Server(
User_ID int not null, Diary_Entry varchar(45),
Diary_ID int,
Entry_ID int,Entry_Date datetime, 
foreign key (User_ID) references users(User_ID), 
foreign key (Diary_ID) references Diary_Management(Diary_ID), 
foreign key (Entry_ID) references Entry_Management(Entry_ID));

create table if not exists Entry_Management(
Entry_ID int not null primary key, 
Diary_Name varchar(45),
Entry_Name varchar(45),
Entry_Date datetime,Diary_ID int, 
foreign key (Diary_ID) references Diary_Management(Diary_ID));

create table if not exists Diary_Catalog(
DiaryCatalog_ID int, Diary_ID int,
DiaryCatalog_Name varchar(45),
DiaryCatalog_Date datetime,Diary_Name varchar(45),
foreign key (Diary_ID) references Diary_Management(Diary_ID));

create table if not exists Entry_Catalog(
EntryCatalog_ID int, Entry_ID int,
EntryCatalog_Name varchar(45),EntryCatalog_Date datetime,
Entry_Name varchar(45),
foreign key (Entry_ID) references Entry_Management(Entry_ID));

create table if not exists Edit_Log(
Diary_Name varchar(45), Entry_ID int not null,
Diary_ID int,Entry_Time datetime,
Edit_Comment varchar(45),
foreign key (Entry_ID) references Entry_Management(Entry_ID),
foreign key (Diary_ID) references Diary_Management(Diary_ID));

create table if not exists Works_For(
Manager_ID int, Admin_ID int, 
foreign key (Manager_ID) references Manager(Manager_ID),
foreign key (Admin_ID) references Admin(Admin_ID));

create table if not exists Entry_Log(
Entry_ID int,
Entry_Content varchar(200),
Diary_ID int,
foreign key (Entry_ID) references Entry_Management(Entry_ID),
foreign key (Diary_ID) references Diary_Management(Diary_ID));


explain users;
explain Admin;
explain Manager;
explain Databases_Management;
explain Diary_Management;
explain Server;
explain Entry_Management;
explain Diary_Catalog;
explain Entry_Catalog;
explain Edit_Log;
explain Works_For;
explain Entry_Log;