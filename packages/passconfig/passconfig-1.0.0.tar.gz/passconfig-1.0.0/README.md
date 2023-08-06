# A Simple Username and Password Manager with ConfigParser

## Installation
```bash
pip install passconfig
```

## Basic Usage
```python
from passconfig import PassConfig

pc = PassConfig()
username, password = pc.get()
print(username, password)
# login or something with username and password
# save if right
# example:
# if login(username, password):
#     pc.save()
```


## Example with `imaplib`
```python
import imaplib
import passconfig

pc = passconfig.PassConfig(section='imap4')
username, password = pc.get()  # input at the first time

mail = imaplib.IMAP4_SSL('imap.exmail.qq.com')

res = mail.login(username, password)
if res[0] == 'OK':
    pc.save()
```