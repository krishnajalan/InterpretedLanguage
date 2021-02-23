import basic, signal, sys

def Exit(signal, frame):
    print("\nProgram terminated! ")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, Exit)
    while True:
        text = input("REPL > ").strip()
        if (text==''): continue
        result, error = basic.run('<stdin>', text)
        print(error.as_string() if error else result)

main()
