select Id, AncestorId from Path
where
((Id = 5) or Id in (select Id from Path where AncestorId = 5)) and
AncestorId in (select AncestorId from Path where Id = 5)

