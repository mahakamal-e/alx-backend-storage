-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser,
-- that computes and store the average weighted score for a student.
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score INT;
    DECLARE total_weights INT;

    SELECT
        SUM(corrections.score * projects.weight),
        SUM(projects.weight)
    INTO 
        total_score, total_weights
    FROM corrections
    JOIN projects ON projects.id = corrections.project_id
    WHERE corrections.user_id = user_id;

    IF total_weights > 0 THEN
        UPDATE users
        SET average_score = total_score / total_weights
        WHERE users.id = user_id;
    ELSE
        UPDATE users
        SET average_score = 0
        WHERE users.id = user_id;
    END IF;
END//

DELIMITER ;
