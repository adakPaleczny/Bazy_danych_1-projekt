-- Sprawdzanie czy członek należy do tego zespołu, który jest na polu namiotowmym
CREATE OR REPLACE FUNCTION check_same_team()
RETURNS TRIGGER AS $$
DECLARE 
    team_czlonek INTEGER;
    team_nocleg INTEGER;
    czlonek_team INTEGER;
BEGIN
    -- Get the team of the member
    SELECT INTO team_czlonek TEAM_ID FROM projekt.czlonkowie WHERE czlonek_ID = NEW.czlonek_ID;
    
    SELECT INTO czlonek_team czlonek_ID FROM projekt.nocleg_czlonkow WHERE nocleg_ID = NEW.nocleg_ID LIMIT 1;
    
    IF czlonek_team IS NULL THEN
        RETURN NEW;
    END IF;

    SELECT INTO team_nocleg TEAM_ID FROM projekt.czlonkowie WHERE czlonek_ID = czlonek_team;
    -- Check if the team of the member is the same as the team in the new record
    IF team_czlonek != team_nocleg THEN
        RAISE EXCEPTION 'Członek nie należy do tego zespołu.';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_team_before_insert_or_update
BEFORE INSERT OR UPDATE ON projekt.nocleg_czlonkow
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
BEFORE INSERT OR UPDATE ON projekt.nocleg_czlonkow
FOR EACH ROW EXECUTE PROCEDURE check_if_too_much_people();


-- Dodawnia noclegu dla nowego członka
CREATE OR REPLACE FUNCTION add_sleeping_for_new_user()
RETURNS TRIGGER AS $$
    DECLARE
        team_id_ INTEGER;
        empty_places INTEGER;
        free_places INTEGER;
    BEGIN
        -- Get new team_id from insert
        SELECT team_id INTO team_id_ from projekt.czlonkowie where czlonek_id = NEW.team_id;

        -- Get empty places
        SELECT pole_namiotowe_id INTO empty_places
        FROM projekt.pola_namiotowe 
        WHERE pole_namiotowe_id NOT IN (SELECT distinct nocleg_id from projekt.nocleg_czlonkow) LIMIT 1;
        RAISE NOTICE 'Empty places: %', empty_places;

        --Choose places that have free spaces from same team
        SELECT distinct nc.nocleg_id INTO free_places
        from projekt.nocleg_czlonkow nc 
        join projekt.nocleg n on n.numer_pola_namiotowego = nc.nocleg_id
        join projekt.czlonkowie c on c.czlonek_id = nc.czlonek_id
        join projekt.pola_namiotowe p on p.pole_namiotowe_id = n.numer_pola_namiotowego
        where c.team_id = team_id_ and p.ilosc_osob > (select count(*) from projekt.nocleg_czlonkow where nocleg_id = nc.nocleg_id) LIMIT 1;
        RAISE NOTICE 'Free places: %', free_places;

        IF free_places IS NOT NULL THEN
            INSERT INTO projekt.nocleg_czlonkow VALUES (free_places, NEW.czlonek_id);
            RETURN NEW;
        END IF;

        IF empty_places IS NOT NULL THEN
            INSERT INTO projekt.nocleg_czlonkow VALUES (empty_places, NEW.czlonek_id);
            RETURN NEW;
        END IF;

        RAISE EXCEPTION 'Nie ma wolnych miejsc na polu namiotowym.';


    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER add_sleeping_for_new_user
AFTER INSERT ON projekt.czlonkowie
FOR EACH ROW EXECUTE PROCEDURE add_sleeping_for_new_user();
