import sys
import time

class loadingAnimation:
    def __init__(self, message, offset):
        
        timeout = time.time() + offset

        while time.time() < timeout:
            symbols="\|/-\|/-"
            for symbol in symbols:
                sys.stdout.write(f"\r{symbol} \t {message} \t {symbol}")
                sys.stdout.flush()
                time.sleep(0.1)
        
        print("\n")
    