import shutil
from fastapi import HTTPException
import pulp
import json

def load_days():
    return ['Monday', 'Tuesday', 'Wednesday']

def load_periods():
    mwf_periods = {
        1: {'start_time': '8:00AM', 'duration': 50},
        2: {'start_time': '9:05AM', 'duration': 50},
        3: {'start_time': '10:10AM', 'duration': 50},
        4: {'start_time': '11:15AM', 'duration': 50},
        5: {'start_time': '12:20PM', 'duration': 50},
        6: {'start_time': '1:25PM', 'duration': 50},
        7: {'start_time': '2:30PM', 'duration': 50},
        8: {'start_time': '3:35PM', 'duration': 50},
}

# TTH periods (75 minutes each)
    tth_periods = {
        1: {'start_time': '8:00AM', 'duration': 75},
        2: {'start_time': '9:30AM', 'duration': 75},
        3: {'start_time': '11:00AM', 'duration': 75},
        4: {'start_time': '12:30PM', 'duration': 75},
        5: {'start_time': '2:00PM', 'duration': 75},
        6: {'start_time': '3:30PM', 'duration': 75},
        7: {'start_time': '5:00PM', 'duration': 75}
    }

# MW periods (75 minutes each)
    mw_periods = {
    1: {'start_time': '8:00AM', 'duration': 75},
    3: {'start_time': '10:10AM', 'duration': 75},
    5: {'start_time': '12:20PM', 'duration': 75},
    7: {'start_time': '2:30PM', 'duration': 75},
}
    return mwf_periods, tth_periods, mw_periods


def load_meeting_patterns(mwf_periods, tth_periods, mw_periods):
    meeting_patterns = {
    'MWF': {'days': ['Monday', 'Wednesday', "Friday"], 'periods': mwf_periods},
    'TTH': {'days': ['Tuesday', 'Thursday'], 'periods': tth_periods},
    'MW': {'days': ['Monday', "Wednesday"], 'periods': mw_periods},
    #'WF': {'days': ['Wednesday', 'Friday'], 'periods': wf_periods}
}
    return meeting_patterns

def backup_data():
    FILE_PATH = "professors.json"
    BACKUP_PATH = "professors_backup.json"
    try:
        shutil.copy(FILE_PATH, BACKUP_PATH)
    except FileNotFoundError:
        with open(BACKUP_PATH, "w") as backup_file:
            json.dump({}, backup_file, indent=4)

def restore_backup():
    FILE_PATH = "professors.json"
    BACKUP_PATH = "professors_backup.json"
    try:
        shutil.copy(BACKUP_PATH, FILE_PATH)
        print("Rollback successful. Changes have been undone.")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Backup file not found. Cannot restore.")

def get_professordata():
    file_path = "professors.json"

    with open(file_path) as file:
        data = json.load(file)
    return data

def add_professor(name, qualified_courses, availability, max_classes):
    backup_data()
    file_path = "professors.json"

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if name in data:
        print(f"Professor {name} already exists in the dataset.")
        return data
    data[name] = {
        "qualified_courses": qualified_courses,
        "availability": availability,
        "max_classes": max_classes
    }
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return data

def update_professor(name, qualified_courses = None, availability = None, max_classes = None):
    backup_data()
    file_path = "professors.json"
    try: 
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No data file found. Cannot update.")
    if name not in data:
        raise HTTPException(status_code=404, detail=f"Professor {name} not found.")
    professor = data[name]
    if qualified_courses is not None:
        professor["qualified_courses"] = qualified_courses
    if availability is not None:
        professor["availability"] = availability
    if max_classes is not None:
        professor["max_classes"] = max_classes
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return data

def delete_professor(name):
    backup_data()
    file_path = "professors.json"
    try: 
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No data file found. Cannot delete.")
    if name not in data:
        raise HTTPException(status_code=404, detail=f"Professor {name} not found.")  
    del data[name]
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)    
    return data 

def backup_courses():
    FILE_PATH = "course.json"
    BACKUP_PATH = "courses_backup.json"
    try:
        shutil.copy(FILE_PATH, BACKUP_PATH)
    except FileNotFoundError:
        with open(BACKUP_PATH, "w") as backup_file:
            json.dump({}, backup_file, indent=4)

def restore_courses():
    FILE_PATH = "courses.json"
    BACKUP_PATH = "courses_backup.json"
    try:
        shutil.copy(BACKUP_PATH, FILE_PATH)
        print("Rollback successful. Changes have been undone.")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Backup file not found. Cannot restore.")

