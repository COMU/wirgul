-- MySQL dump 10.13  Distrib 5.5.24, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: wirguldb
-- ------------------------------------------------------
-- Server version	5.5.24-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `web_faculty`
--

DROP TABLE IF EXISTS `web_faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_faculty` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `web_faculty`
--

LOCK TABLES `web_faculty` WRITE;
/*!40000 ALTER TABLE `web_faculty` DISABLE KEYS */;
INSERT INTO `web_faculty` VALUES (1,'Ayvacık Meslek Yüksekokulu'),(2,'Bayramiç Meslek Yüksekokulu'),(3,'Beden Eğitimi ve Spor Yüksekokulu'),(4,'Biga İktisadi ve İdari Bilimler Fakültesi'),(5,'Biga İktisadi ve İdari Bilimler Fakültes'),(6,'Biga Meslek Yüksekokulu'),(7,'Çan Meslek Yüksekokulu'),(8,'Çanakkale Meslek Yüksekokulu'),(9,'Canakkale Sağlık Hizmetleri Meslek Yüksekokulu'),(10,'Canakkale Sağlık Hizmetleri Meslek Yüksekoulu'),(11,'Canakkale Sağlık Yüksekokulu'),(12,'Eğitim Fakültesi'),(13,'Ezine Meslek Yüksekokulu'),(14,'Fen Edebiyat Fakültesi'),(15,'Gelibolu Piri Reis Meslek Yüksekokulu'),(16,'Gökçeada Meslek Yüksekokulu'),(17,'Gökçeada Uygulamalı Bilimler Yüksekokulu'),(18,'Güzel Sanatlar Fakültesi'),(19,'İlahiyat Fakültesi'),(20,'Lapseki Meslek Yüksekokulu'),(21,'Mühendislik ve Mimarlık Fakültesi'),(22,'Su Ürünleri Fakültesi'),(23,'Tıp Fakültesi'),(24,'Turizm İşletmeciliği ve Otelcilik Yüksek'),(25,'Yenice Meslek Yüksekokulu'),(26,'Ziraat Fakültesi'),(27,'Turizm İşletmeciliği ve Otelcilik Yüksekokulu'),(29,'Eğitim Bilimleri Enstitüsü'),(30,'Fen Bilimleri Enstitüsü'),(31,'Sosyal Bilimler Enstitüsü'),(32,'Sağlık Bilimleri Enstitüsü'),(38,'Rektörlüğe Bağlı Birimler');
/*!40000 ALTER TABLE `web_faculty` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-08-30 10:40:36
