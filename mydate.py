from datetime import datetime, timedelta

now = datetime.now()

def date_j():
    yest = now
    yest = (str(yest)[0:10])
    return yest
    return now_day

def date_j1():
    yest = now - timedelta(1)
    yest = (str(yest)[0:10])
    return yest

def date_j2():
    bf_yest = now - timedelta(2)
    bf_yest = (str(bf_yest)[0:10])
    return bf_yest

def date_j3():
    bf_yest = now - timedelta(3)
    bf_yest = (str(bf_yest)[0:10])
    return bf_yest

def hour_light():
    hour = (now.strftime("%H%M"))
    return hour

def dh_light():
    x= (now.strftime("%y%m%d_%H%M"))
    return x
