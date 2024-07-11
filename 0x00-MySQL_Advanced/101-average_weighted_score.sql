-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers.
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users AS user
    SET average_score = (
        SELECT IFNULL(SUM(corrections.score * projects.weight) / SUM(projects.weight), 0)
        FROM corrections
        JOIN projects ON projects.id = corrections.project_id
        WHERE corrections.user_id = user.id
    );
END //

DELIMITER ;
