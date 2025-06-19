import sys
import ui

def main(args:list[str]):
    app = ui.Application(args) 
    app.run()

if __name__ == "__main__":
    main(sys.argv[1:])