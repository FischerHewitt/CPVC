from types import SimpleNamespace

from services import catalog
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


class FakeResponse:
    def __init__(self, text: str):
        self.text = text

    def raise_for_status(self):
        return None


def test_get_dept_courses_parses_2026_catalog_text_fallback(monkeypatch):
    html = """
    <html><body>
      <h3>ASCI Courses</h3>
      <p>ASCI 2230 Beef and Dairy Cattle Management (3 units)</p>
      <p>Term Typically Offered: F, SP</p>
      <p>Prerequisite: ASCI 112; or ASCI 1101, ASCI 1102, and ASCI 1103.</p>
      <p>ASCI 4419 Animal Metabolism and Nutritional Modeling (3 units)</p>
      <p>Formerly ASCI 419.</p>
      <p>ASCI 4470 Special Advanced Topics (1-3 units)</p>
      <p>Repeatable up to 6 units.</p>
    </body></html>
    """

    catalog._dept_cache.clear()
    monkeypatch.setattr(catalog.httpx, "get", lambda *args, **kwargs: FakeResponse(html))

    courses = catalog.get_dept_courses("asci")

    assert courses["ASCI 2230"]["title"] == "Beef and Dairy Cattle Management"
    assert courses["ASCI 2230"]["units"] == "3"
    assert "ASCI 1101" in courses["ASCI 2230"]["description"]
    assert courses["ASCI 4419"]["title"] == "Animal Metabolism and Nutritional Modeling"
    assert courses["ASCI 4470"]["units"] == "1-3"


def test_get_dept_courses_falls_back_to_bundled_polyplanner_catalog_on_fetch_failure(monkeypatch):
    catalog._dept_cache.clear()
    monkeypatch.setattr(
        catalog.httpx,
        "get",
        lambda *args, **kwargs: SimpleNamespace(raise_for_status=lambda: (_ for _ in ()).throw(RuntimeError())),
    )

    courses = catalog.get_dept_courses("asci")

    assert "ASCI 2230" in courses
    assert courses["ASCI 2230"]["title"]


def test_search_catalog_courses_matches_exact_compact_title_and_unknown():
    exact = catalog.search_catalog_courses("COMS 1126", limit=5)
    compact = catalog.search_catalog_courses("coms1126", limit=5)
    department = catalog.search_catalog_courses("COMS", limit=5)
    title = catalog.search_catalog_courses("argument advocacy", limit=5)
    missing = catalog.search_catalog_courses("notarealcourse9999", limit=5)
    browse = catalog.search_catalog_courses("", limit=5)
    next_browse = catalog.search_catalog_courses("", limit=5, offset=5)

    assert exact[0] == {
        "course_number": "COMS 1126",
        "title": "Argument and Advocacy",
        "units": 3,
    }
    assert compact[0]["course_number"] == "COMS 1126"
    assert all(course["course_number"].startswith("COMS ") for course in department)
    assert any(course["course_number"] == "COMS 1126" for course in title)
    assert missing == []
    assert len(browse) == 5
    assert browse != next_browse


def test_course_search_endpoint_returns_normalized_courses():
    response = client.get("/api/courses/search", params={"q": "coms1126", "limit": 3})

    assert response.status_code == 200
    assert response.json()["courses"][0] == {
        "course_number": "COMS 1126",
        "title": "Argument and Advocacy",
        "units": 3,
    }


def test_course_search_endpoint_supports_free_elective_picker_queries():
    compact = client.get("/api/courses/search", params={"q": "coms1126", "limit": 3})
    title = client.get("/api/courses/search", params={"q": "argument advocacy", "limit": 10})
    department = client.get("/api/courses/search", params={"q": "COMS", "limit": 2})
    browse = client.get("/api/courses/search", params={"q": "", "limit": 5, "offset": 5})
    unknown = client.get("/api/courses/search", params={"q": "notarealcourse9999"})

    assert compact.status_code == 200
    assert compact.json()["courses"][0]["course_number"] == "COMS 1126"
    assert any(course["course_number"] == "COMS 1126" for course in title.json()["courses"])
    assert department.status_code == 200
    assert len(department.json()["courses"]) == 2
    assert all(course["course_number"].startswith("COMS ") for course in department.json()["courses"])
    assert browse.status_code == 200
    assert len(browse.json()["courses"]) == 5
    assert unknown.json()["courses"] == []
