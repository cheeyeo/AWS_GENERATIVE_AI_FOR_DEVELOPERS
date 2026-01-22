import os
import json
import stat
import shutil
import sqlite3
from datetime import datetime


shutil.copy('employee_database.db', '/tmp/employee_database.db')
os.chmod('/tmp/employee_database.db', stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH | stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)


def get_available_vacations_days(employee_id):
    conn = sqlite3.connect('/tmp/employee_database.db')
    c = conn.cursor()

    if employee_id:
        c.execute("""
            SELECT employee_vacation_days_available
            FROM vacations
            WHERE employee_id = ?
            ORDER BY year DESC
            LIMIT 1
        """, (employee_id,))

        available_vacation_days = c.fetchone()

        if available_vacation_days:
            available_vacation_days = available_vacation_days[0]
            conn.close()
            return available_vacation_days
        else:
            conn.close()
            return f"No vacation data found for employed_id {employee_id}"
    else:
        conn.close()
        raise Exception("No employee id provided")
    

def reserve_vacation_time(employee_id, start_date, end_date):
    conn = sqlite3.connect("/tmp/employee_database.db")
    c = conn.cursor()

    if not employee_id or not start_date or not end_date:
        conn.close()
        raise Exception("Missing required parameters")
    
    # Calculate vacation days
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date()
    vacation_days = (end - start).days + 1

     # Insert into planned_vacations
    c.execute("""
        INSERT INTO planned_vacations (employee_id, vacation_start_date, vacation_end_date, vacation_days_taken)
        VALUES (?, ?, ?, ?)
    """, (employee_id, start_date, end_date, vacation_days))

    # Update available vacation days
    c.execute("""
        UPDATE vacations 
        SET employee_vacation_days_available = employee_vacation_days_available - ?,
            employee_vacation_days_taken = employee_vacation_days_taken + ?
        WHERE employee_id = ? AND year = (SELECT MAX(year) FROM vacations WHERE employee_id = ?)
    """, (vacation_days, vacation_days, employee_id, employee_id))
    
    conn.commit()
    conn.close()
    
    return f"Reserved {vacation_days} vacation days from {start_date} to {end_date} for employee {employee_id}"


    

def lambda_handler(event, context):
    print(event)
    print(context)

    try:
        parameters = event.get("parameters", [])
        function_name = event.get("function")

        # Parse parameters
        params_dict = {}
        for param in parameters:
            params_dict[param.get("name")] = param.get("value")

        # Route to appropriate function
        if function_name == "get_available_vacations_days":
            employee_id = int(params_dict.get("employee_id"))
            result = get_available_vacations_days(employee_id)
        elif function_name == "reserve_vacation_time":
            employee_id = int(params_dict.get("employee_id"))
            start_date = params_dict.get("start_date")
            end_date = params_dict.get("end_date")
            result = reserve_vacation_time(employee_id, start_date, end_date)
        else:
            raise Exception(f"Unknown function: {function_name}")
        
        # return Bedrock expected format
        return {
            "response": {
                "actionGroup": event.get("actionGroup"),
                "function": event.get("function"),
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps({"result": result})
                        }
                    }
                }
            }
        }
    except Exception as e:
        return {
            "response": {
                "actionGroup": event.get("actionGroup"),
                "function": event.get("function"),
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps({"error": str(e)})
                        }
                    }
                }
            }
        }
