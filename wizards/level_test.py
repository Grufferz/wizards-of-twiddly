
total = 0

tnl = 30

fac = 0.80

levels = 20

for level in range(levels):
    print("Level=" + str(level) + " total=" + str(int(total)) + " next level=" + str(int(tnl)))

    total += tnl
    tnl = tnl * (1 + pow(fac, level))