-- Creer la table panier
CREATE TABLE `panier` (
  `panier_id` int(11) NOT NULL AUTO_INCREMENT,
  `panier_date_creation` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`panier_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Modifier la colonne user_compte_id en panier_id dans la table user
ALTER TABLE `user`
    CHANGE COLUMN `user_compte_id` `panier_id` int(11) DEFAULT NULL;
-- Ajouter une clé étrangère entre user.panier_id et panier.panier_id
ALTER TABLE `user`
    ADD CONSTRAINT `fk_user_panier` FOREIGN KEY (`panier_id`) REFERENCES `panier`(`panier_id`) ON DELETE SET NULL ON UPDATE CASCADE;


-- Créer une table produit_panier pour gérer les produits dans les paniers
CREATE TABLE `produit_panier` (
  `produit_panier_id` int(11) NOT NULL AUTO_INCREMENT,
  `panier_id` int(11) NOT NULL,
  `id_produit` int(11) NOT NULL,
  `quantite` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`produit_panier_id`),
  KEY `fk_produit_panier_panier` (`panier_id`),
  KEY `fk_produit_panier_produit` (`id_produit`),
  CONSTRAINT `fk_produit_panier_panier` FOREIGN KEY (`panier_id`) REFERENCES `panier` (`panier_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_produit_panier_produit` FOREIGN KEY (`id_produit`) REFERENCES `produit` (`id_p`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- Pour les utilisateurs existants, créer un panier vide et l'associer à l'utilisateur
INSERT INTO `panier` (`panier_id`, `panier_date_creation`)
SELECT `user_id`, current_timestamp() FROM `user`;
UPDATE `user` SET `panier_id` = `user_id`;