-- SQL script that creates a function SafeDiv that divides (and returns) the first.
DELIMITER //

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT
BEGIN
    DECLARE result FLOAT;
    IF b = 0 THEN
	SET result = 0;
    ELSE
	SET result = a / b;
    END IF;
    RETURN result;
END //

DELIMITER;
