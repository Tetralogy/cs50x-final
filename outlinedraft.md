<!-----



Conversion time: 3.139 seconds.


Using this Markdown file:

1. Paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β36
* Mon Jul 15 2024 11:40:49 GMT-0700 (PDT)
* Source doc: schema for cleaning app
* Tables are currently converted to HTML tables.
----->


Basic user experience outline

TODO: #23 FULL APP MOCKUP

DONE #4 1. Register/create an account
    1. Login
    2. Logout
    3. Session cookies and user activity etc.
2. Onboarding
    4. Establish the user’s home environment
        1. House size
        2. Number of levels
        3. Layout



            1. 
Important rooms


                1. Bedrooms
                2. Bathrooms
                3. kitchen
                4. Others
                5. Etc.
    5. User’s abilities and disabilities are entered
        4. This will affect the evaluation of effort required and advice for tasks, as well as products/services suggested
    6. Initial Walkthrough
        5. Systematically go to every room in the house to note workload
        6. App guides and prompts and User takes wide photo of each area to annotate later
        7. Interior spaces documented
        8. Exterior spaces if applicable based on user’s initial setup
    7. Annotation and organization of tasks
        9. User clicks on each area in the photos to be cleaned and maintained and is visually marked up
        10. Information about specific spots is entered



            2. 
Appliances


            3. 
Surface types per room


            4. 
General usage and lifestyle of spaces


                6. Frequency of use
                7. Importance
                8. Aesthetical issues
                9. Dirtiness and effort required
                10. Tools/supplies on hand
                11. Tools/supplies required



            5. 
User needs to do 


        11. Map of house with visualizations of amount of work and type of tasks is populated



            6. 
Markers, colors, graphs and other ways to show progress at a glance


        12. A master task list is generated



            7. 
The tasks must be reasonably simplified such that each are not whole projects but easily completed in a short period of time.


            8. 
The list of tasks is organized as a “Do next” or “Do now” based on urgency score and user availability.


            9. 
The urgency score for each task is updated dynamically based on several factors


                12. Preparing for visits
                13. Messes by pets or kids
                14. Things need repair or replacement
                15. etc.



            10. 
The user’s current status is the main determinant of what the next task should be and when


                16. Where in the house is the user currently?
                17. Does the user have the supplies on hand for the task?
                    1. If not, acquiring the tools will be an attached guided task
                18. What is the user’s current focus?
                19. What is most important for the user currently?
                20. What is the user’s mental mood and physical energy currently?
                    2. Biometric data or user input
                21. User’s schedule and availability



            11. 
Tasks are reasonably spaced out and logically sequenced and intelligently scheduled


        13. Guidance



            12. 
General advice and “how to” is provided for common tasks


                22. Product recommendations are linked, $ purchases can be made



            13. 
Unique tailored suggestions are given for disabilities and difficulties


                23. Services can be linked or integrated into the app for ease of use and consolidation
                    3. $ subscriptions



            14. 
Encouragement and other “juice” to keep the user motivated


        14. Original walkthrough photo is the visual for the before image unless otherwise updated
3. Task completion
    8. As each task is completed the user is required to upload an “after” photo to officially mark them as completed
    9. Statistics and graphs are updated to show progress over time and other things the user might be interested in
4. Automation
    10. Combined with the products and services suggestions the user is guided to practical ways to automate tasks and make home maintenance easier until all tasks are fully automated and accounted for


# Tables

### Basic User Experience Outline

#### 1. Account Management

- **Register/Create an Account**

  - User inputs: Username, Email, Password

  - Verification: Email verification

- **Login**

  - User inputs: Username, Password

  - Authentication: Secure login with session management

- **Logout**

  - Ends user session

- **Session Cookies and User Activity**

  - Track user activity

  - Maintain session cookies for a seamless experience

#### 2. Onboarding

- **Establish the User’s Home Environment**

  - **House Size**

	- Total square footage

	- Number of levels

  - **Layout**

	- Floor plans or general layout description

  - **Important Rooms**

	- Bedrooms

	- Bathrooms

	- Kitchen

	- Living room

	- Dining room

	- Home office

	- Other specific rooms (e.g., laundry room, garage)

- **User’s Abilities and Disabilities**

  - Input any disabilities or physical limitations

  - Adjust task difficulty and recommendations accordingly

#### 3. Initial Walkthrough

- **Document Interior Spaces**

  - Guide user through each room

  - User takes wide photos of each area

  - App prompts for key information

