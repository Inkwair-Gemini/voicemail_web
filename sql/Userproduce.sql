DELIMITER //
-- 创建存储过程 addUser
CREATE PROCEDURE addUser(
    IN p_username VARCHAR(100),
    IN p_password VARCHAR(100)
)
BEGIN
    DECLARE p_success BOOLEAN;
    DECLARE p_message VARCHAR(100);
    -- 检查用户名是否为空
    IF p_username IS NULL OR TRIM(p_username) = '' THEN
        SET p_success = FALSE;
        SET p_message = '用户名为空';
    -- 检查密码是否为空
    ELSEIF p_password IS NULL OR TRIM(p_password) = '' THEN
        SET p_success = FALSE;
        SET p_message = '密码为空';
    -- 检查用户名是否已被注册
    ELSEIF EXISTS (SELECT 1 FROM user WHERE username = p_username) THEN
        SET p_success = FALSE;
        SET p_message = '用户名已被注册';
    -- 插入新用户
    ELSE
        INSERT INTO user (username, password) VALUES (p_username, p_password);
        SET p_success = TRUE;
        SET p_message = '注册成功';
    END IF;
    -- 返回结果
    SELECT p_success, p_message AS result;
END//
DELIMITER ;
DELIMITER //
-- 登录验证
CREATE PROCEDURE LoginVerify(IN p_username varchar(100) , IN p_password VARCHAR(100))
BEGIN
    DECLARE v_count INT;
    DECLARE d_count INT;
    DECLARE a_id INT;
    DECLARE a_avatarUrl VARCHAR(100);
    DECLARE v_username VARCHAR(255);
    DECLARE f_count VARCHAR(255);
    -- 检查是否存在匹配的记录
    SELECT COUNT(*) INTO v_count
    FROM user
    WHERE username = p_username AND password = p_password;

    SELECT  COUNT(*) INTO d_count
    FROM voice
    WHERE deletestatus = 1;

    SELECT COUNT(*) INTO f_count
    FROM user
    WHERE username = p_username AND password != p_password;

    SELECT COUNT(*) INTO a_id
    FROM user
    WHERE username = p_username AND password = p_password;

    SELECT avatarUrl INTO a_avatarUrl
    FROM user
    WHERE username = p_username AND password = p_password;

    -- 设置布尔值结果
    IF v_count > 0 THEN
        -- 查询用户的名字
        SELECT username INTO v_username
        FROM user
        WHERE username = p_username;

        SELECT '1','登录成功',a_id,a_avatarUrl,p_username,d_count AS result;

    ELSEIF f_count > 0 THEN
        SELECT '0','密码不正确',0,0,0,0 AS result;

    ELSE
        SELECT '0','用户不存在',0,0,0,0 AS result;
    END IF;
END//
DELIMITER ;

-- 修改头像地址
CREATE PROCEDURE ChangeUserAvatarUrl(
    IN p_username VARCHAR(16),
    IN p_avatarUrl VARCHAR(100)
)
BEGIN
    -- Check if the passenger exists

    UPDATE user SET avatarUrl = p_avatarUrl WHERE username = p_username;
    SELECT 'Ture' AS result;


END;
-- 根据用户名找记录
CREATE PROCEDURE selectuserByUsername(
    IN p_username VARCHAR(255)
)
BEGIN
    DECLARE p_count INT;
     -- 检查是否存在匹配的记录
    SELECT COUNT(*) INTO p_count
    FROM user
    WHERE username = p_username;

    IF p_count >0 THEN
        SELECT 'Ture' AS result;
    ELSE
        SELECT 'Fasle' AS result;
    END IF;
END;