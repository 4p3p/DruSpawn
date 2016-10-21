create table componentes(id_proyecto text primary key, nombre text, tipo text, ref text);
create table core(id_core text primary key, hash text);
create table vulnerabilidades(id_vuln text primary key, id_proyecto text, version text, fecha text, nivel text, descripcion text, tipo text, solucion text, url text, foreign key(id_proyecto) references componentes(id_proyecto));
create table cve(id_cve text primary key, id_vuln text, url text, foreign key(id_vuln) references vulnerabilidades(id_vuln));