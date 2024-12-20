This is a list of possible options when loading in lists:

hx-get="/show_list/"

for task lists:

"parent": "{{ current\_user.active\_home }}",

infinite nesting: "sublevel_limit": 100,

no nesting*: "sublevel_limit": 0,

"list\_type": "Task",

"view\_override": "text-hierarchy"

"root\_parent": "{{ current\_user.active\_home }}",&#x20;

quicknote:

hx-vals='{"list\_type": "Task", "view\_override":"quicknote", "sublevel\_limit": 3, "force\_new\_list": "true"}'

List of all homes for the user:

            hx-vals='{"list_model": "Home", 

"sublevel\_limit": 1, "view\_override": "text-hierarchy"}'

---

            class="row g-0 row-cols-4 container-fluid bg-dark border border-success border-5 rounded-bottom-4 p-1"

            id="task-list-loader"

            hx-get="/show_list/"

            hx-vals='{"parent": "{{ current_user.active_home }}", "sublevel_limit": 100, }' #todo extract and make simple list of possible actions

            hx-trigger="load once"

            hx-swap="outerHTML"

            hx-indicator="#updating-indicator"

        >

            <input id="dummy-placeholder" type="hidden" name="items" />

</div>

<h1>This is a view of all tasks for the cureent home:</h1>

<div

            class="row g-0 row-cols-4 container-fluid bg-dark border border-success border-5 rounded-bottom-4 p-1"

            id="task-list-loader"

            hx-get="/show_list/"

            hx-vals='{"list_model": "Task", "parent": "{{ current_user.active_home }}", "sublevel_limit": 100}'

            hx-trigger="load once"

            hx-swap="outerHTML"

            hx-indicator="#updating-indicator"

        >

            <input id="dummy-placeholder" type="hidden" name="items" />

</div>

<h1>List of all homes for the user:</h1>

<div

            class="row g-0 row-cols-4 container-fluid bg-dark border border-success border-5 rounded-bottom-4 p-1"

            id="task-list-loader"

            hx-get="/show_list/"

            hx-vals='{"list_model": "Home", "parent": "{{ current_user.active_home }}", "sublevel_limit": 100}'

            hx-trigger="load once"

            hx-swap="outerHTML"

            hx-indicator="#updating-indicator"

        >

            <input id="dummy-placeholder" type="hidden" name="items" />

</div>

individual rooom task list:

list to show is chosen by current\_room id

        </div>