# django-channels-redis-chatapp 

## Setup Steps:

1. Install docker:

        https://docs.docker.com/engine/install/ubuntu/

2. Open the terminal and run the below command to spin up the redis container:

        sudo docker run --rm -p 6379:6379 redis:7
3. Clone the repository from Github and switch to the new directory:

        $ git clone https://github.com/VedankPande/django-channels-redis-chatapp.git

        $ cd chatapp
    
4. Activate the virtualenv for your project (optional, but recommended)
    
5. Install project dependencies:

        $ pip install -r requirements.txt

6. Apply the migrations:

        $ python manage.py migrate  

7. Run the development server:

        $ python manage.py runserver


## Using Postman to test the APIs

- POST http://127.0.0.1:8000/api/login/

        Login endpoint that takes a username and password. Returns an access and refresh token. (Refresh token is set as a HTTP Only Cookie)

- POST http://127.0.0.1:8000/api/register/

        Register endpoint that takes username,email, and password and registers a user

- POST http://127.0.0.1:8000/api/logout/

        Logout endpoint that sets the user as offline and blacklists the refresh token saved in the cookie

- POST http://127.0.0.1:8000/api/login/refresh/

        Endpoint that accepts a refresh token and returns a new access and refresh token pair. Previous refresh token is blacklisted for security.

- GET http://127.0.0.1:8000/api/online-users/

        Endpoint to retrieve a list of users that are "online"

- GET http://127.0.0.1:8000/api/suggested-friends/<int:user_id>

        Endpoint to get a list of suggested users for the `user_id` that is provided in the url

- http://127.0.0.1:8000/api/chat/start/<int:user_id>

        Endpoint that returns a success if the specified is online and an error if offline

- ws://127.0.0.1:8000/chat/send/<int:target>?sender=

        - Websocket endpoint for users to connect with other users and send messages
        - IMPORTANT: The endpoint takes query parameters to specify sender and receivers
        - example:  ws://127.0.0.1:8000/chat/send/1?sender=2 - 1 refers to the user id to which you wish to connect to and `sender` is the current users id
         


