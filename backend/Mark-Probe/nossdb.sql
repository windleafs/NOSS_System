CREATE TABLE nossuser (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    noss_points INT DEFAULT 0,
    role VARCHAR(20) DEFAULT 'user'
);
