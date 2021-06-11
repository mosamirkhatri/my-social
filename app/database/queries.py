class Query:
    CREATE_USER_TABLE = '''
        CREATE TABLE `user` IF NOT EXISTS (
        `id` int NOT NULL AUTO_INCREMENT,
        `first_name` varchar(60) NOT NULL,
        `last_name` varchar(60) NOT NULL,
        `username` varchar(60) NOT NULL,
        `password` varchar(200) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `username_UNIQUE` (`username`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    '''
    CREATE_POST_TABLE = '''
       CREATE TABLE `post` IF NOT EXISTS (
        `id` int NOT NULL AUTO_INCREMENT,
        `description` varchar(200) DEFAULT NULL,
        `created_at` timestamp NULL DEFAULT NULL,
        `author` int NOT NULL,
        PRIMARY KEY (`id`),
        KEY `author_idx` (`author`),
        CONSTRAINT `author` FOREIGN KEY (`author`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    '''
    CREATE_COMMENT_TABLE = '''
        CREATE TABLE `comment` IF NOT EXISTS (
        `id` int NOT NULL AUTO_INCREMENT,
        `description` varchar(200) NOT NULL,
        `created_at` timestamp NOT NULL,
        `author` int NOT NULL,
        `post_id` int NOT NULL,
        PRIMARY KEY (`id`),
        KEY `author_idx` (`author`),
        KEY `post_id_idx` (`post_id`),
        CONSTRAINT `comment_author` FOREIGN KEY (`author`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT `post_id` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    '''
    CREATE_LIKE_POST_TABLE = '''
        CREATE TABLE `like_post` IF NOT EXISTS (
        `post_id` int NOT NULL,
        `user_id` int NOT NULL,
        `status` tinyint unsigned NOT NULL,
        PRIMARY KEY (`post_id`,`user_id`),
        KEY `like_user_id_idx` (`user_id`),
        CONSTRAINT `like_post_id` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT `like_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    '''
    EXISTING_USER = '''
        SELECT * FROM `user` u WHERE username = %s;
    '''
    CREATE_NEW_USER = '''
        INSERT INTO `user` (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)
    '''
    CREATE_NEW_POST = '''
        INSERT INTO `post` (description, created_at, author) VALUES (%s, %s, %s);
    '''
    GET_ALL_POSTS = '''
        SELECT p.*, u.first_name, u.last_name,u.username
        FROM `post` p 
        JOIN `user` u 
        ON p.author = u.id
        ORDER BY p.created_at DESC;
    '''
    GET_USER_POSTS = '''
        SELECT p.*, u.first_name, u.last_name,u.username FROM
            (SELECT *
            FROM `post` 
            WHERE author = %s) p
        JOIN `user` u
        ON p.author = u.id
        ORDER BY p.created_at DESC;
    '''
    GET_POST = '''
        SELECT p.*, u.first_name, u.last_name,u.username FROM
            (SELECT * 
            FROM `post`
            WHERE id = %s) p
        JOIN `user` u
        ON p.author = u.id;
    '''
    DELETE_POST = '''
        DELETE FROM `post` WHERE id = %s;
    '''
    GET_POST_FOR_CHECK = '''
        SELECT id 
        FROM `post`
        WHERE id = %s
    '''
    GET_LIKE_ENTRY = '''
        SELECT * FROM `like_post` WHERE post_id = %s AND user_id = %s;
    '''
    INSERT_LIKE = '''
        INSERT INTO `like_post` (post_id, user_id, status) VALUES (%s, %s, %s);
    '''
    UPDATE_LIKE = '''
        UPDATE `like_post`
        SET status = %s
        WHERE post_id = %s AND user_id = %s;
    '''
