from datetime import timedelta

a = 1.445852
b = -0.0020
volume = 20    
ciclos = 35    
preparacao = 500
descarregar = 180


# ramp speed (°C/s)
def ramp_speed(volume):
    return a + b * volume


# duração da PCR em segundos
def estimate_pcr(volume, ciclos):
    incubation = (30 + 30 + 60) * ciclos
    ramps = (40 + 17 + 23) * ciclos / ramp_speed(volume)
    return incubation + ramps


# tempo total de ocupação em minutos
def total_estimate_occupancy(volume, ciclos):
    pcr = estimate_pcr(volume, ciclos) 
    return preparacao + pcr + descarregar


def test_model():
    print("Ciclos | Volume | Esperado | Calculado")

    print(35, "|", 10, "|", "01:42:47", "|",
          timedelta(seconds=round(estimate_pcr(10, 35))))

    print(52, "|", 50, "|", "02:35:17", "|",
          timedelta(seconds=round(estimate_pcr(50, 52))))

    print(69, "|", 100, "|", "03:31:46", "|",
          timedelta(seconds=round(estimate_pcr(100, 69))))

print("Ramp speed:", round(ramp_speed(volume), 4), "°C/s")
print("Duração da PCR:", timedelta(seconds=round(estimate_pcr(volume, ciclos))))
print("Ocupação total:", timedelta(seconds=round(total_estimate_occupancy(volume, ciclos))))

test_model()