"""
really bad and dirty code. should have named variables appropriately and made functions, but was rushing it so

crash course on using pwn to connect and send stuff
to connect:
p = remote('website.com', port number)

to read:
data = p.read()
(you can use readline but i found that it doesnt print the last line)

to send:
p.send() or p.sendline()

to close:
p.close()
i didnt add a close thing because the connection automatically closes after 10 secs

pwntools has many other functions such as crypto and hashes
using it to connect isnt the main one i think, so the documentation for it is really bad
an alternative to pwntools is socket but for this challenge it didnt send data. also its more complicated than pwntools
therefore i think pwntools > socket

the challenge was to connect and submit calculations and conversions. there's about 10 and you have to do it all under 10 secs
the first few ones were arithmetic (addition, subtraction, ...)
then there were conversions like binary to hexadecimal
fortunately they were always the same
i could make a detailed writeup with comments for the code for this challenge, but i think its too simple for one
here are the steps to solving this challenge:
1. connect and store the output into a variable (data in this case)
2. remove unnecessary stuff to isolate the number
3. identify what the problem is asking you to do by finding operators or words like "hexadecimal"
4. calculate it and send it
there was a lot of string manipulation and i used split, in, replace a lot
to convert from one base to another, you use hex(), oct(), or int()

it was a fun and easy challenge and i think y'all can easily get the flag too
code might look scary and complicated but thats because i didnt write it cleanly, not because challenge is hard
"""

from pwn import *
p = remote('pwn.ctf.unswsecurity.com', 5008) #connects
data = ''
banana = ['']
pear = []
while True: 
    data = str(p.read()) #reads the output and stores it in variable data
    print(data)
    if "What's " in data:
        cherry = data.replace("What's ", '')
        cherry = cherry.replace(' as an ASCII character? "', '')
        cherry = cherry.split('x')
        print(cherry[1])
        p.sendline(bytearray.fromhex(cherry[1]).decode())
    banana = data.split("What is ")
    if len(banana) == 2:
        apple = banana[1]
        apple = apple.replace('?', '')
        apple = apple.replace('"', '')
        apple = apple.replace("'", '')
        apple = apple.replace(' ', '')
        apple = apple.replace('in', '')
        if "+" in apple and not("octal" in apple):
            pear = apple.split('+')
            pineapple = int(pear[0]) + int(pear[1])
            p.sendline(str(pineapple))
        elif "-" in apple:
            pear = apple.split('-')
            pineapple = int(pear[0]) - int(pear[1])
            p.sendline(str(pineapple))
        elif "*" in apple:
            pear = apple.split('*')
            pineapple = int(pear[0]) * int(pear[1])
            p.sendline(str(pineapple))
        elif "%" in apple:
            pear = apple.split('%')
            pineapple = int(pear[0]) % int(pear[1])
            p.sendline(str(pineapple))
        elif "hexadecimal" in apple:
            apple = apple.replace('hexadecimal', '')
            grapes = apple.split('b')
            print(str(hex(int(grapes[1], 2))))
            p.sendline(str(hex(int(grapes[1], 2))))
        elif "decimal" in apple:
            apple = apple.replace('decimal', '')
            grapes = apple.split('x')
            p.sendline(str(int(grapes[1], 16)))
        elif "octal" in apple and not("+" in apple):
            apple = apple.replace('octal', '')
            grapes = apple.split('x')
            p.sendline(str(oct(int(grapes[1], 16))))
        elif "+" in apple and "octal" in apple:
            apple = apple.replace('octal', '')
            grapes = apple.split('+')
            print(grapes)
            grapes[0] = int(grapes[0], 16)
            grapes[1] = int(grapes[1], 2)
            summ = grapes[0] + grapes[1]
            p.sendline(str(oct(summ)))