- **Document Exterior Spaces**

  - If applicable, based on user’s initial setup

#### 4. Annotation and Organization of Tasks

- **Visual Markup**

  - User clicks on areas in photos for cleaning and maintenance

  - App visually marks up selected areas

- **Specific Information Input**

  - Appliances in each area

  - Surface types per room

  - Usage and lifestyle of spaces

  - Frequency of use

  - Importance and aesthetic issues

  - Dirtiness and effort required

- **Tools/Supplies Management**

  - Track tools and supplies on hand

  - Identify tools and supplies required

#### 5. Task Mapping and Visualization

- **House Map Visualization**

  - Map of house with work amount and task types visualized

  - Use markers, colors, graphs for progress tracking

- **Master Task List Generation**

  - Simplify tasks into manageable chunks

  - Organize tasks into “Do next” or “Do now” based on urgency and user availability

#### 6. Dynamic Task Management

- **Urgency Score Calculation**

  - Factors: User’s current location, supplies on hand, user’s focus, mental mood, physical energy, schedule and availability

- **Preparation for Visits**

  - Manage urgent tasks for upcoming events (e.g., pet messes, repairs)

#### 7. Task Sequencing and Scheduling

- **Task Sequencing**

  - Logically space out and sequence tasks

- **Guided Acquisition of Tools**

  - Guide user to acquire necessary tools if not available

#### 8. Guidance and Recommendations

- **General Advice and “How to”**

  - Provide guidance for common tasks

  - Link product recommendations with purchase options

- **Tailored Suggestions**

  - Offer unique suggestions based on user’s disabilities or difficulties

  - Link services for ease of use

- **Motivation and Encouragement**

  - Use original walkthrough photos for before and after comparisons

  - Offer encouragement and motivational “juice”

#### 9. Task Completion

- **Completion Validation**

  - User uploads “after” photo for task completion

  - Update statistics and graphs to show progress

#### 10. Automation

- **Automation Guidance**

  - Recommend products and services for task automation

  - Guide user to automate home maintenance tasks

### Example Table Definitions

```sql

-- Users table

CREATE TABLE Users (

	user_id INTEGER PRIMARY KEY AUTOINCREMENT,

	username TEXT UNIQUE,

	email TEXT UNIQUE,

	password_hash TEXT,

	profile_picture_url TEXT,

	created_at DATETIME,

	last_login DATETIME

);

-- Homes table

CREATE TABLE Homes (

	home_id INTEGER PRIMARY KEY AUTOINCREMENT,

	user_id INTEGER,

	home_address TEXT,

	home_size REAL,

	number_of_levels INTEGER,

	layout TEXT,

	FOREIGN KEY (user_id) REFERENCES Users(user_id)

);

-- Rooms table

CREATE TABLE Rooms (

	room_id INTEGER PRIMARY KEY AUTOINCREMENT,

	home_id INTEGER,

	room_name TEXT,

	room_size REAL,

	room_type TEXT,

	room_flooring_type TEXT,

	room_windows INTEGER,

	room_usage TEXT,

	room_frequency_of_use TEXT,

	room_importance TEXT,

	room_dirtiness_level TEXT,

	room_tools_supplies_on_hand TEXT,

	room_tools_supplies_required TEXT,

	FOREIGN KEY (home_id) REFERENCES Homes(home_id)

);

-- Photos table

CREATE TABLE Photos (

	photo_id INTEGER PRIMARY KEY AUTOINCREMENT,

	user_id INTEGER,

	room_id INTEGER,

	photo_url TEXT,

	photo_timestamp DATETIME,

	FOREIGN KEY (user_id) REFERENCES Users(user_id),

	FOREIGN KEY (room_id) REFERENCES Rooms(room_id)

);

-- Tasks table

CREATE TABLE Tasks (

	task_id INTEGER PRIMARY KEY AUTOINCREMENT,

	user_id INTEGER,

	room_id INTEGER,

	task_title TEXT,

	task_description TEXT,

	task_created_at DATETIME,

	task_due_time DATETIME,

	task_priority INTEGER,

	task_status TEXT,

	task_tags TEXT,

	task_scheduled_time DATETIME,

	task_type TEXT,

	FOREIGN KEY (user_id) REFERENCES Users(user_id),

	FOREIGN KEY (room_id) REFERENCES Rooms(room_id)

);

-- TaskProgress table

CREATE TABLE TaskProgress (

	progress_id INTEGER PRIMARY KEY AUTOINCREMENT,

	task_id INTEGER,

	progress_photo_url TEXT,

	progress_timestamp DATETIME,

	progress_description TEXT,

	completion_percentage REAL,

	FOREIGN KEY (task_id) REFERENCES Tasks(task_id)

);

-- SharedTasks table

CREATE TABLE SharedTasks (

	share_id INTEGER PRIMARY KEY AUTOINCREMENT,

	task_id INTEGER,

	shared_with TEXT,

	share_timestamp DATETIME,

	comments TEXT,

	likes INTEGER,

	feedback TEXT,

	FOREIGN KEY (task_id) REFERENCES Tasks(task_id)

);

-- Notifications table

CREATE TABLE Notifications (

	notification_id INTEGER PRIMARY KEY AUTOINCREMENT,

	user_id INTEGER,

	task_id INTEGER,

	notification_message TEXT,

	notification_status TEXT,

	reminder_time DATETIME,

	FOREIGN KEY (user_id) REFERENCES Users(user_id),

	FOREIGN KEY (task_id) REFERENCES Tasks(task_id)

);

```

