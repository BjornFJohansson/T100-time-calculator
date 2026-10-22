import numpy as np

CAL = {10: 1.4237, 50: 1.3500, 100: 1.2445}  

def etr(steps, cycles, vol):
    """steps: [(temp_C, seconds), ...] for one cycle. Returns total seconds."""
    temps, secs = zip(*steps)
    deg = sum(abs(a - b) for a, b in zip(temps, temps[1:] + temps[:1]))  
    speed = np.polyval(np.polyfit(list(CAL), list(CAL.values()), 1), vol) 
    return cycles * (sum(secs) + deg / speed)

if __name__ == "__main__":
    n = int(input("Steps per cycle: "))
    steps = [tuple(map(float, input(f"Step {i+1} (temp sec): ").split())) for i in range(n)]
    s = round(etr(steps, int(input("Cycles: ")), float(input("Volume (uL): "))))
    print(f"ETR: {s//3600:02d}:{s%3600//60:02d}:{s%60:02d}")
    
