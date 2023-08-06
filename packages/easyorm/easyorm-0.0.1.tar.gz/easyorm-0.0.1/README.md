
This is a simple example package. You can use

# easyorm   
easyorm is a basic simple orm

list of database :
- [x] sqlite
- [x] mysql
- [ ] mongodb

Create new model
- > python manager.py model
- > nom du module : <new_module>
- > encodage utilisé : utf-8
- > mode de base de données : (db_sqLite_source ou db_mysql_source)
- > nom de la base de données : (nouvelle_base_de_données)
- > nom de la propriété : (nouvelle_propriété ou entre pour quitter)
- > type de propriété : (string, integer, boolean)
- > taille : (valeur_entière)
- > valeur par défaut : (facultatif)
- > utiliser comme valeur unique ? (True or False)
- > valeur doit être obligatoire ? (True or False)
- > description de la propriété : (facultatif)

method list of model
- > get()
- > add()
- > findOne(parms :id)
- > find()
- > remove()
- > execute(query)

liste des datasource
- > 1- db_mysql_source
- > 2- db_sqlite_source
- > 3- db_mongo_source

liste des types de variable prise en compte
- > 1- string
- > 2- integer
- > 3- boolean