#creacion de tablas

CREATE TABLE IF NOT EXISTS prioridades(
  id_prioridad INT NOT NULL,
  nombre_prioridad VARCHAR(15),
  PRIMARY KEY (id_prioridad)
);

CREATE TABLE IF NOT EXISTS estados(
  id_estado INT NOT NULL,
  nombre_estado VARCHAR(25),
  PRIMARY KEY (id_estado)
);
CREATE TABLE IF NOT EXISTS roles(
  role_id INT NOT NULL,
  role_name VARCHAR(10),
  PRIMARY KEY (role_id)
);
CREATE TABLE IF NOT EXISTS dispositivos(
  id_dispositivo INT NOT NULL,
  descripcion VARCHAR(15),
  PRIMARY KEY (id_dispositivo)
);
CREATE TABLE IF NOT EXISTS categorias(
  id_categoria INT NOT NULL,
  nombre_categoria VARCHAR(30),
  PRIMARY KEY (id_categoria)
);
CREATE TABLE IF NOT EXISTS users(
  user_name VARCHAR(15),
  user_username VARCHAR(15) NOT NULL,
  user_email VARCHAR(20),
  user_password VARCHAR(15),
  user_role INT NOT NULL,
  PRIMARY KEY (user_username),
  FOREIGN KEY (user_role) REFERENCES roles(role_id)
);
CREATE TABLE IF NOT EXISTS incidencias(
  id_incidencia           INT NOT NULL AUTO_INCREMENT,
  titulo                  VARCHAR(15),
  descripcion             VARCHAR(256),
  id_dispositivo          INT,
  fecha_incidencia        DATETIME NOT NULL,
  fecha_alta              DATETIME NOT NULL,
  fecha_asignacion        DATETIME,
  fecha_cierre_solicitado DATETIME,
  fecha_cierre            DATETIME,
  username                 VARCHAR(15),
  categoria               INT,
  estado                  INT,
  prioridad               INT,
  PRIMARY KEY (id_incidencia),
  FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id_dispositivo),
  FOREIGN KEY (usuario) REFERENCES users(user_username),
  FOREIGN KEY (categoria) REFERENCES categorias(id_categoria),
  FOREIGN KEY (estado) REFERENCES estados(id_estado),
  FOREIGN KEY (prioridad) REFERENCES prioridades(id_prioridad)
);
CREATE TABLE IF NOT EXISTS asignaciones(
  id_incidencia INT NOT NULL,
  username VARCHAR(10) NOT NULL,
  PRIMARY KEY (id_incidencia,username),
  FOREIGN KEY (id_incidencia) REFERENCES incidencias(id_incidencia),
  FOREIGN KEY (username) REFERENCES users(user_username)
);
CREATE TABLE IF NOT EXISTS comentarios(
  id_comentario INT NOT NULL AUTO_INCREMENT,
  id_incidencia INT NOT NULL,
  username VARCHAR(10) NOT NULL,
  contenido VARCHAR(255),
  PRIMARY KEY (id_comentario,id_incidencia,username),
  FOREIGN KEY (id_incidencia) REFERENCES incidencias(id_incidencia),
  FOREIGN KEY (username) REFERENCES users(user_username)
);


