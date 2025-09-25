# THOMAZ JULIANN BONCOMPAGNI - Análise e Desenvolvimento de Sistemas - Internet das Coisas - 25/09/2025

import dht              # lib do sensor DHT11 (pega temp e umidade)
import machine          # lib para controlar pinos da ESP32
import urequests        # lib pra mandar os dados pela internet
import time             # temporizador, para controlar tempo de delay
import wifi_lib         # a lib que eu criei pra conectar no Wi-Fi

# primeiro de tudo: conecta no Wi-Fi
# se não tiver internet, não tem como mandar nada pro ThingSpeak
wifi_lib.conecta("FAMILIA_BUSCAPE", "Peganois2024!@") #já troquei a senha!

# configurando o sensor DHT11 no pino 4 da ESP32
sensor = dht.DHT11(machine.Pin(4))

# configurando o relé no pino 17
# começo deixando ele desligado (valor 0)
RELE_PIN = machine.Pin(17, machine.Pin.OUT)
RELE_PIN.value(0)

# função que manda os dados pro ThingSpeak
# basicamente monta a URL com os valores e faz um GET
def thingspeak(temperatura, umidade, rele_estado):
    try:
        url = "https://api.thingspeak.com/update?api_key=FX5LBL6NHHYQP35Q&field1={}&field2={}&field3={}".format(
            temperatura, umidade, rele_estado
        )
        response = urequests.get(url)   # manda os dados
        response.close()                # fecha a conexão pra não pesar
        print("Dados enviados pro ThingSpeak: Temp={}°C, Umidade={}%, Relé={}".format(
            temperatura, umidade, rele_estado
        ))
    except Exception as e:
        print("Deu ruim ao enviar os dados:", e)

# aqui eu crio a lógica de quando o relé liga ou desliga
# se passar de 31°C ou umidade maior que 70% -> liga o relé
def verificar_condicoes(temperatura, umidade):
    if temperatura > 31 or umidade > 70:
        RELE_PIN.value(1)  # liga
        print("Relé ligado!")
        return 1
    else:
        RELE_PIN.value(0)  # desliga
        print("Relé desligado.")
        return 0

# loop principal: fica rodando pra sempre
while True:
    try:
        sensor.measure()                # faz a leitura
        temperatura = sensor.temperature()
        umidade = sensor.humidity()
        
        # mostra no terminal só pra acompanhar
        print("Temperatura: {}°C, Umidade: {}%".format(temperatura, umidade))
        
        # checa se precisa ligar/desligar o relé
        rele_estado = verificar_condicoes(temperatura, umidade)
        
        # manda pro ThingSpeak
        thingspeak(temperatura, umidade, rele_estado)
        
    except OSError as e:
        # se o sensor der erro de leitura, mostra aqui
        print("Erro ao ler o sensor:", e)
    
    time.sleep(2)  # espera 2 segs e repete tudo de novo
