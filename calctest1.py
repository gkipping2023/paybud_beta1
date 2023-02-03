raw_time = '8:01'
(h,m) = raw_time.split(':')
hour = float(h)
min = float(m)
dec = min / 60
result = hour + dec
print (result)