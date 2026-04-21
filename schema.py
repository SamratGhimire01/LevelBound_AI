
def user_helper(info):
    return{
        'id': str(info['_id']),
        'username': info['username'],
        'hashed_password': info['hashed_password'],
        'level': info['level'],
        'exp' : info['exp'],
        'streak': info['streak']
    }
    
def login_user_helper(created_user):
    return{
        "message":'User Created SuccessFully',
        'id': str(created_user['_id']),
        'username': created_user['username'],
        'level': created_user['level'],
        'exp' : created_user['exp'],
        'streak': created_user['streak']
    } 
    
def serial_user_helper(infos):
    return [user_helper(data) for data in infos]