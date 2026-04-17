-- 1. Поиск контактов по имени или телефону
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p TEXT)
RETURNS TABLE(name TEXT, phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT pb.name, pb.phone
    FROM phonebook pb
    WHERE pb.name ILIKE '%' || p || '%'
       OR pb.phone ILIKE '%' || p || '%';
END;
$$;


-- 2. Пагинация (LIMIT / OFFSET)
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(name TEXT, phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT pb.name, pb.phone
    FROM phonebook pb
    ORDER BY pb.name
    LIMIT p_limit OFFSET p_offset;
END;
$$;