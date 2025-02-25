CREATE DATABASE IF NOT EXISTS UF_Athletics_Databank;

USE UF_Athletics_Databank;

CREATE TABLE IF NOT EXISTS Athletes (
    athlete_uuid BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth DATE,
    year_of_birth YEAR,
    home_state TEXT,
    home_town TEXT,
    high_school TEXT,
    is_current BOOLEAN,
    PRIMARY KEY (athlete_uuid)
);

CREATE TABLE IF NOT EXISTS Consent (
    record_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    athlete_uuid BIGINT UNSIGNED NOT NULL,
    is_consented BOOLEAN NOT NULL,
    PRIMARY KEY (record_id),
    FOREIGN KEY (athlete_uuid) REFERENCES Athletes(athlete_uuid)
);

CREATE TABLE IF NOT EXISTS Athlete_Metadata (
    record_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    athlete_uuid BIGINT UNSIGNED NOT NULL,
    date_uploaded DATE,
    record_type TEXT,
    record_value BLOB,
    PRIMARY KEY (record_id),
    FOREIGN KEY (athlete_uuid) REFERENCES Athletes(athlete_uuid)
);

CREATE TABLE IF NOT EXISTS Seasons (
    season_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    season_year YEAR,
    sport TEXT,
    PRIMARY KEY (season_id)
);

CREATE TABLE IF NOT EXISTS Teams (
    team_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    sport TEXT,
    sex TEXT,
    PRIMARY KEY (team_id)
);

CREATE TABLE IF NOT EXISTS Athlete_Seasons (
    athlete_season_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    athlete_uuid BIGINT UNSIGNED NOT NULL,
    season_id BIGINT UNSIGNED NOT NULL,
    team_id BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (athlete_season_id),
    FOREIGN KEY (athlete_uuid) REFERENCES Athletes(athlete_uuid),
    FOREIGN KEY (season_id) REFERENCES Seasons(season_id),
    FOREIGN KEY (team_id) REFERENCES Teams(team_id)
);

CREATE TABLE IF NOT EXISTS Modalities (
    modality_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    company TEXT,
    model TEXT,
    PRIMARY KEY (modality_id)
);

CREATE TABLE IF NOT EXISTS Tests (
    test_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    modality_id BIGINT UNSIGNED NOT NULL,
    athlete_uuid BIGINT UNSIGNED NOT NULL,
    team_id BIGINT UNSIGNED NOT NULL,
    start_unix BIGINT UNSIGNED,
    end_unix BIGINT UNSIGNED,
    date_uploaded DATE,
    test_type TEXT,
    PRIMARY KEY (test_id),
    FOREIGN KEY (modality_id) REFERENCES Modalities(modality_id),
    FOREIGN KEY (athlete_uuid) REFERENCES Athletes(athlete_uuid),
    FOREIGN KEY (team_id) REFERENCES Teams(team_id)
);

CREATE TABLE IF NOT EXISTS Test_Results (
    test_results_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    test_id BIGINT UNSIGNED NOT NULL,
    result BLOB,
    is_raw BOOLEAN,
    PRIMARY KEY (test_results_id),
    FOREIGN KEY (test_id) REFERENCES Tests(test_id)
);

CREATE TABLE IF NOT EXISTS Events (
    event_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    team_id BIGINT UNSIGNED NOT NULL,
    event_type TEXT,
    opponent TEXT,
    start_unix BIGINT UNSIGNED,
    end_unix BIGINT UNSIGNED,
    team_result TEXT,
    PRIMARY KEY (event_id),
    FOREIGN KEY (team_id) REFERENCES Teams(team_id)
);

CREATE TABLE IF NOT EXISTS Performances (
    performance_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    event_id BIGINT UNSIGNED NOT NULL,
    athlete_uuid BIGINT UNSIGNED NOT NULL,
    athlete_opponent TEXT,
    start_unix BIGINT UNSIGNED,
    end_unix BIGINT UNSIGNED,
    result TEXT,
    PRIMARY KEY (performance_id),
    FOREIGN KEY (event_id) REFERENCES Events(event_id),
    FOREIGN KEY (athlete_uuid) REFERENCES Athletes(athlete_uuid)
);

CREATE TABLE IF NOT EXISTS Performance_Results (
    performance_result_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    performance_id BIGINT UNSIGNED NOT NULL,
    modality_id BIGINT UNSIGNED NOT NULL,
    result BLOB,
    is_raw BOOLEAN,
    PRIMARY KEY (performance_result_id),
    FOREIGN KEY (performance_id) REFERENCES Performances(performance_id),
    FOREIGN KEY (modality_id) REFERENCES Modalities(modality_id)
);
