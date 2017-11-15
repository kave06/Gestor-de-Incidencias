

CREATE TABLE IF NOT EXISTS roles(
    role_id INT NOT NULL AUTO_INCREMENT,
    role_name VARCHAR(15),
    PRIMARY KEY (role_id)
);

CREATE TABLE IF NOT EXISTS users(
    user_id INT NOT NULL AUTO_INCREMENT,
    user_name VARCHAR(20),
    user_username VARCHAR(45),
    user_email VARCHAR(30),
    user_password VARCHAR(8),
    user_role INT,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_role) REFERENCES roles(role_id)
);

INSERT INTO roles (role_name) VALUES('cliente');
INSERT INTO roles (role_name) VALUES('tecnico');
INSERT INTO roles (role_name) VALUES('supervisor');

INSERT INTO users (user_name, user_username, user_email, user_password, user_role)
VALUES('kave', 'kave00', 'kave06@yahoo.es', '1234', 1);
INSERT INTO users (user_name, user_username, user_email, user_password, user_role)
VALUES('jose', 'jose00', 'jose00@yahoo.es', '5678', 2);
INSERT INTO users (user_name, user_username, user_email, user_password, user_role)
VALUES('alberto', 'alberto00', 'alberto00@yahoo.es', '9012', 3);



