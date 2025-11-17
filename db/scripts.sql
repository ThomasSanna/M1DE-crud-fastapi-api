-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : lun. 17 nov. 2025 à 14:31
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `2025_m1`
--

-- --------------------------------------------------------

--
-- Structure de la table `historique_prix`
--

CREATE TABLE `historique_prix` (
  `id_hist` int(11) NOT NULL,
  `id_produit` int(11) NOT NULL,
  `ancien_prix` decimal(10,2) NOT NULL,
  `nouveau_prix` decimal(10,2) NOT NULL,
  `date_modification` timestamp NOT NULL DEFAULT current_timestamp(),
  `motif` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Structure de la table `produit`
--

CREATE TABLE `produit` (
  `id_p` int(11) NOT NULL,
  `type_p` varchar(100) NOT NULL,
  `designation_p` varchar(255) NOT NULL,
  `prix_ht` decimal(10,2) NOT NULL,
  `date_in` date NOT NULL,
  `timeS_in` timestamp NOT NULL DEFAULT current_timestamp(),
  `stock_p` int(11) DEFAULT 0,
  `image_p` varchar(255) DEFAULT 'default.png',
  `ppromo` decimal(5,2) DEFAULT NULL COMMENT 'Pourcentage de promotion (ex: 15.00 pour 15%)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Déclencheurs `produit`
--
DELIMITER $$
CREATE TRIGGER `after_produit_price_update` AFTER UPDATE ON `produit` FOR EACH ROW BEGIN
    -- Vérifier si le prix a changé
    IF OLD.prix_ht != NEW.prix_ht THEN
        INSERT INTO `historique_prix` (`id_produit`, `ancien_prix`, `nouveau_prix`, `motif`)
        VALUES (NEW.id_p, OLD.prix_ht, NEW.prix_ht, 'Modification du prix');
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `user_login` text NOT NULL,
  `user_password` longtext NOT NULL,
  `user_mail` text NOT NULL,
  `user_role` enum('user','admin') NOT NULL DEFAULT 'user',
  `user_date_new` timestamp NOT NULL DEFAULT current_timestamp(),
  `user_date_login` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
(19, 'adminadmin@gmail.com', '$2b$12$n7ZTPTKIsgL8vTipWeCJdugwp3qES2is.Y53weN2Oawybf3orLbry', 5, 'adminadmin@gmail.com', 'admin', '2025-11-10 16:58:28', '2025-11-17 12:14:34');

--
-- Index pour la table `historique_prix`
--
ALTER TABLE `historique_prix`
  ADD PRIMARY KEY (`id_hist`),
  ADD KEY `fk_historique_produit` (`id_produit`);

--
-- Index pour la table `produit`
--
ALTER TABLE `produit`
  ADD PRIMARY KEY (`id_p`);

--
-- Index pour la table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `historique_prix`
--
ALTER TABLE `historique_prix`
  MODIFY `id_hist` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `produit`
--
ALTER TABLE `produit`
  MODIFY `id_p` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=190;

--
-- AUTO_INCREMENT pour la table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `historique_prix`
--
ALTER TABLE `historique_prix`
  ADD CONSTRAINT `fk_historique_produit` FOREIGN KEY (`id_produit`) REFERENCES `produit` (`id_p`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
