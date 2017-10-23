from gammabin import db


class Paste(db.Model):
    __tablename__ = 'pastes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    content = db.Column(db.Text)
    expiration = db.Column(db.DateTime)
    uri = db.Column(db.String(), nullable=False)

    author_ip = db.Column(db.String(), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    views = db.Column(db.Integer, nullable=False)
    private = db.Column(db.String(), nullable=False)

    def __init__(self, title, content, expiration, uri, author_ip, time, private):
        self.title = title
        self.content = content
        self.expiration = expiration
        self.uri = uri
        self.author_ip = author_ip
        self.time = time
        self.views = 0
        self.private = private

    def as_dict(self):
        result = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        del result['id']
        return result
