create user test createdb password 'test';
-- create database test
-- 	with owner test;
-- comment on database test is 'default administrative connection database';
-- create schema projekt
create table if not exists test.projekt."user"
(
	id serial not null
		constraint projekt_user_pk
			primary key,
	name varchar(25),
	surename varchar(25),
	login varchar(25),
	password varchar(25),
	lastlogin date default now(),
	lastlogintime time default now()
);

alter table test.projekt."user" owner to test;

create unique index if not exists projekt_user_id_uindex
	on test.projekt."user" (id);

create table if not exists test.projekt.book
(
	id serial not null
		constraint projekt_text_pk
			primary key,
	user_id integer not null,
	name_of_the_book varchar(9999),
	"Author" varchar(100),
	edited_date date default CURRENT_TIMESTAMP
);

alter table test.projekt.book owner to test;

create unique index if not exists projekt_text_id_uindex
	on test.projekt.book (id);

create table if not exists test.projekt.book_chapter
(
	id serial not null
		constraint projekt_book_chapter_pk
			primary key,
	book_id integer,
	edited_date date default CURRENT_TIMESTAMP,
	chapter_id integer
);

alter table test.projekt.book_chapter owner to test;

create unique index if not exists projekt_book_chapter_id_uindex
	on test.projekt.book_chapter (id);

create table if not exists test.projekt.chapter
(
	id serial not null
		constraint chapter_pk
			primary key,
	chapter_name varchar(999),
	edited_date date default now()
);

alter table test.projekt.chapter owner to test;

create unique index if not exists chapter_id_uindex
	on test.projekt.chapter (id);

create table if not exists test.projekt.subject
(
	id serial not null
		constraint subject_pk
			primary key,
	subject varchar(99),
	teacher varchar(99),
	method_of_course_completion varchar(99),
	edited_date date default now()
);

alter table test.projekt.subject owner to test;

create unique index if not exists subject_id_uindex
	on test.projekt.subject (id);

create table if not exists test.projekt.user_subject
(
	id serial not null
		constraint user_subject_pk
			primary key,
	user_id integer,
	subject_id integer,
	attendance_actual integer default 0,
	attendance_max integer default 15,
	grade integer,
	edited_date date default now()
);

alter table test.projekt.user_subject owner to test;

create unique index if not exists user_subject_id_uindex
	on test.projekt.user_subject (id);



