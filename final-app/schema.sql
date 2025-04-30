DROP TABLE IF EXISTS USERS
DROP TABLE IF EXISTS GYM
DROP TABLE IF EXISTS PT
DROP TABLE IF EXISTS FindGym
DROP TABLE IF EXISTS ReviewGym
DROP TABLE IF EXISTS Recipes
DROP TABLE IF EXISTS MakeRecipes
DROP TABLE IF EXISTS ReviewRecipes
DROP TABLE IF EXISTS Ingredients
DROP TABLE IF EXISTS hasIngredients
DROP TABLE IF EXISTS WorkInGym
DROP TABLE IF EXISTS ReviewPT
DROP TABLE IF EXISTS Match


CREATE TABLE USERS (
user_id INT PRIMARY KEY NOT NULL ,
Name VARCHAR(255)
age INT NOT NULL,
weight INT NOT NULL,
fitness_goal VARCHAR(255) NOT NULL,
allergy VARCHAR(255),
day_streak int NOT NULL,
playlist_genre VARCHAR(255)
Address varchar (255)
)


CREATE TABLE GYM (
Address varchar(255) PRIMARY KEY,
Hours int,
Name varchar(255),
Phone int,
Email varchar(255)
)

CREATE TABLE PT (
pt_id int PRIMARY KEY,
Experience int,
name varchar (255),
Phone int
)

CREATE TABLE FindGym(
User_id int PRIMARY KEY,
gym_Address varchar(255)  PRIMARY KEY,
Radius int
)

CREATE TABLE ReviewGym(
	User_id int PRIMARY KEY,
Address varchar(255)  PRIMARY KEY,
Rating int CHECK (rating>=1 AND rating<=5)

)


CREATE TABLE Recipes (

	Rid int PRIMARY KEY,
Description varchar(255),
Meal_name varchar(255),
Calories int,
Prep time int
)

CREATE TABLE MakeRecipes(
User_id int PRIMARY KEY,
Rid int PRIMARY KEY,
)

CREATE TABLE ReviewRecipes(
User_id int PRIMARY KEY,
Rid int PRIMARY KEY,
Rating int CHECK (rating>=1 AND rating<=5

)



CREATE TABLE Ingredients(
	Name varchar (255) PRIMARY KEY,
	Serving varchar (255),
)


CREATE TABLE hasIngredients(
	Name varchar (255)PRIMARY KEY
	Rid int PRIMARY KEY
)


CREATE TABLE WorkInGym(
	Pt_id int PRIMARY KEY,
	Address PRIMARY KEY,
)


CREATE TABLE ReviewPT(
	Ratings int,
	User_id int PRIMARY KEY,
pt_id int PRIMARY KEY,
)

CREATE TABLE Match (
	User_id int PRIMARY KEY,
	Pt_id int PRIMARY KEY,
)