def get_coursedata():
    file_path = "courses.json"
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)    
    except FileNotFoundError: 
        raise HTTPException(status_code=404, detail = "No data file found.") 
    return data

def add_courses(title, sections):
    #backup_courses()
    file_path = "courses.json"
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if title in data:
        print(f"Course {title} already exists in the dataset.")
        return data
    data[title] = {
        "sections": sections
    }
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return data

def update_course(title, sections):
    #backup_courses()
    file_path = "courses.json"
    try: 
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No data file found. Cannot update.")
    if title not in data:
        raise HTTPException(status_code=404, detail=f"Professor {title} not found.")
    course = data[title]
    if sections is not None:
        course["sections"] = sections

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return data

def delete_course(title):
    #backup_courses()
    file_path = "courses.json"
    try: 
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No data file found. Cannot delete.")
    if title not in data:
        raise HTTPException(status_code=404, detail=f"Course {title} not found.")  
    del data[title]
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)    
    return data 

def get_roomdata():
    file_path = "rooms.json"
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)    
    except FileNotFoundError: 
        raise HTTPException(status_code=404, detail = "No data file found.") 
    return data

def add_room(name, capacity):
    file_path = "rooms.json"
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if name in data:
        print(f"Room {name} already exists in the dataset.")
        return data
    data[name] = {
        "capacity": capacity
    }
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return data    

def update_room(name, capacity):
    file_path = "rooms.json"
    try: 
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No data file found. Cannot update.")
    if name not in data:
        raise HTTPException(status_code=404, detail=f"Professor {name} not found.")
    room = data[name]
    room["capacity"] = capacity
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return data

def delete_room(name):
    #backup_courses()
    file_path = "rooms.json"
    try: 
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No data file found. Cannot delete.")
    if name not in data:
        raise HTTPException(status_code=404, detail=f"Course {name} not found.")  
    del data[name]
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)    
    return data 

def backup_rooms():
    FILE_PATH = "rooms.json"
    BACKUP_PATH = "rooms_backup.json"
    try:
        shutil.copy(FILE_PATH, BACKUP_PATH)
    except FileNotFoundError:
        with open(BACKUP_PATH, "w") as backup_file:
            json.dump({}, backup_file, indent=4)

def restore_rooms():
    FILE_PATH = "rooms.json"
    BACKUP_PATH = "rooms_backup.json"
    try:
        shutil.copy(BACKUP_PATH, FILE_PATH)
        print("Rollback successful. Changes have been undone.")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Backup file not found. Cannot restore.")

def get_manually_scheduled_data():
    file_path = "manually_scheduled_courses.json"
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)    
    except FileNotFoundError: 
        raise HTTPException(status_code=404, detail = "No data file found.") 
    return data

def is_prof_available_for_time_slot(p, mp, period):
    return (mp, period) in professors[p]['availability']

def is_prof_available_and_qualified(p, c, ts):
    professors = get_professordata()
    return int(ts in professors[p]['availability'] and c in professors[p]['qualified_courses'])

