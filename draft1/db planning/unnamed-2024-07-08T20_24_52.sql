
CREATE TABLE Advice
(
  advice_id INTEGER NULL    ,
  text      TEXT    NOT NULL,
  PRIMARY KEY (advice_id AUTOINCREMENT)
);

CREATE TABLE Inventory
(
  inventory_id INTEGER NULL    ,
  user_id      INTEGER NULL    ,
  product_id   INTEGER NULL    ,
  quantity     INTEGER NULL    ,
  PRIMARY KEY (inventory_id AUTOINCREMENT),
  FOREIGN KEY (user_id) REFERENCES Users (user_id),
  FOREIGN KEY (product_id) REFERENCES Products (product_id)
);

CREATE TABLE Products
(
  product_id           INTEGER NOT NULL,
  name                 TEXT    NOT NULL,
  description          TEXT    NULL    ,
  price                REAL    NULL    ,
  rating               REAL    NULL    ,
  image_url            TEXT    NULL    ,
  product_referral_url TEXT    NULL    ,
  PRIMARY KEY (product_id AUTOINCREMENT)
);

CREATE TABLE Task_History
(
  history_id     INTEGER  NULL    ,
  task_id        INTEGER  NULL    ,
  user_id        INTEGER  NULL    ,
  completed_time DATETIME NULL    ,
  PRIMARY KEY (history_id AUTOINCREMENT),
  FOREIGN KEY (task_id) REFERENCES Tasks (task_id),
  FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE Task_Notes
(
  note_id INTEGER NULL    ,
  task_id INTEGER NULL    ,
  text    TEXT    NULL    ,
  PRIMARY KEY (note_id AUTOINCREMENT),
  FOREIGN KEY (task_id) REFERENCES Tasks (task_id)
);

CREATE TABLE Tasks
(
  task_id                   INTEGER  NULL    ,
  user_id                   INTEGER  NULL    ,
  title                     TEXT     NOT NULL,
  description               TEXT     NULL    ,
  scheduled_time            DATETIME NULL    ,
  priority                  INTEGER  NULL    ,
  completed                 BOOLEAN  NULL    ,
  product_recommendation_id INTEGER  NULL    ,
  PRIMARY KEY (task_id AUTOINCREMENT),
  FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE Urgency_Level
(
  urgency_level_id INTEGER NULL    ,
  task_id          INTEGER NULL    ,
  urgency_level    INTEGER NULL    ,
  PRIMARY KEY (urgency_level_id AUTOINCREMENT),
  FOREIGN KEY (task_id) REFERENCES Tasks (task_id)
);

CREATE TABLE User_Energy_Level
(
  energy_level_id INTEGER NULL    ,
  user_id         INTEGER NULL    ,
  time_of_day     TEXT    NULL    ,
  energy_level    INTEGER NULL    ,
  PRIMARY KEY (energy_level_id AUTOINCREMENT),
  FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE User_Preferences
(
  preference_id INTEGER NULL    ,
  user_id       INTEGER NULL    ,
  text          TEXT    NULL    ,
  PRIMARY KEY (preference_id AUTOINCREMENT),
  FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE Users
(
  user_id       INTEGER NULL    ,
  username      TEXT    NOT NULL,
  password_hash TEXT    NOT NULL,
  email         TEXT    NOT NULL,
  energy_level  INTEGER NULL    ,
  location      TEXT    NULL    ,
  PRIMARY KEY (user_id AUTOINCREMENT)
);
