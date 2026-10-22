import warnings
from datetime import timedelta

# --- Calibração medida: volume (µL) -> velocidade de rampa (°C/s) ---
VOLUMES_CALIB = (10, 50, 100)
VELOCIDADES_CALIB = (1.4237, 1.3500, 1.2445)


def ajuste_linear(xs, ys):
    """Mínimos quadrados: devolve (declive, ordenada na origem)."""
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    declive = (sum((x - mx) * (y - my) for x, y in zip(xs, ys))
               / sum((x - mx) ** 2 for x in xs))
    return declive, my - declive * mx


DECLIVE, ORDENADA = ajuste_linear(VOLUMES_CALIB, VELOCIDADES_CALIB)


def ramp_speed_para_volume(volume):
    """Velocidade de rampa (°C/s) estimada para um dado volume (µL)."""
    if not (min(VOLUMES_CALIB) <= volume <= max(VOLUMES_CALIB)):
        warnings.warn(
            f"Volume {volume} µL fora do intervalo calibrado "
            f"({min(VOLUMES_CALIB)}-{max(VOLUMES_CALIB)} µL): "
            "valor extrapolado, usar com cuidado."
        )
    return DECLIVE * volume + ORDENADA


def T100_time(temperatures=(95, 55, 72),
              incubation_durations=(30, 30, 60),
              volume=50,
              cycles=69) -> timedelta:
    incubation_time = sum(incubation_durations) * cycles   # segundos
    ramp_speed = ramp_speed_para_volume(volume)            # °C/s

    # soma das variações de temperatura num ciclo (incluindo a volta ao início)
    t = temperatures
    steps = [abs(t[i] - t[i - 1]) for i in range(len(t))]
    ramp_time = sum(steps) * cycles / ramp_speed           # segundos

    total_time = incubation_time + ramp_time
    return timedelta(seconds=round(total_time))


def pedir_valor(texto, tipo, defeito):
    """Pergunta um valor; Enter sem escrever usa o valor por defeito."""
    while True:
        resposta = input(f"{texto} [{defeito}]: ").strip()
        if resposta == "":
            return defeito
        try:
            return tipo(resposta)
        except ValueError:
            print("  Valor inválido, tenta outra vez.")


def pedir_lista(texto, defeito):
    """Pergunta uma lista de números separados por vírgulas, ex: 95,55,72."""
    defeito_txt = ",".join(str(x) for x in defeito)
    while True:
        resposta = input(f"{texto} [{defeito_txt}]: ").strip()
        if resposta == "":
            return tuple(defeito)
        try:
            return tuple(float(x) for x in resposta.split(","))
        except ValueError:
            print("  Formato inválido. Usa números separados por vírgulas.")


if __name__ == "__main__":
    print("=== Calculadora de tempo T100 ===")
    temperaturas = pedir_lista("Temperaturas (°C)", (95, 55, 72))
    duracoes = pedir_lista("Durações de incubação (s)", (30, 30, 60))
    volume = pedir_valor("Volume (µL)", float, 50)
    ciclos = pedir_valor("Número de ciclos", int, 69)

    resultado = T100_time(temperatures=temperaturas,
                          incubation_durations=duracoes,
                          volume=volume,
                          cycles=ciclos)
    print(f"\nVelocidade de rampa usada: {ramp_speed_para_volume(volume):.4f} °C/s")
    print(f"Tempo total: {resultado}")
