import json
from datetime import datetime
from datetime import timedelta

data = None

def check_func():
    """
    random function to check random outputs
    """
    from datetime import datetime

    # dt = datetime(2025, 6, 15, 14, 30, 45, 123456)

    # Date components
    # print("Year:", dt.year)        # 2025
    # print("Month:", dt.month)      # 6
    # print("Day:", dt.day)          # 15

    # # Time components  
    # print("Hour:", dt.hour)        # 14
    # print("Minute:", dt.minute)    # 30
    # print("Second:", dt.second)    # 45
    # print("Microsecond:", dt.microsecond)  # 123456
    # # Get weekday (0=Monday, 6=Sunday)
    # print("Weekday:", dt.weekday())

    # # Get day of year
    # print("Day of year:", dt.timetuple().tm_yday)

    # # Get timestamp
    # print("Timestamp:", dt.timestamp())
    from datetime import datetime

# Convert datetime to timestamp
    dt = datetime(2024, 9, 19, 15, 30, 0)
    timestamp = dt.timestamp()
    print(f"Timestamp: {timestamp}")

    # Convert timestamp back to datetime
    dt_from_timestamp = datetime.fromtimestamp(timestamp)
    print(f"From timestamp: {dt_from_timestamp}")





def print_data():
    if data is not None:
        print(data[0].get("employee_id", ""))

def total_working_hours(emp_id: str):
    """
    Calculates the total working hours for a given employee ID.
    
    :param emp_id: Employee ID as a string.
    :return: Total working hours as an integer.

    {
        "employee_id": "emp_001",
        "name": "Alice Johnson",
        "department": "Engineering",
        "sessions": [
        {
            "session_id": "s_001",
            "start_time": "2024-01-15T09:00:00Z",
            "end_time": "2024-01-15T12:30:00Z",
            "activity_type": "coding",
            "project": "web_app"
        },
        {
            "session_id": "s_002",
            "start_time": "2024-01-15T13:30:00Z",
            "end_time": "2024-01-15T17:00:00Z",
            "activity_type": "meetings",
            "project": "web_app"
        }
        ]
    }
    """
    
    if data is None:
        return 0
    
    total_hours = 0
    emp_record = {}
    for record in data:
        if record.get("employee_id") == emp_id:
            emp_record = record
            break

    if not emp_record:
        return 0
    
    if not emp_record:
        return 0
    
    total_milliseconds = 0
    days = 0
    # Calculate total time for all sessions
    for session in emp_record.get("sessions", []):
        start_time_str = session.get("start_time")
        end_time_str = session.get("end_time")
        # print(start_time_str, end_time_str)
        if start_time_str and end_time_str:
            # Parse ISO format timestamps
            start_time = datetime.fromisoformat(start_time_str.replace('Z',""))
            end_time = datetime.fromisoformat(end_time_str.replace('Z', ""))
            # print(start_time)
            # Calculate duration in milliseconds
            duration = end_time - start_time
            total_milliseconds += duration.total_seconds() * 1000
            # days+= duration.days
    
    # Convert milliseconds to hours
    total_hours = total_milliseconds / (1000 * 60 * 60)

    
    return total_hours

def calculate_break_time(emp_id: str):

    if data is None:
        return 0
    total_break_time = 0
    emp_record = {}
    for record in data:
        if record.get("employee_id") == emp_id:
            emp_record = record
            break
    if not emp_record:
        return 0
    total_milliseconds = 0
    prev_end_time = None
    # Calculate total break time for all sessions
    for session_id in range(1, len(emp_record.get("sessions", []))):
        prev_end_time = datetime.strptime(emp_record["sessions"][session_id-1].get("end_time"), "%Y-%m-%dT%H:%M:%SZ")
        start_time = datetime.strptime(emp_record["sessions"][session_id].get("start_time"), "%Y-%m-%dT%H:%M:%SZ")
        
        break_duration = start_time - prev_end_time
        if break_duration.total_seconds() > 0:
            total_milliseconds += break_duration.total_seconds() * 1000
    # Convert milliseconds to hours
    total_break_time = total_milliseconds / (1000 * 60 * 60)
    return total_break_time

def calculate_total_time_per_activity(activity_type: str):
    pass



def most_active_timeperiod():
    """
    Determines the most active time period for all employees, i.e, this function should return the time period when there are maximum number of concurrent sessions.
    
    :return: A dictionary with the most active time period and concurrent sessions during that period.
    """
    if data is None:
        return {}

    time_periods = {}
    
    for record in data:
        for session in record.get("sessions", []):
            start_time_str = session.get("start_time")
            end_time_str = session.get("end_time")
            if start_time_str and end_time_str:
                start_time = datetime.fromisoformat(start_time_str.replace('Z', ""))
                end_time = datetime.fromisoformat(end_time_str.replace('Z', ""))
                
                # Increment the count for each hour in the session
                current_time = start_time
                while current_time < end_time:
                    hour_key = current_time.strftime("%Y-%m-%d %H:00:00")
                    if hour_key not in time_periods:
                        time_periods[hour_key] = 0
                    time_periods[hour_key] += 1
                    current_time += timedelta(hours=1)

    # Find the time period with the maximum concurrent sessions
    most_active_period = max(time_periods, key=time_periods.get)
    max_sessions = time_periods[most_active_period]

    return {
        "most_active_period": most_active_period,
        "max_sessions": max_sessions
    }

