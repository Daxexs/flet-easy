from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Optional, Union

from flet import Page

from flet_easy.core.job import Job
from flet_easy.core.models import Msg
from flet_easy.exceptions import (
    AlgorithmJwtError,
    ConfigurationError,
    LoginError,
    LogoutError,
    SecretKeyError,
)
from flet_easy.migration import go_page
from flet_easy.security.config import (
    DecodeError,
    ExpiredSignatureError,
    InvalidKeyError,
    SecretKey,
    _decode_payload,
    encode_verified,
)
from flet_easy.ui.controls import SessionStorageEdit, SharedPreferencesEdit


class AuthMixin:
    """Mixin containing all logic for Authentication, JWT decoding, Storage, and Session Management."""

    page: Page
    _shared_preferences: Union[SessionStorageEdit, SharedPreferencesEdit]
    _use_client_storage: bool
    key_login: Optional[str]
    _key_login: Optional[str]
    _login_done: bool
    _sleep_auth: int
    route_login: Optional[str]
    secret_key: Optional[SecretKey]
    auto_logout: bool
    _run_go: Callable[..., Any]

    """--------- Storage Compatibility Helpers -------"""

    def _get_client_identity(self) -> Optional[tuple[str, str]]:
        """Returns (client_ip, client_user_agent) if both are available, else None."""
        client_ip = getattr(self.page, "client_ip", None)
        client_user_agent = getattr(self.page, "client_user_agent", None)
        if client_ip and client_user_agent:
            return client_ip, client_user_agent
        return None

    async def _storage_set_async(self, key: str, value: Any) -> None:
        if self._use_client_storage:
            client_storage = getattr(self.page, "client_storage")  # noqa: B009
            await client_storage.set_async(key, value)
        else:
            await self._shared_preferences.set(key, str(value))

    async def _storage_get_async(self, key: str) -> Any:
        try:
            if self._use_client_storage:
                client_storage = getattr(self.page, "client_storage")  # noqa: B009
                return await client_storage.get_async(key)

            return await self._shared_preferences.get(key)
        except Exception:
            await self._storage_remove_async(key)
            return None

    async def _storage_remove_async(self, key: str) -> None:
        if self._use_client_storage:
            client_storage = getattr(self.page, "client_storage")  # noqa: B009
            await client_storage.remove_async(key)
        else:
            await self._shared_preferences.remove(key)

    """--------- login authentication : asynchronously | synchronously -------"""

    def _evaluate_secret_key(self) -> None:
        """Validates that the provided SecretKey matches the chosen algorithm's requirements."""

        if self.secret_key is None:
            raise SecretKeyError("SecretKey is not configured.")

        valid = (
            self.secret_key.secret is None
            and self.secret_key.algorithm == "RS256"
            or self.secret_key.pem_key is None
            and self.secret_key.algorithm == "HS256"
        )
        if not valid:
            raise SecretKeyError(
                f"Algorithm '{self.secret_key.algorithm}' mismatch: "
                f"HS256 requires 'secret' (pem_key must be None), "
                f"RS256 requires 'pem_key' (secret must be None). "
                f"Got secret={'set' if self.secret_key.secret else 'None'}, "
                f"pem_key={'set' if self.secret_key.pem_key else 'None'}."
            )

    @property
    def _active_key(self) -> Any:
        """Returns the correct decoding key based on the configured algorithm."""

        if self.secret_key is None:
            raise SecretKeyError("SecretKey is not configured.")

        if self.secret_key.secret is not None:
            return self.secret_key.secret
        if self.secret_key.pem_key is not None:
            return self.secret_key.pem_key.public
        return None

    def _create_task_login_update(self, decode: dict[str, Any]) -> None:
        """Updates the login status, in case it does not exist it creates a new task that checks the user's login status."""

        if self._key_login is None:
            raise LoginError("Key login is not configured.")
        exp = decode.get("exp")
        if exp is None:
            return

        time_exp = datetime.fromtimestamp(float(exp), tz=timezone.utc)
        time_now = datetime.now(tz=timezone.utc)
        time_res = time_exp - time_now
        self._login_done = True
        Job(
            func=self.logout,
            key=str(self._key_login),
            every=time_res,
            page=self.page,
            login_done=lambda: self._login_done,
            sleep_time=self._sleep_auth,
        ).start()

    def page_web_pubsub(self, msg: Msg) -> None:
        identity = self._get_client_identity()
        if identity:
            client_ip, client_user_agent = identity
            self.page.pubsub.send_all_on_topic(client_ip + client_user_agent, msg)
        else:
            raise LoginError("page_web_pubsub: client_ip or client_user_agent not available.")

    def logout(self, key: str, next_route: Optional[str] = None) -> None:
        """Closes the sessions of all browser tabs or the device used, which has been previously configured with the `login` method.

        ## Parameters
        - key: Key to store the value used in the `login` method of `Datasy`.
        - next_route: Route to redirect to after logout.
        """

        if self.route_login is None and next_route is None:
            raise ConfigurationError(
                "Cannot logout: no route to redirect to. "
                "Set 'route_login' in FletEasy() or pass 'next_route' to logout()."
            )

        if self.page.web:
            self.page_web_pubsub(Msg("logout", key, {"next_route": next_route}))
        else:
            self.page.run_task(self._storage_remove_async, key)
            self.page.run_task(go_page, self.page, next_route or self.route_login)

    async def _logout_init(self, topic: str, msg: Msg) -> None:
        """Initializes the logout process."""

        if msg.method == "login":
            val = msg.value
            if isinstance(val, dict) and msg.key is not None:
                await self._storage_set_async(msg.key, val.get("value"))
                if self.page.route == self.route_login:
                    target = val.get("next_route")
                    if target:
                        await go_page(self.page, str(target))

        elif msg.method == "logout":
            self._login_done = False
            if msg.key is not None:
                await self._storage_remove_async(msg.key)
            val = msg.value
            target = val.get("next_route") if isinstance(val, dict) else None
            target = target or self.route_login
            if target:
                await go_page(self.page, str(target))

        elif msg.method == "updateLogin":
            self._login_done = bool(msg.value)

        elif msg.method == "updateLoginSessions":
            self._login_done = bool(msg.value)

            if self.key_login is None:
                raise ConfigurationError("key_login is not configured in FletEasy().")

            if self.secret_key is None:
                raise SecretKeyError("SecretKey is not configured.")

            if self.secret_key.algorithm is None:
                raise AlgorithmJwtError("Algorithm not configured in SecretKey.")

            jwt = await self._storage_get_async(self.key_login)

            if jwt:
                self._create_task_login_update(
                    decode=_decode_payload(
                        jwt=jwt,
                        secret_key=self._active_key,
                        algorithms=self.secret_key.algorithm,
                    )
                )
        else:
            raise ConfigurationError(
                f"Unknown pubsub method '{msg.method}' received in session handler. "
                f"Expected: 'login', 'logout', 'updateLogin', or 'updateLoginSessions'."
            )

    def _create_login(self) -> None:
        """Create the connection between sessions."""
        if self.page.web:
            identity = self._get_client_identity()
            if identity:
                client_ip, client_user_agent = identity
                self.page.pubsub.subscribe_topic(client_ip + client_user_agent, self._logout_init)
            else:
                raise LoginError(
                    "_create_login: client_ip or client_user_agent not available for web session."
                )

    def _create_tasks(self, time_expiry: Optional[timedelta], key: str, sleep: int) -> None:
        """Creates the logout task when logging in."""
        if time_expiry is not None:
            Job(
                func=self.logout,
                key=key,
                every=time_expiry,
                page=self.page,
                login_done=lambda: self._login_done,
                sleep_time=sleep,
            ).start()

    def _login_core(
        self,
        key: str,
        value: Any,
        next_route: str,
        time_expiry: Optional[timedelta] = None,
        sleep: int = 1,
    ) -> Any:
        """Core login logic."""

        if time_expiry:
            if not isinstance(value, dict):
                raise ConfigurationError(
                    f"login() 'value' must be a dict when 'time_expiry' is set, "
                    f"got {type(value).__name__}. Use a dict for JWT payload or remove time_expiry."
                )
            if self.secret_key is None:
                raise SecretKeyError(
                    "login() requires 'secret_key' in FletEasy() when 'time_expiry' is used. "
                    "Example: FletEasy(secret_key=SecretKey(secret='your-secret', algorithm='HS256'))"
                )

        if self.secret_key:
            self._evaluate_secret_key()
            self._key_login = key
            self._sleep_auth = sleep
            value = encode_verified(self.secret_key, value, time_expiry)
            self._login_done = True

        if self.auto_logout:
            self._create_tasks(time_expiry, key, sleep)

        if self.page.web:
            self.page_web_pubsub(Msg("login", key, {"value": value, "next_route": next_route}))

        return value

    def login(
        self,
        key: str,
        value: Any,
        next_route: str,
        time_expiry: Optional[timedelta] = None,
        sleep: int = 1,
    ) -> None:
        """Registering in the client's storage the key and value in all browser or device sessions.

        ## Parameters
        - key: Key to store the value.
        - value: Value to store.
        - next_route: Route to redirect to after login.
        - time_expiry: Time to expire the value.
        - sleep: Time to sleep before logging out.
        """
        try:
            self.page.run_task(self.login_async, key, value, next_route, time_expiry, sleep).result(
                timeout=5
            )
        except TimeoutError as e:
            raise LoginError("Login error, using login_async() instead.", e)

    async def login_async(
        self,
        key: str,
        value: Any,
        next_route: str,
        time_expiry: Optional[timedelta] = None,
        sleep: int = 1,
    ) -> None:
        """Registering in the client's storage the key and value in all browser or device sessions.

        ## Parameters
        - key: Key to store the value.
        - value: Value to store.
        - next_route: Route to redirect to after login.
        - time_expiry: Time to expire the value.
        - sleep: Time to sleep before logging out.
        """

        value = self._login_core(key, value, next_route, time_expiry, sleep)
        await self._storage_set_async(key, value)

        async def _go_route() -> None:
            await self._run_go(next_route)

        self.page.run_task(_go_route)

    def decode_jwt(self, key: str) -> Union[dict[str, Any], bool]:
        """Decode JWT

        ## Parameters
        - key: Key to store the value used in the `login` method of `Datasy`.
        """
        try:
            return self.page.run_task(self.decode_jwt_async, key).result(timeout=5)
        except TimeoutError as e:
            raise LoginError("Decode error, using decode_async:", e)

    async def decode_jwt_async(self, key_login: str) -> Union[dict[str, Any], bool]:
        """Decode JWT asynchronously

        ## Parameters
        - key: Key to store the value used in the `login` method of `Datasy`.
        """
        jwt_token = await self._storage_get_async(key_login)

        try:
            self._key_login = key_login

            self._evaluate_secret_key()

            if self.secret_key is None:
                raise SecretKeyError("SecretKey is not configured.")

            if jwt_token is None:
                return False

            if self.auto_logout and not self._login_done:
                identity = self._get_client_identity()
                if identity:
                    client_ip, client_user_agent = identity
                    self.page.pubsub.send_others_on_topic(
                        client_ip + client_user_agent, Msg("updateLogin", value=self._login_done)
                    )

            if self.secret_key.algorithm is None:
                raise AlgorithmJwtError("Algorithm not configured in SecretKey.")

            decode = _decode_payload(
                jwt=jwt_token,
                secret_key=self._active_key,
                algorithms=self.secret_key.algorithm,
            )

            # It checks if there is a logout time, if there is a logout task running
            if decode.get("exp") and not self._login_done and self.auto_logout:
                self._create_task_login_update(decode)
            return decode

        except (ExpiredSignatureError, InvalidKeyError):
            self.logout(key_login)
            return False
        except DecodeError as e:
            self.logout(key_login)
            raise LogoutError(
                "Decoding error, possibly there is a double use of the storage 'key', Secret key invalid! or ",
                e,
            )
