def handle_user_data(data):
    print(f'Recieved {data}')
    request_type = data["request_type"] 
    
    match request_type:
        case "registration":
            
            return {
                "status": "success",
                "user_id": "test"
            }
        
        case "login":
            
            return {
                "status": "success",
                "user_id": "test"
            }
            
        case _:
            
            return {
                "status": "error",
                "message": "Service does not exist"
            }
