def handle_user_data(data):
    print(f'Recieved {data}')
    request_type = None 
    
    match request_type:
        case _:
            return "Success"