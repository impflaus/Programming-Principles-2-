-- 1. Поиск по шаблону (по имени или номеру)
CREATE OR REPLACE FUNCTION search_by_pattern(pattern TEXT)
RETURNS TABLE(id INT, name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    WHERE name ILIKE '%' || pattern || '%'
       OR phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Добавление или обновление одного пользователя
CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;

-- 3. Массовое добавление с валидацией телефонов
CREATE OR REPLACE PROCEDURE insert_many_users(
    p_names TEXT[],
    p_phones TEXT[],
    OUT invalids TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT := 1;
BEGIN
    invalids := ARRAY[]::TEXT[];
    WHILE i <= array_length(p_names, 1) LOOP
        IF p_phones[i] ~ '^[0-9]+$' THEN
            CALL insert_or_update_user(p_names[i], p_phones[i]);
        ELSE
            invalids := array_append(invalids, p_names[i]);
        END IF;
        i := i + 1;
    END LOOP;
END;
$$;

-- 4. Постраничный вывод
CREATE OR REPLACE FUNCTION get_paginated(limit_num INT, offset_num INT)
RETURNS TABLE(id INT, name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    ORDER BY id
    LIMIT limit_num OFFSET offset_num;
END;
$$ LANGUAGE plpgsql;

-- 5. Удаление по имени или номеру
CREATE OR REPLACE PROCEDURE delete_by_name_or_phone(p_value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_value OR phone = p_value;
END;
$$;