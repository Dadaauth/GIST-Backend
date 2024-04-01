-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema content_management
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema content_management
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `content_management` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
-- -----------------------------------------------------
-- Schema user_management
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema user_management
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `user_management` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `content_management` ;

-- -----------------------------------------------------
-- Table `content_management`.`posts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `content_management`.`posts` (
  `id` VARCHAR(150) NOT NULL,
  `user_id` VARCHAR(150) NOT NULL,
  `content` LONGTEXT NOT NULL,
  `image_url` VARCHAR(150) NULL DEFAULT NULL,
  `video_url` VARCHAR(150) NULL DEFAULT NULL,
  `send_time` DATETIME NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `id_idx` (`user_id` ASC) VISIBLE,
  INDEX `user_id_idx` (`user_id` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `content_management`.`comments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `content_management`.`comments` (
  `id` VARCHAR(150) NOT NULL,
  `post_id` VARCHAR(150) NOT NULL,
  `content` MEDIUMTEXT NOT NULL,
  `user_id` VARCHAR(150) NOT NULL,
  `send_time` DATETIME NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `FK_1` (`post_id` ASC) VISIBLE,
  CONSTRAINT `FK_3`
    FOREIGN KEY (`post_id`)
    REFERENCES `content_management`.`posts` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `content_management`.`conversation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `content_management`.`conversation` (
  `id` VARCHAR(150) NOT NULL,
  `name` VARCHAR(300) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `content_management`.`conversation_participants`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `content_management`.`conversation_participants` (
  `user_id` VARCHAR(150) NOT NULL,
  `conversation_id_1` VARCHAR(150) NOT NULL,
  `conversation_id` VARCHAR(150) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  `id` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`user_id`, `conversation_id_1`, `id`),
  INDEX `FK_1` (`conversation_id` ASC) VISIBLE,
  CONSTRAINT `FK_6`
    FOREIGN KEY (`conversation_id`)
    REFERENCES `content_management`.`conversation` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `content_management`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `content_management`.`likes` (
  `id` VARCHAR(150) NOT NULL,
  `post_id` VARCHAR(150) NOT NULL,
  `user_id` VARCHAR(150) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `FK_1` (`post_id` ASC) VISIBLE,
  CONSTRAINT `FK_4`
    FOREIGN KEY (`post_id`)
    REFERENCES `content_management`.`posts` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `content_management`.`message`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `content_management`.`message` (
  `id` VARCHAR(150) NOT NULL,
  `sender_id` VARCHAR(150) NOT NULL,
  `conversation_id` VARCHAR(150) NOT NULL,
  `content` LONGTEXT NULL DEFAULT NULL,
  `image_url` VARCHAR(150) NULL DEFAULT NULL,
  `video_url` VARCHAR(150) NULL DEFAULT NULL,
  `send_time` DATETIME NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `FK_1` (`conversation_id` ASC) VISIBLE,
  CONSTRAINT `FK_5`
    FOREIGN KEY (`conversation_id`)
    REFERENCES `content_management`.`conversation` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `content_management`.`notifications`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `content_management`.`notifications` (
  `id` VARCHAR(150) NOT NULL,
  `user_id` VARCHAR(150) NOT NULL,
  `type` ENUM('posts', 'friend requests', 'calls', 'messages') NOT NULL,
  `content` MEDIUMTEXT NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;

USE `user_management` ;

-- -----------------------------------------------------
-- Table `user_management`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user_management`.`users` (
  `id` VARCHAR(150) NOT NULL,
  `email` VARCHAR(200) NOT NULL,
  `first_name` VARCHAR(150) NOT NULL,
  `last_name` VARCHAR(150) NOT NULL,
  `password` VARCHAR(200) NOT NULL,
  `profile_pic_name` VARCHAR(200) NULL DEFAULT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `user_management`.`friends`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user_management`.`friends` (
  `id` VARCHAR(150) NOT NULL,
  `friend_id` VARCHAR(150) NOT NULL,
  `user_id` VARCHAR(150) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  `status` ENUM('pending', 'friends', 'blocked') NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `FK_1` (`friend_id` ASC) VISIBLE,
  INDEX `FK_2` (`user_id` ASC) VISIBLE,
  CONSTRAINT `FK_1`
    FOREIGN KEY (`friend_id`)
    REFERENCES `user_management`.`users` (`id`),
  CONSTRAINT `FK_2`
    FOREIGN KEY (`user_id`)
    REFERENCES `user_management`.`users` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
