-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema certificacion_02
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `certificacion_02` DEFAULT CHARACTER SET utf8mb4 ;
USE `certificacion_02` ;

-- -----------------------------------------------------
-- Table `certificacion_02`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `certificacion_02`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `apellido` VARCHAR(45) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `certificacion_02`.`viajes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `certificacion_02`.`viajes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `destino` VARCHAR(100) NOT NULL,
  `fecha_inicio` DATE NOT NULL,
  `fecha_fin` DATE NOT NULL,
  `itinerario` VARCHAR(40) NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `usuario_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_viajes_usuarios_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_viajes_usuarios`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `certificacion_02`.`usuarios` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `certificacion_02`.`viajeros`
-- tabla intermedia: que usuarios se unieron a que viaje
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `certificacion_02`.`viajeros` (
  `usuario_id` INT NOT NULL,
  `viaje_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  PRIMARY KEY (`usuario_id`, `viaje_id`),
  INDEX `fk_viajeros_viajes_idx` (`viaje_id` ASC) VISIBLE,
  CONSTRAINT `fk_viajeros_usuarios`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `certificacion_02`.`usuarios` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_viajeros_viajes`
    FOREIGN KEY (`viaje_id`)
    REFERENCES `certificacion_02`.`viajes` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
