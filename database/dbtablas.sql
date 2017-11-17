CREATE TABLE IF NOT EXISTS Incidencia (
  id_incidencia                    VARCHAR(10) NOT NULL,
  descripcion             VARCHAR(10),
  id_dispositivo          VARCHAR(10),
  fecha_incidencia        DATE,
  fecha_alta              DATE,
  fecha_asignacion        DATE,
  fecha_cierre_solicitado DATE,
  fecha_cierre            DATE,
  usuario                 VARCHAR(10),
  categoria               INT,
  estado                  INT,
  prioridad               INT,
  PRIMARY KEY (id_incidencia),
  FOREIGN KEY (id_dispositivo) REFERENCES Dispositivo(id_dispositivo),
  FOREIGN KEY (usuario) REFERENCES Usuario(id_usuario),
  FOREIGN KEY (categoria) REFERENCES Categoria(id_categoria),
  FOREIGN KEY (estado) REFERENCES Estado(id_estado),
  FOREIGN KEY (prioridad) REFERENCES Prioridad(id_prioridad)
);
CREATE TABLE IF NOT EXISTS Prioridad(
  id_prioridad INT NOT NULL,
  nombre_prioridad VARCHAR(10),
  PRIMARY KEY (id_prioridad)
);
CREATE TABLE IF NOT EXISTS Estado(
  id_estado INT NOT NULL,
  nombre_estado VARCHAR(25),
  PRIMARY KEY (id_estado)
);
CREATE TABLE IF NOT EXISTS Asignacion(
  id_incidencia VARCHAR(10) NOT NULL,
  id_usuario VARCHAR(10) NOT NULL,
  PRIMARY KEY (id_incidencia,id_usuario),
  FOREIGN KEY (id_incidencia) REFERENCES Incidencia(id_incidencia),
  FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);
CREATE TABLE IF NOT EXISTS Usuario(
  id_usuario VARCHAR(10) NOT NULL,
  passwd VARCHAR(10),
  nombre VARCHAR(10),
  rol INT NOT NULL,
  PRIMARY KEY (id_usuario),
  FOREIGN KEY (rol) REFERENCES Rol(id_rol)
);
CREATE TABLE IF NOT EXISTS Dispositivo(
  id_dispositivo VARCHAR(10) NOT NULL,
  descripcion VARCHAR(10),
  PRIMARY KEY (id_dispositivo)
);
CREATE TABLE IF NOT EXISTS Categoria(
  id_categoria INT NOT NULL,
  nombre_categoria VARCHAR(30),
  PRIMARY KEY (id_categoria)
);
CREATE TABLE IF NOT EXISTS Rol(
  id_rol INT NOT NULL,
  nombre_rol VARCHAR(10),
  PRIMARY KEY (id_rol)
);
CREATE TABLE IF NOT EXISTS Comentario(
  id_comentario INT NOT NULL,
  id_usuario VARCHAR(10) NOT NULL,
  id_incidencia VARCHAR(10) NOT NULL,
  contenido VARCHAR(255),
  PRIMARY KEY (id_comentario,id_incidencia,id_usuario),
  FOREIGN KEY (id_incidencia) REFERENCES Incidencia(id_incidencia),
  FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);