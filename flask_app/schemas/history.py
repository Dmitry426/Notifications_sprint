from app import ma

from flask_app.db.postgresql import db
from flask_app.models.models import AuthHistory


class HistorySchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ("created", "ip_address", "user_agent", "platform", "browser")
        model = AuthHistory
        load_instance = True
        sqla_session = db.session


history_schema = HistorySchema()
histories_schema = HistorySchema(many=True)
