-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: penguins_db
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `moulting_logs`
--

DROP TABLE IF EXISTS `moulting_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `moulting_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `penguin_id` int DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `stage` enum('not_started','moulting','done') DEFAULT NULL,
  `mass` float DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `penguin_id` (`penguin_id`),
  KEY `ix_moulting_logs_id` (`id`),
  CONSTRAINT `moulting_logs_ibfk_1` FOREIGN KEY (`penguin_id`) REFERENCES `penguins` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moulting_logs`
--

LOCK TABLES `moulting_logs` WRITE;
/*!40000 ALTER TABLE `moulting_logs` DISABLE KEYS */;
INSERT INTO `moulting_logs` VALUES (1,NULL,'2025-05-03 22:54:01','not_started',NULL,NULL),(2,NULL,'2025-05-06 12:07:44','moulting',NULL,NULL),(3,NULL,'2025-05-06 13:07:18','done',NULL,NULL),(4,NULL,'2025-05-06 13:32:21','moulting',NULL,NULL),(5,NULL,'2025-05-06 13:32:23','moulting',NULL,NULL),(6,NULL,'2025-05-16 11:55:42','not_started',2.8,'string'),(7,NULL,'2025-05-16 13:43:59','not_started',2.6,'string'),(8,NULL,'2025-05-16 13:48:31','not_started',2.6,'/static/images/4d3afeef70c84d88a7c0dfa55195a34f.jpg'),(9,NULL,'2025-05-17 00:41:58','not_started',2.5,'/static/images/701268aaf0e34c49a7c834f5c431a074.jpg'),(10,8,'2025-05-17 01:50:46','not_started',2.9,'/static/images/0f595cae4f7147b5ab25bd2f09aed3ab.jpg'),(11,8,'2025-05-17 01:52:48','not_started',2.8,'string'),(12,8,'2025-05-17 02:07:40','not_started',2.7,'/static/images/195a81d5cb5e4df0b00e4795056b905d.jpg'),(13,9,'2025-05-17 04:42:22','moulting',1.8,'/static/images/c58af0285adb430590200a44a8449b94.jpg'),(14,10,'2025-05-17 04:42:45','moulting',2,'/static/images/b4657d09a92646d3a2e8af1bf3c6199a.jpg'),(15,11,'2025-05-17 04:45:51','done',1.5,'/static/images/d04c9b7aa6514aba8178d2e2d0417328.jpg'),(16,12,'2025-05-17 04:46:42','moulting',1.7,'/static/images/c5b9d2d24d74423bba4b7cb290a4b82e.jpg'),(17,13,'2025-05-17 04:47:21','not_started',1,'/static/images/8864ae0f870346d6b14493f1d7ea97fa.jpg'),(18,9,'2025-05-17 04:49:28','moulting',1.8,'string'),(19,10,'2025-05-17 04:49:50','moulting',1.8,'string'),(20,11,'2025-05-17 04:50:22','done',1.7,'string'),(21,12,'2025-05-17 04:50:46','moulting',1.6,'string'),(22,13,'2025-05-17 04:51:15','not_started',1,'string');
/*!40000 ALTER TABLE `moulting_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `penguin_images`
--

DROP TABLE IF EXISTS `penguin_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `penguin_images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `penguin_id` int DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `penguin_id` (`penguin_id`),
  KEY `ix_penguin_images_id` (`id`),
  CONSTRAINT `penguin_images_ibfk_1` FOREIGN KEY (`penguin_id`) REFERENCES `penguins` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `penguin_images`
--

LOCK TABLES `penguin_images` WRITE;
/*!40000 ALTER TABLE `penguin_images` DISABLE KEYS */;
INSERT INTO `penguin_images` VALUES (1,NULL,'images\\1_1747266009.jpg','2025-05-15 01:40:09'),(2,NULL,'/static/images/4d3afeef70c84d88a7c0dfa55195a34f.jpg','2025-05-16 13:48:31'),(3,NULL,'/static/images/701268aaf0e34c49a7c834f5c431a074.jpg','2025-05-17 00:41:58'),(4,8,'/static/images/0f595cae4f7147b5ab25bd2f09aed3ab.jpg','2025-05-17 01:50:46'),(5,8,'/static/images/195a81d5cb5e4df0b00e4795056b905d.jpg','2025-05-17 02:07:40'),(6,9,'/static/images/c58af0285adb430590200a44a8449b94.jpg','2025-05-17 04:42:22'),(7,10,'/static/images/b4657d09a92646d3a2e8af1bf3c6199a.jpg','2025-05-17 04:42:45'),(8,11,'/static/images/d04c9b7aa6514aba8178d2e2d0417328.jpg','2025-05-17 04:45:51'),(9,12,'/static/images/c5b9d2d24d74423bba4b7cb290a4b82e.jpg','2025-05-17 04:46:42'),(10,13,'/static/images/8864ae0f870346d6b14493f1d7ea97fa.jpg','2025-05-17 04:47:21');
/*!40000 ALTER TABLE `penguin_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `penguins`
--

DROP TABLE IF EXISTS `penguins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `penguins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rfid_tag` varchar(50) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `mass` float DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL,
  `status` enum('not_started','moulting','done') DEFAULT NULL,
  `danger_flag` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rfid_tag` (`rfid_tag`),
  KEY `ix_penguins_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `penguins`
--

LOCK TABLES `penguins` WRITE;
/*!40000 ALTER TABLE `penguins` DISABLE KEYS */;
INSERT INTO `penguins` VALUES (8,'1','P1',2.7,'2025-05-17 02:07:40','not_started',0,'2025-05-17 03:45:18'),(9,'2','P2',1.8,'2025-05-17 04:49:28','moulting',1,'2025-05-17 06:15:24'),(10,'3','P3',1.8,'2025-05-17 04:49:50','moulting',1,'2025-05-17 06:16:21'),(11,'4','P4',1.7,'2025-05-17 04:50:22','done',0,'2025-05-17 06:16:57'),(12,'5','P5',1.6,'2025-05-17 04:50:46','moulting',1,'2025-05-17 06:17:21'),(13,'6','P6',1,'2025-05-17 04:51:15','not_started',0,'2025-05-17 06:18:38');
/*!40000 ALTER TABLE `penguins` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-18 16:32:59
