-- Sprawdzanie czy członek należy do tego zespołu, który jest na polu namiotowmym
CREATE OR REPLACE FUNCTION check_same_team()
RETURNS TRIGGER AS $$
DECLARE 
    team_czlonek INTEGER;
    team_nocleg INTEGER;
    czlonek_team INTEGER;
BEGIN
    -- Get the team of the member
    SELECT INTO team_czlonek TEAM_ID FROM czlonkowie WHERE czlonek_ID = NEW.czlonek_ID;
    
    SELECT INTO czlonek_team czlonek_ID FROM nocleg_czlonkow WHERE nocleg_ID = NEW.nocleg_ID LIMIT 1;
    
    IF czlonek_team IS NULL THEN
        RETURN NEW;
    END IF;

    SELECT INTO team_nocleg TEAM_ID FROM czlonkowie WHERE czlonek_ID = czlonek_team;
    -- Check if the team of the member is the same as the team in the new record
    IF team_czlonek != team_nocleg THEN
        RAISE EXCEPTION 'Członek nie należy do tego zespołu.';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_team_before_insert_or_update
BEFORE INSERT OR UPDATE ON nocleg_czlonkow
FOR EACH ROW EXECUTE PROCEDURE check_same_team();


-- Sprawdzenie czy nie za dużo ludzi na polu namiotowym
CREATE OR REPLACE FUNCTION check_if_too_much_people()
RETURNS TRIGGER AS $$
DECLARE
    max_people INTEGER;
    current_people INTEGER;
    nocleg_id_get INTEGER;
BEGIN
    --GET MAX PEOPLE
    SELECT INTO nocleg_id_get numer_pola_namiotowego from nocleg WHERE nocleg_ID = NEW.nocleg_ID;
    SELECT INTO max_people ilosc_osob FROM pola_namiotowe WHERE pole_namiotowe_id = nocleg_id_get;
    SELECT into current_people COUNT(*) FROM nocleg_czlonkow WHERE nocleg_ID = NEW.nocleg_ID;

    IF current_people >= max_people THEN
        RAISE EXCEPTION 'Za dużo ludzi na polu namiotowym.';
    ELSE
        RETURN NEW;
    END IF;

END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_if_too_much_people
BEFORE INSERT OR UPDATE ON nocleg_czlonkow
FOR EACH ROW EXECUTE PROCEDURE check_if_too_much_people();
    
    