import requests
from urllib.parse import urljoin
from datetime import datetime
from typing import Union
from requests.auth import HTTPBasicAuth
import html
import xml.etree.ElementTree as ET

AUTH_ENDPOINT = "auth/tokens"
MOBILE_DEVICE_ENDPOINT = "v2/mobile-devices"
MOBILE_DEVICE_PRESTAGE_ENDPOINT = "v2/mobile-device-prestages"
SEARCH_DEVICE_ENDPOINT = "v1/search-mobile-devices"

VALIDATION_ENDPOINT = "auth/current"
INVALIDATE_ENDPOINT = "auth/invalidateToken"
CLASSIC_ENDPOINT = "/JSSResource"
CLASSIC_DEVICENAME_ENDPOINT = (
    f"{CLASSIC_ENDPOINT}/mobiledevicecommands/command/DeviceName"
)
CLASSIC_SEARCH_DEVICE_ENDPOINT = f"{CLASSIC_ENDPOINT}/mobiledevices/match"
DEVICES_PAGE_SIZE = 2500


class PCJAMF:
    """
    The PCJAMF class provides an interface to the Pine Crest JAMF
    server for mobile device management (MDM)

    Class Methods:
        available: checks to see if the server is accessible
            server (str): the protocol, url, and port of a JAMF server
            path (str): the path to the server. (optional)
            verify (str, bool): whether to verify SSL certificates.
                Set to a PEM CA store
                for custom validation. Set to False for self-signed certs

    Args:
        username: the username to use for authentication
        password: the password to use for authentication
        server: the JAMF server path, including protocol, fqdn, and port
        verify (str, bool): the path to a CA file for cert verification
            or False to disable SSL certificate verification

    """

    jamf_api_root = "/api/"

    @classmethod
    def available(
        cls,
        server: str,
        path: str = "v2/jamf-pro-server-url",
        verify: Union[str, bool] = True,
    ) -> bool:
        """checks to see if the JAMF server is available

        Args:
            server (str): full url for server, including port
            path (str, optional): endpoint to use for verification.
            Defaults to "v2/jamf-pro-server-url".
            verify (Union[str, bool], optional): whether to verify
            SSL certificates. Defaults to True.

        Returns:
            bool: True if server responds with 2XX or 401, False otherwise
        """

        cls.jamf_url = urljoin(server, cls.jamf_api_root)
        url = urljoin(cls.jamf_url, path)
        response = requests.get(url, verify=verify)
        print(f"{url}: {response.status_code}")
        return response.ok or response.status_code == 401

    def __init__(
        self, username: str, password: str, server: str, verify: Union[str, bool] = True
    ):
        self.jamf_server = server
        self.jamf_url = urljoin(self.jamf_server, self.jamf_api_root)
        self.session = requests.Session()
        self.session.verify = verify
        self.credentials = (username, password)
        self.session.headers.update({"Accept": "application/json"})
        self.token = None
        self.auth_expiration = None
        self.classic_session = requests.Session()
        self.classic_session.verify = verify
        self.classic_session.auth = HTTPBasicAuth(username, password)
        self.classic_session.headers.update({"Accept": "application/xml"})

    def close(self):
        if self.authenticated:
            self.invalidate()
            self.session.close()
            self.classic_session.close()

    def authenticate(self):
        """
        Connect to the JAMF server, authenticate using existing
        credentials, and get an API token

        Raises:
            Exception: [description]
        """

        """
        """
        self.session.auth = self.credentials
        r = self.session.post(self._url(AUTH_ENDPOINT))
        r.raise_for_status()
        auth_data = r.json()
        self.token = auth_data["token"]
        self.auth_expiration = datetime.fromtimestamp(auth_data["expires"] / 1000)
        self.session.auth = None
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    @property
    def authenticated(self) -> bool:
        """
        Indicates if the server object is currently authenticated

        Returns:
            bool: True if the server object is currently authenticated
        """
        return self.token and self.auth_expiration > datetime.now()

    def _url(self, endpoint):
        return urljoin(self.jamf_url, endpoint)

    def all_devices(self) -> Union[list, dict]:
        """Fetch all mobile devices in JAMF database

        Returns:
            Union[list, dict]: json object from response
        """
        params = {"page-size": DEVICES_PAGE_SIZE}
        r = self.session.get(self._url(MOBILE_DEVICE_ENDPOINT), params=params)
        r.raise_for_status()
        return r.json()

    def search_devices(
        self,
        *,
        serial: str = None,
        name: str = None,
        udid: str = None,
        asset_tag: str = None,
    ):
        """[summary]
        Args:
            serial (str, optional): [description]. Defaults to None.
            name (str, optional): [description]. Defaults to None.
            udid (str, optional): [description]. Defaults to None.
            asset_tag (str, optional): [description]. Defaults to None.
        Raises:
            Exception: [description]
        Returns:
            [type]: [description]
        """
        search_params = {"pageNumber": 0, "pageSize": 100}
        if not any((serial, name, udid, asset_tag)):
            raise Exception("You must provide at least one search term")

        if name:
            search_params["name"] = name
        if serial:
            search_params["serialNumber"] = serial
        if udid:
            search_params["udid"] = udid
        if asset_tag:
            search_params["assetTag"] = asset_tag

        r = self.session.post(url=self._url(SEARCH_DEVICE_ENDPOINT), json=search_params)
        r.raise_for_status()
        payload = r.json()

        return payload.get("results", [])

    def search_query(self, query: str):
        """Search JAMF using the classic API for matches

        Args:
            query (str): A query term including name, mac address, assetTag, etc.

        Raises:
            HTTPError: based on response from server

        Returns:
            str: first device id in returned results
        """

        r = self.classic_session.get(
            url=self._url(html.escape(f"{CLASSIC_SEARCH_DEVICE_ENDPOINT}/{query}")), data=""
        )
        r.raise_for_status()
        root = ET.fromstring(r.text)
        device_ids = root.findall(".//id")
        return [device_id.text for device_id in device_ids]

    def device(self, device_id, detail=False):
        url = self._url(f"{MOBILE_DEVICE_ENDPOINT}/{device_id}")
        if detail:
            url += "/detail"
        r = self.session.get(url)
        if r.status_code == 200:
            return r.json()

    def update_device_name(self, device_id, name):

        url = self._url(
            html.escape(f"{CLASSIC_DEVICENAME_ENDPOINT}/{name}/id/{device_id}")
        )
        cr = self.classic_session.post(url=url, data="")
        cr.raise_for_status()
        return cr.status_code == 201

    def wipe_device(self, device_id):

        url = self._url(
            html.escape(
                f"{CLASSIC_ENDPOINT}/mobiledevicecommands/command/"
                "EraseDevice/id/{device_id}"
            )
        )
        cr = self.classic_session.post(url=url, data="")
        if cr.status_code != 201:
            return "Unable to wipe device"

        return cr.text

    def update_inventory(self, device_id: int) -> str:
        url = self._url(
            f"{CLASSIC_ENDPOINT}/mobiledevicecommands/command/"
            f"UpdateInventory/id/{device_id}"
        )
        cr = self.classic_session.post(url=url)
        if cr.status_code != 201:
            print(url)
            print(cr.text)
            print(cr.status_code)
            raise Exception("Unable to push device update inventory")

        return cr.text

    def update_os(self, device_id: int, force_install: bool = True) -> str:
        install_action = 2 if force_install else 1
        self.flush_mobile_device_commands(device_id=device_id)

        url = self._url(
            f"{CLASSIC_ENDPOINT}/mobiledevicecommands/command/"
            f"ScheduleOSUpdate/{install_action}/id/{device_id}"
        )
        cr = self.classic_session.post(url=url)
        cr.raise_for_status()
        return cr.text

    def recalculate_smart_groups(self, device_id):
        """Recalculates the smart groups for a device and returns the count
        of active smart groups

        Args:
            device_id (str): a string verion of the JSS id

        Returns:
            int: an integer count of the number of smart groups for the device
        """
        endpoint = MOBILE_DEVICE_ENDPOINT.replace("v2/", "v1/", 1)
        url = self._url(html.escape(f"{endpoint}/{device_id}/recalculate-smart-groups"))
        r = self.session.post(url=url)
        r.raise_for_status()
        return int(r.json().get("count"))

    def clear_location_from_device(self, device_id):
        location = {
            "buildingId": None,
            "departmentId": None,
            "emailAddress": "",
            "realName": "",
            "position": "",
            "phoneNumber": "",
            "room": "",
            "username": "",
        }
        self.update_device(device_id, location=location)
        self.recalculate_smart_groups(device_id)

    def delete_device(self, device_id):
        url = self._url(html.escape(f"{CLASSIC_ENDPOINT}/mobiledevices/id/{device_id}"))
        print(f"deleting device {device_id}")
        cr = self.classic_session.delete(url=url, data="")
        if cr.status_code == 200:
            print(f"Device {device_id} successfully deleted.")
            return True
        else:
            print(url)
            print(cr.text)
            raise Exception("Unable to push device name command")

    def device_flattened(self, device_id):
        device = {}
        extended_device_info = self.device(device_id=device_id, detail=True)
        device.update(
            {
                k: v
                for k, v in extended_device_info.items()
                if not isinstance(v, list) and not isinstance(v, dict)
            }
        )
        if "location" in extended_device_info:
            device.update(
                {
                    f"location_{k}": v
                    for k, v in extended_device_info["location"].items()
                    if not isinstance(v, dict) and not isinstance(v, list)
                }
            )
            device.update(
                {
                    f"location_{k}_name": v["name"]
                    for k, v in extended_device_info["location"].items()
                    if isinstance(v, dict) or isinstance(v, list)
                }
            )
        if "ios" in extended_device_info:
            device.update(
                {
                    k: v
                    for k, v in extended_device_info.get("ios", {}).items()
                    if not isinstance(v, dict) and not isinstance(v, list)
                }
            )
            device["application_count"] = len(
                extended_device_info["ios"]["applications"]
            )
            device.update(
                {
                    f"network_{k}": v
                    for k, v in extended_device_info["ios"]["network"].items()
                }
            )
        return device

    def validate(self):
        r = self.session.post(self._url(VALIDATION_ENDPOINT))
        return r.status_code == 200

    def invalidate(self):
        if not self.authenticated:
            return True
        r = self.session.post(self._url(INVALIDATE_ENDPOINT))
        if r.ok:
            del self.session.headers["Accept"]
            del self.token
            del self.auth_expiration
        return bool(r.ok)

    def change_device_configuration_profile_exclusion(
        self, device_id: int, configuration_profile_id: int, exclude_device: bool = True
    ) -> bool:
        """
        Add or remove a mobile device from a mobile device configuration
        profile exclusion list
        """
        device = self.device(device_id=device_id)
        root = self.get_configuration_profile(configuration_profile_id)
        excluded_devices = root.findall(".//exclusions/mobile_devices")[0]
        excluded_ids = [
            elm.text for elm in excluded_devices.findall("./mobile_device/id")
        ]
        if exclude_device and device_id not in excluded_ids:
            device_element = ET.SubElement(excluded_devices, "mobile_device")
            try:
                ET.SubElement(device_element, "id").text = str(device_id)
                ET.SubElement(device_element, "name").text = device["name"]
                ET.SubElement(device_element, "udid").text = device["udid"]
                ET.SubElement(device_element, "wifi_mac_address").text = device[
                    "wifiMacAddress"
                ]
            except KeyError:
                raise Exception(f"device was not properly formed. {device}")
        elif not exclude_device:
            try:
                device_element = excluded_devices.findall(
                    f"./mobile_device/[id='{device_id}']"
                )[0]
                excluded_devices.remove(device_element)
            except IndexError:
                return True  # We don't really care if it's missing from the list
        else:
            return True
        return self.update_configuration_profile(root)

    def get_configuration_profile(
        self, configuration_profile_id: int
    ) -> ET.ElementTree:
        r = self.classic_session.get(
            f"{self.jamf_server}JSSResource/mobiledeviceconfigurationprofiles/id/"
            "{configuration_profile_id}"
        )
        return ET.fromstring(r.text)

    def update_configuration_profile(
        self, configuration_profile: ET.ElementTree
    ) -> bool:
        configuration_id = configuration_profile.findall("./general/id")[0].text
        r = self.classic_session.put(
            f"{self.jamf_server}JSSResource/mobiledeviceconfigurationprofiles/id/"
            f"{configuration_id}",
            ET.tostring(configuration_profile),
        )
        return r.status_code == 201

    def update_device(self, device_id, payload=None, **kwargs):
        if not payload:
            payload = kwargs
        r = self.session.patch(
            self._url(f"{MOBILE_DEVICE_ENDPOINT}/{device_id}"), json=payload
        )
        print(payload)
        r.raise_for_status()
        return r.ok

    def set_device_room(self, device_id: int, room_name: str) -> dict:
        """
        Method to update a device's room location from JAMF
        """
        return self.update_device(device_id, location={"room": room_name})

    def get_buildings(self) -> dict:
        return self.get_object_list("v1/buildings/")["results"]

    def get_building(self, building_name: str, strip_extra: bool = False):
        buildings = self.get_buildings()
        building = self.get_object_by_name(buildings, building_name)
        if strip_extra:
            building = self.strip_extra_location_information(building)
        return building

    def get_departments(self) -> dict:
        return self.get_object_list("v1/departments/")["results"]

    def get_department(self, department_name: str, strip_extra: bool = True) -> dict:
        departments = self.get_departments()
        department = self.get_object_by_name(departments, department_name)
        if strip_extra:
            department = self.strip_extra_location_information(department)
        return department

    def add_device_to_prestage(
        self, prestage_id: int, device_id: int = None, serial_number: str = None
    ):
        if device_id and not serial_number:
            serial_number = self.device(device_id)["serialNumber"]
        current_serials, version_lock = self.get_prestage_serials_and_vlock(prestage_id)
        if serial_number in current_serials:
            return True
        else:
            current_serials.append(serial_number)
        return self.update_prestage_scope(prestage_id, current_serials, version_lock)

    def get_prestage_id_for_device(self, device_id: int):
        device_serial = self.device(device_id)["serialNumber"]
        url = f"{MOBILE_DEVICE_PRESTAGE_ENDPOINT}/scope"
        return (
            self.session.get(url=self._url(url))
            .json()["serialsByPrestageId"]
            .get(device_serial)
        )

    def get_prestage_serials_and_vlock(self, prestage_id: int):
        url = f"{MOBILE_DEVICE_PRESTAGE_ENDPOINT}/{prestage_id}/scope"
        r = self.session.get(url=self._url(url))
        payload = r.json()
        current_serials = [
            assignment["serialNumber"] for assignment in payload["assignments"]
        ]
        version_lock = payload["versionLock"]
        return current_serials, version_lock

    def update_prestage_scope(self, prestage_id: int, serials: list, version_lock):
        url = f"{MOBILE_DEVICE_PRESTAGE_ENDPOINT}/{prestage_id}/scope"
        payload = {"serialNumbers": serials, "versionLock": version_lock}
        r = self.session.put(url=self._url(url), json=payload)
        if not r.ok:
            print(f"Error {r.status_code}: {r.text}")
        else:
            print(f"Adding Prestage: {self._url(url)} with payload {payload}")
        return r.ok

    def remove_device_from_prestage(
        self, device_id: int = None, serial_number: str = None
    ):
        if device_id and not serial_number:
            device = self.device(device_id, True)
            serial_number = device["serialNumber"]
        if not device_id and serial_number:
            device_id = self.search_devices(serial=serial_number)[0].get("id")
        prestage_id = self.get_prestage_id_for_device(device_id)
        if not prestage_id:
            return True
        current_serials, version_lock = self.get_prestage_serials_and_vlock(prestage_id)
        new_serials = [serial for serial in current_serials if serial != serial_number]
        return self.update_prestage_scope(prestage_id, new_serials, version_lock)

    @staticmethod
    def strip_extra_location_information(location: dict) -> dict:
        if location:
            return {"id": location["id"], "name": location["name"]}

    def get_sites(self) -> dict:
        return self.get_object_list("settings/sites")

    def get_site(self, site_name: str, strip_extra: bool = False) -> dict:
        sites = self.get_sites()
        site = self.get_object_by_name(sites, site_name)
        if strip_extra:
            site = self.strip_extra_location_information(site)
        return site

    def get_object_list(self, path: str) -> list:
        r = self.session.get(self._url(path))
        if not r.raise_for_status():
            return r.json()

    def get_object_by_name(self, object_list, name) -> dict:
        return next((item for item in object_list if item["name"] == name), None)

    def flush_mobile_device_commands(self, device_id, status=None):

        if not status:
            status = "Pending+Failed"

        if status not in ("Pending", "Failed", "Pending+Failed"):
            raise ValueError(f"Invalid Status: {status}")

        url = self._url(
            html.escape(
                f"{CLASSIC_ENDPOINT}/commandflush/mobiledevices/id/{device_id}"
                f"/status/{status}"
            )
        )

        r = self.classic_session.delete(url, headers={"accept": "application/json"})
        r.raise_for_status()
        return r.ok
