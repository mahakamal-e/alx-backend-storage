-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers.
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE average_weighted_score FLOAT;

    SET total_weighted_score = 0;
    SET total_weight = 0;

    SELECT SUM(score * weight) INTO total_weighted_score
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id;

    SELECT SUM(weight) INTO total_weight
    FROM projects;

    IF total_weight > 0 THEN
        SET average_weighted_score = total_weighted_score / total_weight;
    ELSE
        SET average_weighted_score = 0;
    END IF;

    UPDATE users
    SET average_score = average_weighted_score;
END //

DELIMITER ;
