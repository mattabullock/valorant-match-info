import requests
import json
import urllib.parse


class ValorantAPI(object):
    access_token = None
    cookies = None
    entitlements_token = None

    def __init__(self, username, password, region):
        self.username = username
        self.password = password
        self.region = region

        self.authenticate()

        self.user_info, self.game_name = self.get_user_info()

    def get_cookies(self):
        data = {
            "client_id": "play-valorant-web-prod",
            "nonce": "1",
            "redirect_uri": "https://playvalorant.com/opt_in",
            "response_type": "token id_token",
            "scope": "account openid",
        }
        r = requests.post(
            "https://auth.riotgames.com/api/v1/authorization",
            json=data,
        )

        # If handle_response wants to retry
        if self.handle_response(r):
            r = requests.post(
                "https://auth.riotgames.com/api/v1/authorization",
                json=data,
            )

        cookies = r.cookies

        return cookies

    def get_access_token(self):
        data = {"type": "auth", "username": self.username, "password": self.password}
        r = requests.put(
            "https://auth.riotgames.com/api/v1/authorization",
            json=data,
            cookies=self.cookies,
        )

        # If handle_response wants to retry
        if self.handle_response(r):
            r = requests.put(
                "https://auth.riotgames.com/api/v1/authorization",
                json=data,
                cookies=self.cookies,
            )

        uri = r.json()["response"]["parameters"]["uri"]
        jsonUri = urllib.parse.parse_qs(uri)

        access_token = jsonUri["https://playvalorant.com/opt_in#access_token"][0]
        print("access token: " + access_token)

        return access_token

    def get_entitlements_token(self):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        r = requests.post(
            "https://entitlements.auth.riotgames.com/api/token/v1",
            headers=headers,
            json={},
            cookies=self.cookies,
        )

        # If handle_response wants to retry
        if self.handle_response(r):
            r = requests.post(
                "https://entitlements.auth.riotgames.com/api/token/v1",
                headers=headers,
                json={},
                cookies=self.cookies,
            )

        entitlements_token = r.json()["entitlements_token"]
        print("entitlements token: " + entitlements_token)

        return entitlements_token

    def get_user_info(self):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        r = requests.post(
            "https://auth.riotgames.com/userinfo",
            headers=headers,
            json={},
            cookies=self.cookies,
        )

        # If handle_response wants to retry
        if self.handle_response(r):
            r = requests.post(
                "https://auth.riotgames.com/userinfo",
                headers=headers,
                json={},
                cookies=self.cookies,
            )

        jsonData = r.json()
        user_info = jsonData["sub"]
        name = jsonData["acct"]["game_name"]
        tag = jsonData["acct"]["tag_line"]
        game_name = name + " #" + tag

        return user_info, game_name

    def get_competitive_match_history(self, user_id=""):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-Riot-Entitlements-JWT": f"{self.entitlements_token}",
        }

        user_id = self.user_info if user_id == "" else user_id
        print("user_id")

        r = requests.get(
            f"https://pd.{self.region}.a.pvp.net/mmr/v1/players/{user_id}/competitiveupdates?startIndex=0&endIndex=20",
            headers=headers,
            cookies=self.cookies,
        )

        # If handle_response wants to retry
        if self.handle_response(r):
            r = requests.get(
                f"https://pd.{self.region}.a.pvp.net/mmr/v1/players/{user_id}/competitiveupdates?startIndex=0&endIndex=20",
                headers=headers,
                cookies=self.cookies,
            )

        jsonData = r.json()

        return jsonData

    def get_match_history(self, user_id="", start_index=0, end_index=20):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-Riot-Entitlements-JWT": f"{self.entitlements_token}",
        }
        user_id = self.user_info if user_id == "" else user_id
        r = requests.get(
            f"https://pd.{self.region}.a.pvp.net/match-history/v1/history/{user_id}?startIndex={start_index}&endIndex={end_index}",
            headers=headers,
            cookies=self.cookies,
        )

        # If handle_response wants to retry
        if self.handle_response(r):
            r = requests.get(
                f"https://pd.{self.region}.a.pvp.net/match-history/v1/history/{user_id}?startIndex={start_index}&endIndex={end_index}",
                headers=headers,
                cookies=self.cookies,
            )

        jsonData = r.json()

        return jsonData

    def get_match_details(self, match_id):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-Riot-Entitlements-JWT": f"{self.entitlements_token}",
        }

        r = requests.get(
            f"https://pd.{self.region}.a.pvp.net/match-details/v1/matches/{match_id}?startIndex=0&endIndex=20",
            headers=headers,
            cookies=self.cookies,
        )

        # If handle_response wants to retry
        if self.handle_response(r):
            r = requests.get(
                f"https://pd.{self.region}.a.pvp.net/match-details/v1/matches/{match_id}?startIndex=0&endIndex=20",
                headers=headers,
                cookies=self.cookies,
            )

        jsonData = r.json()

        return jsonData

    def get_content_ids(self):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-Riot-Entitlements-JWT": f"{self.entitlements_token}",
            "X-Riot-ClientVersion": "release-01.14-32-502227",
        }

        r = requests.get(
            "https://shared.na.a.pvp.net/content-service/v2/content",
            headers=headers,
            cookies=self.cookies,
        )

        # If handle_response wants to retry
        if self.handle_response(r):
            r = requests.get(
                "https://shared.na.a.pvp.net/content-service/v2/content",
                headers=headers,
                cookies=self.cookies,
            )

        jsonData = r.json()

        return jsonData

    def authenticate(self) -> None:
        self.cookies = self.get_cookies()
        self.access_token = self.get_access_token()
        self.entitlements_token = self.get_entitlements_token()

    def handle_response(self, response) -> bool:
        """
        Returns if you should retry the request
        """
        # request succeeded
        if response.status_code == 200:
            return False

        # authentication expired
        response_json = response.json()
        if response_json["httpStatus"] == 400:
            self.authenticate()
            return True

        raise UnexpectedResponse("Got unexpected response", response_json)


class UnexpectedResponse(Exception):
    def __init__(self, message, data):
        self.message = message
        self.data = data

    def __str__(self):
        return f"{self.message} - {str(self.data)}"
