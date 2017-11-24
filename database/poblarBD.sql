insert into prioridades values(1,'Muy alta');
insert into prioridades values(2,'Alta');
insert into prioridades values(3,'Media');
insert into prioridades values(4,'Baja');
insert into prioridades values(5,'Muy baja');


insert into estados values(1,'Solicitada');
insert into estados values(2,'Aceptada');
insert into estados values(3,'Rechazada');
insert into estados values(4,'Asignada');
insert into estados values(5,'Notivicada_resolucion');
insert into estados values(6,'Cerrada_resuelta');
insert into estados values(7,'Cerrada_no_resuelta');



insert into roles values(1,'cliente');
insert into roles values(2,'tecnico');
insert into roles values(3,'supervisor');

insert into dispositivos values(1,'ordenador de mesa');
insert into dispositivos values(2,'portatil');
insert into dispositivos values(3,'router');
insert into dispositivos values(4,'servidor');
insert into dispositivos values(5,'software');

insert into categorias values(1,'Hardware');
insert into categorias values(2,'Software básico');
insert into categorias values(3,'Problemas con aplicaciones');
insert into categorias values(4,'Software de aplicaciones');

INSERT INTO users
VALUES('kave', 'kave00', 'kave06@yahoo.es', '1234', 1);
INSERT INTO users
VALUES('jose', 'jose00', 'jose00@yahoo.es', '5678', 2);
INSERT INTO users
VALUES('alberto', 'alberto00', 'alberto00@yahoo.es', '9012', 3);

insert into incidencias(titulo,descripcion,
        id_dispositivo,
        fecha_incidencia,fecha_alta,
        usuario,categoria,estado)
values('No enciende','Mi ordenador no enciende',1,
        '2017-11-23 13:10:00','2017-11-23 13:15:00',
        'kave00',1,1);

insert into asignaciones
        values(1,'jose00');
insert into comentarios(id_incidencia,username,contenido)
        values(1,'jose00','La incidencia parece estar resuelta al conectar el cable del ordenador');


