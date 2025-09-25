import network
import time

def conecta(ssid, senha):
    station = network.WLAN(network.STA_IF)
    if not station.isconnected():
        print("Ativando interface Wi-Fi...")
        station.active(True)
        print(f"Conectando à rede {ssid}...")
        station.connect(ssid, senha)

        for tentativa in range(50):
            if station.isconnected():
                break
            print(f"Tentativa {tentativa+1}/50...")
            time.sleep(0.1)

    if station.isconnected():
        print("Conexão estabelecida certinho!")
        print("Configuração de rede:", station.ifconfig())
    else:
        print("É irmão. Acho que o boleto não foi pago, porque não conectou.")

    return station
