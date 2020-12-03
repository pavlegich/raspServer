import requests
from requests.exceptions import HTTPError
from lxml import html
import time

addr = 'http://192.168.1.102:5000'
user1 = 'admin'
user2 = 'receive'
passw = 'admin'
message = "Hello! Let's do the shopping tomorrow at 5 p.m. I will call you! See you there."

session = requests.Session()

login = session.post(addr+'/', {'username' : user1, 'password' : passw})


t1 = time.time()

manual_drive = session.get(addr+'/latest_image')

t2 = time.time()

print(t2 - t1)

# for url in [addr]:
#     try:
#         response = requests.get(url)
        
#         response.raise_for_status()
#     except HTTPError as http_err:
#         print(f'HTTP error occurred: {http_err}')
#     except Exception as err:
#         print(f'Other error occurred: {err}') 
#     else:
#         print('Server is working...\n')

# session = requests.Session()
# #REGISTER USER1
# register1 = session.post(addr+'/register', {'user' : user1, 'password' : passw})
# if register1.status_code == 200:
# 	print('User {} was created!'.format(user1.upper()))
# #REGISTER USER2
# register2 = session.post(addr+'/register', {'user' : user2, 'password' : passw})
# if register2.status_code == 200:
# 	print('User {} was created!'.format(user2.upper()))
# #LOGIN THE FIRST USER
# login1 = session.post(addr+'/login', {'nm' : user1, 'ps' : passw})
# if login1.status_code == 200:
# 	print('\nLogin as {}...'.format(user1.upper()))
# #SEND MESSAGE
# session.post(addr+'/list', {'receiver' : user2})
# send = session.post(addr+'/send', {'message' : message})
# if send.status_code == 200:
# 	print('Message was sent to {}.'.format(user2.upper()))
# #LOGOUT
# logout = session.get(addr+'/logout')
# if logout.status_code == 200:
# 	print('\nYou have been logged out!')
# #LOGIN AS ANOTHER USER
# login2 = session.post(addr+'/login', {'nm' : user2, 'ps' : passw})
# if login2.status_code == 200:
# 	print('\nLogin as {}...'.format(user2.upper()))
# #CHECK RECEIVED MESSAGES
# received = session.get(addr+'/received')
# tree = html.fromstring(received.text)
# msg = tree.xpath('//p[@class = "msg"]') # все p теги
# print("Received messages:")
# i = 1
# for item in msg:
# 	print(str(i)+' - <'+item.text+'>')
# 	i+=1