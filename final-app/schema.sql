DROP TABLE IF EXISTS Match;
DROP TABLE IF EXISTS ReviewPT;
DROP TABLE IF EXISTS WorkInGym;
DROP TABLE IF EXISTS hasIngredients;
DROP TABLE IF EXISTS Ingredients;
DROP TABLE IF EXISTS ReviewRecipes;
DROP TABLE IF EXISTS MakeRecipes;
DROP TABLE IF EXISTS Recipes;
DROP TABLE IF EXISTS ReviewGym;
DROP TABLE IF EXISTS FindGym;
DROP TABLE IF EXISTS PT;
DROP TABLE IF EXISTS GYM;
DROP TABLE IF EXISTS USERS;

CREATE TABLE USERS (
    user_id INT PRIMARY KEY NOT NULL,
    name VARCHAR(255),
    age INT NOT NULL,
    weight INT NOT NULL,
    fitness_goal VARCHAR(255) NOT NULL,
    allergy VARCHAR(255),
    day_streak INT NOT NULL,
    playlist_genre VARCHAR(255),
    address VARCHAR(255)
);

CREATE TABLE GYM (
    address VARCHAR(255) PRIMARY KEY,
    hours INT,
    name VARCHAR(255),
    phone INT,
    email VARCHAR(255)
);

CREATE TABLE PT (
    pt_id INT PRIMARY KEY,
    experience INT,
    name VARCHAR(255),
    phone INT
);

CREATE TABLE FindGym (
    user_id INT,
    gym_address VARCHAR(255),
    radius INT,
    PRIMARY KEY (user_id, gym_address)
);

CREATE TABLE ReviewGym (
    user_id INT,
    address VARCHAR(255),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    PRIMARY KEY (user_id, address)
);

CREATE TABLE Recipes (
    rid INT PRIMARY KEY,
    description VARCHAR(255),
    meal_name VARCHAR(255),
    calories INT,
    prep_time INT
);

CREATE TABLE MakeRecipes (
    user_id INT,
    rid INT,
    PRIMARY KEY (user_id, rid)
);

CREATE TABLE ReviewRecipes (
    user_id INT,
    rid INT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    PRIMARY KEY (user_id, rid)
);

CREATE TABLE Ingredients (
    name VARCHAR(255) PRIMARY KEY,
    serving VARCHAR(255)
);

CREATE TABLE hasIngredients (
    name VARCHAR(255),
    rid INT,
    PRIMARY KEY (name, rid)
);


CREATE TABLE WorkInGym (
    pt_id INT,
    address VARCHAR(255),
    PRIMARY KEY (pt_id, address)
);


CREATE TABLE ReviewPT (
    ratings INT,
    user_id INT,
    pt_id INT,
    PRIMARY KEY (user_id, pt_id)
);


CREATE TABLE Match (
    user_id INT,
    pt_id INT,
    PRIMARY KEY (user_id, pt_id)
);
