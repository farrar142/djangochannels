import platform

def ipchooser():
    if platform.system().strip()=="Windows":
        return '127.0.0.1'
    else:
        return '172.17.0.1'
redis_ip = ipchooser()
print(f'redis://:sbs123414@{redis_ip}:6379/0')
broker_url = f'redis://:sbs123414@{redis_ip}:6379/0'
result_backend = f'redis://:sbs123414@{redis_ip}:6379/0'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Seoul'
enable_utc = False