def get_overall_time_concurrent_sessions():
    """
    Calculates the overall time when there are concurrent sessions across all employees.
    
    :return: A dictionary with the overall time and the number of concurrent sessions during that time.
    """
    if data is None:
        return {}

    time_periods = {}
    
    for record in data.get("employees", []):
        for session in record.get("sessions", []):
            start_time_str = session.get("start_time")
            end_time_str = session.get("end_time")
            if start_time_str and end_time_str:
                start_time = datetime.fromisoformat(start_time_str.replace('Z', ""))
                end_time = datetime.fromisoformat(end_time_str.replace('Z', ""))
                
                # Increment the count for each hour in the session
                current_time = start_time
                while current_time < end_time:
                    hour_key = current_time.strftime("%Y-%m-%d %H:00:00")
                    if hour_key not in time_periods:
                        time_periods[hour_key] = 0
                    time_periods[hour_key] += 1
                    current_time += timedelta(hours=1)

    return time_periods


def get_number_employees_logged_in_at_time(time_str):
    """
    Returns the number of employees logged in at a specific time.
    
    :param time_str: Time in ISO format (e.g., "2024-01-15T10:00:00Z").
    :return: Number of employees logged in at that time.
    """
    
    if data is None:
        return 0
    
    count = 0
    target_time = datetime.fromisoformat(time_str.replace('Z', ""))
    
    for record in data.get("employees", []):
        for session in record.get("sessions", []):
            start_time_str = session.get("start_time")
            end_time_str = session.get("end_time")
            if start_time_str and end_time_str:
                start_time = datetime.fromisoformat(start_time_str.replace('Z', ""))
                end_time = datetime.fromisoformat(end_time_str.replace('Z', ""))
                
                if start_time <= target_time <= end_time:
                    count += 1
                    break  # No need to check further sessions for this employee
    
    return count