This outline provides a structured plan for developing a comprehensive home management app, ensuring a user-friendly and engaging experience while keeping track of tasks and progress.


## users


<table>
  <tr>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
  </tr>
</table>



     Here is a list of possible tables that could be used in a database for a home cleaning todo app with scheduling, prioritizing tasks, relevant advice, product recommendations, and inventory tracking functionality:

1. **Users** table: This table will store information about the users who use the app. Some possible columns include `user_id`, `username`, `password_hash`, `email`, `energy_level`, and `location`.

2. **Tasks** table: This table will store information about each individual task that a user can add to their todo list. Some possible columns include `task_id`, `user_id` (foreign key), `title`, `description`, `scheduled_time`, `priority`, `completed`, and `product_recommendation_id`.

3. **Advice** table: This table will store relevant cleaning advice for each task that a user can view while creating or completing the task. Some possible columns include `advice_id` and `text`.

4. **Products** table: This table will store information about various cleaning products that the app can recommend to users based on their needs and wants. Some possible columns include `product_id`, `name`, `description`, `price`, `rating`, and `image_url`.

5. **Inventory** table: This table will track the user's inventory supply of tools and materials needed for cleaning tasks. Some possible columns include `inventory_id`, `user_id` (foreign key), `product_id` (foreign key), and `quantity`.

6. **User\_Preferences** table: This table will store information about the user's preferences, such as their preferred brands or cleaning methods, which can be used to personalize product recommendations. Some possible columns include `preference_id`, `user_id` (foreign key), and `text`.

7. **Task\_History** table: This table will store information about the user's completed tasks, which can be used for analytics purposes or to provide insights into the user's cleaning habits. Some possible columns include `history_id`, `task_id` (foreign key), `user_id` (foreign key), and `completed_time`.

8. **User\_Energy\_Level** table: This table will store information about the user's energy level at various times of the day, which can be used to prioritize tasks and suggest cleaning methods that are more or less energy-intensive. Some possible columns include `energy_level_id`, `user_id` (foreign key), `time_of_day`, and `energy_level`.

9. **Urgency\_Level** table: This table will store information about the urgency level of each task, which can be used to prioritize tasks based on their importance and time sensitivity. Some possible columns include `urgency_level_id`, `task_id` (foreign key), and `urgency_level`.

10. **Task\_Notes** table: This table will store any additional notes that the user may add to a task, such as specific instructions or reminders. Some possible columns include `note_id`, `task_id` (foreign key), and `text`.

This list of tables should provide a good starting point for designing a database schema for a home cleaning todo app with scheduling, prioritizing tasks, relevant advice, product recommendations, and inventory tracking functionality. However, the specific columns and relationships between tables may need to be adjusted based on the unique requirements and goals of the app.

-- Users table

