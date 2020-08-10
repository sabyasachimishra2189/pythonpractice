def multiplexers():
    return [lambda n: index * n for index in range(4)]


print([m(2) for m in multiplexers()])

#output=[6,6,6,6]

