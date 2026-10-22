from datetime import timedelta

def T100_time(temperatures=(95, 55, 72),
              incubation_durations=(30, 30, 60),
              volume=50,
              cycles=69) -> timedelta:
    #references values 10uL=1,4237ºC/s
    slope=(1.2445-1.4237)/(100-10)
    ramp_speed=1.4237+ slope*(volume-10)
    incubation_time=sum(incubation_durations)*cycles
    ramp_time=(abs(temperatures[0]-temperatures[1])+abs(temperatures[-1]-temperatures[1])+abs(temperatures[0]-temperatures[-1]))*cycles/ramp_speed
    return timedelta(seconds=incubation_time + ramp_time)

print(T100_time())
