
def user_helper(info):
    return{
        'id': str(info['_id']),
        'username': info['username'],
        'hashed_password': info['hashed_password'],
        'level': info['level'],
        'exp' : info['exp'],
        'streak': info['streak']
    }
    
def serial_user_helper(infos):
    return [user_helper(data) for data in infos]