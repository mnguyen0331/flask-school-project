DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` 
(
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(255) UNIQUE,
	`password` VARCHAR(255),
    `created_on` DATETIME DEFAULT NOW()
);

INSERT INTO users(username, password)
VALUES ('admin', 'testing');