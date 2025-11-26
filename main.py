from fastapi import UploadFile,FastAPI
import csv
import io
import uvicorn


app = FastAPI()


@app.post("/upload-csv")
def upload_csv(file: UploadFile):

    
    if file.content_type != "text/csv":
         return {"error": "File must be a CSV"}
    
    content = file.file.read().decode("utf-8")

    reader = csv.reader(io.StringIO(content))
    header = next(reader)
    rows = list(reader)
    file.file.close()

    for line in rows:
        print(line)


    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "total_rows": len(rows),
        "columns": header,
        "data": rows[0:2],
        "message": f"Successfully processed CSV with {len(rows)} rows"
    }

@app.get("/upload-csv/search")
def search(limit: int = 10, sort: int = "asc"):
    return {"limit": limit, "sort": sort}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0" ,port=8000)




