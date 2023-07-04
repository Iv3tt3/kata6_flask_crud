CREATE TABLE "movements" (
	"id"	INTEGER,
	"Date"	TEXT NOT NULL,
	"Abstract"	TEXT NOT NULL,
	"Amount"	REAL NOT NULL,
	"Currency"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);