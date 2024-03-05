from flask import Flask
from flask_mysqldb import MySQL
app = Flask(__name__)
# Configure MySQL connection (qui sera en réalité une connexion MariaDB)
app.config['MYSQL_HOST'] = '10.0.5.20'
app.config['MYSQL_USER'] = 'mon_utilisateur'
app.config['MYSQL_PASSWORD'] = 'mon_mot_de_passe'
app.config['MYSQL_DB'] = 'ma_base_de_donnee'
mysql = MySQL(app)
@app.route('/')
def index():
	cur = mysql.connection.cursor()
	# Créer une table si elle n'existe pas
	cur.execute('''CREATE TABLE IF NOT EXISTS visits (id INT AUTO_INCREMENT PRIMARY KEY,timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
	# Insérer un nouvel enregistrement de visite
	cur.execute('INSERT INTO visits (id) VALUES (NULL)')
	mysql.connection.commit()
	# Récupérer le nombre de visites
	cur.execute('SELECT COUNT(*) FROM visits')
	visit_count = cur.fetchone()[0]
	cur.close()
	return f'Bonjour, monde ! Cette page a été visitée {visit_count} fois.'
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=80)
