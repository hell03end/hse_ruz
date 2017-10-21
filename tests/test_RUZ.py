import pytest
from ruz import RUZ, REQUEST_SCHEMA
from ruz.utils import RUZ_API_ENDPOINTS, RUZ_API_URL as RUZ_URL


class TestRUZ:
    def setup_class(self):
        self.api = RUZ(strict_v1=True)
        self.api2 = RUZ(strict_v1=False)

    def test_v(self):
        assert self.api.v == 1
        assert self.api2.v == 2

    def test_schema(self):
        assert self.api.schema == REQUEST_SCHEMA
        assert self.api2.schema == REQUEST_SCHEMA

    def test__make_url(self):
        RUZ_URL2 = RUZ_URL + "v2/"
        for key, endpoint in RUZ_API_ENDPOINTS.items():
            assert self.api._make_url(key) == RUZ_URL + endpoint
            assert self.api._make_url(key, v=2) == RUZ_URL + endpoint
            assert self.api2._make_url(key, v=1) == RUZ_URL + endpoint
            assert self.api2._make_url(key, v=2) == RUZ_URL2 + endpoint
        with pytest.raises(KeyError):
            self.api._make_url("")

    def test__request(self) -> NotImplemented:
        return NotImplemented

    def test__verify_schema(self):
        with pytest.raises(KeyError) as excinfo:
            self.api._verify_schema("")
        assert excinfo
        for endpoint in RUZ_API_ENDPOINTS:
            with pytest.raises(KeyError) as excinfo:
                self.api._verify_schema(endpoint, tmp=None)
            assert excinfo
            if endpoint == 'schedule':
                with pytest.raises(ValueError) as excinfo:
                    self.api._verify_schema(endpoint, email=123)
                assert excinfo
            assert not self.api._verify_schema(endpoint)

    def test_check_email(self):
        correct_emails = ("somemail@edu.hse.ru", "somemail@hse.ru")
        incorrect_emails = ("somemail@hse.com", "somem@il@edu.hse.ru",
                            "somemail@google.ru")
        for email in incorrect_emails:
            with pytest.raises(ValueError) as excinfo:
                self.api.check_email(email)
            assert excinfo
        for email in correct_emails:
            assert self.api.check_email(email) is None

    def test__verify_email(self):
        correct_emails = ("somemail@edu.hse.ru", "somemail@hse.ru")
        incorrect_emails = ("somemail@hse.com", "somem@il@edu.hse.ru",
                            "somemail@google.ru")
        for email in incorrect_emails:
            with pytest.raises(ValueError) as excinfo:
                self.api._verify_email(email)
            assert excinfo
        for email in correct_emails:
            assert self.api._verify_email(email) is None
        with pytest.raises(ValueError) as excinfo:
            self.api._verify_email(correct_emails[0], receiver_type=-1)
        assert excinfo
        with pytest.raises(ValueError) as excinfo:
            self.api._verify_email(correct_emails[0], receiver_type=2)
        assert excinfo

    def test__get(self):
        incorrect_email = "somemail@hse.com"
        for endpoint in RUZ_API_ENDPOINTS:
            if endpoint == "schedule":
                with pytest.raises(ValueError) as excinfo:
                    self.api._get(endpoint, email=incorrect_email)
                assert excinfo
            else:
                with pytest.raises(KeyError) as excinfo:
                    self.api._get(endpoint, tmp=None)
                assert excinfo
        assert self.api._get("kind_of_works")

    def test_schedules(self):
        with pytest.raises(ValueError) as excinfo:
            self.api.schedules(123)
        assert excinfo
        assert isinstance(self.api.schedules('abc'), map)
        assert isinstance(self.api.schedules(['abc']), map)
