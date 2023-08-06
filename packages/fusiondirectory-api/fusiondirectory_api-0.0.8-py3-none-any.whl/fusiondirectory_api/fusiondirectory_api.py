"""
A wrapper for the webservice (RPC API) for FusionDirectory.
"""

import requests


class FusionDirectoryAPI:
    def __init__(
        self,
        host,
        user,
        password,
        database,
        verify_cert=True,
        login=True,
        enforce_encryption=True,
        client_id="python_api_wrapper",
    ):
        """
        Log in to FusionDirectory server (Request a session ID)

        Args:
            host: The address of the FusionDirectory host including protocol (https://)
            user: The name of the FD user to log in as
            password: The password of the FD user
            database: The database to use (As seen in FD GUI)
            verify_cert: Verify server certificate (Default: True).
            See requests documentation for options (https://2.python-requests.org/en/master/user/advanced/#verification)
            login: Automatically log in on object instantiation (Default: True)
            enforce_encryption: Raise an exception if traffic is unencrypted (Not https:// in host)
        """

        # Must encrypt traffic
        if "https://" not in host and enforce_encryption:
            raise ValueError("Unencrypted host not allowed: {host}")

        # The session to use for all requests
        self._session = requests.Session()

        # The URL of the FD server
        self._url = f"{host}/jsonrpc.php"

        # Log in to get this ID from FD
        self._session_id = None

        # Pass to requests
        self._verify_cert = verify_cert

        # Send this ID with all requests
        self._client_id = client_id

        # Login to FD (Get a session_id)
        if login:
            self.login(user, password, database)

    def delete_object(self, object_type, object_dn):
        """
        Delete an object

        Args:
            object_type (str): The type of the object to remove
            object_dn (str): The DN of the object to remove

        Returns:
            True on success
        """
        data = {
            "method": "delete",
            "params": [self._session_id, object_type, object_dn],
        }
        r = self._post(data)
        # Api returns nothing on success, so anything is an error
        if r:
            raise LookupError(r)
        else:
            return True

    def get_base(self):
        """
        Return the configured LDAP base for the selected LDAP
        in this webservice session (see login)
        """
        data = {"method": "getBase", "params": [self._session_id]}
        return self._post(data)

    def get_fields(self, object_type, object_dn=None, tab=None):
        """
        Get all fields of an object type as they are stored in FusionDirectory.
        Not very usefull unless using data for a GUI.

        Args:
            object_type (str): The type of object to get the fields for
            dn (str): The optional object to load values from
            tab (str): The name tab to show (main by default)

        Returns:
            All FD attributes organized as sections
        """
        data = {
            "method": "getFields",
            "params": [self._session_id, object_type, object_dn, tab],
        }
        return self._post(data)

    def get_number_of_objects(self, object_type, ou=None, filter=None):
        """
        Get the number of a given object type limited by OU and/or filter

        Args:
            object_type (str): The object type
            ou (str): The OU to search for objects in. Base is used if OU is None
            filter (str): An LDAP filter to limit the results

        Returns:
            The number of objects of type object_type in the OU (int)
            Some object types including "DASHBOARD", "SPECIAL", "LDAPMANAGER"
            maybe others, results in a None value from the API. This functions
            returns -1 in those cases.
        """

        data = {
            "method": "count",
            "params": [self._session_id, object_type, ou, filter],
        }
        r = self._post(data)
        # The API returns None for some object types
        # I'm aware of these: ["DASHBOARD", "SPECIAL", "LDAPMANAGER"]
        # Let's return -1, so we always return an int
        if r == None:
            r = -1
        # assert type(r) == int
        return r

    def get_session_id(self):
        """
        Get current session ID

        Returns:
            The currents session id (str)
        """
        # Not logged in
        if not self._session_id:
            return self._session_id

        data = {"method": "getId", "params": [self._session_id]}
        return self._post(data)

    def get_object(self, object_type, dn, attributes={"objectClass": "*"}):
        """
        Get attributes for a single object.

        Arguments:
            object_type (str): The object type to list
            dn: The DN of the object to retrieve
            attributes: The attributes to fetch.
            If this is a single value, the resulting dictionary will have
            for each dn the value of this attribute.
            If this is an array, the keys must be the wanted attributes,
            and the values can be either 1, '*', 'b64' or 'raw'
            depending if you want a single value or an array of values.
            Other values are considered to be 1.
            'raw' means untouched LDAP value and is only useful for dns.
            'b64' means an array of base64 encoded values and is mainly useful for binary attributes.

        Returns:
            A dictionary of attributes for the object
        """
        # Grab the left most part of the dn (uid=??) as filter
        f = dn.split(",")[0]
        filter = f"({f})"
        # DN with out left most part is OU (Base for search)
        ou = ",".join(dn.split(",")[1:])
        data = {
            "method": "ls",
            "params": [self._session_id, object_type, attributes, ou, filter],
        }
        # FIXME: Check what data is returned if no objects are found
        r = self._post(data)
        # API returns an empty list is on no results. I need a dict.
        if r == []:
            r = {}
        else:
            # Api returns the user's data as value for key DN. We just
            # want the value (The LDAP fields)
            r = r[dn]
        # assert type(r) == dict
        return r

    def get_objects(self, object_type, attributes=None, ou=None, filter=None):
        """
        Get objects of a certain type. Potentially with LDAP attributes and limited
        by OU and/or a filter.

        Arguments:
            object_type (str): The object type to list
            attributes: The attributes to fetch.
            If this is a single value, the resulting dictionary will have
            for each dn the value of this attribute.
            If this is an array, the keys must be the wanted attributes,
            and the values can be either 1, '*', 'b64' or 'raw'
            depending if you want a single value or an array of values.
            Other values are considered to be 1.
            'raw' means untouched LDAP value and is only useful for dns.
            'b64' means an array of base64 encoded values and is mainly useful for binary attributes.
            ou (str): The LDAP branch to search in, base will be used if it is None
            filter (str): An additional filter to use in the LDAP search.

        Returns:
            A list of objects as a dictionary with DN as keys (list)
        """
        data = {
            "method": "ls",
            "params": [self._session_id, object_type, attributes, ou, filter],
        }
        # FIXME: Check what data is returned if no objects are found
        r = self._post(data)
        # An empty list is returned on no results. I need a dict.
        if r == []:
            r = {}
        # assert type(r) == dict
        return r

    def get_databases(self):
        """
        List LDAP databases/servers managed by FD. These are the valid
        values for the 'database' argument in login()

        Returns:
            A dict of databases managed by FusionDirectory. Key is id,
            value is displayable name.
        """
        data = {"method": "listLdaps", "params": []}
        return self._post(data)

    def get_object_types(self):
        """
        Get object types known to the server

        Returns:
            A dictionary with object type as key and
            object name (Used in GUI) as value
        """
        data = {"method": "listTypes", "params": [self._session_id]}
        return self._post(data)

    def get_tabs(self, object_type, object_dn=None):
        """
        Get tabs for on an object type. If a DN is supplied
        the data returned will show if the tab is active
        for the object with the supplied DN.

        Args:
            object_type (str): The object type to get tabs for
            object_dn (str): The dn of an object to get active values from

        Returns:
            A dictionary with tabs as keys and a dictionary with
            tab name (str) and active (Bool)
        """
        data = {
            "method": "listTabs",
            "params": [self._session_id, object_type, object_dn],
        }
        return self._post(data)

    def get_object_type_info(self, object_type):
        """
        Get the information on an object type

        Args:
            object_type: The type of object to get information for

        Returns:
            A dictionary of information on the object type
        """
        data = {"method": "infos", "params": [self._session_id, object_type]}
        return self._post(data)

    def user_is_locked(self, user_dn):
        """
        Is the user locked?

        Args:
            user_dn (str/list): A single DN or a list of DNs

        Returns:
            True if user locked. False if not locked.
        """
        # API accepts both list of DNs and a single DN. I don't
        if type(user_dn) != str:
            raise ValueError("user_dn must be a string")
        data = {"method": "isUserLocked", "params": [self._session_id, user_dn]}
        r = self._post(data)
        # API returns a dict with DN as key, and 0 or 1 in value
        # assert len(r) == 1
        # Return value in dict as bool
        return bool(list(r.values())[0])

    def lock_user(self, user_dn):
        """
        Lock a user

        Args:
            user_dn (str): The DN of the user to lock

        Returns:
            Bool: True on success
        """
        data = {"method": "lockUser", "params": [self._session_id, user_dn, "lock"]}
        self._post(data)
        return True

    def login(self, user, password, database):
        """
        Login to FD by getting a session ID to include in posts

        Args:
            user (str): The username to login as
            password (str): The password of the user
            database (str): The name of the LDAP database/server to use

        Returns:
            Session id (str)
        """
        data = {"method": "login", "params": [database, user, password]}
        self._session_id = self._post(data)
        return self._session_id

    def logout(self):
        """
        Log out of FusionDirectory. Deletes session ID

        Returns:
            Bool: True
        """
        data = {"method": "logout", "params": [self._session_id]}
        r = self._post(data)
        self._session_id = None
        return r

    def get_recovery_token(self, email):
        """
        Generate a password recovery token for a user

        Args:
            email (str): An email address associated with a user

        Returns:
            A recovery token (str)
        """
        data = {"method": "recoveryGenToken", "params": [self._session_id, email]}
        r = self._post(data)
        # FIXME: I get no UID in the dict (Value == None).
        # According to the documentation, I should?
        return r["token"]

    def get_template(self, object_type, template_dn):
        """
        Get a template

        Args:
            object_type (str): The type of the object the template is for
            dn (str): The DN of the template

        Returns:
            dict: FusionDirectory attributes organized as tabs
        """
        data = {
            "method": "gettemplate",
            "params": [self._session_id, object_type, template_dn],
        }
        return self._post(data)

    def delete_tab(self, object_type, object_dn, tab):
        """
        Deletes a tab, with fields, from an object

        Args:
            object_type (str): The type of the object to remove a tab from
            object_dn (str): The dn of the object to remove a tab from
            tab (str): The tab to remove

        Returns:
            The object DN on success
        """
        data = {
            "method": "removetab",
            "params": [self._session_id, object_type, object_dn, tab],
        }
        return self._post(data)

    def _set_fields(self, object_type, object_dn, values):
        """
        Update an object

        Args:
            object_type (str): The type of the object to update
            object_dn (str): The dn of the object to update (Creates new object if None)
            values (str): A dictionary of values to update the object with.
            First level keys are tabs, second level keys should be the same
            keys returned by get_fields (without section, directly the attributes).

        Returns:
            The object DN on success
        """
        data = {
            "method": "setFields",
            "params": [self._session_id, object_type, object_dn, values],
        }
        return self._post(data)

    def create_object(self, object_type, values, template_dn=None):
        """
        Create a new object. Optionally from a template.

        Args:
            object_type (str): The type of object to create
            values (dict): The values to use for the new object.
            template_dn (str): Optional template for object creation
            Outher keys are tabs, then fields with values

        Returns:
            The DN of the created object (str)
        """
        if template_dn:
            return self._create_object_from_template(object_type, template_dn, values)
        else:
            return self._set_fields(object_type, None, values)

    def update_object(self, object_type, object_dn, values):
        """
        Update an object

        Args:
            object_type (str): The type of object update
            values (dict): A dictionary of tabs->field:value
            object_dn (str): The DN of the object to update

        Returns:
            The DN of the updated object (str)
        """
        return self._set_fields(object_type, object_dn, values)

    def set_password(self, uid, password, token):
        """
        Set the password of a user

        Args:
            uid (str): UID of the user to change password for
            password (str): The new password for the user
            token (str): a token generated by a get_recovery_token()

        Returns:
            True on success
        """
        data = {
            "method": "recoveryConfirmPasswordChange",
            "params": [self._session_id, uid, password, password, token],
        }
        return self._post(data)

    def unlock_user(self, user_dn):
        """
        Unlock a user

        Args:
            user_dn (str): The DN of the user to unlock

        Returns:
            result: True on success
        """
        data = {"method": "lockUser", "params": [self._session_id, user_dn, "unlock"]}
        self._post(data)
        return True

    def _create_object_from_template(self, object_type, template_dn, values):
        """
        Create an object from a template

        Args:
            object_type (str): The type of the object to create
            template_dn (str): The dn of the template to use
            values (str): A dictionary of values for the fields in the new object.
            First level keys are tabs, second level keys should be the same
            keys returned by get_fields (without section, directly the attributes).

        Returns:
            The object DN of the new object on success
        """
        data = {
            "method": "usetemplate",
            "params": [self._session_id, object_type, template_dn, values],
        }
        r = self._post(data)
        return r

    def _post(self, data):
        """
        Send data to the FusionDirectory server

        Args:
            data: The data to post

        Returns:
            result: The value of the key 'result' in the JSON returned by the server
        """
        # Client ID (Se we can identify calls in server logs?
        data["id"] = self._client_id

        # Post
        r = self._session.post(self._url, json=data, verify=self._verify_cert)

        # Raise exception on error codes
        r.raise_for_status()

        # Get the json in the response
        r = r.json()

        if r["error"]:
            raise LookupError(f"FD returned error: {r['error']}")
        else:
            # The result value can have the key errors with a list
            if type(r["result"]) == dict and r["result"].get("errors"):
                raise LookupError("".join(r["result"]["errors"]))
            else:
                return r["result"]
