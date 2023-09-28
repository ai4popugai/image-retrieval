import time
from dres_api import UserApi, ClientRunInfoApi, SubmissionApi, LogApi
from dres_api.configuration import Configuration
from dres_api.models import LoginRequest, UserDetails, QueryResult, QueryEvent
from dres_api.exceptions import ApiException
from omegaconf import OmegaConf


class Client:
    def __init__(self):
        config = OmegaConf.load('credentials.yaml')

        # Setup
        user_api = UserApi()
        self.submission_api = SubmissionApi()
        user_api.api_client.configuration.host = config.host

        try:
            login_request = LoginRequest(username=config.username, password=config.password)
            login = user_api.post_api_v1_login(login_request)
        except ApiException as ex:
            print(f"Could not log in due to exception: {ex.message}")
            return

        # Login successful
        print(f"Successfully logged in.\n"
              f"user: '{login.username}'\n"
              f"role: '{login.role}'\n"
              f"session_id: '{login.session_id}'")

        # Store session token for future requests
        self.session_id = login.session_id

    def submit(self):
        submission_response = None
        try:
            submission_response = self.submission_api.get_api_v1_submit(
                session=self.session_id,
                collection=None,
                item="some_item_name",
                frame=None,
                shot=None,
                timecode="00:00:10:00",
                text=None
            )
        except ApiException as e:
            if e.status == 401:
                print("There was an authentication error during submission. Check the session id.")
            elif e.status == 404:
                print("There is currently no active task which would accept submissions.")
            else:
                print(f"Something unexpected went wrong during the submission: '{e.message}'.")
                return

        if submission_response is not None and submission_response.status:
            print("The submission was successfully sent to the server.")


if __name__ == '__main__':
    client = Client()
    client.submit()