from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

# En esta parate se muestra el Pilar de "ABSTRACCIÓN"
class Item(ABC):
    def __init__(self, titulo: str, id: str):
        self.titulo = titulo
        self.id = id
        self.prestado = False
        self.fecha_prestamo: Optional[datetime] = None
        self.usuario_prestado: Optional[str] = None

# En esta parte podremso observar el Pilar de "POLIMORFISMO"
    @abstractmethod
    def prestar(self, usuario_id: str) -> bool:
        pass

    def devolver(self) -> bool:
        if self.prestado:
            self.prestado = False
            self.fecha_prestamo = None
            self.usuario_prestado = None
            return True
        return False

# En esta parte podremos ver el Pilar de "HERENCIA"
class Libro(Item):
    def __init__(self, titulo: str, autor: str, isbn: str):
        super().__init__(titulo, isbn)  
        self.edicion: Optional[str] = None
        self.anio_publicacion: Optional[int] = None

    def prestar(self, usuario_id: str) -> bool:
        if not self.prestado:
            self.prestado = True
            self.fecha_prestamo = datetime.now()
            self.usuario_prestado = usuario_id
            return True
        return False

class Revista(Item):
    def __init__(self, titulo: str, issn: str):
        super().__init__(titulo, issn)  
        self.numero: Optional[int] = None
        self.periodicidad: Optional[str] = None

    def prestar(self, usuario_id: str) -> bool:
        if not self.prestado:
            self.prestado = True
            self.fecha_prestamo = datetime.now()
            self.usuario_prestado = usuario_id
            return True
        return False

# En esta parte esta el Pilar "ENCAPSULAMIENTO"
class Usuario:
    def __init__(self, nombre: str, id_usuario: str):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.items_prestados: List[Item] = []  
        self.historial_prestamos: List[dict] = [] 

    def prestar_item(self, item: Item) -> bool:
        if len(self.items_prestados) < 3:  
            if item.prestar(self.id_usuario):
                self.items_prestados.append(item)
                self.historial_prestamos.append({
                    'item': item.titulo,
                    'fecha_prestamo': datetime.now(),
                    'id_item': item.id
                })
                return True
        return False

    def devolver_item(self, item: Item) -> bool:
        if item in self.items_prestados:
            if item.devolver():
                self.items_prestados.remove(item)
                return True
        return False

class Biblioteca:
    def __init__(self):
        self.items: List[Item] = []  
        self.usuarios: List[Usuario] = []  

    def agregar_item(self, item: Item) -> None:
        self.items.append(item)

    def registrar_usuario(self, usuario: Usuario) -> None:
        self.usuarios.append(usuario)

    def buscar_item(self, id_item: str) -> Optional[Item]:
        for item in self.items:
            if item.id == id_item:
                return item
        return None

    def buscar_usuario(self, id_usuario: str) -> Optional[Usuario]:
        for usuario in self.usuarios:
            if usuario.id_usuario == id_usuario:
                return usuario
        return None

    # En esta parte se muestra el Pilar de "POLIMORFISMO"
    def prestar_item(self, id_item: str, id_usuario: str) -> bool:
        item = self.buscar_item(id_item)
        usuario = self.buscar_usuario(id_usuario)
        
        if item and usuario:
            if usuario.prestar_item(item):
                print(f"Item '{item.titulo}' prestado a {usuario.nombre}")
                return True
            else:
                print("No se pudo prestar el item")
        else:
            print("Item o usuario no encontrado")
        return False

    def devolver_item(self, id_item: str, id_usuario: str) -> bool:
        item = self.buscar_item(id_item)
        usuario = self.buscar_usuario(id_usuario)
        
        if item and usuario:
            if usuario.devolver_item(item):
                print(f"Item '{item.titulo}' devuelto por {usuario.nombre}")
                return True
            else:
                print("No se pudo devolver el item")
        else:
            print("Item o usuario no encontrado")
        return False

    def listar_items_prestados(self) -> None:
        print("\nItems prestados:")
        for item in self.items:
            if item.prestado:
                print(f"- {item.titulo} (Prestado a: {item.usuario_prestado})")

    def listar_usuarios_con_prestamos(self) -> None:
        print("\nUsuarios con préstamos:")
        for usuario in self.usuarios:
            if usuario.items_prestados:
                print(f"\n{usuario.nombre}:")
                for item in usuario.items_prestados:
                    print(f"- {item.titulo}")
