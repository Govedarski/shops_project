from enum import Enum


class UserRoles(Enum):
    customer = "Customer"
    owner = "Shop Owner"


class AdminRoles(Enum):
    admin = "Admin"
    super_admin = "Super Admin"


class ProductCategories(Enum):
    clothing = "Clothing"
    shoes = "Shoes"
    electronics = "Consumer electronics"
    books = "Books"
    games = "Games"
    cosmetics = "Cosmetics and body care"
    accessories = "Accessories"
    food = "Food and drinks"
    appliances = "Household appliances"
    furniture = "Furniture and household goods"
    sport = "Sport and outdoor"
    toys = "Toys and baby products"
    gardens = "Garden"
    pets = "Pets"


class PaymentMethod(Enum):
    online = "Online"
    cache = "Cache"
