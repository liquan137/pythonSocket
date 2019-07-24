status = 'test'

def Data():
    if status == 'test':
        data = {
            'host': '127.0.0.1',
            'port': '5000',
            'user': 'root',
            'password': 'root',
            'database': 'test'
        }
    else:
        data = {
            'host': '127.0.0.1',
            'port': '5000',
            'user': 'root',
            'password': 'root',
            'database': 'test'
        }
    return data
