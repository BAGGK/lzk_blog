from blog import db
from blog.fitness.model import Fitness

session: db.Session = db.session

session.query(Fitness)

