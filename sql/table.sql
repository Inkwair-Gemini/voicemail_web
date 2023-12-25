DROP TABLE IF EXISTS voice, user;

-- 创建user表
CREATE TABLE IF NOT EXISTS user (
    id INT(8) UNSIGNED ZEROFILL PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(100) NOT NULL,
    avatarUrl VARCHAR(100)
);

-- 创建voice表
CREATE TABLE IF NOT EXISTS voice (
    id INT(8) UNSIGNED ZEROFILL PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    title VARCHAR(100),
    timestamp DATETIME,
    text VARCHAR(10000),
    url VARCHAR(100),
    deletestatus TINYINT(1) NOT NULL DEFAULT 0,
    FOREIGN KEY (username) REFERENCES user(username)
);
