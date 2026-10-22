from datetime import timedelta

def T100_time(temperatures=(95, 55, 72),
              incubation_durations=(30, 30, 60),
              volume=10,
              cycles=35) -> timedelta:
    declive = (1.2445 - 1.4237) / (100 - 10)
    ordenada = 1.4237 - declive * 10
    ramp_speed = declive * volume + ordenada
    incubation= sum(incubation_durations)*cycles 
    graus = 2 * (max(temperatures) - min(temperatures))   
    ramp_time = graus * cycles / ramp_speed

    return timedelta(seconds=round(incubation + ramp_time))

print(T100_time(volume=10, cycles=35))