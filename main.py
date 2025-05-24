import sys
import database.models
import ui

def main(args:list[str]):
    database.models.make_database("database.sqlite")
    app = ui.Application(args) 
    app.run()

if __name__ == "__main__":
    main(sys.argv[1:])