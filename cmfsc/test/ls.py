@app.get("/new")
async def get_new_code():
    try:
        conn = get_db_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM files WHERE status = 'SUBMITTED' ORDER BY created_at ASC LIMIT 1")
        file_record = cursor.fetchone()

        if file_record is None:
            raise HTTPException(status_code=204, detail="No new code available")

        file_path = base_dir / file_record['filename']
        if not file_path.exists():
            raise HTTPException(status_code=500, detail="File not found on server")

        with open(file_path, 'rb') as file:
            file_content = file.read()

        cursor.execute("UPDATE files SET status = %s, updated_at = %s WHERE id = %s",
                       ("PROCESSING", int(time.time()), file_record['id']))
        conn.commit()
        cursor.close()
        conn.close()

        return Response(file_content, media_type='application/octet-stream')

    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        logger.error(f"Error fetching new code: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching new code: {e}")

@app.patch("/update_status/{file_id}")
async def update_status(file_id: int, status: str):
    try:
        conn = get_db_conn()
        cursor = conn.cursor()

        cursor.execute("UPDATE files SET status = %s, updated_at = %s WHERE id = %s",
                       (status, int(time.time()), file_id))
        conn.commit()
        cursor.close()
        conn.close()

        return {"status": "success"}
    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        logger.error(f"Error updating status: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating status: {e}")
