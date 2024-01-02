SET search_path TO public;

CREATE OR REPLACE VIEW projekt.wyniki AS
SELECT B.wynik_overal as wynik, z.nazwa as zespol, b.Numer_startowy as numer, b.nazwa as bolid, b.typ as typ
from projekt.bolidy b join projekt.zespoly z on b.team_id = z.team_id
order by b.wynik_overal; 