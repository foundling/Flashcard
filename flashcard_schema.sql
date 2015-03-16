drop table if exists flashcards;
create table flashcards (
  id integer primary key autoincrement,
  front text not null,
  back text not null,
  views integer not null
);
