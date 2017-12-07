

insert into priorities values(1,'Muy baja');
insert into priorities values(2,'Baja');
insert into priorities values(3,'Media');
insert into priorities values(4,'Alta');
insert into priorities values(5,'Muy Alta');


insert into type_of_status values(1,'Solicitada');
insert into type_of_status values(2,'Aceptada');
insert into type_of_status values(3,'Rechazada');
insert into type_of_status values(4,'Asignada');
insert into type_of_status values(5,'Notificada_resolucion');
insert into type_of_status values(6,'Cerrada');



insert into roles values(1,'cliente');
insert into roles values(2,'tecnico');
insert into roles values(3,'supervisor');

insert into devices values(1,'ordenador de mesa');
insert into devices values(2,'portatil');
insert into devices values(3,'router');
insert into devices values(4,'servidor');
insert into devices values(5,'software');

insert into categories values(1,'Hardware');
insert into categories values(2,'Software básico');
insert into categories values(3,'Problemas con aplicaciones');
insert into categories values(4,'Software de aplicaciones');

INSERT INTO users
VALUES('kave', 'kave00', 'kave06@yahoo.es', '1234', 1);
INSERT INTO users 
VALUES('rodrigo', 'rodrigo00', 'rodrigo00@yahoo.es', '1234', 1);
INSERT INTO users
VALUES('jose', 'jose00', 'jose00@yahoo.es', '1234', 2);
INSERT INTO users 
VALUES('alberto', 'alberto00', 'alberto00@yahoo.es', '1234', 3);



insert into incidences(incidence_id,title,description,
	username,incidence_date,category_id,priority_id,
	technician_hours,resolve) 
values('INC_2017_0001','No enciende','Mi ordenador no enciende',
	'kave00','2017-11-23 13:10:00',1,1,0,false);

insert into assigned_technicians
	values(1,'jose00');

insert into status
	values('INC_2017_0001','kave00',1,'2017-11-23 13:10:00');
insert into status
	values('INC_2017_0001','alberto00',2,'2017-11-30 12:00:00');
insert into status
	values('INC_2017_0001','jose00',4,'2017-12-01 12:00:00');
#la incidencia se encuentra en notificada resolucion


insert into assigned_devices
	values('INC_2017_0001',1);
insert into assigned_devices
	values('INC_2017_0001',3);

insert into comments
	values(1,'INC_2017_0001','jose00',4,'La incidence parece estar resuelta al conectar el cable del ordenador');

insert into notifications
	values(1,'INC_2017_0001','jose00','alberto00',
	5,'Ya esta solucionada',false);


