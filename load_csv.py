from fastapi import FastAPI, UploadFile, File
import csv
import io
import uvicorn


app = FastAPI()

dorms = []
soldiers = []
waiting_list = []



# @app.post("/upload-csv")
# def upload_csv(file: UploadFile):

#     if file.content_type != "text/csv":
#          return {"error": "File must be a CSV"}
    

#     content = file.file.read().decode("utf-8")

#     reader = csv.reader(io.StringIO(content))
#     header = next(reader)
#     rows = list(reader)
#     file.file.close()

#     for line in rows:
#         print(line)


#     return {
#         "filename": file.filename,
#         "content_type": file.content_type,
#         "total_rows": len(rows),
#         "columns": header,
#         "data": rows[0:5],
#         "message": f"Successfully processed CSV with {len(rows)} rows"
#     }



def create_dorms():
    result = []
    for name in ["Dorm A", "Dorm B"]:
        rooms = []
        for i in range(10):
            rooms.append({
                "number": i,
                "soldiers": []
            })
        result.append({
            "name": name,
            "rooms": rooms
        })
    return result



def Bubble_sort_by_distance(list_to_sort):
    for i in range(len(list_to_sort)):
        for j in range(i + 1, len(list_to_sort)):
            if list_to_sort[j]["distance"] > list_to_sort[i]["distance"]:
                list_to_sort[i], list_to_sort[j] = list_to_sort[j], list_to_sort[i]
    return list_to_sort


def assign():
    global waiting_list
    waiting_list = []

    sorted_list = Bubble_sort_by_distance(soldiers)

    for soldier in sorted_list:
        find_a_place = False
        for dorm in dorms:
            for room in dorm["rooms"]:
                if len(room["soldiers"]) < 8:
                    room["soldiers"].append(soldier)
                    soldier["status"] = "assigned"
                    soldier["dorm"] = dorm["name"]
                    soldier["room"] = room["number"]
                    find_a_place = True
                    break
            if find_a_place:
                break

        if not find_a_place:
            soldier["status"] = "waiting"
            waiting_list.append(soldier)


@app.post("/upload-csv")
def upload_csv(file: UploadFile):

    global soldiers, dorms

    soldiers = []
    dorms = create_dorms()

    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(content)


    for row in reader:
        soldiers.append({
            "personal_id": int(row["personal_id"]),
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "gender": row["gender"],
            "city": row["city"],
            "distance": int(row["distance"]),
            "status": "waiting",
            "dorm": None,
            "room": None
        })

    assign()

    result = {
        "assigned": len(soldiers) - len(waiting_list),
        "waiting_list": len(waiting_list),
        "soldiers": []
    }

    for soldier in soldiers:
        result["soldiers"].append({
            "personal_id": soldier["personal_id"],
            "name": soldier["first_name"] + " " + soldier["last_name"],
            "assigned": soldier["status"] == "assigned",
            "dorm": soldier["dorm"],
            "room": soldier["room"],
            "waiting": soldier["status"] == "waiting"
        })

    return result


@app.get("/space")
def space():
    res = []

    for dorm in dorms:
        full = 0
        partial = 0
        empty = 0

        for room in dorm["rooms"]:
            count = len(room["soldiers"])
            if count == 8:
                full += 1
            elif count == 0:
                empty += 1
            else:
                partial += 1

        res.append({
            "dorm": dorm["name"],
            "full_rooms": full,
            "partial_rooms": partial,
            "empty_rooms": empty
        })

    return res



@app.get("/waitingList")
def waiting_list_route():
    res = []
    for soldier in waiting_list:
        res.append({
            "personal_id": soldier["personal_id"],
            "name": soldier["first_name"] + " " + soldier["last_name"],
            "distance": soldier["distance"]
        })
    return res



@app.get("/search")
def search(personal_id):
    for soldier in soldiers:
        if soldier["personal_id"] == personal_id:
            return {
                "personal_id": soldier["personal_id"],
                "name": soldier["first_name"] + " " + soldier["last_name"],
                "assigned": soldier["status"] == "assigned",
                "dorm": soldier["dorm"],
                "room": soldier["room"],
                "waiting": soldier["status"] == "waiting"
            }

    return {"error": "soldier not found"}