create table contributed(nombre text primary key, tipo text, url text);
create table core(id_core text primary key, hash text);
create table vulns(id_vuln text primary key, proyecto text, version text, fecha text, nivel text, descripcion text, solucion text, url text);
create table cve(id_cve text primary key, id_vuln text, url text);