#####################################################################
#
# author:  sheisc@163.com
#
#####################################################################

import requests

# "//i.xiao84.com/en-nce/1mp3-en/lesson1.mp3"
prefix = 'https://i.xiao84.com/en-nce/2mp3-en/Lesson '
#prefix = 'https://i.xiao84.com/en-nce/2mp3-en/Lesson%20'
#prefix = 'https://i.xiao84.com/en-nce/1mp3-en/lesson'
name = '01'
postfix = '.mp3'
target_dir = 'D:/NCE/'
#target_dir = 'D:/NCE1/'

i = 1
while i <= 3:
    name = "{:0>2d}".format(i)
    #name = "{0}".format(i)
    url = prefix + name + postfix
    print(url + " ...... ")
    response = requests.get(url)
    open(target_dir + name + postfix, 'wb').write(response.content)
    print(" done")
    i += 1







