from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from urllib.parse import urlparse, parse_qs

characters = {}

class Character:
    def __init__(self):
        self.name = None
        self.level = None
        self.role = None
        self.charisma = None
        self.strength = None
        self.dexterity = None

    

class CharacterBuilder:
    def __init__(self):
        self.character = Character()

    def set_name(self, name):
        self.character.name = name
    
    def set_level(self, level):
        self.character.level = level
    
    def set_role(self, role):
        self.character.role = role
        
    def set_charisma(self, charisma):
        self.character.charisma = charisma
    
    def set_strength(self, strength):
        self.character.strength = strength
    
    def set_dexterity(self, dexterity):
        self.character.dexterity = dexterity

    def get_character(self):
        return self.character


class Game:
    def __init__(self, builder):
        self.builder = builder

    def create_character(self, name, level, role, charisma, strength, dexterity):
        self.builder.set_name(name)
        self.builder.set_level(level)
        self.builder.set_role(role)
        self.builder.set_charisma(charisma)
        self.builder.set_strength(strength)
        self.builder.set_dexterity(dexterity)
        return self.builder.get_character()


# Aplicando el principio de responsabilidad única (S de SOLID)
class GameService:
    def __init__(self):
        self.builder = CharacterBuilder()
        self.game = Game(self.builder)

    def create_character(self, data):
        name = data.get("name", None)
        level = data.get("level", None)
        role = data.get("role", None)
        charisma = data.get("charisma", None)
        strength = data.get("strength", None)
        dexterity = data.get("dexterity", None)
        

        character = self.game.create_character(name, level, role, charisma, strength, dexterity)
        
        if characters:
            id=max(characters.keys())+1
        else:
            id=1
        
        characters[id] = character
        
        return character

    def read_characters(self):
        return {index: character.__dict__ for index, character in characters.items()}
    
    def filter_character(self, nombre1, tipo1, nombre2, tipo2):
        filter_characters={
            index: character.__dict__ for index, character in characters.items() if character.__dict__[f"{nombre1}"]==tipo1 and character.__dict__[f"{nombre2}"]==tipo2
        }
        if filter_characters:
            return filter_characters
        else:
            return None
        
        
        
        
    
    def read_character(self, id):
        for index in characters:
            character = characters[index]
            if index == id:
                return character 
        return None
    
    
    
    def update_character(self, id, data):
        for index in characters:
            character = characters[index]
            if index == id:
                name = data.get("name", None)
                level = data.get("level", None)
                role = data.get("role", None)
                charisma = data.get("charisma", None)
                strength = data.get("strength", None)
                dexterity = data.get("dexterity", None)
                
                if name:
                    character.name = name
                if level:
                    character.level = level
                if role:
                    character.role = role
                if charisma:
                    character.charisma = charisma
                if strength:
                    character.strength = strength
                if dexterity:
                    character.dexterity = dexterity
                    
                return character
        
        return None

    def delete_character(self, id):
        for index in characters:
            character = characters[index]
            if index == id:
                characters.pop(index)
                return character   
        return None


class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))
        

# Manejador de solicitudes HTTP
class GameHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = GameService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/characters":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.create_character(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if parsed_path.path == "/characters":
            response_data = self.controller.read_characters()
            HTTPDataHandler.handle_response(self, 200, response_data)
        elif "role" in query_params and "charisma" in query_params:
            role = query_params["role"][0]
            charisma = query_params["charisma"][0]
            response_data = self.controller.filter_character("role", role, "charisma", charisma)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 202, {"message": f"ningun character con tales parametros {role} and {charisma}"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/characters/"):
            id = int(self.path.split("/")[2])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.update_character(id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Índice de character no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/characters/"):
            id = int(self.path.split("/")[2])
            deleted_character = self.controller.delete_character(id)
            if deleted_character:
                HTTPDataHandler.handle_response(
                    self, 200, {"message": f"Character with id {id} has been deleted successfully"}
                )
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Id no valido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


def run(server_class=HTTPServer, handler_class=GameHandler, port=8000):
    try:
        server_address = ("", port)
        httpd = server_class(server_address, handler_class)
        print(f"Iniciando servidor HTTP en puerto {port}...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor...")
        httpd.socket.close()


if __name__ == "__main__":
    run()