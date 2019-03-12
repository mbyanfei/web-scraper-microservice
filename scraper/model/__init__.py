from extensions import db


class PageText(db.Model):
    url = db.Column(db.String, primary_key=True)
    text = db.Column(db.String)

    def __repr__(self):
        return '<PageText {}>'.format(self.url)


class PageImage(db.Model):
    url = db.Column(db.String, primary_key=True)
    image = db.Column(db.LargeBinary)
    page_url = db.Column(db.String)

    def __repr__(self):
        return '<PageImage {}>'.format(self.url)
