-- phpMyAdmin SQL Dump
-- version 4.0.10.14
-- http://www.phpmyadmin.net
--
-- Host: localhost:3306
-- Generation Time: Jan 09, 2017 at 12:12 AM
-- Server version: 5.5.52-cll-lve
-- PHP Version: 5.6.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `noticias_bot`
--

-- --------------------------------------------------------

--
-- Table structure for table `asked`
--

CREATE TABLE IF NOT EXISTS `asked` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sender_id` varchar(30) NOT NULL,
  `flag` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=31 ;

--
-- Dumping data for table `asked`
--

INSERT INTO `asked` (`id`, `sender_id`, `flag`) VALUES
(1, '0', 'dfds');

-- --------------------------------------------------------

--
-- Table structure for table `placement2016-17`
--

CREATE TABLE IF NOT EXISTS `placement2016-17` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company` varchar(30) NOT NULL,
  `number` int(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;

--
-- Dumping data for table `placement2016-17`
--

INSERT INTO `placement2016-17` (`id`, `company`, `number`) VALUES
(5, 'tower research capital', 4),
(4, 'parthenon', 6),
(6, 'goldman sachs', 13),
(7, 'itc', 4),
(8, 'uber', 2),
(9, 'microsoft', 6),
(10, 'credit suisse', 16);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
