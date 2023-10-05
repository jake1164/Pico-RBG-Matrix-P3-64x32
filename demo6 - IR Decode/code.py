import pulseio
import board
import adafruit_irremote

try:
    pulsein = pulseio.PulseIn(board.GP28, maxlen=120, idle_state=True)
    decoder = adafruit_irremote.GenericDecode()
except Exception as ex:
    print('boom!', ex)
    
while True:
    pulses = decoder.read_pulses(pulsein)
    print(f'Heard {len(pulses)} Pulses: {pulses}')
    
    try:
        code = decoder.decode_bits(pulses)
        print(f'Decoded: {code}')
        
    except adafruit_irremote.IRNECRepeatException:
        print('NEC repeat!')
    except adafruit_irremote.IRDecodeException as e:
        print('failed to decode: ', e.args)
              
              
    print('---------------------')