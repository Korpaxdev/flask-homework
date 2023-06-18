from flask import Flask

from utils.sq import Sq
from views.advertisement_detail import AdvertisementDetailView
from views.index import IndexView
from views.user_login import UserLogin
from views.user_logout import UserLogoutView
from views.user_registration import UserRegistrationView

app = Flask(__name__)
Sq.create_engine().create_tables()

app.add_url_rule("/advertisements/", view_func=IndexView.as_view(name="advertisements"))
app.add_url_rule("/advertisements/<id>/", view_func=AdvertisementDetailView.as_view(name="advertisement_detail"))

app.add_url_rule("/users/register/", view_func=UserRegistrationView.as_view(name="user_registration"))
app.add_url_rule("/users/login/", view_func=UserLogin.as_view(name="user_login"))
app.add_url_rule("/users/logout/", view_func=UserLogoutView.as_view(name="user_logout"))
