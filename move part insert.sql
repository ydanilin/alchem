select Id, AncestorId from
(
select 1 as sor, 5 as Id, 3 as AncestorId
union
select 2, 5, AncestorId from Path where Id = 3
union
select 3, Id, 3 from Path where AncestorId = 5
union
select 4, a.Id, b.AncestorId from Path a, Path b where
                a.AncestorId = 5 and b.Id = 3
order by sor
)
