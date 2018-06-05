from models import display


lines = [line.rstrip('\n') for line in open('settings.txt')]
for line in lines:
    if len(line) != 0:
        if line[0] != "#" :
            exec(line)




dapp = display.DisplayApp(1200, 675)
dapp.main()
