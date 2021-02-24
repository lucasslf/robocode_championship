CREATE TABLE `robot` (
  `id` varbinary(16) NOT NULL,
  `name` varchar(64) NOT NULL,
  `file_name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;