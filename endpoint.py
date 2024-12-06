from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from algorithm import get_manually_scheduled_data, load_days, load_meeting_patterns, load_periods, run_scheduling_algorithm, get_professordata, add_professor, update_professor, delete_professor, add_courses, update_course, delete_course, get_coursedata, get_roomdata, add_room, update_room, delete_room
from fastapi.middleware.cors import CORSMiddleware
from schemas import Professor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000/", "http://127.0.0.1:5500"],  # React app origin during development
    allow_credentials=True,
    allow_methods=[""],  # Allow all HTTP methods
    allow_headers=[""],  # Allow all HTTP headers
)

@app.get("/")
def schedule_classes():
    manually_scheduled_classes = get_manually_scheduled_data()
    days = load_days()
    mwf_periods, tth_periods, mw_periods = load_periods()
    meeting_patterns =  load_meeting_patterns(mwf_periods, tth_periods, mw_periods)
    professors =  get_professordata()
    courses =  get_coursedata()
    rooms =  get_roomdata()

    try:
        # Run the scheduling algorithm
        results = run_scheduling_algorithm(
            days=days,
            meeting_patterns=meeting_patterns,
            professors=professors,
            courses=courses,
            rooms=rooms,
            manually_scheduled_classes=manually_scheduled_classes
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
class Professor(BaseModel):
    name: str
    qualified_courses: list[str]
    availability: list[list]
    max_classes: int

@app.get("/professors")
def get_professors():
    try: 
        results = get_professordata()
        return results
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    

@app.post("/professors")
def create_professor(professor: Professor):
    try: 
        results = add_professor(professor.name, professor.qualified_courses, professor.availability, professor.qualified_courses)
        return results
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

@app.put("/professors/{name}")
def update_professors(professor: Professor):
    try: 
        results = update_professor(professor.name, professor.qualified_courses, professor.availability, professor.qualified_courses)
        return results
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

@app.delete("/professor/{name}")
def delete_professors(professor:Professor):
    try: 
        results = delete_professor(professor.name)
        return results
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))


class Course(BaseModel):
    title: str
    section: list[dict]

@app.get("/courses")
def get_course():
    try: 
        results = get_coursedata()
        return results
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
@app.post("/courses")
def create_courses(course:Course):
    try: 
        results = add_courses(course.title, course.section)
        return results
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))    
    
@app.put("/courses{title}")
def update_professors(course:Course):
    try: 
        results = update_course(course.title, course.section)
        return results
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))      
    
@app.delete("/courses{title}")
def delete_courses(course:Course):
    try: 
        results = delete_course(course.title)
        return results
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))   
       
class Room(BaseModel):
    name: str
    capacity: int

@app.get("/rooms")
def get_rooms():
    try: 
        results = get_roomdata()
        return results
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
@app.post("/rooms")
def create_room(room:Room):
    try: 
        results = add_room(room.name, room.capacity)
        return results
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))    
    
@app.put("/rooms{name}")
def update_rooms(room:Room):
    try: 
        results = update_room(room.name, room.capacity)
        return results
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))      
    
@app.delete("/rooms{name}")
def delete_rooms(room:Room):
    try: 
        results = delete_room(room.name)
        return results
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e)) 

class Manaully_Scheduled_Course(BaseModel):
    course: str
    section: int
    professor: str
    meeting_pattern: str
    time_slot: list
    room: str

@app.get("/manual")
def get_rooms():
    try: 
        results = get_manually_scheduled_data()
        return results
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))