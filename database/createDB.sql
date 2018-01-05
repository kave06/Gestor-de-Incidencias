#creacion de tablas



CREATE TABLE IF NOT EXISTS type_of_status(
  status_id INT,
  status_name VARCHAR(25),
  PRIMARY KEY (status_id)

);
CREATE TABLE IF NOT EXISTS roles(
  role_id INT NOT NULL,
  role_name VARCHAR(10),
  PRIMARY KEY (role_id)
);
CREATE TABLE IF NOT EXISTS devices(
  device_id INT NOT NULL,
  description VARCHAR(30),
  PRIMARY KEY (device_id)
);
CREATE TABLE IF NOT EXISTS categories(
  category_id INT NOT NULL,
  category_name VARCHAR(30),
  PRIMARY KEY (category_id)
);
CREATE TABLE IF NOT EXISTS priorities(
  priority_id INT NOT NULL,
  priority_name VARCHAR(15),
  PRIMARY KEY (priority_id)
);
CREATE TABLE IF NOT EXISTS users(
  username_id VARCHAR(20) NOT NULL,
  name VARCHAR(20),
  email VARCHAR(20),
  password VARCHAR(20),
  role_id INT NOT NULL,
  PRIMARY KEY (username_id),
  FOREIGN KEY (role_id) REFERENCES roles(role_id)
);
CREATE TABLE IF NOT EXISTS incidences(
  incidence_id           VARCHAR(15) NOT NULL,
  title		 	 VARCHAR(30),
  description            VARCHAR(500),
  username 	         VARCHAR(20),
  incidence_date         DATETIME NOT NULL,
  category               INT,
  priority               INT,
  technician_hours	 INT,
  resolve		 BOOLEAN,
  PRIMARY KEY (incidence_id),
  FOREIGN KEY (username) REFERENCES users(username_id),
  FOREIGN KEY (category) REFERENCES categories(category_id),
  FOREIGN KEY (priority) REFERENCES priorities(priority_id)
);
CREATE TABLE IF NOT EXISTS assigned_technicians(
  incidence_id VARCHAR(15) NOT NULL,
  technician_id               VARCHAR(20),
  PRIMARY KEY (incidence_id,technician_id),
  FOREIGN KEY (incidence_id) REFERENCES incidences(incidence_id),
  FOREIGN KEY (technician_id) REFERENCES users(username_id)
);
CREATE TABLE IF NOT EXISTS assigned_devices(
  incidence_id VARCHAR(15) NOT NULL,
  device_id INT NOT NULL,
  PRIMARY KEY (incidence_id,device_id),
  FOREIGN KEY (incidence_id) REFERENCES incidences(incidence_id),
  FOREIGN KEY (device_id) REFERENCES devices(device_id)
);
CREATE TABLE IF NOT EXISTS comments(
  comment_id INT NOT NULL AUTO_INCREMENT,
  incidence_id VARCHAR(15) NOT NULL,
  username VARCHAR(20) NOT NULL,
  status  INT NOT NULL,
  content VARCHAR(255),
  PRIMARY KEY (comment_id),
  FOREIGN KEY (incidence_id) REFERENCES incidences(incidence_id),
  FOREIGN KEY (username) REFERENCES users(username_id),
  FOREIGN KEY (status) REFERENCES type_of_status(status_id)
);

CREATE TABLE IF NOT EXISTS status(
  incidence_id VARCHAR(15),
  username VARCHAR(20),
  status_id INT NOT NULL,
  end_date DATETIME,
  PRIMARY KEY (status_id,incidence_id,username),
  FOREIGN KEY (incidence_id) REFERENCES incidences(incidence_id),
  FOREIGN KEY (username) REFERENCES users(username_id),
  FOREIGN KEY (status_id) REFERENCES type_of_status(status_id)
);



