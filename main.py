# ============================================
#   Medidor de Temperatura - Raspberry Pi Pico
#   Sensor: DS18B20 (protocolo 1-Wire)
#   Simulador: Wokwi (wokwi.com)
# ============================================
#
# Conexao do sensor DS18B20:
#   - VCC  -> Pino 3.3V (pino 36)
#   - GND  -> Pino GND  (pino 38)
#   - DATA -> GP22      (pino 29)
#   - Resistor 4.7k ohm entre VCC e DATA
#
# ============================================

import machine
import onewire
import ds18x20
import time

# Pino de dados do sensor (GP22)
PINO_SENSOR = 22

# Intervalo entre leituras em segundos
INTERVALO = 2


def classificar_temperatura(temp):
    """Retorna uma descricao textual da temperatura."""
    if temp < 0:
        return "Abaixo de zero!"
    elif temp < 10:
        return "Muito frio"
    elif temp < 18:
        return "Frio"
    elif temp < 24:
        return "Confortavel"
    elif temp < 30:
        return "Morno"
    elif temp < 37:
        return "Quente"
    else:
        return "Muito quente!"


def main():
    print("===========================================")
    print("  Medidor de Temperatura - Pico + DS18B20  ")
    print("===========================================\n")

    # Configura o pino e o protocolo 1-Wire
    pino = machine.Pin(PINO_SENSOR)
    barramento = onewire.OneWire(pino)
    sensor = ds18x20.DS18X20(barramento)

    # Procura sensores conectados
    print("Procurando sensores...")
    sensores = sensor.scan()

    if not sensores:
        print("ERRO: Nenhum sensor DS18B20 encontrado!")
        print("Verifique as conexoes no simulador.")
        return

    print(f"Sensor encontrado! Total: {len(sensores)}\n")
    print(f"{'Leitura':<10} {'Temp (C)':<12} {'Condicao':<20}")
    print("-" * 42)

    leitura = 1

    while True:
        try:
            # Solicita a conversao de temperatura
            sensor.convert_temp()

            # Aguarda 750ms (tempo necessario para o DS18B20 converter)
            time.sleep_ms(750)

            # Le a temperatura do primeiro sensor encontrado
            temperatura = sensor.read_temp(sensores[0])

            condicao = classificar_temperatura(temperatura)
            print(f"#{leitura:<9} {temperatura:<12.2f} {condicao:<20}")

        except Exception as e:
            print(f"#{leitura:<9} {'ERRO':<12} {str(e):<20}")

        leitura += 1
        time.sleep(INTERVALO)


# Inicia o programa
main()