def run_scheduling_algorithm (
    days,
    meeting_patterns,
    professors,
    courses,
    rooms,
    manually_scheduled_classes,
    small_class_threshold=100,
    rush_hour_penalty=0,
    possible_meeting_patterns=['MWF', 'TTH', 'MW']
):
    for p in professors:
    # Convert the availability list of lists
        flattened_availability = []
        for sublist in professors[p]['availability']:
            for slot in sublist:
                # Each slot is something like ["MWF", 1]
                # Convert it to a tuple ("MWF", 1)
                flattened_availability.append(tuple(slot))
    # Replace the original availability with the converted list of tuples
        professors[p]['availability'] = flattened_availability
    # -----------------------------
    # Initialize Variables
    # -----------------------------
    if manually_scheduled_classes is None:
        manually_scheduled_classes = []

    # Create the LP problem (Maximize the number of classes scheduled)
    prob = pulp.LpProblem("Course_Scheduling_Problem", pulp.LpMaximize)

    # Create time slots specific to each meeting pattern
    time_slots_mp = {}
    for mp in meeting_patterns:
        mp_time_slots = []
        for period in meeting_patterns[mp]['periods'].keys():
            mp_time_slots.append((mp, period))
        time_slots_mp[mp] = mp_time_slots

    # Identify small and large classes based on seat capacity
    small_classes = []
    large_classes = []
    for c in courses:
        for section in courses[c]['sections']:
            s = section['section_number']
            seat_capacity = section['seat_capacity']
            if seat_capacity is not None:
                if seat_capacity >= small_class_threshold:
                    large_classes.append((c, s))
                else:
                    small_classes.append((c, s))

    # Generate all valid combinations of indices for x
    x_indices = []
    
    for c in courses:
        for section in courses[c]['sections']:
            s = section['section_number']
            seat_capacity = section['seat_capacity']
            for mp in possible_meeting_patterns:
                for period in meeting_patterns[mp]['periods'].keys():
                    ts = (mp, period)
                    for r in rooms.keys():
                        # Enforce large classes to use 'university' room only
                        if (c, s) in large_classes and r != 'university':
                            continue  # Skip this combination
                        # Enforce small classes not to use 'university' room
                        if (c, s) in small_classes and r == 'university':
                            continue  # Skip this combination
                        # Enforce room capacity constraints
                        if seat_capacity is not None and rooms[r]['capacity'] < seat_capacity:
                            continue  # Skip this combination
                        idx = (c, s, mp, period, r)
                        x_indices.append(idx)

    # Define the decision variables
    x = {}
    for idx in x_indices:
        var_name = "x_%s_%s_%s_%s_%s" % idx
        x[idx] = pulp.LpVariable(var_name, cat='Binary')

    y = {}
    for c in courses:
        for section in courses[c]['sections']:
            s = section['section_number']
            y[(c, s)] = pulp.LpVariable(f"y_{c}_{s}", cat='Binary')

    z = {}
    for c in courses:
        for section in courses[c]['sections']:
            s = section['section_number']
            for p in professors:
                if c in professors[p]['qualified_courses']:
                    z[(c, s, p)] = pulp.LpVariable(f"z_{c}_{s}_{p}", cat='Binary')

    # -----------------------------
    # Manually Scheduled Classes (Constraints)
    # -----------------------------
    # Process manually scheduled classes
    for entry in manually_scheduled_classes:
        c = entry['course']
        s = entry['section']
        # Ensure the class is scheduled
        prob += y[(c, s)] == 1, f"Manual_Class_Scheduled_{c}_{s}"

        # Fix professor assignment if specified
        if 'professor' in entry:
            p = entry['professor']
            # Ensure the professor is assigned to the class
            prob += z[(c, s, p)] == 1, f"Manual_Professor_Assigned_{c}_{s}_{p}"

        # Fix meeting pattern, period, and room if specified
        if 'meeting_pattern' in entry and 'period' in entry and 'room' in entry:
            mp = entry['meeting_pattern']
            period = entry['period']
            r = entry['room']
            idx = (c, s, mp, period, r)
            if idx in x:
                prob += x[idx] == 1, f"Manual_Schedule_{c}_{s}_{mp}_{period}_{r}"
            else:
                print(f"Warning: Invalid manual schedule for class {c} section {s}.")
        else:
            # Fix meeting pattern if specified
            if 'meeting_pattern' in entry:
                mp = entry['meeting_pattern']
                prob += pulp.lpSum([
                    x[idx]
                    for idx in x_indices
                    if idx[0] == c and idx[1] == s and idx[2] == mp
                ]) == y[(c, s)], f"Manual_Meeting_Pattern_{c}_{s}_{mp}"

            # Fix period if specified
            if 'period' in entry:
                period = entry['period']
                prob += pulp.lpSum([
                    x[idx]
                    for idx in x_indices
                    if idx[0] == c and idx[1] == s and idx[3] == period
                ]) == y[(c, s)], f"Manual_Period_{c}_{s}_{period}"

            # Fix room if specified
            if 'room' in entry:
                r = entry['room']
                prob += pulp.lpSum([
                    x[idx]
                    for idx in x_indices
                    if idx[0] == c and idx[1] == s and idx[4] == r
                ]) == y[(c, s)], f"Manual_Room_{c}_{s}_{r}"

    # -----------------------------
    # Constraints
    # -----------------------------

    # 1. Link x and y variables
    for c in courses:
        for section in courses[c]['sections']:
            s = section['section_number']
            prob += pulp.lpSum([
                x[idx]
                for idx in x_indices
                if idx[0] == c and idx[1] == s
            ]) == y[(c, s)], f"Link_x_y_{c}_{s}"

    # 2. Professors assigned to sections must be qualified and available
    for c in courses:
        for section in courses[c]['sections']:
            s = section['section_number']
            qualified_professors = [p for p in professors if c in professors[p]['qualified_courses']]
            prob += pulp.lpSum([
                z[(c, s, p)]
                for p in qualified_professors
            ]) == y[(c, s)], f"Prof_Assignment_{c}_{s}"

    # 3. Limit professors to maximum number of classes
    for p in professors:
        prob += pulp.lpSum([
            z[(c, s, p)]
            for c in courses
            for section in courses[c]['sections']
            for s in [section['section_number']]
            if (c, s, p) in z
        ]) <= professors[p]['max_classes'], f"Max_Classes_{p}"

    # 4. A professor cannot teach more than one class at the same time
    for p in professors:
        for mp in meeting_patterns:
            for period in meeting_patterns[mp]['periods']:
                constraint_name = f"Prof_Time_Conflict_{p}_{mp}_{period}"
                # Sum over all classes assigned to professor p at (mp, period)
                prob += pulp.lpSum([
                    x[idx]
                    for idx in x_indices
                    if (idx[0], idx[1], p) in z
                    and idx[2] == mp
                    and idx[3] == period
                ]) <= 1, constraint_name

    # 5a. If z[(c, s, p)] == 1, then x[idx] == 1 for some idx
    for c in courses:
        for section in courses[c]['sections']:
            s = section['section_number']
            for p in professors:
                if (c, s, p) in z:
                    constraint_name = f"Link_z_x_{c}_{s}_{p}"
                    
                    prob += pulp.lpSum([
                        x[idx]
                        for idx in x_indices
                        if idx[0] == c and idx[1] == s and is_prof_available_for_time_slot(p, idx[2], idx[3])
                    ]) >= z[(c, s, p)], constraint_name

    # 5b. If x[idx] == 1, then z[(c, s, p)] == 1 for some p
    for idx in x_indices:
        c, s, mp, period, r = idx
        constraint_name = f"Link_x_z_{c}_{s}_{mp}_{period}_{r}"
        
        prob += x[idx] <= pulp.lpSum([
            z[(c, s, p)]
            for p in professors
            if (c, s, p) in z and is_prof_available_for_time_slot(p, mp, period)
        ]), constraint_name

    # 6. Room capacity constraints (no double booking)
    # Collect all unique day-period combinations
    all_day_periods = set()
    for mp in meeting_patterns:
        days = meeting_patterns[mp]['days']
        periods = meeting_patterns[mp]['periods'].keys()
        for day in days:
            for period in periods:
                all_day_periods.add((day, period))

    # 6. Room capacity constraints (no double booking)
    for r in rooms:
        if r != 'university':
            for mp in meeting_patterns:
                for period in meeting_patterns[mp]['periods']:
                    constraint_name = f"Room_Capacity_{r}_{mp}_{period}"
                    prob += pulp.lpSum([
                        x[idx]
                        for idx in x_indices
                        if idx[4] == r
                        and idx[2] == mp
                        and idx[3] == period
                    ]) <= 1, constraint_name
    # 7. Room overlap constraints
    for r in rooms:
        for d in days:
            periods = sorted(meeting_patterns['MW']['periods'].keys())
            for p in periods:
                next_p = p + 1
                if next_p in meeting_patterns['MW']['periods'].keys():
                    current_ts = (d, p)
                    next_ts = (d, next_p)
                    mw_current = pulp.lpSum([
                        x[idx] for idx in x_indices
                        if idx[2] == 'MW' and idx[3] == current_ts and idx[4] == r
                    ])
                    mwf_next = pulp.lpSum([
                        x[idx] for idx in x_indices
                        if idx[2] == 'MWF' and idx[3] == next_ts and idx[4] == r
                    ])
                    mw_next = pulp.lpSum([
                        x[idx] for idx in x_indices
                        if idx[2] == 'MW' and idx[3] == next_ts and idx[4] == r
                    ])
                    prob += mw_current + mwf_next + mw_next <= 1, f"Room_Overlap_{r}_{d}_{p}"

    # 8. Rush-hour penalties and objective function
    rush_hour_time_slots = set()
    for mp in meeting_patterns:
        for day in meeting_patterns[mp]['days']:
            for period, info in meeting_patterns[mp]['periods'].items():
                start_time = info['start_time']
                # Convert start_time to minutes since midnight
                time_parts = start_time[:-2].split(':')
                hour = int(time_parts[0])
                minute = int(time_parts[1])
                am_pm = start_time[-2:]
                if am_pm == 'PM' and hour != 12:
                    hour += 12
                elif am_pm == 'AM' and hour == 12:
                    hour = 0
                start_minutes = hour * 60 + minute
                # Define rush-hour as 11:00 AM (660 minutes) to 2:00 PM (840 minutes)
                if 660 <= start_minutes < 840:
                    rush_hour_time_slots.add((day, period))

    # Identify x indices in rush-hour
    rush_hour_x_indices = [
        idx for idx in x_indices
        if idx[3] in rush_hour_time_slots
    ]

    # Define room costs
    room_cost = {}
    for idx in x_indices:
        c, s, mp, ts, r = idx
        if r == 'university' and (c, s) in small_classes:
            room_cost[idx] = 1  # Assign a penalty cost
        else:
            room_cost[idx] = 0

    # Modify the objective function
    prob += (
        pulp.lpSum([
            y[(c, s)]
            for c in courses
            for section in courses[c]['sections']
            for s in [section['section_number']]
        ])
        - pulp.lpSum([
            room_cost[idx] * x[idx]
            for idx in x_indices
        ])
        - rush_hour_penalty * pulp.lpSum([
            x[idx]
            for idx in rush_hour_x_indices
        ])
    ), "Objective_Function"

    # -----------------------------
    # Solve the Problem
    # -----------------------------
    prob.solve()

    # -----------------------------
    # Output the Schedule and Store Assignments
    # -----------------------------
    if pulp.LpStatus[prob.status] == 'Optimal':
        schedule = []
        unscheduled_classes = []
        assignment = {}  # Dictionary to store current assignments
        for c in courses:
            for section in courses[c]['sections']:
                s = section['section_number']
                if pulp.value(y[(c, s)]) == 1:
                    # Class is scheduled
                    assigned = False
                    for idx in x_indices:
                        if idx[0] == c and idx[1] == s and pulp.value(x[idx]) == 1:
                            c, s, mp, period, r = idx
                            section = next(sec for sec in courses[c]['sections'] if sec['section_number'] == s)
                            seat_capacity = section['seat_capacity']
                            # Find the assigned professor
                            assigned_professor = None
                            for p in professors:
                                if (c, s, p) in z and pulp.value(z[(c, s, p)]) == 1:
                                    assigned_professor = p
                                    break
                            days = meeting_patterns[mp]['days']
                            start_time = meeting_patterns[mp]['periods'][period]['start_time']
                            schedule.append({
                                'Course': c,
                                'Section': s,
                                'Title': courses[c]['title'],
                                'Professor': assigned_professor,
                                'Meeting Pattern': mp,
                                'Days': days,
                                'Period': period,
                                'Start Time': start_time,
                                'Room': r,
                                'Seat Capacity': seat_capacity
                            })
                            assignment[(c, s)] = idx  # Store the current assignment
                            assigned = True
                            break
                    if not assigned:
                        unscheduled_classes.append((c, s))
                else:
                    # Class is not scheduled
                    unscheduled_classes.append((c, s))

        # Initialize a dictionary to count classes assigned to each professor
        professor_class_counts = {p: 0 for p in professors}

        # Iterate over the assignment variables z to count classes
        for (c, s, p) in z:
            if pulp.value(z[(c, s, p)]) == 1:
                professor_class_counts[p] += 1

        # List of professors with no classes assigned
        professors_with_no_classes = [p for p, count in professor_class_counts.items() if count == 0]

        # Return the results
        result = {
            'schedule': schedule,
            'unscheduled_classes': unscheduled_classes,
            'professors_with_no_classes': professors_with_no_classes,
            'assignment': assignment,
            'prob_status': pulp.LpStatus[prob.status]
        }
        assignment_serializable = {str(k): list(v) if isinstance(v, tuple) else v for k, v in assignment.items()}
        result['assignment'] = assignment_serializable
        return result
    else:
        # No feasible solution found
        result = {
            'schedule': [],
            'unscheduled_classes': [],
            'professors_with_no_classes': [],
            'assignment': {},
            'prob_status': pulp.LpStatus[prob.status],
            'message': f"No feasible solution found. Solver Status: {pulp.LpStatus[prob.status]}"
        }
        return result


manually_scheduled_classes = get_manually_scheduled_data()
days = load_days()
mwf_periods, tth_periods, mw_periods = load_periods()
meeting_patterns =  load_meeting_patterns(mwf_periods, tth_periods, mw_periods)
professors =  get_professordata()
courses =  get_coursedata()
rooms =  get_roomdata()

results = run_scheduling_algorithm(
days=days,
meeting_patterns=meeting_patterns,
professors=professors,
courses=courses,
rooms=rooms,
manually_scheduled_classes=manually_scheduled_classes
)
print(results)
