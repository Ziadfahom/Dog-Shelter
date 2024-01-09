-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: dogshelterdb
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (4,'Vet'),(3,'Viewer');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (62,3,4),(65,3,8),(66,3,12),(68,3,16),(70,3,20),(71,3,24),(72,3,28),(61,3,32),(63,3,36),(64,3,40),(67,3,44),(69,3,48),(73,4,1),(74,4,2),(75,4,3),(76,4,4),(77,4,5),(78,4,6),(79,4,7),(80,4,8),(81,4,9),(82,4,10),(83,4,11),(84,4,12),(85,4,13),(86,4,14),(87,4,15),(88,4,16),(89,4,17),(90,4,18),(91,4,19),(92,4,20),(93,4,21),(94,4,22),(95,4,23),(96,4,24),(97,4,25),(98,4,26),(99,4,27),(100,4,28),(101,4,29),(102,4,30),(103,4,31),(104,4,32),(105,4,33),(106,4,34),(107,4,35),(108,4,36),(109,4,37),(110,4,38),(111,4,39),(112,4,40),(113,4,41),(114,4,42),(115,4,43),(116,4,44),(117,4,45),(118,4,46),(119,4,47),(120,4,48);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add dog',1,'add_dog'),(2,'Can change dog',1,'change_dog'),(3,'Can delete dog',1,'delete_dog'),(4,'Can view dog',1,'view_dog'),(5,'Can add owner',2,'add_owner'),(6,'Can change owner',2,'change_owner'),(7,'Can delete owner',2,'delete_owner'),(8,'Can view owner',2,'view_owner'),(9,'Can add camera',3,'add_camera'),(10,'Can change camera',3,'change_camera'),(11,'Can delete camera',3,'delete_camera'),(12,'Can view camera',3,'view_camera'),(13,'Can add observes',4,'add_observes'),(14,'Can change observes',4,'change_observes'),(15,'Can delete observes',4,'delete_observes'),(16,'Can view observes',4,'view_observes'),(17,'Can add treatment',5,'add_treatment'),(18,'Can change treatment',5,'change_treatment'),(19,'Can delete treatment',5,'delete_treatment'),(20,'Can view treatment',5,'view_treatment'),(21,'Can add entrance examination',6,'add_entranceexamination'),(22,'Can change entrance examination',6,'change_entranceexamination'),(23,'Can delete entrance examination',6,'delete_entranceexamination'),(24,'Can view entrance examination',6,'view_entranceexamination'),(25,'Can add kennel',7,'add_kennel'),(26,'Can change kennel',7,'change_kennel'),(27,'Can delete kennel',7,'delete_kennel'),(28,'Can view kennel',7,'view_kennel'),(29,'Can add dog placement',8,'add_dogplacement'),(30,'Can change dog placement',8,'change_dogplacement'),(31,'Can delete dog placement',8,'delete_dogplacement'),(32,'Can view dog placement',8,'view_dogplacement'),(33,'Can add observation',9,'add_observation'),(34,'Can change observation',9,'change_observation'),(35,'Can delete observation',9,'delete_observation'),(36,'Can view observation',9,'view_observation'),(37,'Can add dog stance',10,'add_dogstance'),(38,'Can change dog stance',10,'change_dogstance'),(39,'Can delete dog stance',10,'delete_dogstance'),(40,'Can view dog stance',10,'view_dogstance'),(41,'Can add news',11,'add_news'),(42,'Can change news',11,'change_news'),(43,'Can delete news',11,'delete_news'),(44,'Can view news',11,'view_news'),(45,'Can add profile',12,'add_profile'),(46,'Can change profile',12,'change_profile'),(47,'Can delete profile',12,'delete_profile'),(48,'Can view profile',12,'view_profile'),(49,'Can add log entry',13,'add_logentry'),(50,'Can change log entry',13,'change_logentry'),(51,'Can delete log entry',13,'delete_logentry'),(52,'Can view log entry',13,'view_logentry'),(53,'Can add permission',14,'add_permission'),(54,'Can change permission',14,'change_permission'),(55,'Can delete permission',14,'delete_permission'),(56,'Can view permission',14,'view_permission'),(57,'Can add group',15,'add_group'),(58,'Can change group',15,'change_group'),(59,'Can delete group',15,'delete_group'),(60,'Can view group',15,'view_group'),(61,'Can add user',16,'add_user'),(62,'Can change user',16,'change_user'),(63,'Can delete user',16,'delete_user'),(64,'Can view user',16,'view_user'),(65,'Can add content type',17,'add_contenttype'),(66,'Can change content type',17,'change_contenttype'),(67,'Can delete content type',17,'delete_contenttype'),(68,'Can view content type',17,'view_contenttype'),(69,'Can add session',18,'add_session'),(70,'Can change session',18,'change_session'),(71,'Can delete session',18,'delete_session'),(72,'Can view session',18,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$dYK6viisPEYaAS06EOqqKJ$35Zqk+1L3haLN+thwgw5G1IzdjbkDxrpJ2yu657QOo0=','2024-01-05 00:16:01.336368',1,'ZiadFa','Ziad','Fa','ziad.fa@gmail.com',1,1,'2023-07-02 14:42:48.901527'),(2,'pbkdf2_sha256$600000$ecsT0h4kNi5n3m3OqwBHtr$wCRSCf0vKywN0s97MLRdqp9YDAgbQg+201JXv9kC4cE=','2023-12-26 22:40:01.370043',0,'RegularJoe','Reggie','Joe','regular@joe.com',0,1,'2023-07-02 20:53:20.544552'),(3,'pbkdf2_sha256$600000$a855XJUg7wIg7IvHoa9814$90iJ6q257tjGjnHpkQn1Ob3DIRgzCqmfu4axvoys7+Q=','2023-07-28 14:26:07.959295',0,'VetUser','Martin','Martinson','vetty@gmail.com',0,1,'2023-07-02 20:58:55.718035'),(6,'pbkdf2_sha256$600000$IXEdk4bPz4zjFRqZgSrd4c$2c7rNlrNyy+Km9xJ5EHSW7ouhrKcd2tjqAYb/1Ywme8=','2023-12-17 11:59:13.419382',0,'Testguy','test','guy','test@guy.com',0,1,'2023-08-01 15:13:27.126545');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (29,2,3),(26,3,4),(27,6,3);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=307 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2023-07-02 14:47:35.631019','1','Longtail the Dalmatian',1,'[{\"added\": {}}]',1,1),(2,'2023-07-02 14:49:03.350030','1','Bran Stark',1,'[{\"added\": {}}]',2,1),(3,'2023-07-02 14:49:11.727306','1','Longtail the Dalmatian',2,'[{\"changed\": {\"fields\": [\"Owner\"]}}]',1,1),(4,'2023-07-02 14:55:14.239094','1','Treatment: \'Viral Rash\' on Longtail the Dalmatian, by Gianna',1,'[{\"added\": {}}]',5,1),(5,'2023-07-02 14:56:16.834428','1','Longtail the Dalmatian, examined by Gianna on: 30-06-2023',1,'[{\"added\": {}}]',6,1),(6,'2023-07-02 14:56:32.120739','1','Camera #1',1,'[{\"added\": {}}]',3,1),(7,'2023-07-02 14:56:36.335117','2','Camera #2',1,'[{\"added\": {}}]',3,1),(8,'2023-07-02 14:57:22.515989','1','Camera #1 on Longtail the Dalmatian',1,'[{\"added\": {}}]',4,1),(9,'2023-07-02 14:57:46.519673','1','Kennel #1',1,'[{\"added\": {}}]',7,1),(10,'2023-07-02 14:58:25.349374','1','Longtail the Dalmatian in Kennel #1 entered on 01-07-2023',1,'[{\"added\": {}}]',8,1),(11,'2023-07-02 14:59:06.505769','1','Camera #1 on Longtail the Dalmatian, on 01-07-2023 at 17:58',1,'[{\"added\": {}}]',9,1),(12,'2023-07-02 16:21:19.565282','3','Camera #3',1,'[{\"added\": {}}]',3,1),(13,'2023-07-02 16:21:24.043533','4','Camera #4',1,'[{\"added\": {}}]',3,1),(14,'2023-07-02 16:21:29.148802','5','Camera #5',1,'[{\"added\": {}}]',3,1),(15,'2023-07-02 16:21:33.545055','6','Camera #6',1,'[{\"added\": {}}]',3,1),(16,'2023-07-02 16:21:38.560592','7','Camera #7',1,'[{\"added\": {}}]',3,1),(17,'2023-07-02 16:22:09.583243','2','Camera #2 on Timmy',1,'[{\"added\": {}}]',4,1),(18,'2023-07-02 16:22:18.002005','3','Camera #3 on Timmy',1,'[{\"added\": {}}]',4,1),(19,'2023-07-02 16:22:24.328517','4','Camera #3 on Max the German Shepherd',1,'[{\"added\": {}}]',4,1),(20,'2023-07-02 16:22:30.460373','2','Camera #2 on Timmy',2,'[]',4,1),(21,'2023-07-02 16:22:40.989400','5','Camera #4 on Oscar the Husky',1,'[{\"added\": {}}]',4,1),(22,'2023-07-02 16:22:47.310057','6','Camera #5 on Ryan the Golden Retriever',1,'[{\"added\": {}}]',4,1),(23,'2023-07-02 16:22:52.780759','7','Camera #6 on Bryan the Mastiff',1,'[{\"added\": {}}]',4,1),(24,'2023-07-02 16:22:58.707649','8','Camera #7 on Craig the Husky',1,'[{\"added\": {}}]',4,1),(25,'2023-07-02 16:23:04.842683','9','Camera #7 on Timmy',1,'[{\"added\": {}}]',4,1),(26,'2023-07-02 16:23:11.663333','10','Camera #6 on Timmy',1,'[{\"added\": {}}]',4,1),(27,'2023-07-02 18:16:41.964357','2','Kennel #2',1,'[{\"added\": {}}]',7,1),(28,'2023-07-02 18:18:04.112141','3','Kennel #3',1,'[{\"added\": {}}]',7,1),(29,'2023-07-02 18:18:08.432752','4','Kennel #4',1,'[{\"added\": {}}]',7,1),(30,'2023-07-02 18:18:13.595303','5','Kennel #5',1,'[{\"added\": {}}]',7,1),(31,'2023-07-02 18:18:17.512953','6','Kennel #6',1,'[{\"added\": {}}]',7,1),(32,'2023-07-02 18:18:22.738647','7','Kennel #7',1,'[{\"added\": {}}]',7,1),(33,'2023-07-02 18:18:27.378719','8','Kennel #8',1,'[{\"added\": {}}]',7,1),(34,'2023-07-02 18:18:32.153974','9','Kennel #9',1,'[{\"added\": {}}]',7,1),(35,'2023-07-02 18:18:37.130944','10','Kennel #10',1,'[{\"added\": {}}]',7,1),(36,'2023-07-02 18:18:50.285183','2','Kennel #2',2,'[{\"changed\": {\"fields\": [\"KennelImage\"]}}]',7,1),(37,'2023-07-02 18:20:56.503833','3','Kennel #3',2,'[{\"changed\": {\"fields\": [\"KennelImage\"]}}]',7,1),(38,'2023-07-02 18:21:02.001151','4','Kennel #4',2,'[{\"changed\": {\"fields\": [\"KennelImage\"]}}]',7,1),(39,'2023-07-02 18:21:07.612609','5','Kennel #5',2,'[{\"changed\": {\"fields\": [\"KennelImage\"]}}]',7,1),(40,'2023-07-02 18:21:13.368908','6','Kennel #6',2,'[{\"changed\": {\"fields\": [\"KennelImage\"]}}]',7,1),(41,'2023-07-02 18:21:18.334720','7','Kennel #7',2,'[{\"changed\": {\"fields\": [\"KennelImage\"]}}]',7,1),(42,'2023-07-02 18:21:23.263724','8','Kennel #8',2,'[{\"changed\": {\"fields\": [\"KennelImage\"]}}]',7,1),(43,'2023-07-02 18:21:31.847905','9','Kennel #9',2,'[{\"changed\": {\"fields\": [\"KennelImage\"]}}]',7,1),(44,'2023-07-02 18:21:37.752738','10','Kennel #10',2,'[{\"changed\": {\"fields\": [\"KennelImage\"]}}]',7,1),(45,'2023-07-02 18:21:41.949516','11','Kennel #11',1,'[{\"added\": {}}]',7,1),(46,'2023-07-02 18:21:44.582163','12','Kennel #12',1,'[{\"added\": {}}]',7,1),(47,'2023-07-02 18:21:46.832311','13','Kennel #13',1,'[{\"added\": {}}]',7,1),(48,'2023-07-02 18:21:49.055074','14','Kennel #14',1,'[{\"added\": {}}]',7,1),(49,'2023-07-02 18:21:51.335439','15','Kennel #15',1,'[{\"added\": {}}]',7,1),(50,'2023-07-02 20:54:58.557785','1','Vet',1,'[{\"added\": {}}]',15,1),(51,'2023-07-02 20:55:39.240983','2','Regular',1,'[{\"added\": {}}]',15,1),(52,'2023-07-02 22:45:05.088006','7','Longtail the Dalmatian in Kennel #4 entered on 25-01-2023',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Kennel\"]}}]',8,1),(53,'2023-07-02 22:50:37.660028','18','Unknown camera on Unknown dog, on 02-07-2023 at 01:50',1,'[{\"added\": {}}]',9,1),(54,'2023-07-02 22:50:58.240751','19','Unknown camera on Unknown dog, on 29-04-2023 at 18:00',1,'[{\"added\": {}}]',9,1),(55,'2023-07-02 22:51:19.703283','20','Unknown camera on Unknown dog, on 23-06-2023 at 00:00',1,'[{\"added\": {}}]',9,1),(56,'2023-07-02 22:51:35.121395','21','Unknown camera on Unknown dog, on 15-06-2023 at 12:00',1,'[{\"added\": {}}]',9,1),(57,'2023-07-02 22:51:52.460734','22','Unknown camera on Unknown dog, on 16-06-2023 at 00:00',1,'[{\"added\": {}}]',9,1),(58,'2023-07-02 22:52:07.225289','23','Unknown camera on Unknown dog, on 01-07-2023 at 01:51',1,'[{\"added\": {}}]',9,1),(59,'2023-07-02 22:52:56.453132','1','Craig the Husky in Kennel #6 entered on 01-07-2023',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Kennel\"]}}]',8,1),(60,'2023-07-02 22:53:25.764272','10','Camera #6 on Darlene the Dachshund',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Camera\"]}}]',4,1),(61,'2023-07-03 08:11:18.252350','11','Longtail the Dalmatian in Kennel #2 entered on 29-05-2023',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Kennel\"]}}]',8,1),(62,'2023-07-03 08:11:23.152217','2','Oscar the Husky in Kennel #2 entered on 01-05-2023',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Kennel\"]}}]',8,1),(63,'2023-07-03 08:11:28.577016','8','Ryan the Golden Retriever in Kennel #4 entered on 13-04-2023',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Kennel\"]}}]',8,1),(64,'2023-07-03 08:11:30.616369','8','Ryan the Golden Retriever in Kennel #4 entered on 13-04-2023',2,'[]',8,1),(65,'2023-07-03 08:11:37.564278','9','Craig the Husky in Kennel #5 entered on 01-03-2023',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Kennel\"]}}]',8,1),(66,'2023-07-03 08:11:45.365567','3','Darlene the Dachshund in Kennel #6 entered on 10-02-2023',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Kennel\"]}}]',8,1),(67,'2023-07-03 08:11:53.098311','14','Julie the Husky in Kennel #7 entered on 12-01-2023',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Kennel\"]}}]',8,1),(68,'2023-07-03 08:11:58.758135','5','Cynthia the Boxer in Kennel #8 entered on 16-12-2022',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Kennel\"]}}]',8,1),(69,'2023-07-03 08:12:04.997832','4','Bonnie the Boxer in Kennel #9 entered on 06-12-2022',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Kennel\"]}}]',8,1),(70,'2023-07-03 08:12:10.884446','13','Bryan the Mastiff in Kennel #9 entered on 04-05-2022',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Kennel\"]}}]',8,1),(71,'2023-07-03 08:12:17.257398','15','Paige the Dachshund in Kennel #10 entered on 07-04-2022',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Kennel\"]}}]',8,1),(72,'2023-07-03 08:12:23.936101','12','Lindsay the Dachshund in Kennel #11 entered on 22-04-2021',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Kennel\"]}}]',8,1),(73,'2023-07-03 08:12:31.073383','10','Leah the Husky in Kennel #12 entered on 13-11-2020',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Kennel\"]}}]',8,1),(74,'2023-07-03 08:13:33.750470','22','Max the German Shepherd, examined by Rob on: 24-06-2022',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(75,'2023-07-03 08:13:36.523577','21','Longtail the Dalmatian, examined by Michael on: 20-02-2023',2,'[]',6,1),(76,'2023-07-03 08:13:41.416431','20','Oscar the Husky, examined by Anastasia on: 09-03-2023',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(77,'2023-07-03 08:13:46.057165','21','Julie the Husky, examined by Michael on: 20-02-2023',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(78,'2023-07-03 08:13:50.290268','19','Darlene the Dachshund, examined by Ali on: 06-01-2023',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(79,'2023-07-03 08:13:54.408354','18','Julie the Husky, examined by Samantha on: 13-12-2022',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(80,'2023-07-03 08:13:58.978466','17','Cynthia the Boxer, examined by Charlie on: 08-05-2022',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(81,'2023-07-03 08:14:03.879904','16','Bonnie the Boxer, examined by Charlie on: 10-05-2021',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(82,'2023-07-03 08:14:08.103147','15','Paige the Dachshund, examined by Shelly on: 29-09-2022',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(83,'2023-07-03 08:14:12.291277','14','Christopher the Dachshund, examined by Meirav on: 23-06-2022',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(84,'2023-07-03 08:14:34.252547','13','Timmy, examined by Shelly on: 13-03-2021',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(85,'2023-07-03 08:14:37.718827','12','James the Golden Retriever, examined by Roey on: 18-05-2021',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(86,'2023-07-03 08:14:41.097129','11','Leah the Husky, examined by Charlie on: 30-05-2023',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(87,'2023-07-03 08:14:44.599675','10','Jessica the Golden Retriever, examined by Charlie on: 03-05-2022',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(88,'2023-07-03 08:14:48.001172','9','James the Golden Retriever, examined by Michael on: 11-07-2021',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(89,'2023-07-03 08:14:51.369726','8','Lindsay the Dachshund, examined by Ali on: 26-08-2021',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(90,'2023-07-03 08:14:55.430758','7','Leah the Husky, examined by George on: 10-01-2021',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(91,'2023-07-03 08:14:59.685060','6','Christopher the Dachshund, examined by Sami on: 14-12-2022',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(92,'2023-07-03 08:15:03.864855','5','Melissa the Golden Retriever, examined by Roey on: 05-01-2019',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(93,'2023-07-03 08:15:07.620059','4','Paige the Dachshund, examined by George on: 10-01-2021',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(94,'2023-07-03 08:15:11.538937','3','Max the German Shepherd, examined by Sami on: 14-12-2022',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(95,'2023-07-03 08:15:15.138667','2','Ryan the Golden Retriever, examined by Roey on: 05-01-2019',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(96,'2023-07-03 08:15:33.655024','9','Camera #7 on Max the German Shepherd',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Camera\"]}}]',4,1),(97,'2023-07-03 08:15:37.959569','8','Camera #1 on Longtail the Dalmatian',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Camera\"]}}]',4,1),(98,'2023-07-03 08:15:45.754984','7','Camera #4 on Bryan the Mastiff',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Camera\"]}}]',4,1),(99,'2023-07-03 08:15:50.026415','6','Camera #4 on Julie the Husky',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Camera\"]}}]',4,1),(100,'2023-07-03 08:15:55.602113','5','Camera #5 on Cynthia the Boxer',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Camera\"]}}]',4,1),(101,'2023-07-03 08:16:02.412659','4','Camera #6 on Bonnie the Boxer',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Camera\"]}}]',4,1),(102,'2023-07-03 08:16:09.188017','3','Camera #6 on Ryan the Golden Retriever',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Camera\"]}}]',4,1),(103,'2023-07-03 08:16:14.484305','2','Camera #7 on Oscar the Husky',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Camera\"]}}]',4,1),(104,'2023-07-03 08:16:25.788743','1','Camera #1 on Oscar the Husky',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Camera\"]}}]',4,1),(105,'2023-07-03 08:27:37.342500','11','Longtail the Dalmatian in Kennel #2 entered on 29-05-2023',2,'[]',8,1),(106,'2023-07-03 08:28:32.795777','14','Camera #6 on Darlene the Dachshund, on 23-05-2023 at 12:53',2,'[{\"changed\": {\"fields\": [\"Observes\"]}}]',9,1),(107,'2023-07-03 09:23:42.762316','19','Treatment: \'Underweight\' on Longtail the Dalmatian, by Johnathan',2,'[]',5,1),(108,'2023-07-03 09:23:46.930321','18','Treatment: \'Infection\' on Max the German Shepherd, by Meirav',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(109,'2023-07-03 09:23:51.500949','17','Treatment: \'Coughing\' on Oscar the Husky, by Meirav',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(110,'2023-07-03 09:23:55.855361','16','Treatment: \'Underweight\' on Ryan the Golden Retriever, by Anastasia',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(111,'2023-07-03 09:24:00.977101','15','Treatment: \'Coughing\' on Bryan the Mastiff, by Charlie',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(112,'2023-07-03 09:24:06.572082','14','Treatment: \'Rash Treatment\' on Craig the Husky, by Charlie',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(113,'2023-07-03 09:24:11.077445','13','Treatment: \'Rash Treatment\' on Darlene the Dachshund, by Charlie',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(114,'2023-07-03 09:24:16.490432','12','Treatment: \'Sneezing\' on Julie the Husky, by Samantha',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(115,'2023-07-03 09:24:22.181016','11','Treatment: \'Sneezing\' on Cynthia the Boxer, by Rob',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(116,'2023-07-03 09:24:35.653679','10','Treatment: \'Fatigue\' on Timmy, by Meirav',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(117,'2023-07-03 09:24:41.791118','9','Treatment: \'High Fever\' on James the Golden Retriever, by Mac',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(118,'2023-07-03 09:24:46.099035','8','Treatment: \'Fleas\' on Leah the Husky, by Rob',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(119,'2023-07-03 09:24:49.915022','7','Treatment: \'Coughing\' on Jessica the Golden Retriever, by Ali',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(120,'2023-07-03 09:24:52.758812','6','Treatment: \'Fatigue\' on Lindsay the Dachshund, by Meirav',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(121,'2023-07-03 09:24:56.032022','5','Treatment: \'Rash Treatment\' on Christopher the Dachshund, by Meirav',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(122,'2023-07-03 09:24:59.524205','4','Treatment: \'Fatigue\' on Melissa the Golden Retriever, by Shelly',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(123,'2023-07-03 09:25:03.675933','2','Treatment: \'Rash Treatment\' on Ryan the Golden Retriever, by Roey',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(124,'2023-07-03 09:25:18.670884','10','Treatment: \'Fatigue\' on Longtail the Dalmatian, by Meirav',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',5,1),(125,'2023-07-03 09:45:50.890915','13','Longtail the Dalmatian, examined by Shelly on: 13-03-2021',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(126,'2023-07-03 10:15:55.146588','16','Camera #1 on Longtail the Dalmatian, on 02-03-2023 at 02:32',2,'[{\"changed\": {\"fields\": [\"Observes\"]}}]',9,1),(127,'2023-07-03 10:16:03.048275','15','Camera #1 on Longtail the Dalmatian, on 13-02-2023 at 20:15',2,'[{\"changed\": {\"fields\": [\"Observes\"]}}]',9,1),(128,'2023-07-03 10:18:06.398380','9','Camera #1 on Longtail the Dalmatian, on 19-06-2023 at 14:26',2,'[{\"changed\": {\"fields\": [\"IsKong\"]}}]',9,1),(129,'2023-07-03 13:32:31.794114','19','Timmy',2,'[{\"changed\": {\"fields\": [\"DogImage\"]}}]',1,1),(130,'2023-07-03 21:40:23.394573','2','Camera #6 on Darlene the Dachshund, on 23-05-2023 at 09:53, starting at 16:12',2,'[{\"changed\": {\"fields\": [\"DogLocation\"]}}]',10,1),(131,'2023-07-03 22:01:15.165308','3','Camera #6 on Ryan the Golden Retriever, on 31-03-2023 at 18:39, starting at 22:45',2,'[{\"changed\": {\"fields\": [\"DogLocation\"]}}]',10,1),(132,'2023-07-03 22:01:18.878557','10','Camera #6 on Ryan the Golden Retriever, on 21-08-2022 at 16:10, starting at 18:45',2,'[]',10,1),(133,'2023-07-03 22:01:26.773533','15','Camera #7 on Max the German Shepherd, on 15-06-2023 at 09:00, starting at 12:20',2,'[]',10,1),(134,'2023-07-03 22:01:30.560254','4','Camera #7 on Max the German Shepherd, on 16-06-2023 at 02:53, starting at 10:26',2,'[]',10,1),(135,'2023-07-03 22:01:41.004963','9','Camera #1 on Longtail the Dalmatian, on 19-06-2023 at 14:26',2,'[{\"changed\": {\"fields\": [\"IsKong\"]}}]',9,1),(136,'2023-07-03 22:11:43.557456','5','Camera #6 on Bonnie the Boxer, on 26-03-2022 at 00:00',2,'[{\"changed\": {\"fields\": [\"IsKong\"]}}]',9,1),(137,'2023-07-03 22:12:55.149952','21','Camera #6 on Bonnie the Boxer, on 25-03-2022 at 21:00, starting at 01:12',1,'[{\"added\": {}}]',10,1),(138,'2023-07-04 00:09:52.637370','6','Oscar the Husky in Kennel #5 entered on 02-08-2020',2,'[{\"changed\": {\"fields\": [\"Dog\", \"Kennel\"]}}]',8,1),(139,'2023-07-28 14:41:41.137383','1','Vet',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',15,1),(140,'2023-07-28 14:47:22.842672','1','Vet',3,'',15,1),(141,'2023-07-28 14:47:22.846623','2','Viewer',3,'',15,1),(142,'2023-09-14 14:58:39.629920','18','Camera #1 on Longtail the Dalmatian, on 02-07-2023 at 01:50',2,'[{\"changed\": {\"fields\": [\"Observes\"]}}]',9,1),(143,'2023-09-14 14:58:56.294481','20','Camera #1 on Longtail the Dalmatian, on 23-06-2023 at 00:00',2,'[{\"changed\": {\"fields\": [\"Observes\"]}}]',9,1),(144,'2023-09-14 14:59:18.592499','22','Camera #1 on Longtail the Dalmatian, on 16-06-2023 at 00:00',2,'[{\"changed\": {\"fields\": [\"Observes\"]}}]',9,1),(145,'2023-09-14 14:59:30.127911','7','Camera #1 on Longtail the Dalmatian, on 31-03-2023 at 21:39',2,'[{\"changed\": {\"fields\": [\"Observes\"]}}]',9,1),(146,'2023-09-14 14:59:48.828939','12','Camera #1 on Longtail the Dalmatian, on 24-01-2023 at 11:20',2,'[{\"changed\": {\"fields\": [\"Observes\"]}}]',9,1),(147,'2023-09-14 15:00:14.419988','14','Camera #1 on Longtail the Dalmatian, on 23-05-2023 at 12:53',2,'[{\"changed\": {\"fields\": [\"Observes\"]}}]',9,1),(148,'2023-09-16 17:43:53.312660','13','Kennel #13',3,'',7,1),(149,'2023-09-17 12:28:04.705557','1','Camera #7 on Longtail the Dalmatian, on 01-07-2023 at 17:58',2,'[{\"changed\": {\"fields\": [\"Observes\"]}}]',9,1),(150,'2023-09-17 16:17:43.904872','12','Camera #1 on Longtail on 16-09-2023, on 24-01-2023 at 11:20',2,'[{\"changed\": {\"fields\": [\"SessionDurationInMins\"]}}]',9,1),(151,'2023-09-17 16:18:05.131675','12','Camera #1 on Longtail on 16-09-2023, on 24-01-2023 at 11:20',2,'[{\"changed\": {\"fields\": [\"SessionDurationInMins\"]}}]',9,1),(152,'2023-09-17 16:18:22.598958','12','Camera #1 on Longtail on 16-09-2023, on 24-01-2023 at 11:20',2,'[{\"changed\": {\"fields\": [\"SessionDurationInMins\"]}}]',9,1),(153,'2023-09-18 22:02:33.955594','8','Camera #1 on Longtail on 19-09-2023',2,'[{\"changed\": {\"fields\": [\"SessionDate\"]}}]',4,1),(154,'2023-09-18 22:02:57.633712','22','Camera #3 on Longtail on 07-09-2023',2,'[{\"changed\": {\"fields\": [\"SessionDate\"]}}]',4,1),(155,'2023-09-20 12:36:40.297210','12','Camera #1 on Longtail on 19-09-2023, on 20-09-2023 at 11:20',2,'[{\"changed\": {\"fields\": [\"ObsDateTime\"]}}]',9,1),(156,'2023-09-20 12:37:34.765492','15','Camera #1 on Longtail on 19-09-2023, on 15-09-2023 at 20:15',2,'[{\"changed\": {\"fields\": [\"ObsDateTime\"]}}]',9,1),(157,'2023-09-20 12:38:12.083383','14','Camera #1 on Longtail on 19-09-2023, on 08-09-2023 at 12:53',2,'[{\"changed\": {\"fields\": [\"ObsDateTime\"]}}]',9,1),(158,'2023-09-20 12:38:47.232565','14','Camera #1 on Longtail on 19-09-2023, on 08-09-2023 at 12:53',2,'[{\"changed\": {\"fields\": [\"IsKong\"]}}]',9,1),(159,'2023-09-23 13:23:24.280678','3','Camera #1 on Longtail on 19-09-2023, on 02-03-2023 at 02:32, starting at 22:45',2,'[{\"changed\": {\"fields\": [\"Observation\"]}}]',10,1),(160,'2023-09-23 13:23:31.901733','9','Camera #1 on Longtail on 19-09-2023, on 02-03-2023 at 02:32, starting at 22:03',2,'[{\"changed\": {\"fields\": [\"Observation\"]}}]',10,1),(161,'2023-09-23 13:23:38.534449','7','Camera #1 on Longtail on 19-09-2023, on 02-03-2023 at 02:32, starting at 19:00',2,'[{\"changed\": {\"fields\": [\"Observation\"]}}]',10,1),(162,'2023-09-23 13:23:43.409315','10','Camera #1 on Longtail on 19-09-2023, on 02-03-2023 at 02:32, starting at 18:45',2,'[{\"changed\": {\"fields\": [\"Observation\"]}}]',10,1),(163,'2023-09-23 13:23:47.325744','10','Camera #1 on Longtail on 19-09-2023, on 02-03-2023 at 02:32, starting at 18:45',2,'[]',10,1),(164,'2023-09-23 13:23:57.791441','18','Camera #1 on Longtail on 19-09-2023, on 02-03-2023 at 02:32, starting at 16:39',2,'[{\"changed\": {\"fields\": [\"Observation\"]}}]',10,1),(165,'2023-09-23 13:24:09.222059','2','Camera #1 on Longtail on 19-09-2023, on 02-03-2023 at 02:32, starting at 16:12',2,'[{\"changed\": {\"fields\": [\"Observation\"]}}]',10,1),(166,'2023-09-23 13:24:17.025092','14','Camera #1 on Longtail on 19-09-2023, on 02-03-2023 at 02:32, starting at 15:48',2,'[{\"changed\": {\"fields\": [\"Observation\"]}}]',10,1),(167,'2023-09-23 13:24:28.161061','15','Camera #1 on Longtail on 19-09-2023, on 02-03-2023 at 02:32, starting at 12:20',2,'[{\"changed\": {\"fields\": [\"Observation\"]}}]',10,1),(168,'2023-09-23 13:24:37.416934','11','Camera #1 on Longtail on 19-09-2023, on 02-03-2023 at 02:32, starting at 10:55',2,'[{\"changed\": {\"fields\": [\"Observation\"]}}]',10,1),(169,'2023-09-23 13:24:44.596319','4','Camera #1 on Longtail on 19-09-2023, on 02-03-2023 at 02:32, starting at 10:26',2,'[{\"changed\": {\"fields\": [\"Observation\"]}}]',10,1),(170,'2023-09-23 13:25:29.295653','16','Camera #1 on Longtail on 19-09-2023, on 07-10-2023 at 02:32',2,'[{\"changed\": {\"fields\": [\"ObsDateTime\"]}}]',9,1),(171,'2023-09-27 00:50:30.356225','58','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00',1,'[{\"added\": {}}]',9,1),(172,'2023-09-27 00:50:46.968388','59','Camera #7 on Oscar on 16-09-2023, on 06-11-2023 at 02:00',1,'[{\"added\": {}}]',9,1),(173,'2023-09-27 00:51:05.035335','60','Camera #6 on Ryan on 16-09-2023, on 07-11-2023 at 03:00',1,'[{\"added\": {}}]',9,1),(174,'2023-09-27 00:51:25.516811','61','Camera #6 on Bonnie on 16-09-2023, on 08-11-2023 at 04:00',1,'[{\"added\": {}}]',9,1),(175,'2023-09-27 00:51:52.596101','62','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00',1,'[{\"added\": {}}]',9,1),(176,'2023-09-27 00:52:31.192452','79','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 03:52',1,'[{\"added\": {}}]',10,1),(177,'2023-09-27 00:54:18.577038','80','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 03:54',1,'[{\"added\": {}}]',10,1),(178,'2023-09-27 00:54:31.684531','81','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 03:54',1,'[{\"added\": {}}]',10,1),(179,'2023-09-27 00:55:27.294203','82','Camera #7 on Oscar on 16-09-2023, on 06-11-2023 at 02:00, starting at 03:55',1,'[{\"added\": {}}]',10,1),(180,'2023-09-27 00:55:37.515952','83','Camera #6 on Ryan on 16-09-2023, on 07-11-2023 at 03:00, starting at 03:55',1,'[{\"added\": {}}]',10,1),(181,'2023-09-27 00:55:44.999005','25','Camera #1 on Longtail on 19-09-2023, on 07-10-2023 at 02:32, starting at 22:59',2,'[{\"changed\": {\"fields\": [\"DogStance\"]}}]',10,1),(182,'2023-09-27 00:55:52.381739','24','Camera #1 on Longtail on 19-09-2023, on 07-10-2023 at 02:32, starting at 22:47',2,'[{\"changed\": {\"fields\": [\"DogStance\"]}}]',10,1),(183,'2023-09-27 00:55:55.543414','26','Camera #1 on Longtail on 19-09-2023, on 07-10-2023 at 02:32, starting at 23:00',2,'[]',10,1),(184,'2023-09-27 00:56:01.232961','23','Camera #1 on Longtail on 19-09-2023, on 07-10-2023 at 02:32, starting at 22:46',2,'[{\"changed\": {\"fields\": [\"DogStance\"]}}]',10,1),(185,'2023-09-27 00:57:00.272232','84','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 03:56',1,'[{\"added\": {}}]',10,1),(186,'2023-09-27 00:58:16.760906','85','Camera #7 on Oscar on 16-09-2023, on 06-11-2023 at 02:00, starting at 03:58',1,'[{\"added\": {}}]',10,1),(187,'2023-09-27 00:59:39.768473','86','Camera #6 on Bonnie on 16-09-2023, on 08-11-2023 at 04:00, starting at 03:59',1,'[{\"added\": {}}]',10,1),(188,'2023-09-27 01:00:34.955200','87','Camera #6 on Bonnie on 16-09-2023, on 08-11-2023 at 04:00, starting at 04:00',1,'[{\"added\": {}}]',10,1),(189,'2023-09-27 01:01:36.669416','88','Camera #6 on Bonnie on 16-09-2023, on 08-11-2023 at 04:00, starting at 04:01',1,'[{\"added\": {}}]',10,1),(190,'2023-09-27 01:05:32.923088','89','Camera #6 on Bonnie on 16-09-2023, on 08-11-2023 at 04:00, starting at 12:00',1,'[{\"added\": {}}]',10,1),(191,'2023-09-27 01:12:58.581050','90','Camera #6 on Bonnie on 16-09-2023, on 08-11-2023 at 04:00, starting at 04:12',1,'[{\"added\": {}}]',10,1),(192,'2023-09-27 01:15:08.930862','91','Camera #6 on Bonnie on 16-09-2023, on 08-11-2023 at 04:00, starting at 04:15',1,'[{\"added\": {}}]',10,1),(193,'2023-09-27 01:15:47.875654','92','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 04:15',1,'[{\"added\": {}}]',10,1),(194,'2023-09-27 01:16:19.888680','93','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 04:16',1,'[{\"added\": {}}]',10,1),(195,'2023-09-27 01:39:44.737447','26','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 04:39',2,'[{\"changed\": {\"fields\": [\"Observation\", \"StanceStartTime\"]}}]',10,1),(196,'2023-09-27 01:48:23.919950','94','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 04:48',1,'[{\"added\": {}}]',10,1),(197,'2023-09-27 01:50:42.268454','95','Camera #1 on Longtail on 19-09-2023, on 07-10-2023 at 02:32, starting at 04:50',1,'[{\"added\": {}}]',10,1),(198,'2023-09-27 01:51:43.877183','96','Camera #7 on Oscar on 16-09-2023, on 06-11-2023 at 02:00, starting at 04:51',1,'[{\"added\": {}}]',10,1),(199,'2023-09-27 01:53:12.449655','97','Camera #1 on Longtail on 19-09-2023, on 29-09-2023 at 17:56, starting at 04:53',1,'[{\"added\": {}}]',10,1),(200,'2023-09-27 02:00:00.108011','98','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 04:59',1,'[{\"added\": {}}]',10,1),(201,'2023-09-27 02:00:51.221828','99','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:00',1,'[{\"added\": {}}]',10,1),(202,'2023-09-27 02:01:01.780943','100','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:00',1,'[{\"added\": {}}]',10,1),(203,'2023-09-27 02:01:15.769126','101','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:01',1,'[{\"added\": {}}]',10,1),(204,'2023-09-27 02:01:25.811489','102','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:01',1,'[{\"added\": {}}]',10,1),(205,'2023-09-27 02:02:06.727073','103','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:02',1,'[{\"added\": {}}]',10,1),(206,'2023-09-27 02:02:16.994104','104','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:02',1,'[{\"added\": {}}]',10,1),(207,'2023-09-27 02:02:25.810587','105','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:02',1,'[{\"added\": {}}]',10,1),(208,'2023-09-27 02:02:34.291462','106','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:02',1,'[{\"added\": {}}]',10,1),(209,'2023-09-27 02:02:44.541187','107','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:02',1,'[{\"added\": {}}]',10,1),(210,'2023-09-27 02:02:54.322798','108','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:02',1,'[{\"added\": {}}]',10,1),(211,'2023-09-27 02:03:35.151306','109','Camera #7 on Oscar on 16-09-2023, on 06-11-2023 at 02:00, starting at 05:03',1,'[{\"added\": {}}]',10,1),(212,'2023-09-27 02:03:44.082696','110','Camera #7 on Oscar on 16-09-2023, on 06-11-2023 at 02:00, starting at 05:03',1,'[{\"added\": {}}]',10,1),(213,'2023-09-27 02:03:53.518205','111','Camera #7 on Oscar on 16-09-2023, on 06-11-2023 at 02:00, starting at 05:03',1,'[{\"added\": {}}]',10,1),(214,'2023-09-27 02:04:01.847154','112','Camera #7 on Oscar on 16-09-2023, on 06-11-2023 at 02:00, starting at 05:03',1,'[{\"added\": {}}]',10,1),(215,'2023-09-27 02:04:11.227928','113','Camera #7 on Oscar on 16-09-2023, on 06-11-2023 at 02:00, starting at 05:04',1,'[{\"added\": {}}]',10,1),(216,'2023-09-27 02:04:19.476605','114','Camera #7 on Oscar on 16-09-2023, on 06-11-2023 at 02:00, starting at 05:04',1,'[{\"added\": {}}]',10,1),(217,'2023-09-27 02:04:27.674613','115','Camera #7 on Oscar on 16-09-2023, on 06-11-2023 at 02:00, starting at 05:04',1,'[{\"added\": {}}]',10,1),(218,'2023-09-27 02:04:37.258793','116','Camera #7 on Oscar on 16-09-2023, on 06-11-2023 at 02:00, starting at 05:04',1,'[{\"added\": {}}]',10,1),(219,'2023-09-27 02:04:45.422142','117','Camera #7 on Oscar on 16-09-2023, on 06-11-2023 at 02:00, starting at 05:04',1,'[{\"added\": {}}]',10,1),(220,'2023-09-27 02:04:52.541479','118','Camera #6 on Ryan on 16-09-2023, on 07-11-2023 at 03:00, starting at 05:04',1,'[{\"added\": {}}]',10,1),(221,'2023-09-27 02:05:00.655661','119','Camera #6 on Ryan on 16-09-2023, on 07-11-2023 at 03:00, starting at 05:04',1,'[{\"added\": {}}]',10,1),(222,'2023-09-27 02:05:10.854392','120','Camera #6 on Bonnie on 16-09-2023, on 08-11-2023 at 04:00, starting at 05:05',1,'[{\"added\": {}}]',10,1),(223,'2023-09-27 02:05:20.401117','121','Camera #6 on Bonnie on 16-09-2023, on 08-11-2023 at 04:00, starting at 05:05',1,'[{\"added\": {}}]',10,1),(224,'2023-09-27 02:05:27.386615','122','Camera #6 on Bonnie on 16-09-2023, on 08-11-2023 at 04:00, starting at 05:05',1,'[{\"added\": {}}]',10,1),(225,'2023-09-27 02:05:34.819535','123','Camera #6 on Bonnie on 16-09-2023, on 08-11-2023 at 04:00, starting at 05:05',1,'[{\"added\": {}}]',10,1),(226,'2023-09-27 02:05:41.454960','124','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 05:05',1,'[{\"added\": {}}]',10,1),(227,'2023-09-27 02:05:47.546563','125','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 05:05',1,'[{\"added\": {}}]',10,1),(228,'2023-09-27 02:05:54.565541','126','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 05:05',1,'[{\"added\": {}}]',10,1),(229,'2023-09-27 02:06:03.580010','127','Camera #6 on Bonnie on 16-09-2023, on 08-11-2023 at 04:00, starting at 05:06',1,'[{\"added\": {}}]',10,1),(230,'2023-09-27 02:06:11.011699','128','Camera #6 on Ryan on 16-09-2023, on 07-11-2023 at 03:00, starting at 05:06',1,'[{\"added\": {}}]',10,1),(231,'2023-09-27 02:06:17.844981','129','Camera #6 on Ryan on 16-09-2023, on 07-11-2023 at 03:00, starting at 05:06',1,'[{\"added\": {}}]',10,1),(232,'2023-09-27 02:06:28.803065','130','Camera #6 on Ryan on 16-09-2023, on 07-11-2023 at 03:00, starting at 05:06',1,'[{\"added\": {}}]',10,1),(233,'2023-09-27 02:06:36.654524','131','Camera #6 on Bonnie on 16-09-2023, on 08-11-2023 at 04:00, starting at 05:06',1,'[{\"added\": {}}]',10,1),(234,'2023-09-27 02:06:44.705772','132','Camera #6 on Bonnie on 16-09-2023, on 08-11-2023 at 04:00, starting at 05:06',1,'[{\"added\": {}}]',10,1),(235,'2023-09-27 02:06:53.741503','133','Camera #6 on Bonnie on 16-09-2023, on 08-11-2023 at 04:00, starting at 05:06',1,'[{\"added\": {}}]',10,1),(236,'2023-09-27 02:07:01.104726','134','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 05:06',1,'[{\"added\": {}}]',10,1),(237,'2023-09-27 02:59:15.268937','135','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:59',1,'[{\"added\": {}}]',10,1),(238,'2023-09-27 02:59:25.922601','136','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:59',1,'[{\"added\": {}}]',10,1),(239,'2023-09-27 02:59:37.571333','137','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:59',1,'[{\"added\": {}}]',10,1),(240,'2023-09-27 02:59:46.894211','138','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:59',1,'[{\"added\": {}}]',10,1),(241,'2023-09-27 03:00:04.589505','139','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:59',1,'[{\"added\": {}}]',10,1),(242,'2023-09-27 03:00:16.232025','140','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 06:00',1,'[{\"added\": {}}]',10,1),(243,'2023-09-27 03:00:24.640995','141','Camera #7 on Oscar on 16-09-2023, on 06-11-2023 at 02:00, starting at 06:00',1,'[{\"added\": {}}]',10,1),(244,'2023-09-27 03:00:32.771581','142','Camera #7 on Oscar on 16-09-2023, on 06-11-2023 at 02:00, starting at 06:00',1,'[{\"added\": {}}]',10,1),(245,'2023-09-27 03:00:42.516115','143','Camera #7 on Oscar on 16-09-2023, on 06-11-2023 at 02:00, starting at 06:00',1,'[{\"added\": {}}]',10,1),(246,'2023-09-27 03:00:52.817817','144','Camera #6 on Ryan on 16-09-2023, on 07-11-2023 at 03:00, starting at 06:00',1,'[{\"added\": {}}]',10,1),(247,'2023-09-27 03:01:02.602388','145','Camera #6 on Ryan on 16-09-2023, on 07-11-2023 at 03:00, starting at 06:00',1,'[{\"added\": {}}]',10,1),(248,'2023-09-27 03:01:13.016989','146','Camera #6 on Ryan on 16-09-2023, on 07-11-2023 at 03:00, starting at 06:01',1,'[{\"added\": {}}]',10,1),(249,'2023-09-27 03:01:24.014585','147','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 06:01',1,'[{\"added\": {}}]',10,1),(250,'2023-09-27 03:01:34.964293','148','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 06:01',1,'[{\"added\": {}}]',10,1),(251,'2023-09-27 03:01:43.542015','149','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 06:01',1,'[{\"added\": {}}]',10,1),(252,'2023-09-27 03:01:53.381903','150','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 06:01',1,'[{\"added\": {}}]',10,1),(253,'2023-09-27 03:02:02.194311','151','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 06:01',1,'[{\"added\": {}}]',10,1),(254,'2023-09-30 13:53:09.917654','16','Longtail, examined by Charlie on: 10-05-2021',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',6,1),(255,'2023-09-30 14:42:17.263630','4','Camera #6 on James on 16-09-2023',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',4,1),(256,'2023-09-30 14:42:31.786387','4','James in Kennel #9 entered on 06-12-2022',2,'[{\"changed\": {\"fields\": [\"Dog\"]}}]',8,1),(257,'2023-09-30 21:08:04.114077','90','Axel',3,'',1,1),(258,'2023-10-03 19:21:02.390190','25','Camera #1 on Longtail on 19-09-2023, on 07-10-2023 at 02:32, starting at 22:59',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(259,'2023-10-03 19:21:11.273241','24','Camera #1 on Longtail on 19-09-2023, on 07-10-2023 at 02:32, starting at 22:47',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(260,'2023-10-03 19:22:05.422110','39','Camera #1 on Longtail on 19-09-2023, on 07-10-2023 at 02:32, starting at 22:01',2,'[{\"changed\": {\"fields\": [\"DogStance\"]}}]',10,1),(261,'2023-10-03 19:22:26.550302','18','Camera #1 on Longtail on 19-09-2023, on 07-10-2023 at 02:32, starting at 16:39',2,'[{\"changed\": {\"fields\": [\"DogStance\"]}}]',10,1),(262,'2023-10-03 19:22:36.415803','2','Camera #1 on Longtail on 19-09-2023, on 07-10-2023 at 02:32, starting at 16:12',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(263,'2023-10-03 19:23:19.011142','42','Camera #1 on Longtail on 19-09-2023, on 05-10-2023 at 18:21, starting at 14:00',2,'[{\"changed\": {\"fields\": [\"DogStance\"]}}]',10,1),(264,'2023-10-03 19:23:39.083203','41','Camera #1 on Longtail on 19-09-2023, on 05-10-2023 at 18:21, starting at 14:00',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(265,'2023-10-03 19:23:48.391400','61','Camera #1 on Longtail on 19-09-2023, on 29-09-2023 at 17:56, starting at 12:02',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(266,'2023-10-03 19:23:54.155181','60','Camera #1 on Longtail on 19-09-2023, on 30-09-2023 at 15:56, starting at 12:02',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(267,'2023-10-03 19:24:16.487131','95','Camera #1 on Longtail on 19-09-2023, on 07-10-2023 at 02:32, starting at 04:50',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(268,'2023-10-03 19:24:40.634241','97','Camera #1 on Longtail on 19-09-2023, on 29-09-2023 at 17:56, starting at 04:53',2,'[{\"changed\": {\"fields\": [\"DogLocation\"]}}]',10,1),(269,'2023-10-03 19:26:33.836164','118','Camera #6 on Ryan on 16-09-2023, on 07-11-2023 at 03:00, starting at 05:04',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(270,'2023-10-03 19:26:48.384031','120','Camera #6 on James on 16-09-2023, on 08-11-2023 at 04:00, starting at 05:05',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(271,'2023-10-03 19:26:57.835403','121','Camera #6 on James on 16-09-2023, on 08-11-2023 at 04:00, starting at 05:05',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(272,'2023-10-03 19:27:06.823067','122','Camera #6 on James on 16-09-2023, on 08-11-2023 at 04:00, starting at 05:05',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(273,'2023-10-03 19:27:12.730727','123','Camera #6 on James on 16-09-2023, on 08-11-2023 at 04:00, starting at 05:05',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(274,'2023-10-03 19:27:19.840508','125','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 05:05',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(275,'2023-10-03 19:28:28.171850','152','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 22:28',1,'[{\"added\": {}}]',10,1),(276,'2023-10-03 19:28:36.603765','153','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 22:28',1,'[{\"added\": {}}]',10,1),(277,'2023-10-03 19:28:54.969084','154','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 22:28',1,'[{\"added\": {}}]',10,1),(278,'2023-10-03 19:29:15.816240','155','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 22:29',1,'[{\"added\": {}}]',10,1),(279,'2023-10-03 19:30:26.583039','156','Camera #6 on James on 16-09-2023, on 08-11-2023 at 04:00, starting at 22:30',1,'[{\"added\": {}}]',10,1),(280,'2023-10-03 19:30:38.289863','157','Camera #6 on James on 16-09-2023, on 08-11-2023 at 04:00, starting at 22:30',1,'[{\"added\": {}}]',10,1),(281,'2023-10-03 19:30:59.291701','158','Camera #6 on James on 16-09-2023, on 08-11-2023 at 04:00, starting at 22:30',1,'[{\"added\": {}}]',10,1),(282,'2023-10-03 19:31:14.666207','159','Camera #6 on James on 16-09-2023, on 08-11-2023 at 04:00, starting at 22:31',1,'[{\"added\": {}}]',10,1),(283,'2023-10-03 19:31:34.544322','160','Camera #6 on James on 16-09-2023, on 08-11-2023 at 04:00, starting at 22:31',1,'[{\"added\": {}}]',10,1),(284,'2023-10-03 19:31:48.847699','161','Camera #6 on James on 16-09-2023, on 08-11-2023 at 04:00, starting at 22:31',1,'[{\"added\": {}}]',10,1),(285,'2023-10-03 19:31:59.062293','162','Camera #6 on James on 16-09-2023, on 08-11-2023 at 04:00, starting at 22:31',1,'[{\"added\": {}}]',10,1),(286,'2023-10-03 19:34:15.209473','27','Camera #1 on Longtail on 19-09-2023, on 07-10-2023 at 02:32, starting at 11:50',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(287,'2023-10-03 19:35:39.559558','130','Camera #6 on Ryan on 16-09-2023, on 07-11-2023 at 03:00, starting at 05:06',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(288,'2023-10-03 19:36:54.168109','106','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:02',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(289,'2023-10-03 19:37:00.920028','105','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 05:02',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(290,'2023-10-03 19:37:47.135728','26','Camera #1 on Oscar on 16-09-2023, on 05-11-2023 at 01:00, starting at 04:39',2,'[{\"changed\": {\"fields\": [\"DogStance\", \"DogLocation\"]}}]',10,1),(291,'2023-10-03 19:38:12.693982','8','Camera #1 on Oscar on 16-09-2023, on 19-02-2023 at 00:00, starting at 04:18',2,'[{\"changed\": {\"fields\": [\"DogStance\"]}}]',10,1),(292,'2023-10-03 19:38:54.439874','40','Camera #1 on Longtail on 19-09-2023, on 05-10-2023 at 18:21, starting at 00:59',2,'[{\"changed\": {\"fields\": [\"DogStance\"]}}]',10,1),(293,'2023-10-03 19:38:59.812135','28','Camera #1 on Longtail on 19-09-2023, on 05-10-2023 at 18:21, starting at 01:00',2,'[{\"changed\": {\"fields\": [\"DogStance\"]}}]',10,1),(294,'2023-10-03 19:40:13.763014','159','Camera #6 on James on 16-09-2023, on 08-11-2023 at 04:00, starting at 22:31',2,'[{\"changed\": {\"fields\": [\"DogStance\"]}}]',10,1),(295,'2023-10-03 19:40:18.130869','158','Camera #6 on James on 16-09-2023, on 08-11-2023 at 04:00, starting at 22:30',2,'[{\"changed\": {\"fields\": [\"DogStance\"]}}]',10,1),(296,'2023-10-03 19:40:43.837408','155','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 22:29',2,'[{\"changed\": {\"fields\": [\"DogLocation\"]}}]',10,1),(297,'2023-10-03 19:40:48.341313','154','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 22:28',2,'[{\"changed\": {\"fields\": [\"DogLocation\"]}}]',10,1),(298,'2023-10-03 19:41:01.624219','154','Camera #4 on Julie on 16-09-2023, on 09-11-2023 at 05:00, starting at 22:28',2,'[{\"changed\": {\"fields\": [\"DogLocation\"]}}]',10,1),(299,'2023-12-12 14:28:46.448391','102','ExcelImp',3,'',1,1),(300,'2023-12-12 14:28:46.457241','101','ExcelImp',3,'',1,1),(301,'2023-12-12 14:28:46.462587','100','ExcelImp',3,'',1,1),(302,'2023-12-12 14:28:46.465055','99','ExcelImp',3,'',1,1),(303,'2023-12-12 14:28:46.469999','98','ExcelImp',3,'',1,1),(304,'2023-12-12 14:28:46.473526','95','Axelll',3,'',1,1),(305,'2023-12-12 14:28:46.477564','93','Axel',3,'',1,1),(306,'2023-12-12 14:28:46.481546','91','Axels',3,'',1,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (13,'admin','logentry'),(15,'auth','group'),(14,'auth','permission'),(16,'auth','user'),(17,'contenttypes','contenttype'),(3,'dogs_app','camera'),(1,'dogs_app','dog'),(8,'dogs_app','dogplacement'),(10,'dogs_app','dogstance'),(6,'dogs_app','entranceexamination'),(7,'dogs_app','kennel'),(11,'dogs_app','news'),(9,'dogs_app','observation'),(4,'dogs_app','observes'),(2,'dogs_app','owner'),(12,'dogs_app','profile'),(5,'dogs_app','treatment'),(18,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-07-02 14:42:19.738205'),(2,'auth','0001_initial','2023-07-02 14:42:20.062707'),(3,'admin','0001_initial','2023-07-02 14:42:20.140549'),(4,'admin','0002_logentry_remove_auto_add','2023-07-02 14:42:20.141671'),(5,'admin','0003_logentry_add_action_flag_choices','2023-07-02 14:42:20.141671'),(6,'contenttypes','0002_remove_content_type_name','2023-07-02 14:42:20.188415'),(7,'auth','0002_alter_permission_name_max_length','2023-07-02 14:42:20.235302'),(8,'auth','0003_alter_user_email_max_length','2023-07-02 14:42:20.266859'),(9,'auth','0004_alter_user_username_opts','2023-07-02 14:42:20.282546'),(10,'auth','0005_alter_user_last_login_null','2023-07-02 14:42:20.313810'),(11,'auth','0006_require_contenttypes_0002','2023-07-02 14:42:20.313810'),(12,'auth','0007_alter_validators_add_error_messages','2023-07-02 14:42:20.313810'),(13,'auth','0008_alter_user_username_max_length','2023-07-02 14:42:20.360618'),(14,'auth','0009_alter_user_last_name_max_length','2023-07-02 14:42:20.391890'),(15,'auth','0010_alter_group_name_max_length','2023-07-02 14:42:20.423318'),(16,'auth','0011_update_proxy_permissions','2023-07-02 14:42:20.443221'),(17,'auth','0012_alter_user_first_name_max_length','2023-07-02 14:42:20.475684'),(18,'dogs_app','0001_initial','2023-07-02 14:42:20.569535'),(19,'dogs_app','0002_camera_observes','2023-07-02 14:42:20.663457'),(20,'dogs_app','0003_alter_observes_options','2023-07-02 14:42:20.663457'),(21,'dogs_app','0004_treatment_entranceexamination','2023-07-02 14:42:20.757699'),(22,'dogs_app','0005_kennel_dogplacement','2023-07-02 14:42:20.851530'),(23,'dogs_app','0006_alter_dogplacement_entrancedate_and_more','2023-07-02 14:42:20.851530'),(24,'dogs_app','0007_alter_camera_options','2023-07-02 14:42:20.867165'),(25,'dogs_app','0008_alter_dog_dogimageurl_observation_dogstance','2023-07-02 14:42:21.091609'),(26,'dogs_app','0009_rename_sessiondurationsinmins_observation_sessiondurationinmins','2023-07-02 14:42:21.154248'),(27,'dogs_app','0010_alter_dog_dateofarrival','2023-07-02 14:42:21.169838'),(28,'dogs_app','0011_alter_dog_ownerserialnum','2023-07-02 14:42:21.169838'),(29,'dogs_app','0012_alter_dog_dogname','2023-07-02 14:42:21.279221'),(30,'dogs_app','0013_alter_dog_gender_alter_dog_isdangerous_and_more','2023-07-02 14:42:21.294831'),(31,'dogs_app','0014_news','2023-07-02 14:42:21.310449'),(32,'dogs_app','0015_profile','2023-07-02 14:42:21.341727'),(33,'dogs_app','0016_alter_profile_image','2023-07-02 14:42:21.357325'),(34,'dogs_app','0017_alter_profile_image','2023-07-02 14:42:21.357325'),(35,'dogs_app','0018_remove_dog_dogimageurl_dog_dogimage','2023-07-02 14:42:21.435530'),(36,'dogs_app','0019_alter_dog_dogimage','2023-07-02 14:42:21.471507'),(37,'dogs_app','0020_alter_dog_dogimage_alter_profile_image','2023-07-02 14:42:21.487140'),(38,'dogs_app','0021_alter_profile_image','2023-07-02 14:42:21.487140'),(39,'dogs_app','0022_alter_profile_image','2023-07-02 14:42:21.502793'),(40,'dogs_app','0023_remove_kennel_kennelimageurl_and_more','2023-07-02 14:42:21.596512'),(41,'dogs_app','0024_alter_observation_unique_together_and_more','2023-07-02 14:42:21.799958'),(42,'dogs_app','0025_alter_observation_observes','2023-07-02 14:42:21.878049'),(43,'sessions','0001_initial','2023-07-02 14:42:21.909302'),(44,'dogs_app','0026_alter_dogstance_unique_together_and_more','2023-07-02 19:03:32.798600'),(45,'dogs_app','0027_alter_observes_unique_together_observes_camera_and_more','2023-07-02 21:30:01.667510'),(46,'dogs_app','0028_rename_ownerserialnum_dog_owner_and_more','2023-07-02 22:31:17.754622'),(47,'dogs_app','0029_create_groups','2023-07-28 14:52:29.825569'),(48,'dogs_app','0030_observes_sessiondate','2023-09-16 18:29:37.425354'),(49,'dogs_app','0031_alter_observes_unique_together','2023-09-16 19:39:00.279456'),(50,'dogs_app','0032_alter_observation_sessiondurationinmins','2023-09-17 16:16:09.246358'),(51,'dogs_app','0033_alter_dog_gender_alter_dogstance_doglocation_and_more','2023-10-03 23:39:56.258741'),(52,'dogs_app','0034_alter_dog_gender','2023-10-03 23:43:00.852358'),(53,'dogs_app','0035_alter_owner_phonenum','2023-12-09 13:48:32.116673'),(54,'dogs_app','0036_alter_dog_gender','2023-12-12 14:54:43.788386'),(55,'dogs_app','0037_alter_dog_gender','2023-12-12 14:55:46.085976'),(56,'dogs_app','0038_alter_dog_gender','2023-12-15 11:09:27.097391'),(57,'dogs_app','0039_alter_owner_ownerid','2023-12-17 16:55:06.587717'),(58,'dogs_app','0040_alter_owner_phonenum','2023-12-17 16:56:20.671425');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('00qceq3xxjbqo1nq43jgz4bnfhiw35o3','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qcDZC:RNSX5zChbAO4IbPkf43lGyEfpHmvzaXkJt1C6f5Qs5c','2023-09-15 23:28:42.761549'),('01o34amv19czv35hc206ffpvifwn60ax','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qhqb6:oJK3Z5TQeP6M5_YbANtmiQhZfdBIlQ1sE8Rei8hB4HY','2023-10-01 12:09:56.399038'),('0nxqhst9btogtkzwj26gelzekhda6hh1','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qhZK5:dpppR4A9ru3tLG0M9Pl7bnmYxz51TsAqE2AXjxzhZlU','2023-09-30 17:43:13.421176'),('0nyxy948flwo48kts4o4ysp32trhdige','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qh5d6:8N1CNYvwVSZtncDySZFuQSNsRjZGbTeivcOHOth_Wo4','2023-09-29 10:00:52.845119'),('0w51s6ngq07ujzkx5te4grqka59l18un','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qeP98:hiZF2e6E7hJA7MxpNNceirjkGIxHfxeYUW4YVz6Lf6A','2023-09-22 00:14:50.976272'),('17j07nui0n8homnvoy49i375tndpfd7h','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qc0kh:cc4e9fzWMva_94O2v-0s8WYtAVT6ucj-3qY2NmADns0','2023-09-15 09:47:43.470578'),('1csofkpu8dp0c9jqxr85lyn6og40pztq','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qh889:6EJcR2LRmp21j1r6y8JKLsT3cyHjBPa03yzkq1VFWhg','2023-09-29 12:41:05.952172'),('31xxti2ioou54uapv09m7c9eirfry7yl','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qh4wK:jc-vAxgXKy8iL2OSv0uGHKd5I5gohoKxtmFF1JiMMPU','2023-09-29 09:16:40.473643'),('3bpf19t06sf2165ss5zipsefapki1cnu','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qcv5u:3Mv1N-vIdGu8vdBFUWcsCFp4kcbptP-NeQu3-qtxN9U','2023-09-17 21:57:22.597178'),('479u44owze0xynmh8h80o5593hpl2raj','.eJxVjruOg0AUQ_9lagtx7zzgpkyfL4giNMwjsIlAYkgV5d93kFLsNi7sY8tvNfjXPg2vkrZhjuqkSOGvN_rwSMsRxB-_3NcmrMu-zWNzIM03Lc1ljel5_rL_BiZfptoOzvkovc1tpqzFsRFpHXM0xvTaGNbWsjD74PpstIyppZDGTmLHbLrjVZ6fe9pSHOJ6L_VsUacrQcNAQBbEIAIJepADVdWgDtSiSmUIoiEWFu72-QU03UkW:1r5ua8:wbleNQDim4ut-DHsggrOj81fmd3ghZrwDkLGC9vS004','2023-12-06 21:16:24.546939'),('4mo6nr4o027fme6mtvt5vvw640f4jxev','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qc6I1:J9rqvjGpdFTWpM1PGSRySCEXvWIvEZMpsUL_05-Id94','2023-09-15 15:42:29.147347'),('50i7ob9noyku0wq25427uoge9zg832rd','.eJxVjr0OgzAQg98l8wn18kOAsXufoKrQkbsALQKJwFT13RskhnbxYH-2_FYt7dvQ7knWdmTVKFTw63UUXjIfAT9p7pciLPO2jl1xIMWZpuK2sEzXk_0bGCgNue1El1FzEKxrz85FJ6RNJApVhcaSZlNGK-i89ciuixRDJQHJRzJB-zwax2mTVbjlpU_5bFLNHcGAhRrQAWpABKyhAiwBsxpAD3iBLBYclI_PF5mLSbA:1rIWjV:2jgljA-4jrh_5Q_tz_DFWKUW4PVfSNbDmm2rC8t1ouE','2024-01-10 16:26:13.928001'),('52oj71z1jtj6eupeq3beewkgcf49s80f','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qcsvj:o4WXVGXIlptznQ75WNMfnVhASgT86n4GJ1MD-bJRIIg','2023-09-17 19:38:43.941966'),('5wk3mzkev1672y1byd4pl3kfnjx49g1b','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qcwZM:L3kpyjObrLKpnkGFdWhtC_H_1IrtbDB9WmCafCEETjI','2023-09-17 23:31:52.483165'),('6r0mo0heltiyze9h3tfvum8u80vyb4qg','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qez8C:M9cb9adAwOdQ0L7dV1C09UQZ_A6kO069uYUH0aFt84w','2023-09-23 14:40:16.791064'),('77n1p8ebzegdx4h1s4v6lgcl145okreu','.eJxVjr0OgzAQg98l8wn18kOAsXufoKrQkbsALQKJwFT13RskhnbxYH-2_FYt7dvQ7knWdmTVKFTw63UUXjIfAT9p7pciLPO2jl1xIMWZpuK2sEzXk_0bGCgNue1El1FzEKxrz85FJ6RNJApVhcaSZlNGK-i89ciuixRDJQHJRzJB-zwax2mTVbjlpU_5bFLNHcGAhRrQAWpABKyhAiwBsxpAD3iBLBYclI_PF5mLSbA:1rLiCq:Ds0wbDdxCxobp-ABs_9X2EG6UF_ULOsg-94Y2QvYvPU','2024-01-19 11:17:40.070220'),('8do9pn9rzar3fezzaash3lu9kqgxlfyb','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qcwYH:bUEGuFyLDDhjEFx2gNj52Zz3jWjigMJP-xt6QexbFv4','2023-09-17 23:30:45.159464'),('8epzos0kwrvi6h5mn7o38h4dhgrx8exq','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qgssV:HVDKgAW7k68MF9_7-ftxXy_b3ngnkT5BlGB74iXXBAU','2023-09-28 20:23:55.603707'),('8oht380xns7bstkpzjkjxltmjkgrvz0a','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qeNeS:_I_g7du0ZblUjcFVx4XdoFYefvHZca78xoCPrNz6hAQ','2023-09-21 22:39:04.795995'),('9apaug3asngr6qeo8du7mvca5twal6d9','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qdH6C:XNy7s4Czg-bi7_sS-eo3ahbEHOYof6D177Y63vrJ9OU','2023-09-18 21:27:08.257028'),('a5qiqyzu6iigmka97reyr6dutwrm0q1k','.eJxVjr0OgzAQg98l8wn18kOAsXufoKrQkbsALQKJwFT13RskhnbxYH-2_FYt7dvQ7knWdmTVKFTw63UUXjIfAT9p7pciLPO2jl1xIMWZpuK2sEzXk_0bGCgNue1El1FzEKxrz85FJ6RNJApVhcaSZlNGK-i89ciuixRDJQHJRzJB-zwax2mTVbjlpU_5bFLNHcGAhRrQAWpABKyhAiwBsxpAD3iBLBYclI_PF5mLSbA:1rJud2:vXIUL2K2k_8l_nXoa-b5e8xvmZAiRkOUU6hjMTa6Qyc','2024-01-14 12:09:16.588692'),('a7iu4j70ikeox9xeifrnlra97l1hm5mv','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qf5Al:BLcIJMUzF6ZEbh8KlhykpRdPNIOaoEViD9CFUrvdLKE','2023-09-23 21:07:19.208910'),('adh5i7ngptdramg6n8hvz3y46h8s7fqs','.eJxVjruOg0AUQ_9lagtx7zzgpkyfL4giNMwjsIlAYkgV5d93kFLsNi7sY8tvNfjXPg2vkrZhjuqkSOGvN_rwSMsRxB-_3NcmrMu-zWNzIM03Lc1ljel5_rL_BiZfptoOzvkovc1tpqzFsRFpHXM0xvTaGNbWsjD74PpstIyppZDGTmLHbLrjVZ6fe9pSHOJ6L_VsUacrQcNAQBbEIAIJepADVdWgDtSiSmUIoiEWFu72-QU03UkW:1qnwQ3:ufVAIXZvfoXWorhsoPMD7FaMmcsnZpMAfWjG83hBYzY','2023-10-18 07:35:43.376731'),('adrg66w93zkghyrb6i3lhjazgll7nsti','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qZv70:3Xt4D0rMF1fEZnf8a59m0HnWIt5WnjGgZPhWkYWOMWI','2023-09-09 15:22:06.761142'),('awc75qpxtztvo0853g13h93jky77r9i3','.eJxVjr0OgzAQg98l8wn18kOAsXufoKrQkbsALQKJwFT13RskhnbxYH-2_FYt7dvQ7knWdmTVKFTw63UUXjIfAT9p7pciLPO2jl1xIMWZpuK2sEzXk_0bGCgNue1El1FzEKxrz85FJ6RNJApVhcaSZlNGK-i89ciuixRDJQHJRzJB-zwax2mTVbjlpU_5bFLNHcGAhRrQAWpABKyhAiwBsxpAD3iBLBYclI_PF5mLSbA:1rJui2:TP4dg9TAMgyiCmbWiKo3gmDcNia-sPfuTFV6e9bYuw8','2024-01-14 12:14:26.855906'),('c09u6qdnh00nryca35ilxjn19ih5ofd7','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qfMHp:m8jCClOdB49j4kDJ_mtSbmfEmS_Rt55IKLskSKxae28','2023-09-24 15:23:45.060294'),('c5w9yvau21g3m8cq4o56bollqzvuct7f','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1rBxbh:DZO-Irac581sS2lsFxlJeKE4gr0EEePH73UjtGkpHN8','2023-12-23 13:43:01.031269'),('cx7lhfydpamaheaj2ymsjnzsxwvr7qh3','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qhwBC:RRwRDNgm7adcfc1HF4pX5AjJPxTJYW8UsEpjNeJW0R8','2023-10-01 18:07:34.767917'),('db9dkb2yty9cujm81zqxoi7q50njv8e4','.eJxVjr0OgzAQg98l8wn18kOAsXufoKrQkbsALQKJwFT13RskhnbxYH-2_FYt7dvQ7knWdmTVKFTw63UUXjIfAT9p7pciLPO2jl1xIMWZpuK2sEzXk_0bGCgNue1El1FzEKxrz85FJ6RNJApVhcaSZlNGK-i89ciuixRDJQHJRzJB-zwax2mTVbjlpU_5bFLNHcGAhRrQAWpABKyhAiwBsxpAD3iBLBYclI_PF5mLSbA:1rIFWO:VMjZIq2YmjWzBWBycHb38lsAGhwICRDxbBGrXXVpPHA','2024-01-09 22:03:32.932429'),('ex0yxqzwmckcpbk3mqewzghx36cc3uah','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qfMno:PIunqDSBQjdvPiSXwNfN6221N-D9Zken-j1mIWqG4IY','2023-09-24 15:56:48.409093'),('ffcruyh1xx9v6hjlna7mf8xlklx77eib','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qcwVM:yqubPhd5LwN9t2psgK346cSWGCKnqpXL_1EoWoBk6G8','2023-09-17 23:27:44.432736'),('fq5u3yo4dck71hinc81yilpyw51yg34i','.eJxVjr0OgzAQg98l8wn18kOAsXufoKrQkbsALQKJwFT13RskhnbxYH-2_FYt7dvQ7knWdmTVKFTw63UUXjIfAT9p7pciLPO2jl1xIMWZpuK2sEzXk_0bGCgNue1El1FzEKxrz85FJ6RNJApVhcaSZlNGK-i89ciuixRDJQHJRzJB-zwax2mTVbjlpU_5bFLNHcGAhRrQAWpABKyhAiwBsxpAD3iBLBYclI_PF5mLSbA:1rHYYB:5CKh5oPX-lN8JYmBS1yjA6NFScQ2hEZJNXadHA0xM04','2024-01-08 00:10:31.644070'),('g0pmp2yieu5bwh8a7nsgmmb7pd6y5cvs','.eJxVjr0OgzAQg98l8wn18kOAsXufoKrQkbsALQKJwFT13RskhnbxYH-2_FYt7dvQ7knWdmTVKFTw63UUXjIfAT9p7pciLPO2jl1xIMWZpuK2sEzXk_0bGCgNue1El1FzEKxrz85FJ6RNJApVhcaSZlNGK-i89ciuixRDJQHJRzJB-zwax2mTVbjlpU_5bFLNHcGAhRrQAWpABKyhAiwBsxpAD3iBLBYclI_PF5mLSbA:1rHnok:kbgYC6QKoNL0uJx0zIySdvPmFMmXDuUnkq1s09NDLxE','2024-01-08 16:28:38.021949'),('galkvn8ivf6a2qulva1047k4t0uei217','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qctfs:H4r6HNwCLZKS_W1fevehxYYrNDwLidDSGuHJC8ayfOw','2023-09-17 20:26:24.139284'),('gku2zn4rnmqglwp3x02y2ovs7kqp308h','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qeyRx:Rm-EVWIFLcOxYSOW5gCSCTmcNkF9xMe76vcesh59s-w','2023-09-23 13:56:37.647804'),('gmv8ym4gvlbpf52le5o4p1pm1chsmdee','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qewdF:1J50dGMWy701FmfSY7gq-Qr5XbDgYQeYNKRmngrc6N8','2023-09-23 12:00:09.703941'),('gqiwxfab9zs593q1q0diyw8kkdd0iqvg','.eJxVjMsOwiAUBf-FtSEBSqEu3fsN5HIfUjWQlHZl_Hdt0oVuz8ycl0qwrSVtnZc0kzoro06_WwZ8cN0B3aHemsZW12XOelf0Qbu-NuLn5XD_Dgr08q0921EsIZtpCuS9eAbrBABjNG4AS26UgY0PQzDks4BgZDQQBBzaoN4f-6s4xg:1rLQf8:PB7IGhQ21URZS5MF0X-JqU9oLPstz91czwPonokLlvs','2024-01-18 16:33:42.220626'),('grnyz0ecuzy46tc87fxbdwcg92t7rkgd','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qfMQL:exeiIGbT7g8BpDsXlen2_tJqzYJZKFma0AQattLqOms','2023-09-24 15:32:33.357033'),('h7zlk9iomi0yfis0pjxom580afo8v996','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qcC4e:feq8Cxolf06qFmUXrJAiDVb0jSgpGY_1j3-ThH2dPPM','2023-09-15 21:53:04.860438'),('hb3qzm195cqyys06dpfab526x6wah8yb','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qcD2F:doujw_lzyDQKTFq_UVC-F8cfYhDBmtwUyEVjPuShlgo','2023-09-15 22:54:39.208981'),('hep4xh15ytyt2gilv2ejregt0gabvjn0','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qhwBD:lnKg-Nfrw7QpuD2d5S0crFmaniG9ppw3yzqIyf-JP3k','2023-10-01 18:07:35.069396'),('igmkyv3rnrqtqdul8zrf2k6j5hvk5q5a','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qeP0I:2eEkV2JfQZCjMBOoq6GrLhZTRyL4P9twYiPRy1vDp0M','2023-09-22 00:05:42.056057'),('ine0r2ruy6rar0syojm3yd5urd7c8f32','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qdKPx:06iHnjtK78AP8XUxX_X7Gx-B51kIyyLfyHsVRm-ycqw','2023-09-19 00:59:45.781289'),('j5jr176ergi582pybbrduu08o6tmkoqu','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qc3PU:1XhVNeyQUKVpk6Q4Nq_lV68_fHJeS2eS04EVs02oauk','2023-09-15 12:38:00.256673'),('j8hoydfsummdhaxl03vzowuk9pzl3fej','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qeiN2:kRrvupqtcW9dNK6ao3_cljoVCSHy3bXYz-8MRQdMh1U','2023-09-22 20:46:28.635753'),('j9j9neb41lwfd9mw74r1vf8q6579na2z','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qHO5b:TqsZ_9iIqC-ZWKvF6rj-Dbp8TLfZRm9c-o4oK1xBJ88','2023-07-20 12:28:03.640079'),('jf405map0z9pdx760hmsa8ynxx6o2d67','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qcvrT:TUv-JHL3ETu9c9XT2idRpZc2y-5YoZvA7hPFhkdS1Hk','2023-09-17 22:46:31.901100'),('k53c9ozq2lyg9uh5auhedoh9r6f840ch','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qgrga:ywLotT_LWLPpZPc-WgzEdJ_EIKHhTAjYJbanRehDtU0','2023-09-28 19:07:32.006226'),('k6adhi6vh5lz9z8uavpuyee01fbc9bkc','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qcxPv:7AgjF-zKSg2C0DV57ebcmrcV56f4ihpLkvSmGBUd9nA','2023-09-18 00:26:11.774003'),('kglycrjh7yomyt7hcy8lsolnoqj8c0dx','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qc6AK:IpCTPngGAlYesnoKqVl6YbhU8-os3wQTPSEWhUaMwn4','2023-09-15 15:34:32.406084'),('kslry6xuati67g4cvgegls8tkjawqchz','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qcn5i:-gidfMwZbkOTgEXyM6MA45T1d2y6rIJnumCeBWZFYzM','2023-09-17 13:24:38.429929'),('maauykvoymn7dz7i341p67i11udnfoq0','.eJxVjr0OgzAQg98l8wn18kOAsXufoKrQkbsALQKJwFT13RskhnbxYH-2_FYt7dvQ7knWdmTVKFTw63UUXjIfAT9p7pciLPO2jl1xIMWZpuK2sEzXk_0bGCgNue1El1FzEKxrz85FJ6RNJApVhcaSZlNGK-i89ciuixRDJQHJRzJB-zwax2mTVbjlpU_5bFLNHcGAhRrQAWpABKyhAiwBsxpAD3iBLBYclI_PF5mLSbA:1rLVFw:kRH5O-4ZyYfKf6jEcGcLNHitdetza4PCh1L2nAmGpMU','2024-01-18 21:28:00.914329'),('nhgc836j2wura6x0waxbkde8vcw9ifpz','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qGTDt:o0LJS7h8_wn7zdHVklHubhvNllBfdOMKIhqx4AR6KoU','2023-07-17 23:44:49.315833'),('nl0nkxjxcrucau2bn5cib7oyfod9b78o','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qiB6K:ovNF67Iur7XurwFxpzei-EgVwVgLqXY-ngqbU_9sUYA','2023-10-02 10:03:32.854561'),('nq3dz5cw1yaihbs0og0e3rg9ak3l5nmx','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qiwO3:pNbys7uNi7Iyx9LECz8l_MY9EqAjMX6hacWWbC8OZig','2023-10-04 12:32:59.931024'),('o0kg0kqqppyfsr694jgys4e2zwqzejw7','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qdKTA:n1DPDaFq69_U76QOVpLmPHQpRv7ngrRa7b8-pQoadcY','2023-09-19 01:03:04.911091'),('o7kajrwfxoo7vhnnwg8ye0uu6ldr44pc','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qdJeX:ylNT0ZjNerI210TZXR2eXv5NIckSQko-FggbQQMij1o','2023-09-19 00:10:45.151384'),('okh70skabyepypkgiqvhfb9kw05i3za1','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qfnnu:3yhGxx4YxL9U99v3m_ZYI_HKrukgI5ni2GZ1qHGG_FE','2023-09-25 20:46:42.523340'),('p9evkx0t7p5c1shz56wwdh3av7rmwxzl','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qc6Fm:8HNLijxZ9Y4-blQwZt_7yh5Q5wDYbC5uMX_BkM6LdRY','2023-09-15 15:40:10.553899'),('pnbaaxmigacywpby9gwcj7dikz5up9ba','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qUqHG:ls2Taf0VIxgfKN5Hr3oouQaNTTN2OO-mWtdClNBr5fs','2023-08-26 15:11:42.029293'),('py1symy5h8jud3zi5510qvkhb2vbgdt0','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qhHAU:OQWhz9PsqtCJ1Ae2eSPh7NDjm9O1g9yn0Nwqn_NknoI','2023-09-29 22:20:06.278488'),('qecy4ben8iq123ro5m2qbxojil3d503b','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qhzr6:4LaN6Cf08ClQTHxnFSpCuNGNkxKbbnT0pXCS3MzhXEM','2023-10-01 22:03:04.563610'),('qlveo5ilg3g8tas3li5jugfsdkmgo73m','.eJxVjr0OgzAQg98l8wn18kOAsXufoKrQkbsALQKJwFT13RskhnbxYH-2_FYt7dvQ7knWdmTVKFTw63UUXjIfAT9p7pciLPO2jl1xIMWZpuK2sEzXk_0bGCgNue1El1FzEKxrz85FJ6RNJApVhcaSZlNGK-i89ciuixRDJQHJRzJB-zwax2mTVbjlpU_5bFLNHcGAhRrQAWpABKyhAiwBsxpAD3iBLBYclI_PF5mLSbA:1rLQfE:Me3KoT8zom2F1lRhN0XpysP1xFsN_xACjlCPWw7Znnk','2024-01-18 16:33:48.336928'),('qmqkmbtsw0zplfyz9cbbj3thi504j06h','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qdH4s:B8I2yYIArejQPc3zVRS7m4uIMDL4Do7u1jyZp__6nDs','2023-09-18 21:25:46.862538'),('qyhlvc67j84afv47jneb1xgans55h1go','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qfOI3:hApB_P8qdqvFThgDBINi-bEMbcSqk0XgHTDL08Ai-sE','2023-09-24 17:32:07.273896'),('r2lnebsksv1wfrysiq7gtzsy3ewht4d8','.eJxVjr0OgzAQg98l8wn18kOAsXufoKrQkbsALQKJwFT13RskhnbxYH-2_FYt7dvQ7knWdmTVKFTw63UUXjIfAT9p7pciLPO2jl1xIMWZpuK2sEzXk_0bGCgNue1El1FzEKxrz85FJ6RNJApVhcaSZlNGK-i89ciuixRDJQHJRzJB-zwax2mTVbjlpU_5bFLNHcGAhRrQAWpABKyhAiwBsxpAD3iBLBYclI_PF5mLSbA:1rJvda:dHJvAbtfFMlophZi0AY9Tee5IVn39SI0_dRTO0LHqzA','2024-01-14 13:13:54.475475'),('sli747b2da2ktvigldllfww9ndt97q8q','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qc69N:BvY04HpIjMb6-WPyX4VkxGczpfMcfMYgLJfH-wWpTfw','2023-09-15 15:33:33.921758'),('sncnzvaefpilbrekjwojzuzs257yptae','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qlLT6:NuDRqefP0Dh9VX952WTZPplVoa9rFnbEtXLXqP6xqWg','2023-10-11 03:44:08.893871'),('tmi7ufp9bj9d75960xsk9c5nqkvwasuf','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qiFn0:aNQIh_tYjY4wcVamS0bfGNhqavMM4lbW-HOJmXnnx_o','2023-10-02 15:03:54.301876'),('tu3v9qp5lpxcqadb9lx3lxb811hdee7b','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qjQpY:a_2NuQf4yXVLt4bxN3B85Ornn0GkSAB2K6burq6oUOQ','2023-10-05 21:03:24.664818'),('tuek5n4joexsedog15nj4jbd66pvgvpp','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qc6H4:sPl-cPEskx5JXc008eJbZydmAY1BKYUIdmwEAAbOWwo','2023-09-15 15:41:30.026079'),('ue8k4t5fd2ies6g9r6vut14vrykqunez','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qf4Zp:BIX1wR2v9p9SvFi-UAa2EibUV4rLLMkAx1Ym2Ha_5bQ','2023-09-23 20:29:09.262650'),('v00cotagwhets88i2hm10528jxfo1thp','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qiF2D:Z2LYKmlIsPLphWu5TDFeID8Pwk95VdBQAKO0pjV7S1w','2023-10-02 14:15:33.691962'),('w7j21x3f9rbi793qmne5njgkaclwlblv','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qGRv7:1F8KxXpHK7N2UaLx1CnOFy5dCwPPHO1Tz3a1Al9Aqug','2023-07-17 22:21:21.118460'),('x4gryhe0lw50h6ripwu051yeg0vlkpyn','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qcDZB:McxLzfybhMuUxnaxOWuqJo0BxXQRh3DYw6EEUjxUh9E','2023-09-15 23:28:41.999462'),('xf2e5esawcspqq55892seso5e34kp6ov','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qiKdf:QMaA2HlrUK8h34VbiiDgp9dETd59ODQ_iiQIjr4RR-w','2023-10-02 20:14:35.111002'),('xvaymeidrgf013oc1ssf323rbfxjws5r','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qiDmW:CL1M6PWonvnohYcf8K_5jKtVrdcWGnkv9ovCD6ttulg','2023-10-02 12:55:16.407149'),('zfj4m3gq1es3hlqptonsvf7zkmuh17zc','.eJxVjDsOwjAQBe_iGln2ev1ZSnrOYPmLA8iR4qRC3B0ipYD2zcx7MR-2tfltlMVPmZ2ZZKffLYb0KH0H-R76beZp7usyRb4r_KCDX-dcnpfD_TtoYbRvnYwJmZyuosqqyAASCQOQEdEpRFBaAwGEZFxFRbEImUq0lC0AWsneH7I3NmQ:1qgsag:JYFcjDNb5WCu3w3cfq4Ib9rBDswJMOOdV2evrUo8obY','2023-09-28 20:05:30.314051');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dogs_app_camera`
--

DROP TABLE IF EXISTS `dogs_app_camera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dogs_app_camera` (
  `camID` smallint unsigned NOT NULL,
  PRIMARY KEY (`camID`),
  CONSTRAINT `dogs_app_camera_chk_1` CHECK ((`camID` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dogs_app_camera`
--

LOCK TABLES `dogs_app_camera` WRITE;
/*!40000 ALTER TABLE `dogs_app_camera` DISABLE KEYS */;
INSERT INTO `dogs_app_camera` VALUES (1),(2),(3),(4),(5),(6),(7);
/*!40000 ALTER TABLE `dogs_app_camera` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dogs_app_dog`
--

DROP TABLE IF EXISTS `dogs_app_dog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dogs_app_dog` (
  `dogID` int NOT NULL AUTO_INCREMENT,
  `chipNum` varchar(30) DEFAULT NULL,
  `dogName` varchar(35) NOT NULL,
  `dateOfBirthEst` date DEFAULT NULL,
  `dateOfArrival` date DEFAULT NULL,
  `dateOfVaccination` date DEFAULT NULL,
  `breed` varchar(30) DEFAULT NULL,
  `gender` varchar(1) DEFAULT NULL,
  `furColor` varchar(20) DEFAULT NULL,
  `isNeutered` varchar(1) DEFAULT NULL,
  `isDangerous` varchar(1) DEFAULT NULL,
  `kongDateAdded` date DEFAULT NULL,
  `owner_id` int DEFAULT NULL,
  `dogImage` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`dogID`),
  UNIQUE KEY `chipNum` (`chipNum`),
  KEY `dogs_app_dog_owner_id_c6b52089_fk_dogs_app_owner_ownerSerialNum` (`owner_id`),
  CONSTRAINT `dogs_app_dog_owner_id_c6b52089_fk_dogs_app_owner_ownerSerialNum` FOREIGN KEY (`owner_id`) REFERENCES `dogs_app_owner` (`ownerSerialNum`)
) ENGINE=InnoDB AUTO_INCREMENT=554 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dogs_app_dog`
--

LOCK TABLES `dogs_app_dog` WRITE;
/*!40000 ALTER TABLE `dogs_app_dog` DISABLE KEYS */;
INSERT INTO `dogs_app_dog` VALUES (1,'123123123','Longtail','2019-03-06','2023-08-23','2023-06-10','Dalmatian','M','White','Y','N','2023-06-29',1,'dog_pictures/longtail_elJzWez.jpg'),(3,'0123456789','Max','2023-05-13','2023-08-15','2021-01-06','German Shepherd','M','Brown','Y','N','2022-01-26',2,'dog_pictures/max_TY77wz2.jpg'),(4,'98765432101','Oscar','2020-03-11','2023-08-14','2021-05-05','Husky','M','Black','Y','Y','2020-10-15',2,'dog_pictures/oscar_s79qzsj.jpg'),(5,'5678901234','Ryan','2019-03-15','2019-01-14','2011-06-06','Golden Retriever','F','White','N','','2021-09-06',1,'dog_pictures/ryan_cmHzRon.jpg'),(6,'987650143','Bryan','2021-03-10','2018-04-14','2022-01-01','Mastiff','F','Gray','N','','2022-12-12',3,'dog_pictures/bryan_YhZkRw1.jpg'),(7,'18893700','Craig','2023-02-18','2020-10-10','2022-06-19','Husky','F','Gray','N','N','2023-06-12',9,'dog_pictures/christian-bowen-JTq2E4A5fWs-unsplash.jpg'),(8,'71718691','Darlene','2019-09-05','2021-05-22','2022-10-14','Dachshund','F','Gray','N','N','2022-09-27',9,'dog_pictures/andre-tan-ZQ_0jk66-1E-unsplash.jpg'),(9,'45082623','Julie','2019-11-09','2022-04-06','2022-12-31','Husky','F','Brown','N','N','2023-02-24',10,'dog_pictures/jamie-street-n4TfO-ITgPc-unsplash.jpg'),(10,'19735153','Cynthia','2022-01-09','2020-10-16','2022-02-03','Boxer','M','Black','N','Y','2022-09-14',8,'dog_pictures/kojirou-sasaki-DLdDrb2d4F4-unsplash.jpg'),(11,'20991443','Bonnie','2018-08-30','2021-06-14','2023-03-21','Boxer','M','White','Y','N','2022-08-19',3,'dog_pictures/minnie-zhou-E_YBgxDRVbM-unsplash.jpg'),(12,'54029988','Paige','2020-06-11','2021-07-16','2023-03-10','Dachshund','F','Black','N','N','2023-06-27',9,'dog_pictures/charlesdeluvio-lJJlaUWYrPE-unsplash.jpg'),(13,'40012472','Melissa','2021-01-17','2021-02-11','2022-02-23','Golden Retriever','M','Spotted','N','Y','2022-09-13',14,'dog_pictures/izabelly-marques-Ytp_K5bwa0Q-unsplash.jpg'),(14,'72124425','Christopher','2022-04-22','2020-07-22','2022-01-26','Dachshund','M','White','N','Y','2022-09-05',4,'dog_pictures/julio-bernal-qeY2QHAZfU0-unsplash.jpg'),(15,'30390919','Lindsay','2021-02-23','2021-10-29','2022-04-07','Dachshund','F','Brown','Y','N','2023-06-25',8,'dog_pictures/niki-sanders-5Fq4QaSTjPE-unsplash.jpg'),(16,'48225250','Jessica','2022-02-20','2021-05-15','2023-02-04','Golden Retriever','M','White','N','Y','2022-12-15',8,'dog_pictures/rafael-forseck-qVfSbJjtocI-unsplash.jpg'),(17,'62282994','Leah','2020-10-31','2020-12-17','2021-10-06','Husky','M','Black','Y','Y','2022-07-25',12,'dog_pictures/lucrezia-carnelos-8dZRksE0lEg-unsplash.jpg'),(18,'83660238','James','2023-06-17','2021-02-27','2022-11-26','Golden Retriever','F','Spotted','Y','Y','2022-11-16',16,'dog_pictures/fredrik-ohlander-tGBRQw52Thw-unsplash.jpg'),(19,'','Timmy',NULL,'2021-06-01',NULL,'','M','','','',NULL,NULL,'dog_pictures/default_dog.jpg');
/*!40000 ALTER TABLE `dogs_app_dog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dogs_app_dogplacement`
--

DROP TABLE IF EXISTS `dogs_app_dogplacement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dogs_app_dogplacement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `entranceDate` date NOT NULL,
  `expirationDate` date DEFAULT NULL,
  `placementReason` varchar(75) DEFAULT NULL,
  `dog_id` int DEFAULT NULL,
  `kennel_id` smallint unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dogs_app_dogplacement_dog_id_kennel_id_entranc_c6cafcb1_uniq` (`dog_id`,`kennel_id`,`entranceDate`),
  KEY `dogs_app_dogplacemen_kennel_id_788a46dd_fk_dogs_app_` (`kennel_id`),
  CONSTRAINT `dogs_app_dogplacemen_kennel_id_788a46dd_fk_dogs_app_` FOREIGN KEY (`kennel_id`) REFERENCES `dogs_app_kennel` (`kennelNum`),
  CONSTRAINT `dogs_app_dogplacement_dog_id_30ee7aeb_fk_dogs_app_dog_dogID` FOREIGN KEY (`dog_id`) REFERENCES `dogs_app_dog` (`dogID`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dogs_app_dogplacement`
--

LOCK TABLES `dogs_app_dogplacement` WRITE;
/*!40000 ALTER TABLE `dogs_app_dogplacement` DISABLE KEYS */;
INSERT INTO `dogs_app_dogplacement` VALUES (1,'2023-07-01','2023-07-10','Behavioral Study',7,6),(2,'2023-05-01','2023-05-07','This is an evil dog that likes to bite',4,2),(3,'2023-02-10','2023-02-17',NULL,8,6),(4,'2022-12-06','2022-12-08','Very protective of his bed',18,9),(5,'2022-12-16','2022-12-18','Arrested for being too handsome',10,8),(6,'2020-08-02','2020-09-15','Abandoned in the street',4,5),(8,'2023-04-13','2023-05-26','This is an evil dog that likes to bite',5,4),(9,'2023-03-01','2023-05-22','Owner is irresponsible',7,5),(10,'2020-11-13','2021-01-09','Arrested for being too handsome',17,12),(12,'2021-04-22','2021-07-05','Likes to howl at night',15,11),(13,'2022-05-04','2022-05-21','This is an evil dog that likes to bite',6,9),(14,'2023-01-12','2023-02-12','Likes to howl at night',9,7),(15,'2022-04-07','2022-04-18','This is an evil dog that likes to bite',12,10),(16,'2023-09-15','2023-09-17','Behavioral Study',1,11),(17,'2023-09-11','2023-09-14','No Reason',1,10),(19,'2023-09-16',NULL,NULL,1,9),(26,'2023-08-29',NULL,NULL,1,12),(27,'2023-08-29',NULL,NULL,1,7),(30,'2023-09-22',NULL,'Behavioral Study',NULL,4),(31,'2023-09-16',NULL,'Behavioral Studies',NULL,6),(32,'2023-09-22','2023-09-27','Behavioral Study',NULL,4),(33,'2023-09-16','2023-09-23','Behavioral Studies',NULL,6),(34,'2023-09-22','2023-09-27','Behavioral Study',NULL,16),(35,'2023-09-16','2023-09-23','Behavioral Studies',NULL,17),(36,'2023-09-22','2023-09-27','Behavioral Study',NULL,16),(37,'2023-09-16','2023-09-23','Behavioral Studies',NULL,17),(38,'2023-09-22','2023-09-27','Behavioral Study',NULL,16),(39,'2023-09-16','2023-09-23','Behavioral Studies',NULL,17),(44,'2023-09-22','2023-09-27','Behavioral Study',NULL,16),(45,'2023-09-16','2023-09-23','Behavioral Studies',NULL,17);
/*!40000 ALTER TABLE `dogs_app_dogplacement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dogs_app_dogstance`
--

DROP TABLE IF EXISTS `dogs_app_dogstance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dogs_app_dogstance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `stanceStartTime` time(6) NOT NULL,
  `dogStance` varchar(15) NOT NULL,
  `dogLocation` varchar(10) DEFAULT NULL,
  `observation_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dogs_app_dogstance_observation_id_stanceStartTime_9fc9b763_uniq` (`observation_id`,`stanceStartTime`),
  CONSTRAINT `dogs_app_dogstance_observation_id_01f09501_fk_dogs_app_` FOREIGN KEY (`observation_id`) REFERENCES `dogs_app_observation` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=186 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dogs_app_dogstance`
--

LOCK TABLES `dogs_app_dogstance` WRITE;
/*!40000 ALTER TABLE `dogs_app_dogstance` DISABLE KEYS */;
INSERT INTO `dogs_app_dogstance` VALUES (1,'07:49:52.000000','WALKING_AROUND','BENCH',17),(2,'16:12:05.000000','SLEEPING_LYING','FLOOR',16),(3,'22:45:49.000000','PACING','BENCH',16),(4,'10:26:49.000000','STANDING','FLOOR',16),(5,'01:25:30.000000','ALERT','FLOOR',16),(6,'07:43:46.000000','JUMPING','BENCH',NULL),(7,'19:00:12.000000','JUMPING','ELSE',16),(8,'04:18:31.000000','WALKING_AROUND','FLOOR',3),(9,'22:03:10.000000','ELSE','ONBARS',16),(10,'18:45:02.000000','STANDING','ONBARS',16),(11,'10:55:13.000000','PACING','FLOOR',16),(12,'06:45:41.000000','CIRCLING','ONBARS',11),(13,'05:00:25.000000','EATING','WALLTOWALL',NULL),(14,'15:48:23.000000','SLEEPING_LYING','ONBARS',16),(15,'12:20:42.000000','ALERT','FLOOR',16),(16,'10:01:45.000000','ALERT','ONBARS',10),(17,'00:56:13.000000','JUMPING','WALLTOWALL',4),(18,'16:39:58.000000','SLEEPING_LYING','FLOOR',16),(19,'07:35:35.000000','ALERT',NULL,6),(20,'01:38:23.000000','PACING','ONBARS',16),(21,'01:12:54.000000','STANDING','FLOOR',5),(22,'01:12:54.000000','WALKING_AROUND','ONBARS',16),(23,'22:46:00.000000','STANDING','ONBARS',16),(24,'22:47:00.000000','SITTING','WALLTOWALL',16),(25,'22:59:00.000000','SITTING','WALLTOWALL',16),(26,'04:39:41.000000','CIRCLING','BENCH',58),(27,'11:50:00.000000','ALERT','BENCH',16),(30,'06:00:00.000000','STANDING','WALLTOWALL',56),(34,'01:02:00.000000','SITTING','BENCH',56),(39,'22:01:00.000000','SLEEPING_LYING','FLOOR',16),(41,'14:00:00.000000','SITTING','WALLTOWALL',56),(42,'14:00:02.000000','SLEEPING_LYING','FLOOR',56),(43,'14:00:07.000000','SLEEPING_LYING','BENCH',56),(44,'14:00:09.000000','SLEEPING_LYING','FLOOR',56),(45,'12:00:57.000000','EATING','ONBARS',56),(46,'12:00:52.000000','CIRCLING','ELSE',56),(47,'12:00:59.000000','SITTING','WALLTOWALL',55),(49,'12:00:58.000000','WALKING_AROUND','BENCH',42),(51,'12:00:04.000000','STANDING','BENCH',40),(54,'08:00:00.000000','EATING','FLOOR',40),(55,'07:00:00.000000','STANDING','ONBARS',40),(57,'09:00:00.000000','SITTING','ONBARS',39),(79,'03:52:13.000000','STANDING','BENCH',58),(80,'03:54:12.000000','STANDING','BENCH',58),(81,'03:54:25.000000','STANDING','FLOOR',58),(82,'03:55:21.000000','SITTING','FLOOR',59),(83,'03:55:33.000000','STANDING','FLOOR',60),(84,'03:56:56.000000','STANDING','FLOOR',62),(85,'03:58:13.000000','STANDING','ONBARS',59),(86,'03:59:34.000000','STANDING','ELSE',61),(87,'04:00:15.000000','STANDING','FLOOR',61),(88,'04:01:30.000000','STANDING','ONBARS',61),(89,'12:00:00.000000','STANDING','ONBARS',61),(90,'04:12:51.000000','STANDING','ONBARS',61),(91,'04:15:04.000000','STANDING','ONBARS',61),(92,'04:15:41.000000','STANDING','ONBARS',62),(93,'04:16:14.000000','STANDING','BENCH',58),(94,'04:48:20.000000','STANDING','ONBARS',58),(95,'04:50:38.000000','SITTING','WALLTOWALL',16),(96,'04:51:40.000000','STANDING','FLOOR',59),(98,'04:59:56.000000','STANDING','BENCH',58),(99,'05:00:46.000000','WALKING_AROUND','FLOOR',58),(100,'05:00:57.000000','WALKING_AROUND','BENCH',58),(101,'05:01:11.000000','WALKING_AROUND','ONBARS',58),(102,'05:01:21.000000','WALKING_AROUND','WALLTOWALL',58),(103,'05:02:01.000000','SITTING','BENCH',58),(104,'05:02:10.000000','SITTING','ELSE',58),(105,'05:02:21.000000','WALKING_AROUND','ONBARS',58),(106,'05:02:30.000000','WALKING_AROUND','ONBARS',58),(107,'05:02:40.000000','SITTING','BENCH',58),(108,'05:02:49.000000','SITTING','BENCH',58),(109,'05:03:31.000000','WALKING_AROUND','FLOOR',59),(110,'05:03:40.000000','WALKING_AROUND','FLOOR',59),(111,'05:03:49.000000','WALKING_AROUND','FLOOR',59),(112,'05:03:57.000000','WALKING_AROUND','WALLTOWALL',59),(113,'05:04:05.000000','WALKING_AROUND','BENCH',59),(114,'05:04:15.000000','WALKING_AROUND','ONBARS',59),(115,'05:04:22.000000','SITTING','WALLTOWALL',59),(116,'05:04:31.000000','SITTING','BENCH',59),(117,'05:04:42.000000','SITTING','BENCH',59),(118,'05:04:49.000000','WALKING_AROUND','BENCH',60),(119,'05:04:56.000000','STANDING','BENCH',60),(120,'05:05:06.000000','ALERT','BENCH',61),(121,'05:05:19.000000','ALERT','BENCH',61),(122,'05:05:24.000000','WALKING_AROUND','BENCH',61),(123,'05:05:32.000000','WALKING_AROUND','BENCH',61),(124,'05:05:38.000000','STANDING','BENCH',62),(125,'05:05:45.000000','WALKING_AROUND','BENCH',62),(126,'05:05:51.000000','SITTING','ONBARS',62),(127,'05:06:00.000000','SITTING','BENCH',61),(128,'05:06:08.000000','SITTING','BENCH',60),(129,'05:06:14.000000','SITTING','BENCH',60),(130,'05:06:27.000000','JUMPING','BENCH',60),(131,'05:06:33.000000','WALKING_AROUND','FLOOR',61),(132,'05:06:40.000000','WALKING_AROUND','ELSE',61),(133,'05:06:48.000000','WALKING_AROUND','FLOOR',61),(134,'05:06:57.000000','WALKING_AROUND','ONBARS',62),(135,'05:59:11.000000','SLEEPING_LYING','FLOOR',58),(136,'05:59:21.000000','SLEEPING_LYING','BENCH',58),(137,'05:59:32.000000','SLEEPING_LYING','BENCH',58),(138,'05:59:42.000000','SLEEPING_LYING','BENCH',58),(139,'05:59:57.000000','ALERT','ONBARS',58),(140,'06:00:11.000000','ALERT','BENCH',58),(141,'06:00:21.000000','SLEEPING_LYING','ONBARS',59),(142,'06:00:29.000000','SLEEPING_LYING','BENCH',59),(143,'06:00:38.000000','ALERT','BENCH',59),(144,'06:00:47.000000','SLEEPING_LYING','FLOOR',60),(145,'06:00:58.000000','SLEEPING_LYING','FLOOR',60),(146,'06:01:08.000000','ALERT','BENCH',60),(147,'06:01:17.000000','SLEEPING_LYING','ONBARS',62),(148,'06:01:29.000000','ALERT','ONBARS',62),(149,'06:01:39.000000','ALERT','ONBARS',62),(150,'06:01:49.000000','ALERT','BENCH',62),(151,'06:01:58.000000','ALERT','BENCH',62),(152,'22:28:20.000000','STANDING','BENCH',62),(153,'22:28:33.000000','STANDING','BENCH',62),(154,'22:28:51.000000','STANDING','ONBARS',62),(155,'22:29:11.000000','STANDING','FLOOR',62),(156,'22:30:21.000000','ALERT','BENCH',61),(157,'22:30:33.000000','ALERT','BENCH',61),(158,'22:30:54.000000','SITTING','BENCH',61),(159,'22:31:10.000000','SITTING','BENCH',61),(160,'22:31:29.000000','WALKING_AROUND','ONBARS',61),(161,'22:31:42.000000','WALKING_AROUND','ONBARS',61),(162,'22:31:54.000000','SITTING','WALLTOWALL',61),(163,'22:59:00.000000','STANDING','FLOOR',63),(164,'22:47:00.000000','STANDING','FLOOR',63),(165,'14:00:09.000000','SLEEPING_LYING','FLOOR',64),(166,'14:00:07.000000','SLEEPING_LYING','BENCH',64),(167,'22:59:00.000000','STANDING','FLOOR',65),(168,'22:47:00.000000','STANDING','FLOOR',65),(169,'14:00:09.000000','SLEEPING_LYING','FLOOR',66),(170,'14:00:07.000000','SLEEPING_LYING','BENCH',66),(171,'22:59:00.000000','STANDING','FLOOR',67),(172,'22:47:00.000000','STANDING','FLOOR',67),(173,'14:00:09.000000','SLEEPING_LYING','FLOOR',68),(174,'14:00:07.000000','SLEEPING_LYING','BENCH',68),(175,'11:37:03.000000','SITTING','BENCH',NULL),(176,'12:00:00.000000','SITTING','FLOOR',NULL),(177,'12:11:00.000000','WALKING_AROUND','ONBARS',NULL),(178,'15:00:00.000000','SITTING','FLOOR',NULL),(179,'15:00:02.000000','STANDING','FLOOR',NULL),(180,'12:00:01.000000','WALKING_AROUND','BENCH',NULL),(181,'12:00:57.000000','ELSE','ELSE',NULL),(182,'10:00:00.000000','SITTING','BENCH',56),(183,'10:00:00.000000','WALKING_AROUND','FLOOR',39),(184,'10:00:01.000000','STANDING','FLOOR',39);
/*!40000 ALTER TABLE `dogs_app_dogstance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dogs_app_entranceexamination`
--

DROP TABLE IF EXISTS `dogs_app_entranceexamination`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dogs_app_entranceexamination` (
  `examinationID` int NOT NULL AUTO_INCREMENT,
  `examinationDate` date NOT NULL,
  `examinedBy` varchar(50) NOT NULL,
  `results` varchar(100) DEFAULT NULL,
  `dogWeight` decimal(4,2) DEFAULT NULL,
  `dogTemperature` decimal(4,2) DEFAULT NULL,
  `dogPulse` smallint unsigned DEFAULT NULL,
  `comments` varchar(200) DEFAULT NULL,
  `dog_id` int NOT NULL,
  PRIMARY KEY (`examinationID`),
  KEY `dogs_app_entranceexa_dog_id_f39f14bb_fk_dogs_app_` (`dog_id`),
  CONSTRAINT `dogs_app_entranceexa_dog_id_f39f14bb_fk_dogs_app_` FOREIGN KEY (`dog_id`) REFERENCES `dogs_app_dog` (`dogID`),
  CONSTRAINT `dogs_app_entranceexamination_chk_1` CHECK ((`dogPulse` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dogs_app_entranceexamination`
--

LOCK TABLES `dogs_app_entranceexamination` WRITE;
/*!40000 ALTER TABLE `dogs_app_entranceexamination` DISABLE KEYS */;
INSERT INTO `dogs_app_entranceexamination` VALUES (1,'2023-06-30','Gianna','All Clear',31.00,39.00,125,'Healthy as a horse',1),(2,'2019-01-05','Roey','All looking good!',30.50,39.80,110,'Does not like anyone touching the ears',5),(3,'2022-12-14','Sami',NULL,5.00,38.90,100,'Extremely good boy',3),(4,'2021-01-10','George','A little fatigued',17.16,40.01,119,NULL,12),(5,'2019-01-05','Roey','All looking good!',30.50,39.80,110,'Does not like anyone touching the ears',13),(6,'2022-12-14','Sami',NULL,5.00,38.90,100,'Extremely good boy',14),(7,'2021-01-10','George','A little fatigued',17.16,40.01,119,NULL,17),(8,'2021-08-26','Ali','A little fatigued',32.25,39.57,106,'Extremely good boy',15),(9,'2021-07-11','Michael','Improvement noted',29.70,39.29,75,'Does not like anyone touching the ears',18),(10,'2022-05-03','Charlie','All looking good!',35.60,39.05,70,'Does not like anyone touching the ears',16),(11,'2023-05-30','Charlie','Needs to be rechecked',13.30,40.61,68,'Does not like anyone touching the ears',17),(12,'2021-05-18','Roey','Does not look well',16.63,41.09,65,NULL,18),(14,'2022-06-23','Meirav','A little fatigued',43.01,40.99,106,'Extremely good boy',14),(15,'2022-09-29','Shelly','Further examinations required',28.14,41.22,81,'Extremely good boy',12),(17,'2022-05-08','Charlie','All looking good!',45.43,38.84,76,NULL,10),(18,'2022-12-13','Samantha',NULL,8.30,38.19,84,'Extremely good boy',9),(19,'2023-01-06','Ali','Further examinations required',9.01,38.83,111,'Does not like anyone touching the ears',8),(20,'2023-03-09','Anastasia','A little fatigued',5.09,39.66,66,'Extremely good boy',4),(21,'2023-02-20','Michael','Further treatment required',47.36,39.28,90,'Does not like anyone touching the ears',9),(22,'2022-06-24','Rob','All looking good!',13.64,38.70,101,'Extremely good boy',3),(23,'2023-02-25','Anastasia','Improvement noted',17.05,41.18,76,NULL,1),(25,'2023-09-12','absar','All Clear',20.50,30.10,65,'All healthy!',1),(26,'2023-09-13','absar','All Clear',20.50,30.10,65,'All healthy!',1),(31,'2023-10-01','Gianna','All Clear',90.00,90.00,10,'dfdfg',1),(32,'2023-10-01','Gianna','All Clear',99.00,99.00,10,'dfsf',1);
/*!40000 ALTER TABLE `dogs_app_entranceexamination` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dogs_app_kennel`
--

DROP TABLE IF EXISTS `dogs_app_kennel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dogs_app_kennel` (
  `kennelNum` smallint unsigned NOT NULL,
  `kennelImage` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`kennelNum`),
  CONSTRAINT `dogs_app_kennel_chk_1` CHECK ((`kennelNum` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dogs_app_kennel`
--

LOCK TABLES `dogs_app_kennel` WRITE;
/*!40000 ALTER TABLE `dogs_app_kennel` DISABLE KEYS */;
INSERT INTO `dogs_app_kennel` VALUES (1,'kennel_pictures/kennel2.jpg'),(2,'kennel_pictures/kennel1_CRHYT52.jpg'),(3,'kennel_pictures/1.jpeg'),(4,'kennel_pictures/2.jpg'),(5,'kennel_pictures/3.jpeg'),(6,'kennel_pictures/4.jpeg'),(7,'kennel_pictures/5.jpg'),(8,'kennel_pictures/6.jpg'),(9,'kennel_pictures/7.jpeg'),(10,'kennel_pictures/8.jpg'),(11,'kennel_pictures/default_kennel.jpg'),(12,'kennel_pictures/default_kennel.jpg'),(14,'kennel_pictures/default_kennel.jpg'),(15,'kennel_pictures/default_kennel.jpg'),(16,'kennel_pictures/2.jpg'),(17,'kennel_pictures/4.jpeg');
/*!40000 ALTER TABLE `dogs_app_kennel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dogs_app_news`
--

DROP TABLE IF EXISTS `dogs_app_news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dogs_app_news` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dogs_app_news`
--

LOCK TABLES `dogs_app_news` WRITE;
/*!40000 ALTER TABLE `dogs_app_news` DISABLE KEYS */;
INSERT INTO `dogs_app_news` VALUES (1,'Website is going live! ','Our first website news! ','2023-07-02 15:08:27.070073'),(2,'Hotdogs for all employees','We are distributing free hotdogs for all our employees throughout the week in celebration of our website kicking off and also to celebrate the food with the best name 2023','2023-07-02 15:09:17.471513'),(4,'Lorem Ipsum','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\r\n','2023-08-01 18:53:49.052258'),(15,'Great News Everyone!','Very interesting!','2023-09-27 04:24:16.149354');
/*!40000 ALTER TABLE `dogs_app_news` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dogs_app_observation`
--

DROP TABLE IF EXISTS `dogs_app_observation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dogs_app_observation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `obsDateTime` datetime(6) NOT NULL,
  `sessionDurationInMins` int unsigned NOT NULL,
  `isKong` varchar(1) DEFAULT NULL,
  `jsonFile` varchar(100) DEFAULT NULL,
  `rawVideo` varchar(100) DEFAULT NULL,
  `observes_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dogs_app_observation_observes_id_obsDateTime_d4faa94d_uniq` (`observes_id`,`obsDateTime`),
  CONSTRAINT `dogs_app_observation_observes_id_02a9e480_fk_dogs_app_` FOREIGN KEY (`observes_id`) REFERENCES `dogs_app_observes` (`id`),
  CONSTRAINT `dogs_app_observation_sessionDurationInMins_a296c250_check` CHECK ((`sessionDurationInMins` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dogs_app_observation`
--

LOCK TABLES `dogs_app_observation` WRITE;
/*!40000 ALTER TABLE `dogs_app_observation` DISABLE KEYS */;
INSERT INTO `dogs_app_observation` VALUES (1,'2023-07-01 14:58:38.000000',2,'Y','','',20),(2,'2023-02-16 22:00:00.000000',10,'N','','',1),(3,'2023-02-18 22:00:00.000000',2,'Y','','',1),(4,'2023-01-19 22:00:00.000000',4,'N','','',2),(5,'2022-03-25 21:00:00.000000',6,'N','','',4),(6,'2023-01-14 09:56:30.000000',205,'Y','','',6),(8,'2022-08-21 16:10:16.000000',166,'Y','','',3),(10,'2023-04-05 20:21:38.000000',253,'N','','',9),(11,'2022-10-28 18:26:30.000000',31,'Y','','',3),(13,'2023-06-16 02:53:36.000000',110,'Y','','',9),(16,'2023-10-06 23:32:00.000000',70,'N','','',NULL),(17,'2022-10-06 03:13:27.000000',121,'N','','',1),(19,'2023-04-29 15:00:00.000000',3,'Y','','',6),(39,'2023-09-30 12:56:00.000000',3,'N','','',NULL),(40,'2023-09-30 12:58:00.000000',2,'N','','',NULL),(42,'2023-09-30 13:08:00.000000',2,'N','','',NULL),(55,'2023-10-05 15:55:00.000000',2,'N','','',NULL),(56,'2023-12-13 16:55:00.000000',7,'Y','','',NULL),(58,'2023-11-04 23:00:00.000000',2,'Y','','',1),(59,'2023-11-06 00:00:00.000000',2,'N','','',2),(60,'2023-11-07 01:00:00.000000',2,'N','','',3),(61,'2023-11-08 02:00:00.000000',5,'Y','','',4),(62,'2023-11-09 03:00:00.000000',2,'N','','',6),(63,'2023-10-06 23:32:18.000000',75,'Y','','',28),(64,'2023-10-05 15:21:00.000000',3,'N','','',28),(65,'2023-10-06 23:32:18.000000',75,'Y','','',30),(66,'2023-10-05 15:21:00.000000',3,'N','','',30),(67,'2023-10-06 20:32:18.000000',75,'Y','','',34),(68,'2023-10-05 12:21:00.000000',3,'N','','',34);
/*!40000 ALTER TABLE `dogs_app_observation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dogs_app_observes`
--

DROP TABLE IF EXISTS `dogs_app_observes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dogs_app_observes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `comments` varchar(200) DEFAULT NULL,
  `camera_id` smallint unsigned DEFAULT NULL,
  `dog_id` int DEFAULT NULL,
  `sessionDate` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dogs_app_observes_dog_id_camera_id_sessionDate_90083ae1_uniq` (`dog_id`,`camera_id`,`sessionDate`),
  KEY `dogs_app_observes_camera_id_5cb8b9e0_fk_dogs_app_camera_camID` (`camera_id`),
  KEY `dogs_app_observes_dog_id_5b836e9e` (`dog_id`),
  CONSTRAINT `dogs_app_observes_camera_id_5cb8b9e0_fk_dogs_app_camera_camID` FOREIGN KEY (`camera_id`) REFERENCES `dogs_app_camera` (`camID`),
  CONSTRAINT `dogs_app_observes_dog_id_5b836e9e_fk_dogs_app_dog_dogID` FOREIGN KEY (`dog_id`) REFERENCES `dogs_app_dog` (`dogID`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dogs_app_observes`
--

LOCK TABLES `dogs_app_observes` WRITE;
/*!40000 ALTER TABLE `dogs_app_observes` DISABLE KEYS */;
INSERT INTO `dogs_app_observes` VALUES (1,'Our first attempt!',1,4,'2023-09-16'),(2,NULL,7,4,'2023-09-16'),(3,NULL,6,5,'2023-09-16'),(4,NULL,6,18,'2023-09-16'),(5,NULL,5,10,'2023-09-16'),(6,NULL,4,9,'2023-09-16'),(7,NULL,4,6,'2023-09-16'),(9,NULL,7,3,'2023-09-16'),(10,NULL,6,8,'2023-09-16'),(11,'Nothing to Say',4,1,'2023-09-13'),(12,'Nothing',3,1,'2023-09-14'),(13,'Wall',2,1,'2023-09-11'),(17,'aa',1,1,'2023-09-15'),(18,'aa',3,1,'2023-09-15'),(19,'aa',5,1,'2023-09-15'),(20,'aa',7,1,'2023-09-15'),(21,'aa',6,1,'2023-09-15'),(22,NULL,3,1,'2023-09-07'),(23,'324',2,1,'2023-09-18'),(24,NULL,3,1,'2023-09-18'),(28,NULL,1,NULL,'2023-09-19'),(29,'Nothing to Say',4,NULL,'2023-09-13'),(30,NULL,1,NULL,'2023-09-19'),(31,'Nothing to Say',4,NULL,'2023-09-13'),(34,NULL,1,NULL,'2023-09-19'),(35,'Nothing to Say',4,NULL,'2023-09-13'),(36,'tews',2,1,'2024-01-04');
/*!40000 ALTER TABLE `dogs_app_observes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dogs_app_owner`
--

DROP TABLE IF EXISTS `dogs_app_owner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dogs_app_owner` (
  `ownerSerialNum` int NOT NULL AUTO_INCREMENT,
  `firstName` varchar(50) NOT NULL,
  `lastName` varchar(50) DEFAULT NULL,
  `ownerID` varchar(9) DEFAULT NULL,
  `ownerAddress` varchar(70) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `phoneNum` varchar(9) DEFAULT NULL,
  `cellphoneNum` varchar(10) DEFAULT NULL,
  `comments` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`ownerSerialNum`),
  UNIQUE KEY `dogs_app_owner_ownerID_d36d18b2_uniq` (`ownerID`),
  CONSTRAINT `cellphoneNum_check` CHECK (regexp_like(`cellphoneNum`,_utf8mb3'^[0-9]{10}$',_utf8mb3'c')),
  CONSTRAINT `phoneNum_check` CHECK (regexp_like(`phoneNum`,_utf8mb3'^[0-9]{9}$',_utf8mb3'c'))
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dogs_app_owner`
--

LOCK TABLES `dogs_app_owner` WRITE;
/*!40000 ALTER TABLE `dogs_app_owner` DISABLE KEYS */;
INSERT INTO `dogs_app_owner` VALUES (1,'Bran','Stark','308657362','George Weisz 16','Tel Aviv','049914669','0545213123','Seemed like he had a great story'),(2,'John','Mortsen','305040448','Volsfon Street, 17th','Tel Aviv','049913567','0546789234','No Comments Whatsoever'),(3,'Jimmy',NULL,NULL,NULL,'Eilat',NULL,NULL,'Ran off like crazy'),(4,'Gene',NULL,NULL,NULL,'Haifa',NULL,NULL,'Red Haired'),(5,'Zachary','Beck','541571834','83165 Shepard Prairie Apt. 464, New Patrickborough, ND 24949','Kyliebury','357491510','0546789234','Generated by Faker'),(6,'Emily','Sullivan','933579643','67911 Miller Trail, West Pamela, PW 22143','Francesstad','121457308','0546789234','Generated by Faker'),(7,'Matthew','Davis','128831127','PSC 9072, Box 2627, APO AA 12466','Port Amy','261585733','0546789234','Generated by Faker'),(8,'Derek','Gay','709680994','09533 Cheryl Walk, Campbellshire, MP 25720','Matthewstad','829605505','0546789234','Generated by Faker'),(9,'David','Moore','110378399','Unit 9763 Box 9198, DPO AE 22270','New Kayla','357866692','0546789234','Generated by Faker'),(10,'Zachary','King','933471964','270 Michael Ford Suite 885, Sheltonshire, TX 81436','North Brandonland','918343364','0546789234','Generated by Faker'),(11,'Logan','Buckley','360873700','30716 James Village, Chaseville, PA 62544','Khanborough','332109889','0546789234','Generated by Faker'),(12,'Elizabeth','Keith','827935545','9827 Ruiz Harbor Suite 739, Danielhaven, OH 03839','Johnsonshire','997818852','0546789234','Generated by Faker'),(13,'Brittany','Thomas','606762744','6165 Tina Springs Suite 301, Hurleyport, KY 97699','New Aaronville','577561512','0546789234','Generated by Faker'),(14,'Stacey','Larson','505609341','Unit 9575 Box 5765, DPO AP 27546','West Anthonyton','620867684','0546789234','Generated by Faker'),(15,'Rebecca','Logan','143353083','804 Sherry Loaf Apt. 416, North Brian, AS 91403','Larryport','970530556','0546789234','Generated by Faker'),(16,'Thomas','Peters','776871977','39200 Jones Road, West Julie, AZ 01606','South Michaelchester','317632142','0546789234','Generated by Faker'),(17,'Bradly','Cooper','308657369','George Weisz 16','Tel Aviv','049914669','0545213123','Looked like he had a great story'),(18,'Bradly','Cooper','308657367','George Weisz 16','Tel Aviv','049914669','0545213123','Looked like he had a great story'),(19,'John','Tucker','308657368','George Weisz 16','Tel Aviv','049914669','0545213123','Looked like he had a great story');
/*!40000 ALTER TABLE `dogs_app_owner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dogs_app_profile`
--

DROP TABLE IF EXISTS `dogs_app_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dogs_app_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(15) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `image` varchar(100) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `dogs_app_profile_user_id_775c32e2_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dogs_app_profile`
--

LOCK TABLES `dogs_app_profile` WRITE;
/*!40000 ALTER TABLE `dogs_app_profile` DISABLE KEYS */;
INSERT INTO `dogs_app_profile` VALUES (1,'0545234562','Saladin','profile_pictures/1666170550315.jpeg',1),(2,NULL,NULL,'profile_pictures/regularjoe.jpg',2),(3,'0548-123-220','HaHistadrut 12, Tel Aviv','/profile_pictures/default.jpg',3),(6,'123123123123',NULL,'profile_pictures/default.jpg',6);
/*!40000 ALTER TABLE `dogs_app_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dogs_app_treatment`
--

DROP TABLE IF EXISTS `dogs_app_treatment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dogs_app_treatment` (
  `treatmentID` int NOT NULL AUTO_INCREMENT,
  `treatmentName` varchar(50) NOT NULL,
  `treatmentDate` date DEFAULT NULL,
  `treatedBy` varchar(50) NOT NULL,
  `comments` varchar(250) DEFAULT NULL,
  `dog_id` int NOT NULL,
  PRIMARY KEY (`treatmentID`),
  KEY `dogs_app_treatment_dog_id_1b7891c2_fk_dogs_app_dog_dogID` (`dog_id`),
  CONSTRAINT `dogs_app_treatment_dog_id_1b7891c2_fk_dogs_app_dog_dogID` FOREIGN KEY (`dog_id`) REFERENCES `dogs_app_dog` (`dogID`)
) ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dogs_app_treatment`
--

LOCK TABLES `dogs_app_treatment` WRITE;
/*!40000 ALTER TABLE `dogs_app_treatment` DISABLE KEYS */;
INSERT INTO `dogs_app_treatment` VALUES (2,'Rash Treatment','2023-05-01','Roey','All good!',5),(4,'Fatigue','2018-12-12','Shelly','Everything looking good',13),(5,'Rash Treatment','2022-05-20','Meirav','Improvement noted',14),(6,'Fatigue','2022-08-15','Meirav','Further treatment required',15),(7,'Coughing','2021-10-10','Ali','Had to tranquilize the dog',16),(8,'Fleas','2020-08-09','Rob','Had to tranquilize the dog',17),(9,'High Fever','2022-10-05','Mac','Needs to be rechecked',18),(11,'Sneezing','2023-01-15','Rob','Had to tranquilize the dog',10),(12,'Sneezing','2023-05-24','Samantha','Everything looking good',9),(13,'Rash Treatment','2020-07-07','Charlie','All good!',8),(14,'Rash Treatment','2021-08-29','Charlie','All good!',7),(15,'Coughing','2022-10-16','Charlie','All good!',6),(16,'Underweight','2022-11-23','Anastasia','Had to tranquilize the dog',5),(17,'Coughing','2022-02-23','Meirav','Had to tranquilize the dog',4),(18,'Infection','2021-09-04','Meirav','Needs to be rechecked',3),(24,'Heart Check','2023-08-29','Junior','Healthy rhythm.',1),(25,'Ears Cleaning','2023-09-13','Dvora','Sometimes the dog would shake when touched too quickly. Longtail is naturally very gentle but has ear sensitivity and must be monitored for further changes. I advice future endearers to tread carefully, he may not be into biting but tread lightly....',1),(46,'hddfs','2023-09-07','sdfsdf','sdfsdfsdf',1),(47,'hdsd','2023-09-07','sdfs','sdfsdf',1),(108,'test','2024-01-06','ana','ss',1),(109,'tests','2024-01-06','ana','ssss',1),(110,'testss','2024-01-06','ana','sssss',1);
/*!40000 ALTER TABLE `dogs_app_treatment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'dogshelterdb'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-05 13:38:30