CREATE TABLE Users (

	user_id INTEGER PRIMARY KEY AUTOINCREMENT,

	username TEXT NOT NULL,

	password_hash TEXT NOT NULL,

	email TEXT NOT NULL,

	energy_level INTEGER,

	location TEXT

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


### 
                **Basic User Information**



1. **user_id**: Unique identifier for the user.
2. **username**: User’s chosen name for login/display.
3. **password_hash**: Hashed password for security.
4. **email**: User’s email address.
5. **profile_picture_url**: URL to the user's profile picture.
6. **created_at**: Date and time when the user account was created.
7. **last_login**: Date and time of the user's last login.

### 
                **Personal Information**

1. **first_name**: User's first name.
2. **last_name**: User's last name.
3. **date_of_birth**: User's date of birth.
4. **gender**: User's gender.
5. **location**: User’s location (city, state, country).

### 
                **Contact Information**

1. **phone_number**: User’s phone number.
2. **address**: User's address (street, city, state, zip code, country).

### 
                **App Usage Information**

1. **login_history**: Timestamps of user logins.
2. **device_information**: Information about devices used to access the app (e.g., device type, OS).
3. **preferences**: User’s app preferences/settings (e.g., dark mode, notification settings).
4. **usage_statistics**: Data on how often and for how long the user uses the app.

### 
                **Task Management**

1. **task_id**: Unique identifier for each task.
2. **task_title**: Title of the task.
3. **task_description**: Description of the task.
4. **task_created_at**: Timestamp when the task was created.
5. **task_due_time**: Due date and time for the task.
6. **task_scheduled_time**: Scheduled start time for the task.
7. **task_priority**: Priority level of the task.
8. **task_status**: Status of the task (e.g., pending, completed, overdue).
9. **task_tags**: Tags/labels associated with the task.
10. **task_comments**: Comments added to the task.
11. **task_attachments**: URLs to files attached to the task.
12. **task_collaborators**: List of users collaborating on the task.
13. **task_recurring_pattern**: Recurrence pattern for repeating tasks.
14. **task_subtasks**: List of subtasks under the main task.
15. **task_notes**: Additional notes for the task.

### 
                **Notifications and Reminders**

1. **reminder_id**: Unique identifier for reminders.
2. **reminder_time**: Time when the reminder is set.
3. **notification_id**: Unique identifier for notifications.
4. **notification_message**: Message content of the notification.
5. **notification_status**: Status of the notification (e.g., read, unread).

### 
                **Product Recommendations and Inventory**

1. **product_recommendation_id**: Unique identifier for product recommendations.
2. **recommended_product_id**: Product ID of the recommended product.
3. **inventory_id**: Unique identifier for inventory items.
4. **product_id**: Product ID for items in inventory.
5. **product_name**: Name of the product.
6. **product_description**: Description of the product.
7. **product_quantity**: Quantity of the product in inventory.
8. **product_price**: Price of the product.
9. **product_rating**: User rating for the product.
10. **product_image_url**: URL to the product image.

### 
                **User Preferences and Customization**

1. **preference_id**: Unique identifier for user preferences.
2. **preference_name**: Name of the preference (e.g., preferred cleaning method).
3. **preference_value**: Value of the preference.
4. **custom_categories**: User-defined task categories.
5. **theme_settings**: User’s theme preferences (e.g., dark mode, light mode).
6. **notification_settings**: User’s notification preferences.

### 
                **Activity and History**

1. **activity_log_id**: Unique identifier for activity logs.
2. **activity_type**: Type of activity (e.g., task creation, task completion).
3. **activity_timestamp**: Timestamp of the activity.
4. **task_history_id**: Unique identifier for task history records.
5. **completed_task_id**: Task ID of completed tasks.
6. **completed_time**: Timestamp when the task was completed.

### 
                **Health and Wellness (for user’s energy levels)**

1. **energy_level_id**: Unique identifier for energy levels.
2. **energy_level**: User’s energy level at a given time.
3. **energy_level_timestamp**: Timestamp for the recorded energy level.
4. **time_of_day**: Specific time of day (morning, afternoon, evening) for energy level records.

### 
                **Social and Collaboration**

1. **collaborator_id**: Unique identifier for collaborators.
2. **collaborator_user_id**: User ID of the collaborator.
3. **collaboration_role**: Role of the collaborator in the task.

### 
                **Security and Authentication**

1. **password_reset_token**: Token for password reset functionality.
2. **two_factor_enabled**: Boolean indicating if two-factor authentication is enabled.
3. **two_factor_secret**: Secret key for two-factor authentication.
4. **login_attempts**: Number of failed login attempts.

### 
                **Additional Data**

1. **custom_fields**: Any additional custom fields defined by the user.
2. **external_integrations**: Information about external services integrated with the app (e.g., calendar, email).
3. **user_feedback**: Feedback provided by the user about the app.
4. **subscription_status**: User’s subscription status (e.g., free, premium).
5. **billing_information**: Information related to billing and payments.
6. **api_keys**: API keys for user’s external integrations.
7. **data_export_requests**: Records of data export requests made by the user.
8. **deactivation_requests**: Records of user account deactivation requests.

### 
                **General Home Information**

1. **home_id**: Unique identifier for the home.
2. **home_address**: Address of the home.
3. **home_type**: Type of home (e.g., apartment, house, condo).
4. **home_size**: Size of the home in square feet or square meters.
5. **number_of_rooms**: Total number of rooms in the home.
6. **number_of_bedrooms**: Number of bedrooms in the home.
7. **number_of_bathrooms**: Number of bathrooms in the home.
8. **home_age**: Age of the home.
9. **home_flooring_type**: Types of flooring in the home (e.g., carpet, hardwood, tile).
10. **home_layout**: General layout or floor plan of the home.

### 
                **Specific Room Information**

1. **room_id**: Unique identifier for each room.
2. **room_name**: Name or designation of the room (e.g., kitchen, living room).
3. **room_size**: Size of the room in square feet or square meters.
4. **room_flooring_type**: Type of flooring in the room.
5. **room_windows**: Number and type of windows in the room.
6. **room_purpose**: Purpose or usage of the room (e.g., bedroom, office).

### 
                **Home Features and Amenities**

1. **outdoor_space**: Information about outdoor spaces (e.g., yard, garden, balcony).
2. **garage**: Information about the garage (e.g., size, number of cars it can accommodate).
3. **home_appliances**: List of major appliances in the home (e.g., refrigerator, washing machine).
4. **heating_system**: Type of heating system in the home.
5. **cooling_system**: Type of cooling system in the home.
6. **home_security_system**: Information about any security systems in place.
7. **home_automation**: Information about any smart home or automation systems.

### 
                **Cleaning and Maintenance Information**

1. **cleaning_frequency**: How often the home or specific areas are cleaned.
2. **preferred_cleaning_products**: User’s preferred cleaning products and brands.
3. **allergies_or_sensitivities**: Any allergies or sensitivities to certain cleaning products or materials.
4. **pet_ownership**: Information about any pets in the home, including types and numbers.
5. **special_cleaning_needs**: Any special cleaning needs or preferences (e.g., hypoallergenic cleaning).

### 
                **Furniture and Decor**

1. **furniture_inventory**: List of major furniture items in the home.
2. **decor_style**: Preferred decor style (e.g., modern, traditional).
3. **valuable_items**: Information about any valuable or delicate items that require special care.

### 
                **Environmental and Energy Information**

1. **energy_efficiency**: Information about the home’s energy efficiency.
2. **solar_panels**: Information about any solar panels installed.
3. **water_usage**: Information about water usage and any water-saving features.
4. **home_insulation**: Information about home insulation quality.

### 
                **Home Improvement and Projects**

1. **current_projects**: List of ongoing home improvement projects.
2. **future_projects**: Planned or desired home improvement projects.
3. **project_budget**: Budget for home improvement projects.
4. **contractor_information**: Information about contractors used for home projects.

### 
                **Miscellaneous**

1. **home_ownership_status**: Whether the user owns or rents the home.
2. **home_insurance**: Information about home insurance policies.
3. **neighborhood_information**: Information about the neighborhood (e.g., safety, amenities).
4. **emergency_contacts**: Contacts for emergencies related to the home (e.g., plumber, electrician).

### 
                **General Photo Information**

1. **photo_id**: Unique identifier for each photo.
2. **photo_url**: URL to the photo stored in a file storage service.
3. **photo_timestamp**: Timestamp when the photo was taken.
4. **room_id**: Identifier for the room where the photo was taken.
5. **user_id**: Identifier for the user who took the photo.

### 
                **Image Processing Information**

1. **detected_items**: List of items detected in the photo.
2. **item_id**: Unique identifier for each detected item.
3. **item_name**: Name of the detected item (e.g., sofa, table).
4. **item_location**: Location of the item in the room (e.g., coordinates in the image).
5. **item_condition**: Condition of the item (e.g., clean, dirty).
6. **item_category**: Category of the item (e.g., furniture, appliance).

### 
                **Task Information**

1. **task_id**: Unique identifier for each task.
2. **task_title**: Title of the task.
3. **task_description**: Description of the task.
4. **task_created_at**: Timestamp when the task was created.
5. **task_due_time**: Due date and time for the task.
6. **task_priority**: Priority level of the task.
7. **task_status**: Status of the task (e.g., pending, completed, overdue).
8. **task_tags**: Tags/labels associated with the task.
9. **task_scheduled_time**: Scheduled start time for the task.
10. **task_type**: Type of task (e.g., cleaning, organizing).

### 
                **Progress Tracking**

1. **progress_id**: Unique identifier for each progress entry.
2. **task_id**: Identifier for the task being tracked.
3. **progress_photo_url**: URL to a photo showing progress on the task.
4. **progress_timestamp**: Timestamp when the progress photo was taken.
5. **progress_description**: Description of the progress made.
6. **completion_percentage**: Percentage of task completion.

### 
                **Sharing and Accountability**

1. **shared_with**: List of users with whom the task or progress is shared.
2. **share_timestamp**: Timestamp when the task or progress was shared.
3. **comments**: Comments from users about the shared task or progress.
4. **likes**: Number of likes or reactions from users on the shared task or progress.
5. **feedback**: Feedback from users about the task or progress.

### 
                **Notifications and Reminders**

1. **notification_id**: Unique identifier for notifications related to the task.
2. **reminder_id**: Unique identifier for reminders related to the task.
3. **notification_message**: Message content of the notification.
4. **reminder_time**: Time when the reminder is set.
5. **notification_status**: Status of the notification (e.g., read, unread).

### 
                **Potential User Workflow**

1. **Photo Upload**: User takes a photo of a room and uploads it to the app.
2. **Image Processing**: App processes the image to detect items and their conditions.
3. **Task Creation**: Based on detected items, the app creates relevant cleaning or organizing tasks.
4. **Progress Tracking**: User updates task progress by uploading new photos and descriptions.
5. **Sharing**: User shares progress with friends or family for accountability and motivation.
6. **Notifications**: App sends reminders and notifications about upcoming tasks and progress updates.


# Basic user experience outline



5. Register/create an account
    11. Login
    12. Logout
    13. Session cookies and user activity etc.
6. Onboarding
    14. Establish the user’s home environment
        15. House size
        16. Number of levels
        17. Layout



            15. 
Important rooms


                24. Bedrooms
                25. Bathrooms
                26. kitchen
                27. Others
                28. Etc.
    15. User’s abilities and disabilities are entered
        18. This will affect the evaluation of effort required and advice for tasks, as well as products/services suggested
    16. Initial Walkthrough
        19. Systematically go to every room in the house to note workload
        20. App guides and prompts and User takes wide photo of each area to annotate later
        21. Interior spaces documented
        22. Exterior spaces if applicable based on user’s initial setup
    17. Annotation and organization of tasks
        23. User clicks on each area in the photos to be cleaned and maintained and is visually marked up
        24. Information about specific spots is entered



            16. 
Appliances


            17. 
Surface types per room


            18. 
General usage and lifestyle of spaces


                29. Frequency of use
                30. Importance
                31. Aesthetical issues
                32. Dirtiness and effort required
                33. Tools/supplies on hand
                34. Tools/supplies required



            19. 
User needs to do 


        25. Map of house with visualizations of amount of work and type of tasks is populated



            20. 
Markers, colors, graphs and other ways to show progress at a glance


        26. A master task list is generated



            21. 
The tasks must be reasonably simplified such that each are not whole projects but easily completed in a short period of time.


            22. 
The list of tasks is organized as a “Do next” or “Do now” based on urgency score and user availability.


            23. 
The urgency score for each task is updated dynamically based on several factors


                35. Preparing for visits
                36. Messes by pets or kids
                37. Things need repair or replacement
                38. etc.



            24. 
The user’s current status is the main determinant of what the next task should be and when


                39. Where in the house is the user currently?
                40. Does the user have the supplies on hand for the task?
                    4. If not, acquiring the tools will be an attached guided task
                41. What is the user’s current focus?
                42. What is most important for the user currently?
                43. What is the user’s mental mood and physical energy currently?
                    5. Biometric data or user input
                44. User’s schedule and availability



            25. 
Tasks are reasonably spaced out and logically sequenced and intelligently scheduled


        27. Guidance



            26. 
General advice and “how to” is provided for common tasks


                45. Product recommendations are linked, $ purchases can be made



            27. 
Unique tailored suggestions are given for disabilities and difficulties


                46. Services can be linked or integrated into the app for ease of use and consolidation
                    6. $ subscriptions



            28. 
Encouragement and other “juice” to keep the user motivated


        28. Original walkthrough photo is the visual for the before image unless otherwise updated
7. Task completion
    18. As each task is completed the user is required to upload an “after” photo to officially mark them as completed
    19. Statistics and graphs are updated to show progress over time and other things the user might be interested in
8. Automation
    20. Combined with the products and services suggestions the user is guided to practical ways to automate tasks and make home maintenance easier until all tasks are fully automated and accounted for