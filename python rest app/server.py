import hashlib
import time

from bson import ObjectId
from sanic import Sanic
from sanic.exceptions import abort
from sanic.request import Request
from sanic.response import json, text
from sanic.views import HTTPMethodView
from sanic_motor import BaseModel
from sanic_jwt import initialize, protected, exceptions

app = Sanic('some_name')
app.config.update({"MOTOR_URI": "mongodb://localhost:27017/myapp"})
BaseModel.init_app(app)


class User(BaseModel):
    __coll__ = "users"
    __unique_fields__ = ['username']


class Post(BaseModel):
    __coll__ = "posts"


def hash_password(password: str):
    salt = "x2Q!T-3(pmrsNcBMeKA0MS!7ZQgcv_Jy"  # This should be private!
    return hashlib.sha512((password + salt).encode("ascii")).hexdigest()


class JWTUser:

    def __init__(self, id, username, password):
        self.user_id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "User(id='{}')".format(self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username}


async def authenticate(request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = await User.find_one({"username": username, "password": hash_password(password)})
    if user is None:
        raise exceptions.AuthenticationFailed("Credentials aren't valid")

    return JWTUser(str(user["_id"]), user["username"], user["password"])


initialize(app, authenticate=authenticate)


class PostsView(HTTPMethodView):
    decorators = [protected()]

    async def post(self, request: Request):
        title = request.json.get("title")
        if title is None or not title:
            abort(400, "'title' is required")
        now = time.time()
        post = await Post.insert_one({"title": title, "createdAt": now})
        return json({"title": title, "createdAt": now, "id": str(post.inserted_id)})

    async def get(self, request: Request):
        posts = await Post.find({})
        responses = []
        for post in posts.objects:
            responses.append({
                "id": str(post["_id"]),
                "title": post["title"],
                "createdAt": post["createdAt"]
            })

        return json(responses)


class PostView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request: Request, id):
        if not ObjectId.is_valid(id):
            abort(400, "Id is not valid!")

        post = await Post.find_one({"_id": ObjectId(id)})

        if post is None:
            abort(404, "Post not found!")
        return json({
            "title": post["title"],
            "createdAt": post["createdAt"],
            "id": str(post["_id"])
        })

    async def delete(self, request: Request, id):
        if not ObjectId.is_valid(id):
            abort(400, "Id is not valid!")

        post = await Post.find_one({"_id": ObjectId(id)})

        if post is None:
            abort(404, "Post not found!")
        await Post.delete_one({"_id": ObjectId(id)})
        return text("Post deleted", status=201)


class RegisterView(HTTPMethodView):
    async def post(self, request: Request):
        username = request.json.get("username")
        password = request.json.get("password")
        if username is None or not username:
            abort(400, "'username' field is required!")
        if password is None or not password:
            abort(400, "'password' field is required!")

        username = username.strip()
        password = password.strip()

        username_len = len(username)
        password_len = len(password)

        if username_len <= 4 or username_len > 16:
            abort(400, "'username' has to have 4 or more characters (not more than 16)")

        if password_len <= 4 or password_len > 16:
            abort(400, "'password' has to have 4 or more characters (not more than 16)")

        user = await User.find_one({"username": username})
        if user is not None:
            abort(400, "'username' is already taken!")

        hashed_password = hash_password(password)
        await User.insert_one({"username": username, "password": hashed_password})
        return json("User created!", status=201)


app.add_route(RegisterView.as_view(), "/register")
app.add_route(PostsView.as_view(), "/posts")
app.add_route(PostView.as_view(), "/posts/<id>")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False, access_log=False)
