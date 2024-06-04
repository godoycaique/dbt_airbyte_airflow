from time import sleep

def primeira():
    print('primeira')
    sleep(2)

def segunda():
    print('segunda')
    sleep(2)

def terceira():
    print('terceira')
    sleep(2)


def pipeline():
    primeira()
    segunda()
    terceira()


pipeline()