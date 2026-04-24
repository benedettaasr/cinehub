create table Movies(
	Id serial primary key,
	Name text not null,
	Year integer,
	LetterboxdURI text unique,
	Rating numeric(3,1) check(Rating between 0.5 and 5.0),
	Rewatch integer,
	WatchedDate date,
	TmdbId integer,
	Director text,
	Runtime integer,
	Genres text[],
	Overview text,
	PosterURL text
);

create index idx_movies_year on Movies(Year);
create index idx_movies_director on Movies(Director);
create index idx_movies_genres on Movies using GIN(Genres);