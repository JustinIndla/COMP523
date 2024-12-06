const items = JSON.parse(localStorage.getItem('selectedItems') || '[]');

console.log(items);

const editList = document.getElementById('list-edit-table');
items.forEach(item => {
    const listItem = document.createElement('div');
    listItem.className = 'edit-list-item';

    const title = document.createElement('div');
    title.innerText = `${item['Course']} Sec. ${item['Section']}`;
    title.className = 'list-item-title';
    listItem.appendChild(title);

    const keys = ['Room', 'Seat Capacity', 'Meeting Pattern', 'Start', 'Prof', 'Title', 'Section', 'Course'];
    const paramDiv = document.createElement('div');
    const params = document.createElement('table');
    params.className = 'params-table';

    paramDiv.appendChild(params);
    paramDiv.className = 'edit-table'

    let idx = 0;
    keys.forEach(key => {
        var row = params.insertRow(idx);
        var cell0 = row.insertCell(0);
        var cell1 = row.insertCell(1);

        cell0.innerText = key + ':'

        var input = null;
        if(key === 'Room'){
            input = document.createElement('select');
            let rooms = Object.keys({
                    'SN-0014': {'capacity': 128},
                    'FB-F009': {'capacity': 86},
                    'SN-0011': {'capacity': 66},
                    'FB-F007': {'capacity': 50},
                    'FB-F141': {'capacity': 50},
                    'SN-0115': {'capacity': 25},
                    'FB-F008': {'capacity': 20},
                    'SN-0252': {'capacity': 20},
                    'SN-0006': {'capacity': 15},
                    'SN-0325': {'capacity': 15},
                    'SN-0155': {'capacity': 14},
                    'FB-F120': {'capacity': 12},
                    'SN-0277': {'capacity': 10},
                    'FB-F331': {'capacity': 16},
                    'university': {'capacity': 300}
                });
            rooms.forEach(room => {
                let opt = document.createElement('option');
                opt.textContent = room;
                input.appendChild(opt);
            });
        } else if(key === 'Meeting Pattern') {
            input = document.createElement('select');
            let patterns = ['MWF', 'TTH', 'MW'];
            patterns.forEach(pattern => {
                let opt = document.createElement('option');
                opt.textContent = pattern;
                input.appendChild(opt);
            });
        } else if(key === 'Prof') {
            input = document.createElement('select');
            let profs = [
                "Montek Singh",
                "Tessa Joseph-Nicholas",
                "Ketan Mayer-Patel",
                "Prairie Goodwin",
                "Sayeed Ghani",
                "P.S. Thiagarajan",
                "Jasleen Kaur",
                "Saba Eskandarian",
                "Ron Alterovitz",
                "Cynthia Sturton",
                "Marc Niethammer",
                "Izzi Hinks",
                "Samarjit Chakraborty",
                "Donald Porter",
                "Alyssa Byrnes",
                "Gedas Bertasius",
                "Roni Sengupta",
                "Kevin Sun",
                "Cece McMahon",
                "Shahriar Nirjon",
                "Jack Snoeyink",
                "Brent Munsell",
                "James Anderson",
                "Danielle Szafir",
                "Daniel Szafir",
                "Parasara Sridhar Duggirala",
                "Praneeth Chakravarthula",
                "Ben Berg",
                "Shashank Srivastava",
                "Snigdha Chaturvedi",
                "Huaxiu Yao",
                "Andrew Kwong",
                "Mike Reed",
                "Paul Stotts",
                "Prasun Dewan",
                "Jorge Silva",
                "Kris Jordan",
                "Junier Oliva",
                "TBD"
            ];
            profs.forEach(prof => {
                let opt = document.createElement('option');
                opt.textContent = prof;
                input.appendChild(opt);
            });
        } else if(key === 'Section' || key === 'Seat Capacity'){
            input = document.createElement('input');
            input.type = 'number';
        } else {
            input = document.createElement('input');
        }
        input.value = item[key]
        cell1.append(input);
    });
    listItem.appendChild(paramDiv);
    editList.appendChild(listItem);
});

const buttons_div = document.getElementById('return-to-update-by-list');
let back_button = document.createElement('button');
let submit_button = document.createElement('button');

back_button.innerText = 'Return';
submit_button.innerText = 'Submit';

back_button.addEventListener('click', () => {
    window.location.href = `list_update.html`;
});

submit_button.addEventListener('click', () => {
    if(validate()){
        console.log('WAHOO!');
    }
});

function validate() {
    const updatedItems = [];
    const listItems = document.querySelectorAll('.edit-list-item');

    listItems.forEach(listItem => {
        let itemData = {};
        const table = listItem.querySelector('.params-table');
        const rows = table.querySelectorAll('tr');

        rows.forEach(row => {
            const keyCell = row.cells[0];
            const valueCell = row.cells[1];
            const key = keyCell.innerText.replace(':', '').trim();
            const inputElement = valueCell.querySelector('input, select');
            itemData[key] = inputElement.value;
        });
        updatedItems.push(itemData);
    });
    console.log(updatedItems);

    for(let item of updatedItems){
        let valid_patterns = null;
        if(item['Meeting Pattern'] === 'MWF'){
            valid_patterns = ['8:00AM', '9:05AM', '10:10AM', '11:15AM', '12:20PM', '1:25PM', '2:30PM', '3:35PM'];
        } else if(item['Meeting Pattern'] === 'TTH'){
            valid_patterns = ['8:00AM', '9:30AM', '11:00AM', '12:30PM', '2:00PM', '3:30PM', '5:00PM'];
        } else {
            valid_patterns = ['8:00AM', '9:05AM', '10:10AM', '11:15AM', '12:20PM', '1:25PM', '2:30PM', '3:35PM'];
        }
        if(!valid_patterns.includes(item['Start'])){
            alert(`Invalid start time for ${item['Course']} Sec. ${item['Section']}`);
            return false;
        } else if(item['Section'] < 1) {
            return false;
        }
    }
    return true;
}

buttons_div.className = 'list-edit-bottom';

buttons_div.appendChild(back_button);
buttons_div.appendChild(submit_button);