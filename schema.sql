DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS beverages;

CREATE TABLE locations (
    locationId INTEGER PRIMARY KEY AUTOINCREMENT,
    locationCreated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    locationName TEXT NOT NULL COLLATE NOCASE
);

CREATE TABLE beverages (
    beverageId INTEGER PRIMARY KEY AUTOINCREMENT,
    beverageCreated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    beverageName TEXT NOT NULL COLLATE NOCASE,
    beverageLocationId INTEGER,
    beverageYear DATE,
    beveragePurchaseDate DATE,
    beverageDrinkBefore DATE,
    beverageNotes TEXT
);