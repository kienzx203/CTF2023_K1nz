SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";
CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
INSERT INTO `admin` (`id`, `username`, `email`, `password`)
VALUES (
    1,
    'administrator',
    'administrator@gmail.com',
    'resuovqm80rq2h80cq3j9ifcam'
  );
CREATE TABLE `item_list` (
  `id` int(11) NOT NULL,
  `item_name` varchar(255) NOT NULL,
  `quantity` int(11) NOT NULL,
  `created_by` varchar(255) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
INSERT INTO `item_list` (`id`, `item_name`, `quantity`, `created_by`)
VALUES (1, 'Blue Shirt', 50, ' admin'),
  (2, 'Red Shoes', 25, ' admin'),
  (3, 'Black Pants', 1337, ' admin');
ALTER TABLE `admin`
ADD PRIMARY KEY (`id`);
ALTER TABLE `item_list`
ADD PRIMARY KEY (`id`);
ALTER TABLE `admin`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
  AUTO_INCREMENT = 3;
ALTER TABLE `item_list`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
  AUTO_INCREMENT = 5;