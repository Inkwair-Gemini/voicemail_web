-- 添加语音记录
CREATE PROCEDURE addVoice(
    IN in_username VARCHAR(100),
    IN in_title VARCHAR(100),
    IN in_timestamp VARCHAR(100),
    IN in_text VARCHAR(10000),
    IN in_url VARCHAR(100)
)
BEGIN
    -- 插入新语音信息
    INSERT INTO voice(username,title, timestamp, text, url)
    VALUES (in_username,in_title,in_timestamp,in_text,in_url);
    -- 返回成功信息
    SELECT '添加成功' AS result;
END;

-- 删除语音信息
CREATE PROCEDURE deleteVoiceByid(
    IN in_id INT(100)
)
BEGIN
    UPDATE voice
    SET deletestatus = 1
    WHERE id = in_id ;

    -- 获取更新的行数
    IF ROW_COUNT() > 0 THEN
        SELECT TRUE AS update_success;
    END IF;
END;
-- 彻底删除语音信息
CREATE PROCEDURE deleteById(
    IN in_id INT(100)
)
BEGIN
    -- 删除指定 ID 的记录
    DELETE FROM voice
    WHERE id = in_id;

    -- 获取更新的行数
    IF ROW_COUNT() > 0 THEN
        SELECT TRUE AS update_success;
    END IF;
END;

-- 恢复语音信息
CREATE PROCEDURE recoverById(
    IN in_id INT(100)
)
BEGIN
    UPDATE voice
    SET deletestatus = 0
    WHERE id = in_id ;

    -- 获取更新的行数
    IF ROW_COUNT() > 0 THEN
        SELECT TRUE AS update_success;
    END IF;
END;
-- 获取deletestatus=1的记录
CREATE PROCEDURE getListByUsername(
    IN in_username VARCHAR(100)
)
BEGIN
    SELECT id,username, title, timestamp, text
    FROM voice
    WHERE username = in_username AND deletestatus = 1;
END;

-- 获取deletestatus=0的记录
CREATE PROCEDURE sendAllVoice(
    IN in_username VARCHAR(100)
)
BEGIN
    SELECT id,username, title, timestamp, text
    FROM voice
    WHERE username = in_username AND deletestatus = 0;
END;