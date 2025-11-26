class Soldier:
   
    def _init_(self, personal_id, first_name, last_name, gender, city, distance):
        self.personal_id = personal_id  
        self.first_name = first_name    
        self.last_name = last_name      
        self.gender = gender           
        self.city = city                
        try:
            self.distance = int(distance)        
        except ValueError:
            return "distance must be int"
            
        self.assignment_status = "hold" 
        self.dorm = None                
        self.room_number = None         

    def object_to_dict(self):
        if self.assignment_status == "inserted":
            is_assigned = "yes"
            details = f" {self.dorm}, {self.room_number}"
        else:
            is_assigned = "no"
            details = "in list_waiting"

        return {
            "inserted": is_assigned,
            "personal_id": self.personal_id,
            "first_name": self.first_name,
            "distance": self.distance,
            "insert_details": details
        }

class Room:

    CAPACITY = 8 

    def _init_(self, room_number):
        self.room_number = room_number
        self.assigned_soldiers = [] 

    def is_full(self):
        return len(self.assigned_soldiers) >= self.CAPACITY
    
    def status_occupancy(self):
        count = len(self.assigned_soldiers)
        if count == self.CAPACITY:
            return "fuul" 
        elif count > 0:
            return "partially full" 
        else:
            return "empty" 
        

class Dorms:

    NUMBER_OF_ROOMS = 10 

    def _init_(self, name):
        self.name = name 

    def first_available_room(self):
        for room in self.rooms:
            if not room.is_full():
                return room
        return None
    
    def report_occupancy(self):

        report = {"full": 0, "occupancy": 0, "empty": 0}
        for room in self.rooms:
            status = room.status_occupancy()
            report[status] += 1
        return report

