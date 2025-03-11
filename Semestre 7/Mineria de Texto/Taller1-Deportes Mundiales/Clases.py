from datetime import datetime

class Deportes:
    # atributos protegidos
    def __init__(self, nombre, descripcion, añoFundacion, nombreFundador):
        self.nombre = nombre
        self.descripcion = descripcion
        self.añoFundacion = añoFundacion
        self.nombreFundador = nombreFundador
    
    # retorna el nombre y descripción del Deporte
    def ConsultarDescripcionDeporte(self):
        return f"Nombre: {self.nombre}: {self.descripcion}"
     
    # recibe atributo Año de fundación y regresa la cantidad de años que fue fundado según la fecha actual.
    def consultarAñoFundacion(self):
        año_actual = datetime.now().year
        return f"Desde {self.añoFundacion} hasta {año_actual} hay {año_actual - self.añoFundacion} años"
    
    # recibe el nombre del fundador y lo retorna.
    def ConsultarFundador(self):
        return f"Nombre del fundador: {self.nombreFundador}"


class Atletismo(Deportes):
    def __init__(self, nombre, descripcion, añoFundacion, nombreFundador, NumPersonasPuedesCorrer):
        super().__init__(nombre, descripcion, añoFundacion, nombreFundador)
        self.NumPersonasPuedesCorrer = NumPersonasPuedesCorrer
    
    # sobreescribe el método de la clase papa Deportes y regresa “atletismo deporte estrella.”
    def ConsultarDescripcionDeporte(self):
        return "Atletismo deporte estrella."
    
    # recibe atributo Año de fundación y regresa la cantidad de años que fue fundado según la fecha actual.
    def ConsultarAñoFundacion(self):
        return super().consultarAñoFundacion()
    
    # recibe el nombre del Nombre del fundador y lo retorna.
    def ConsultarFundador(self):
        return super().ConsultarFundador()
    
    # recibe un año y regresa la cantidad de carreras por año.
    def ConsultaCarrerrasAno(self, año):
        carreras_por_año = {2020: 70, 2021: 120, 2022: 245}
        return carreras_por_año.get(año, "Año no encontrado")
        
    # recibe un entero OpcionAtletismo y retorna el nombre del tipo de atletismo.
    def ConsultarTiposAtletismo(self, OpcionAtletismo):
        tipos = {1: "fondo", 2: "Marcha", 3: "Velocidad", 4: "senderismo"}
        return tipos.get(OpcionAtletismo, "Opción no válida")
    
    # recibe la cantidad de espectadores y retorna un mensaje.
    def ConsultarEstadio(self, espectadores):
        if espectadores <= 50:
            return "no se puede implementar deportes con esa cantidad de espectadores"
        elif espectadores > 50 and espectadores <= 101:
            return "bienvenido al espectáculo"
    
    # recibe la cantidad de kilómetros por recorrer y retorna el tipo de corredor.
    def ConsultarTiposCorredores(self, kilómetrosPorRecorrer):
        if kilómetrosPorRecorrer == 8:
            return "Corredor amateur"
        elif kilómetrosPorRecorrer == 16:
            return "Corredor Senior"
        elif kilómetrosPorRecorrer == 24:
            return "Corredor Maratonista"
        elif kilómetrosPorRecorrer == 42:
            return "Corredor Ultraman"


class Futbol(Deportes):
    def __init__(self, nombre, descripcion, añoFundacion, nombreFundador):
        super().__init__(nombre, descripcion, añoFundacion, nombreFundador)
    
    def ConsultarDescripcionDeporte(self):
        return f"El {self.nombre} es {self.descripcion}."

# Ejemplo de uso
nuevoDeporte = Deportes("Baloncesto", "Deporte de equipo que se juega con una pelota y dos canastas.", 1891, "James Naismith")
print(nuevoDeporte.ConsultarDescripcionDeporte())
print(nuevoDeporte.consultarAñoFundacion())
print(nuevoDeporte.ConsultarFundador())

nuevoAtletismo = Atletismo("Atletismo", "Deporte que incluye diversas disciplinas como correr, saltar y lanzar.", 1776, "Desconocido", 8)
print(nuevoAtletismo.ConsultarDescripcionDeporte())
print(nuevoAtletismo.ConsultarAñoFundacion())
print(nuevoAtletismo.ConsultarFundador())
print(nuevoAtletismo.ConsultaCarrerrasAno(2021))
print(nuevoAtletismo.ConsultarTiposAtletismo(3))
print(nuevoAtletismo.ConsultarEstadio(100))
print(nuevoAtletismo.ConsultarTiposCorredores(42))

nuevoFutbol = Futbol("Fútbol", "Deporte de equipo jugado entre dos conjuntos de once jugadores cada uno.", 1863, "The Football Association")
print(nuevoFutbol.ConsultarDescripcionDeporte())

