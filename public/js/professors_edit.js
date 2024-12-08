const editItems = document.getElementById('prof-edit-table');
let courses = [];

let original_data = [];

fetch('http://127.0.0.1:8000/courses')
    .then(response => response.json())
    .then(data => {
        courses = Object.keys(data);
    })

fetch('http://127.0.0.1:8000/professors')
    .then(response => response.json())
    .then(data => {
        original_data = data;
        for(let prof of Object.keys(data)){
            const list_item = document.createElement('div');
            list_item.className = 'edit-list-item';

            const title = document.createElement('div');
            title.innerText = `${prof}`;
            title.className = 'list-item-title';
            list_item.appendChild(title);

            const courses_scrollable = document.createElement('div');
            courses_scrollable.className = 'scrollable-element';

            for(let course of courses){
                let course_item = document.createElement('div')

                let course_item_input = document.createElement('input');
                course_item_input.type = 'checkbox';
                course_item.value = `${course}`;

                const label = document.createElement('label');
                label.textContent = course;

                courses_scrollable.appendChild(course_item);

                if(data[prof]['qualified_courses'].includes(course)){
                    course_item_input.checked = true;
                }

                course_item.appendChild(course_item_input);
                course_item.appendChild(label);
            }

            let max_input_div = document.createElement('div')
            max_input_div.className = 'max-courses';

            const max_label = document.createElement('label');
            max_label.textContent = 'Max Courses:';

            let max_input = document.createElement('input');
            max_input.value = `${data[prof]['max_classes']}`;
            max_input.className = 'max-course-input';
            max_input.type = 'number';

            max_input_div.appendChild(max_label);
            max_input_div.appendChild(max_input);

            let delete_div = document.createElement('div');
            delete_div.className = 'delete-div';

            let delete_button = document.createElement('button');
            let reset_button = document.createElement('button');
            delete_button.innerText = 'Delete';
            reset_button.innerText = 'Reset';

            delete_div.appendChild(delete_button);
            delete_div.appendChild(reset_button);
            reset_button.className = 'reset-button';

            reset_button.addEventListener('click', () => {
                const profData = original_data[prof];
                max_input.value = profData['max_classes'];
                const originalQualifiedCourses = profData['qualified_courses'];
                const checkboxInputs = courses_scrollable.querySelectorAll('input[type="checkbox"]');
                checkboxInputs.forEach(checkbox => {
                    const label = checkbox.nextSibling;
                    const courseName = label.textContent;
                    checkbox.checked = originalQualifiedCourses.includes(courseName);
                });
            });

            delete_button.addEventListener('click', () => {
                const confirmation = confirm(`Are you sure you want to delete data for ${prof}?`);
                if (confirmation) {
                    // Remove the professor's div from the DOM
                    // list_item.remove();

                    console.log('Working!');
                }
            });

            list_item.appendChild(courses_scrollable);
            list_item.appendChild(max_input_div);
            list_item.appendChild(delete_div);
            editItems.appendChild(list_item);
        }
    })

const buttons_div = document.getElementById('return-to-update-by-list');
let back_button = document.createElement('button');
let submit_button = document.createElement('button');

back_button.innerText = 'Return';
submit_button.innerText = 'Submit';

back_button.addEventListener('click', () => {
    window.location.href = `edit_fields.html`;
});

submit_button.addEventListener('click', () => {
    if(validate()){
        console.log('WAHOO!');
    }
});

function validate() {
    return true;
}

buttons_div.className = 'list-edit-bottom';

buttons_div.appendChild(back_button);
buttons_div.appendChild(submit_button);