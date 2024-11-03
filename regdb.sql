-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 03, 2024 at 11:14 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `regdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `reg`
--

CREATE TABLE `reg` (
  `register_id` int(11) NOT NULL,
  `cedula` mediumtext DEFAULT NULL,
  `contribuyente` mediumtext DEFAULT NULL,
  `nombreinmueble` mediumtext DEFAULT NULL,
  `rif` mediumtext DEFAULT NULL,
  `sector` mediumtext DEFAULT NULL,
  `uso` mediumtext DEFAULT NULL,
  `codcatastral` mediumtext DEFAULT NULL,
  `fechaliquidacion` date DEFAULT NULL
) ENGINE=Aria DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reg`
--

INSERT INTO `reg` (`register_id`, `cedula`, `contribuyente`, `nombreinmueble`, `rif`, `sector`, `uso`, `codcatastral`, `fechaliquidacion`) VALUES
(1, '31625272', 'Cristhian B', 'BrachosBros C.A', 'J-8888888', 'Boqueron', 'Comercial', '6585-7457-5474-7457', '2024-04-19'),
(2, '31625272', 'Cristhian B', 'BrachosBros C.A', 'J-8888888', 'Boqueron', 'Comercial', '6585-7457-5474-7457', '2024-04-19'),
(3, '3763782', 'Nelson V', 'VillalobosInc C.A', 'J-1234432', 'La Floresta', 'Comercial', '2341-1242-2314-1242', '2024-04-20'),
(4, '452365353', 'Fulano', 'Intituto Prueba', '7367633', 'La Floresta', 'Comercial', '34543656-J', '2024-12-31'),
(5, '7546255', 'Criss', 'CrisInc BBBBBBBBBBBBB', '6546-65465-6544', 'La Floresta', 'Comercial', '65654-65454-5654', '2024-12-12'),
(6, '31675830', 'Pablo', 'Pablitos Inc', 'J-8463248', 'Manga', 'Comercial', '7898-8879-7898-7878-', '2024-10-10'),
(7, '12312124', 'asasfa', 'asfaf', 'j-214124214', 'asdasdada', 'adssada', '1231-1313-1231-2131', '2024-12-12'),
(8, 'qweewqe', 'eqwe', 'qweqw', 'qweqe', 'qeqweqwewqe', 'qwe', 'qwe', '0000-00-00'),
(9, '13123213525432', 'qwwqe', 'eqwewqe', 'qqeqe', 'qweeq', 'eqwe', '1231-31313-23-3', '2024-12-12'),
(10, '1231232', 'qweqeqweqe', 'qweqweqweqwe', 'e14123123', 'qweqweqwe', 'qweqwweqwe', '1231-1231-1231-1321', '2024-11-11'),
(11, '7546255', 'Cristian', 'CrisInc Bracho', '6546-65465-6544', 'La Floresta', 'Comercial', '65654-65454-5654', '2024-12-12'),
(12, '7546255', 'Cris', 'CrisInc BBBBBBBBBBBBB', '6546-65465-6544', 'La Floresta', 'Comercial', '65654-65454-5654', '2024-12-12'),
(13, '7546255', 'Cris', 'CrisInc BBBBBBBBBBBBB', '6546-65465-6544', 'La Floresta', 'Comercial', '65654-65454-5654', '2024-12-12');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `reg`
--
ALTER TABLE `reg`
  ADD PRIMARY KEY (`register_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `reg`
--
ALTER TABLE `reg`
  MODIFY `register_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
