-- Users table
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT NOT NULL,
    --current_energy INTEGER,
    current_location TEXT
);

-- Tasks table
CREATE TABLE Tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    scheduled_time DATETIME,
    priority INTEGER,
    completed BOOLEAN,
    product_recommendation_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Advice table
CREATE TABLE Advice (
    advice_id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL
);

-- Products table
CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL,
    rating REAL,
    image_url TEXT
);

-- Inventory table
CREATE TABLE Inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- User_Preferences table
CREATE TABLE User_Preferences (
    preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Task_History table
CREATE TABLE Task_History (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    user_id INTEGER,
    completed_time DATETIME,
    FOREIGN KEY (task_id) REFERENCES Tasks(task_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- User_Energy_Level table
CREATE TABLE User_Energy_Level (
    energy_level_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    time_of_day TEXT,
    energy_level INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Urgency_Level table
CREATE TABLE Urgency_Level (
    urgency_level_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    urgency_level INTEGER,
    FOREIGN KEY (task_id) REFERENCES Tasks(task_id)
);

-- Task_Notes table
CREATE TABLE Task_Notes (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    text TEXT,
    FOREIGN KEY (task_id) REFERENCES Tasks(task_id)
);