def find_free_session():
    """
    find 5 minute free session which is common to all employees where we can schedule a meeting.
    :return: A dictionary with the start and end time of the free session.
    """
    if data is None or not data.get("employees"):
        return {"error": "No data available"}
    
    # Get the date from the data
    date_str = data.get("date", "2024-01-15")
    
    # Define working hours (8 AM to 6 PM)
    work_start = datetime.strptime(f"{date_str}T09:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
    work_end = datetime.strptime(f"{date_str}T18:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
    
    # Create 30-minute time slots
    time_slots = []
    current_slot = work_start
    while current_slot + timedelta(minutes=10) <= work_end:
        time_slots.append({
            "start": current_slot,
            "end": current_slot + timedelta(minutes=10)
        })
        current_slot += timedelta(minutes=10)
    
    # Check each time slot
    for slot in time_slots:
        slot_free = True
        
        # Check if all employees are free during this slot
        for employee in data.get("employees", []):
            employee_free = True
            
            # Check if employee has any sessions during this slot
            for session in employee.get("sessions", []):
                start_time_str = session.get("start_time")
                end_time_str = session.get("end_time")
                
                if start_time_str and end_time_str:
                    session_start = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%SZ")
                    session_end = datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%SZ")
                    
                    # Check if session overlaps with the slot
                    if not (session_end <= slot["start"] or session_start >= slot["end"]):
                        employee_free = False
                        break
            
            # If this employee is not free, this slot won't work
            if not employee_free:
                slot_free = False
                break
        
        # If all employees are free during this slot, return it
        if slot_free:
            return {
                "start_time": slot["start"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                "end_time": slot["end"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                "duration_minutes": 15
            }
    
    return {"error": "No common free slot found between 8 AM and 6 PM"}



def read_json_file(file_path):


    """
    Reads a JSON file and returns its content as a dictionary.
    
    :param file_path: Path to the JSON file.
    :return: Dictionary containing the JSON data.
    """
    
    with open(file_path, 'r') as file:
        return json.load(file)
    

def calculate_actual_number_of_days():
    """
    Calculates the actual number of days between dates in the test cases,
    accounting for leap years and varying month lengths.
    """
    if data is None:
        return []
    
    results = []
    
    # Helper function to check if a year is a leap year
    # def is_leap_year(year):
    #     if year % 400 == 0:
    #         return True
    #     if year % 100 == 0:
    #         return False
    #     if year % 4 == 0:
    #         return True
    #     return False
    
    # # Helper function to get days in a month
    # def days_in_month(year, month):
    #     days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    #     if month == 2 and is_leap_year(year):
    #         return 29
    #     return days_per_month[month - 1]
    
    # Process each test case
    for test_case in data.get("test_cases", []):
        case_id = test_case.get("case_id")
        start_date_str = test_case.get("start_date")
        end_date_str = test_case.get("end_date")
        expected_days = test_case.get("expected_days")
        
        # Parse dates
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        
        # Calculate difference using datetime (simple approach)
        actual_days = (end_date - start_date).days
        
        # Alternative manual calculation for verification
        manual_days = 0
        if start_date <= end_date:
            current_date = start_date
            while current_date < end_date:
                manual_days += 1
                current_date += timedelta(days=1)
        else:
            # Handle negative days (reverse order)
            current_date = end_date
            while current_date < start_date:
                manual_days -= 1
                current_date += timedelta(days=1)
        
        # Store results
        results.append({
            "case_id": case_id,
            "start_date": start_date_str,
            "end_date": end_date_str,
            "expected_days": expected_days,
            "actual_days": actual_days,
            "manual_calculation": manual_days,
            "matches_expected": actual_days == expected_days,
            "description": test_case.get("description", "")
        })
    
    # Process edge cases if they exist
    for edge_case in data.get("edge_cases", []):
        case_id = edge_case.get("case_id")
        start_date_str = edge_case.get("start_date")
        end_date_str = edge_case.get("end_date")
        expected_days = edge_case.get("expected_days")
        
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            actual_days = (end_date - start_date).days
            
            results.append({
                "case_id": case_id,
                "start_date": start_date_str,
                "end_date": end_date_str,
                "expected_days": expected_days,
                "actual_days": actual_days,
                "matches_expected": actual_days == expected_days,
                "description": edge_case.get("description", "")
            })
        except:
            results.append({
                "case_id": case_id,
                "error": "Date parsing error",
                "description": edge_case.get("description", "")
            })
    
    return results


def get_actual_number_of_months():
    """
    Calculates the number of complete months between dates in the test cases,
    accounting for leap years, varying month lengths, and month-end edge cases.
    """
    if data is None:
        return []
    
    results = []
    
    # Helper function to check if a year is a leap year
    def is_leap_year(year):
        if year % 400 == 0:
            return True
        if year % 100 == 0:
            return False
        if year % 4 == 0:
            return True
        return False
    
    # Helper function to get the last day of a month
    def get_last_day_of_month(year, month):
        days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if month == 2 and is_leap_year(year):
            return 29
        return days_per_month[month - 1]
    
    # Helper function to calculate complete months between two dates
    def calculate_complete_months(start_date, end_date):
        # Handle reverse order
        if end_date < start_date:
            return -calculate_complete_months(end_date, start_date)
        
        # Extract year, month, day components
        start_year, start_month, start_day = start_date.year, start_date.month, start_date.day
        end_year, end_month, end_day = end_date.year, end_date.month, end_date.day
        
        # Calculate raw month difference
        months_diff = (end_year - start_year) * 12 + (end_month - start_month)
        
        # Adjust for day comparison
        # Check if we've completed the month by comparing days
        if end_day < start_day:
            # Special case: if start day doesn't exist in end month
            # (e.g., Jan 31 to Feb 28), check if end_day is last day of month
            last_day_of_end_month = get_last_day_of_month(end_year, end_month)
            
            # If end date is at month end and start day > last day of end month,
            # we still count it as incomplete month
            if end_day == last_day_of_end_month and start_day > last_day_of_end_month:
                months_diff -= 1
            else:
                months_diff -= 1
        
        return months_diff
    
    # Process each test case
    for test_case in data.get("test_cases", []):
        case_id = test_case.get("case_id")
        start_date_str = test_case.get("start_date")
        end_date_str = test_case.get("end_date")
        expected_months = test_case.get("expected_months")
        
        # Parse dates
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        
        # Calculate complete months
        actual_months = calculate_complete_months(start_date, end_date)
        
        # Store results
        results.append({
            "case_id": case_id,
            "start_date": start_date_str,
            "end_date": end_date_str,
            "expected_months": expected_months,
            "actual_months": actual_months,
            "matches_expected": actual_months == expected_months,
            "description": test_case.get("description", ""),
            "explanation": test_case.get("explanation", "")
        })
    
    # Process edge cases if they exist
    for edge_case in data.get("edge_cases", []):
        case_id = edge_case.get("case_id")
        start_date_str = edge_case.get("start_date")
        end_date_str = edge_case.get("end_date")
        expected_months = edge_case.get("expected_months")
        
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            actual_months = calculate_complete_months(start_date, end_date)
            
            results.append({
                "case_id": case_id,
                "start_date": start_date_str,
                "end_date": end_date_str,
                "expected_months": expected_months,
                "actual_months": actual_months,
                "matches_expected": actual_months == expected_months,
                "description": edge_case.get("description", ""),
                "explanation": edge_case.get("explanation", "")
            })
        except Exception as e:
            results.append({
                "case_id": case_id,
                "error": f"Date parsing error: {str(e)}",
                "description": edge_case.get("description", "")
            })
    
    return results


if __name__ == "__main__":
    data = read_json_file('scale/json_parsers/dummy_input3.json')
    # print(total_working_hours("emp_001"))
    # print(calculate_break_time("emp_001")) 
    # print(get_overall_time_concurrent_sessions())
    # print(len(data.get("employees", [])))
    print(get_actual_number_of_months())
    
    # print(data[0].get("employee_id", ""))