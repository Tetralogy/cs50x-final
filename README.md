# cs50x-final
Final project for CS50
#[x]: #clean up project files
[x] templates
[x] python
[x]: clean up comments
[x] delete media
[x] ideas folder files
[ ] merge to main

#[X]: WRITE THE PROJECT DOCUMENTATION
#BUG: make the video demo

#BUG: clean up this readme to spec of final assignment
#hack: make git repo public
#hack: submit to github and cs50



    your project’s title;
    your name;
    URL of your video
    and a description of your project.
    your GitHub and edX usernames;
    your city and country;
    and, the date you have recorded this video.


#XXX-------------------------delete above-------------------------XXX#

# House Cleaning Todo App: Final Project for CS50X
by Kyle Mausser
#### Video Demo:  <URL HERE>

#### Description:

This project is a web-based todo application designed to help users manage cleaning tasks in their home. The idea stems from the concept that visually associating tasks with their physical locations can improve motivation and task completion. By combining interactive drag-and-drop functionality, a visual corkboard-style interface, and traditional task management features, this app provides a unique and engaging user experience.

The app was developed as the final project for CS50X, incorporating a variety of technologies to deliver a robust, user-friendly application. Below is a detailed description of the app’s features, development process, and the technologies used.

## Features and Functionality

### User Onboarding

Upon registration and login, users are guided through a simple onboarding process. The journey begins with creating a home profile by naming it and specifying whether it has multiple levels. If multiple levels are indicated, users proceed to floor management, where they can add, rename, and rearrange floors using drag-and-drop functionality. The app allows users to designate a “ground floor” and a “main floor” for better organizational clarity.

Next, users assign predefined room types (such as kitchen, bedroom, or bathroom) to specific floors, visually creating their home layout. This process also employs drag-and-drop functionality for intuitive management, ensuring a seamless experience.

### Map View

Once all floors have at least one room assigned, users gain access to the "Map" view. This central interface displays all floors, each represented by a grid of its rooms. Below the floor grids is a master list of all tasks for the home. Users can drag and drop tasks between rooms and floors, reorder them, or assign tasks as subtasks under other tasks. Additionally, rooms can be rearranged within their respective floors, maintaining a consistent and logical organizational structure.

### Room Walkthrough

Selecting a room from the Map view initiates the "walkthrough" process. In this mode, users can take or upload a picture of the room, which becomes the room’s cover image. Tasks can then be pinned to specific locations on the cover photo, simulating a corkboard-style interaction. This allows users to see tasks in context, directly associated with their physical locations in the room.

Beyond pinning tasks, users can add, reorder, or group them into subtasks. Subtasks can be nested indefinitely, providing flexibility in organizing complex cleaning projects. Tasks can also be marked as complete to track progress effectively.

### Drag-and-Drop Interaction

A key feature of the app is its drag-and-drop functionality, which enhances interactivity and ease of use. Sortable.js powers these interactions, ensuring smooth and responsive experiences across devices, including touchscreens. To maintain a streamlined codebase, the app integrates Sortable.js with HTMX, enabling seamless backend updates without heavy reliance on JavaScript frameworks.

## Development Process

### Backend Technologies

The backend is built with Python and Flask, utilizing SQLAlchemy as the ORM and SQLite for data storage. Flask provides the core framework for routing, session management, and API endpoints. SQLAlchemy handles database interactions, offering a clean and modular approach to managing the app’s data models. SQLite serves as a lightweight and efficient database solution, ideal for a project of this scale.

Key backend functionality includes user authentication, session management, and CRUD operations for floors, rooms, tasks, and subtasks. Dynamic data updates are triggered by HTMX requests, ensuring a responsive and interactive user experience.

### Frontend Technologies

The frontend combines simplicity with interactivity. HTML provides the structural foundation, while Bootstrap ensures a responsive and visually appealing design. Custom CSS enhances the app’s visual identity, addressing specific design requirements. HTMX powers dynamic interactions, reducing the need for extensive JavaScript. Sortable.js enables intuitive drag-and-drop functionality, making task and room management straightforward and efficient.

### Challenges and Solutions

**Dynamic Drag-and-Drop**: Implementing drag-and-drop functionality required seamless integration with backend data updates. This challenge was addressed by leveraging Sortable.js and HTMX to trigger AJAX requests, updating the database in real time.

**Visual Task Pinning**: Associating tasks with specific points on an image posed a challenge, particularly in maintaining a responsive layout. The solution involved mapping tasks to coordinates on the room’s cover photo, with CSS ensuring the layout adapts dynamically to the image’s aspect ratio.

**Multi-Level Organization**: Allowing flexible management of floors, rooms, and tasks while maintaining a logical hierarchy was another challenge. A combination of relational database design and intuitive UI features like drag-and-drop and visual grids provided an effective solution.

## Future Improvements

While the app is functional, there are several areas for future development:

1. **Enhanced Visualization**: Developing a top-down floor plan view for more intuitive navigation and adding custom icons or illustrations for rooms.

2. **Additional Task Features**: Adding due dates, reminders, and recurring tasks, as well as enabling file uploads (e.g., cleaning checklists) attached to specific tasks.

3. **Improved User Experience**: Introducing collaborative features for multiple users in the same household and optimizing performance for larger data sets.

4. **Mobile Optimization**: Further refining touch interactions for mobile devices to enhance usability.

## Reflections

This project was an intensive learning experience that spanned multiple aspects of web development. From designing relational databases to integrating advanced frontend interactions, it provided valuable insights into creating a cohesive and functional application.

HTMX proved to be a powerful tool for simplifying the development of dynamic, interactive features without the overhead of a full-fledged JavaScript framework. Similarly, Sortable.js offered an efficient way to implement drag-and-drop functionality while maintaining responsiveness across devices.

By focusing on user experience and prioritizing visual task management, this app provides a practical and motivating tool for organizing cleaning tasks. It’s a project I’m proud to have completed and a foundation I hope to build upon in the future.

