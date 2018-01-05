

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
VALUES('cliente00', 'kave', 'kave06@yahoo.es', 'cliente0pgpi', 1);
INSERT INTO users
VALUES('cliente01', 'rodrigo', 'rodrigo00@yahoo.es', 'cliente1pgpi', 1);
INSERT INTO users
VALUES('tecnico00', 'jose', 'tecnico00@yahoo.es', 'tecnico0pgpi', 2);
INSERT INTO users
VALUES('tecnico01', 'pepe', 'pepe01@yahoo.es', 'tecnico1pgpi', 2);
INSERT INTO users
VALUES('supervisor00', 'alberto', 'supervisor00@yahoo.es', 'supervisor0pgpi', 3);



insert into incidences(incidence_id,title,description,
	username,incidence_date,category,priority,
	technician_hours,resolve) 
values('INC_2018_0001','No enciende','Mi ordenador no enciende',
	'cliente00','2018-01-01 12:10:00',1,1,4,false);
insert into incidences values('INC_2018_0002','No funciona internet',
	'Mi ordenador no accede a internet',
	'cliente01','2018-01-01 13:10:00',3,1,5,true);
insert into incidences values('INC_2018_0003','incidencia cerrada tec00',
	'descripcion3','cliente00','2018-01-02 13:00:00', 2,3,8,false);
insert into incidences values('INC_2018_0004','incidencia abierta tec01',
	'descripcion4','cliente01','2018-01-02 14:00:00', 2,2,0,false);
insert into incidences values('INC_2018_0005','incidencia solicitada',
	'descripcion5','cliente00','2018-01-02 15:00:00', 4,1,0,false);

#1-abierta clie00
#2-cerrada tec01 clie01
#3-cerrada tec00 clie00
#4-abierta clie01
#5-solicitada clie00

insert into assigned_technicians
	values('INC_2018_0001','tecnico00');
insert into assigned_technicians
	values('INC_2018_0002','tecnico01');
insert into assigned_technicians
	values('INC_2018_0003','tecnico00');
insert into assigned_technicians
	values('INC_2018_0004','tecnico01');

insert into status
	values('INC_2018_0001','cliente00',1,'2018-01-01 12:10:00');
insert into status
	values('INC_2018_0001','supervisor00',2,'2018-01-01 13:00:00');
insert into status
	values('INC_2018_0001','tecnico00',4,'2018-01-02 14:00:00');
insert into status
	values('INC_2018_0001','tecnico00',5,'00-00-00 00:00:00');
#la incidencia 1 se encuentra en notificada resolucion


insert into status
	values('INC_2018_0002','cliente01',1,'2018-01-01 13:10:00');
insert into status
	values('INC_2018_0002','supervisor00',2,'2018-01-02 12:10:00');
insert into status
	values('INC_2018_0002','supervisor00',4,'2018-01-02 13:10:00');
insert into status
	values('INC_2018_0002','tecnico01',5,'2018-01-03 12:10:00');
insert into status
	values('INC_2018_0002','supervisor00',6,'2018-01-03 14:11:00');
#incidencia 2 cerrada, otro tecnico y otro usuario

insert into status
	values('INC_2018_0003','cliente00',1,'2018-01-02 13:00:00');
insert into status
	values('INC_2018_0003','supervisor00',2,'2018-01-02 13:15:00');
insert into status
	values('INC_2018_0003','tecnico00',4,'2018-01-03 12:10:00');
insert into status
	values('INC_2018_0003','tecnico00',5,'2018-01-03 15:10:00');
insert into status
	values('INC_2018_0003','supervisor00',6,'2018-01-04 12:11:00');
#inc3 cerrada tecnico 00 cliente 00

insert into status
	values('INC_2018_0004','cliente01',1,'2018-01-02 14:00:00');
insert into status
	values('INC_2018_0004','supervisor00',2,'2018-01-02 15:00:00');
insert into status
	values('INC_2018_0004','tecnico01',4,'0000-00-00 00:00:00');
#incidencia 4 abierta asignada a tecnico

insert into status
	values('INC_2018_0005','cliente00',1,'0000-00-00 00:00:00');
#incidencia 5 solicitada 

insert into assigned_devices
	values('INC_2018_0001',1);
insert into assigned_devices
	values('INC_2018_0001',3);
insert into assigned_devices
	values('INC_2018_0002',3);

insert into comments
	values(1,'INC_2018_0001','tecnico00',4,
	'La incidencia parece estar resuelta 
	al conectar el cable del ordenador');
insert into comments
	values(2,'INC_2018_0002','tecnico01',4,
	'La red estaba caida, ya esta activa');
