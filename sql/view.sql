CREATE OR REPLACE VIEW projekt.wyniki AS
SELECT B.wynik_overal as wynik, z.nazwa as zespol, b.Numer_startowy as numer, b.nazwa as bolid, b.typ as typ
from projekt.bolidy b join projekt.zespoly z on b.team_id = z.team_id
order by b.wynik_overal; 


-- SELECT wynik, zespol, numer, bolid from projekt.wyniki;

-- SELECT ROW_NUMBER() OVER (ORDER BY wynik) as wynik, zespol, numer, bolid 
-- FROM projekt.wyniki where typ = 'EV';