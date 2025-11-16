"""
Script de génération de données aléatoires avec Faker
Génère des produits de différents types avec des données réalistes
"""
from faker import Faker
from datetime import datetime
from sqlmodel import Session, select
from database import engine
from models import Produit
import random

fake = Faker('fr_FR')  # Utilisation de la locale française

# Définition des types de produits avec leurs caractéristiques
PRODUCT_TYPES = {
    "Électronique": {
        "prefixes": ["Smartphone", "Ordinateur", "Tablette", "Casque", "Montre connectée", 
                     "Écran", "Clavier", "Souris", "Webcam", "Enceinte"],
        "price_range": (50, 2000)
    },
    "Vêtements": {
        "prefixes": ["T-shirt", "Pantalon", "Veste", "Robe", "Pull", 
                     "Chaussures", "Manteau", "Jean", "Short", "Chemise"],
        "price_range": (15, 300)
    },
    "Alimentation": {
        "prefixes": ["Chocolat", "Café", "Thé", "Biscuits", "Pâtes", 
                     "Riz", "Huile", "Jus", "Confiture", "Céréales"],
        "price_range": (2, 50)
    },
    "Maison": {
        "prefixes": ["Lampe", "Coussin", "Tapis", "Vase", "Cadre photo", 
                     "Poubelle", "Miroir", "Horloge", "Rideau", "Étagère"],
        "price_range": (10, 500)
    },
    "Sport": {
        "prefixes": ["Ballon", "Raquette", "Tapis de yoga", "Haltères", "Vélo", 
                     "Corde à sauter", "Gants", "Maillot", "Basket", "Sac de sport"],
        "price_range": (15, 800)
    },
    "Livres": {
        "prefixes": ["Roman", "BD", "Manga", "Guide", "Dictionnaire", 
                     "Atlas", "Encyclopédie", "Livre de cuisine", "Essai", "Polar"],
        "price_range": (5, 40)
    },
    "Jardin": {
        "prefixes": ["Plante", "Outil de jardinage", "Pot", "Engrais", "Tondeuse", 
                     "Arrosoir", "Gant de jardinage", "Serre", "Bac à compost", "Fontaine"],
        "price_range": (8, 600)
    }
}

def generate_designation(product_type: str) -> str:
    """Génère une désignation réaliste pour un produit"""
    config = PRODUCT_TYPES[product_type]
    prefix = random.choice(config["prefixes"])
    
    # Ajout de détails aléatoires
    details = []
    if random.random() > 0.5:
        details.append(fake.color_name())
    if random.random() > 0.6:
        details.append(random.choice(["Premium", "Pro", "Standard", "Deluxe", "Basic", "Ultra"]))
    
    if details:
        return f"{prefix} {' '.join(details)}"
    return prefix

def generate_price(product_type: str) -> float:
    """Génère un prix réaliste pour un type de produit"""
    min_price, max_price = PRODUCT_TYPES[product_type]["price_range"]
    price = round(random.uniform(min_price, max_price), 2)
    # Arrondir souvent à .99 ou .00
    if random.random() > 0.5:
        price = round(price - 0.01, 2)
    return price

def generate_stock() -> int:
    """Génère un niveau de stock réaliste"""
    # Distribution non uniforme : plus de produits avec stock moyen
    weights = [0.1, 0.3, 0.4, 0.15, 0.05]  # Très bas, Bas, Moyen, Haut, Très haut
    ranges = [(0, 5), (5, 20), (20, 100), (100, 300), (300, 1000)]
    selected_range = random.choices(ranges, weights=weights)[0]
    return random.randint(*selected_range)

def generate_promotion() -> float | None:
    """Génère un prix promotionnel (30% de chance)"""
    if random.random() < 0.3:
        return round(random.uniform(0.7, 0.95), 2)  # 5% à 30% de réduction
    return None

def generate_fake_products(num_products: int = 50):
    """
    Génère un nombre spécifié de produits avec des données aléatoires
    
    Args:
        num_products: Nombre de produits à générer (défaut: 50)
    """
    print(f"🎲 Génération de {num_products} produits aléatoires avec Faker...")
    
    sql_statements = []
    
    with Session(engine) as session:
        # Vérifie combien de produits existent déjà
        existing_count = len(session.exec(select(Produit)).all())
        print(f"📊 Produits existants dans la base: {existing_count}")
        
        products_created = 0
        
        for i in range(num_products):
            # Sélection aléatoire du type de produit
            product_type = random.choice(list(PRODUCT_TYPES.keys()))
            
            # Génération des données
            designation = generate_designation(product_type)
            prix_ht = generate_price(product_type)
            stock = generate_stock()
            promo = generate_promotion()
            
            # Date aléatoire dans les 180 derniers jours
            date_creation = fake.date_time_between(start_date='-180d', end_date='now')
            
            # Création du produit
            produit = Produit(
                type_p=product_type,
                designation_p=designation,
                prix_ht=prix_ht,
                date_in=date_creation,
                timeS_in=datetime.now(),
                stock_p=stock,
                image_p="default.png",
                ppromo=promo
            )
            
            session.add(produit)
            
            # Génération de l'instruction SQL
            promo_value = f"{promo}" if promo else "NULL"
            designation_escaped = designation.replace("'", "''")
            sql = f"INSERT INTO produit (type_p, designation_p, prix_ht, date_in, timeS_in, stock_p, image_p, ppromo) VALUES ('{product_type}', '{designation_escaped}', {prix_ht}, '{date_creation.strftime('%Y-%m-%d')}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', {stock}, 'default.png', {promo_value});"
            sql_statements.append(sql)
            
            products_created += 1
            
            # Affichage de la progression tous les 10 produits
            if (i + 1) % 10 == 0:
                print(f"  ✓ {i + 1}/{num_products} produits générés...")
        
        # Commit de tous les produits
        session.commit()
        print(f"\n✅ {products_created} nouveaux produits créés avec succès!")
        
        # Écriture du fichier SQL
        with open('produits_generes.sql', 'w', encoding='utf-8') as f:
            f.write("-- Produits générés automatiquement\n\n")
            for sql in sql_statements:
                f.write(sql + '\n')
        
        print(f"📄 Fichier produits_generes.sql créé avec {len(sql_statements)} instructions SQL")
        
        # Affichage des statistiques par type
        print("\n📈 Répartition par type:")
        for product_type in PRODUCT_TYPES.keys():
            count = len(session.exec(select(Produit).where(Produit.type_p == product_type)).all())
            print(f"  • {product_type}: {count} produits")

if __name__ == "__main__":
    import sys
    
    # Permet de spécifier le nombre de produits en argument
    num_products = 50
    if len(sys.argv) > 1:
        try:
            num_products = int(sys.argv[1])
        except ValueError:
            print("⚠️  Argument invalide, utilisation de la valeur par défaut (50)")
    
    generate_fake_products(num_products)
