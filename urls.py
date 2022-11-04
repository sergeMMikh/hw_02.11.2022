from app import app
from views import UserView, AdvView

app.add_url_rule('/user/<int:user_id>', view_func=UserView.as_view('users_get'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/user/', view_func=UserView.as_view('users'), methods=['POST'])
app.add_url_rule('/adv/<int:adv_id>', view_func=AdvView.as_view('adv_get'), methods=['GET', 'DELETE'])
app.add_url_rule('/adv/', view_func=AdvView.as_view('adv'), methods=['POST'])