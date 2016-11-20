select Id, AncestorId from
(
select 1 as sor, 5 as Id, 3 as AncestorId
union
select 2, 5, AncestorId from Path where Id = 3
order by sor)
