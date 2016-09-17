from docker import Client

docker = Client(base_url='tcp://127.0.0.1:2375', version='auto', tls=True)

redis_config = docker.create_host_config(privileged=False, cap_drop=['MKNOD'])
redis_container = cli.create_container(image='redis:latest', command='redis', name='redisserver', mem_limit='1g', detach=True, host_config=redis_config)

mongo_config = docker.create_host_config(privileged=False, cap_drop=['MKNOD'])
mongo_container = cli.create_container(image='mongo:latest', command='mongo', name='mongoserver', mem_limit='1g', detach=True, host_config=mongo_config)

# response = docer.start(container=redis_container.get('Id'))
# print('redis response: %s' % (response,))
# response = docer.start(container=mongo_container.get('Id'))
# print('mongo response: %s' % (response,))
