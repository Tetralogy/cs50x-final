# Basic User flow for MVP of CS50x final project: Untitled House Cleaning Task Tracker App

1. ## User makes an account username and password ✅
    1. ### /register ✅
        1. [Sign-up form](application/templates/auth/register.html) ✅
            1. UserName ✅
            2. Password ✅
    2. ### /login ✅
        1. [login form](application/templates/auth/login.html) ✅
            1. UserName ✅
            2. Password ✅
2. ## User creates a home profile to describe their environment to track ✴
    1. ### /home/new ✅
        1. [New home form](application/templates/homes/create_home.html.jinja)  ✅
            1. Home name: name ✅
            2. Type of home: select [apartment, condominium, house, trailer, van, tent, cardboard box, other()] ✅
                1. in future references during home setup, the chosen specific home type word is used as the nound instead of "home" ✴️ (house, apartment, condo) 
    2. ### /home/setup ✴️ 
        1. #TODO floor selection form ✴️ ⬅️ 
        2. new floor button (stacked reorderable list)✴️
            1. #fixme Automatically prompts for rename field of new levels 
            2. "Main Floor" is the default name for the first floor ✅
            3. drag and drop floor names above and below eachother to establish number and order of house levels ✅
            4. #fixme drag and drop a floor name outside of house outline area to delete a level
            5. set ground floor and move to next step ✅
        3. home size form ✅
            1. select approx home size ✅
        4. add rooms form
            1. list of room types as blocks with appropriate icons
                1. Default room types (default.json [list of room types])
                2. optional custom user created types
            2. edit floor layout form, tab denoting what floor is selected and currently editing
                1. can select other floor to edit with tabs to switch to editing that floor
                2. drop zone for new rooms
                    1. Drag and drop a room type block into the area
                        1. place the room block in the square approximately where it might physically be in real life
                        2. Automatically +incriments the room type as a placeholder name (bedroom 1, bedroom 2, bedroom 3...)
                        3. can activate the rename field on the room block by tapping/clicking the block once
                        4. click and hold/move to drag and rearrange block
                        5. Drag block out of area to delete a room
            3. "confirm room layout/order for current floor" button
                1. automatically opens the tab for the next floor that has no rooms confirmed
                2. if a floor is not confirmed, it remains in the list of floors to edit
                3. when the final floor is confirmed, go to the house map page
3. ## User performs innitial task collection walkthrough process
    1. ### /home/map/walkthrough/setup
        1. list of rooms on the ground floor are presented on a layout map visually similar to the add rooms form
            1. room blocks are not movable or directly editable in task map view
            2. user is prompted to select the floor and room they are currently in
            3. user is given a choice to select in order which rooms to include in a full walkthrough
                1. user taps each room to select the order
                    1. selected room gets block color change effect
                    2. number of the order selected is applied to the block as a badge
                2. selected blocks can be unselected by clicking again
            4. they can choose not to select the room order themselves
                1. order is then determined by the layout order of the blocks
            5. once all rooms in the level are selected, the user is prompted to go to the next floor
                1. the user can choose to omit rooms if they navigate to another floor after making their selections for the current floor and confirming their selections when prompted
            6. User confirms walkthrough order
    2. ### /walkthrough 
        1. User goes room by room photographing each room and each area containing tasks
            1. User is instructed to walk into the first room in the queue
            2. go to center of room
            3. take photo of room
            4. upload via page form or save to upload later
        2. Quick task notes form
            1. any immediate thoughts and tasks are noted to be organized later
                1. enter text in a text field
                2. any punctuation triggers new task save
                3. line breaks trigger new task save
                4. submit button saves batch of tasks and clears form for the next task entry
                5. enter/return key press saves and clears form for the next task entry
        3. room notes exited, next room in queue is triggered
            1. User is instructed to walk to the next room
            2. repeat until all rooms in the queue on floor have notes
            3. User is instructed to walk to the next floor level and room in the queue
            4. repeat until all rooms in the queue on floor have notes
        4. close and mark initial walkthrough as completed by entering the timestamp in database
    3. ### /walkthrough/edit/photos
        1. #### form to organize photos and associate them with room blocks
            1. unorganized photos shown in an album gallery above the home map
            2. drag and drop unorganized imported photos from the unorganized gallery section to the room block they belong to
            3. added photos appear as a collage inside the corresponding room block
            4. each room that a photo is added to is added to the list of photos for the annotations step
        2. #### once the user is done adding photos to rooms they can click on individual rooms to further clasify their photos
            1. individual room photo designation form
                1. main photo establishment form
                    1. select the photo that is the panoramic representation of the room, that will be the room block's new icon cover
                    2. user confirms and the panoramic photo becomes the canvas background
                2. zone creation and detail entry form
                    1. the remaining photos are shown in a pile to the side, along with a blank zone block for zones the user want's to note but didn't get photos for
                    2. The detail photos or blank zone are able to be dragged and dropped to their corresponding locations within the main panorama photo canvas
                        1. upon dropping a photo in place a zone outline appears with the photo masked inside the shape
                        2. user is prompted to enter a name for the zone
                        3. enter key press or confirm button to finalize zone placement
                    3. choose to add tasks from unorganized room list or create new tasks for the zone
                        1. "Create new task" button
                        2. drag and drop move task line blocks from that room's list to the currently editing zone's list
                    4. at any time the user can click to edit a task's details with an edit task form popup
                        1. edit task details
                            1. text input: task_title
                            2. auto-applied based on room and zone attached:
                                1. user_id
                                2. task_created_at time
                                3. task_updated_at time
                                4. room_id
                                5. zone_id
                                6. completed_at time
                            3. select: task_status:
                                1. incomplete
                                2. in progress
                                3. awaiting supplies
                                4. complete
                            4. select: current condition of attached space
                                1. Excellent: The room is in pristine condition, with no visible signs of wear or damage.
                                2. Good: The room is well-maintained, with minor signs of wear or damage that do not significantly impact its functionality or appearance.
                                3. Fair: The room shows noticeable signs of wear or damage, but it is still functional and safe.
                                4. Poor: The room is in a state of disrepair, with significant signs of wear or damage that impact its functionality or safety.
                                5. Needs Attention: The room requires immediate attention to address specific issues, such as repairs or maintenance.
                                6. Needs Renovation: The room requires significant renovation or remodeling to bring it up to a satisfactory condition.
                                7. Needs Replacement: The room is beyond repair and needs to be replaced entirely.
                            5. optional
                                1. calendar select: task_due_date
                                2. text input: task instructions
                                    1. basic description by the user
                                    2. checklist can be created by user
                                3. text input: task supplies required
                                4. select: user estimated: task_scheduled_time
                        2. Confirm save and close back to zone edit
                    5. user confirm saves and closes zone back to the room edit
                3. when there are active tasks in the room there are task count badges at the corresponding location in the room pano pic indicating the ammount of work to do in that area
                    1. badge showing number of tasks to do in each zone
                    2. color tinting of zones to indicate dirtiness based on the ammount of work
                    3. room's master task list shown beside the room pano map organized by zone and unzoned
            2. user can confirm save edits to room and close back to home map of current floor level
                1. user continues editing rooms until all tasks are added
        3. "end home setup" button confirm saves and takes the user to their main home dashboard page
    4. ### /home 
        1. shows the user's house task status condition in easy to read and understandable widgets
            1. Map
                1. shows color coded hotspots of things that need attention
            2. tasks
                1. master task list ordered by the next thing the user should be doing
    5. ### /map 
        1. shows floor level view of all rooms and color coding of task distribution
    6. ### /tasks 
        1. shows main task list and other items that are relevant to task checking and organization