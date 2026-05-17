from types import SimpleNamespace

from services import catalog


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


def test_get_dept_courses_returns_empty_on_fetch_failure(monkeypatch):
    catalog._dept_cache.clear()
    monkeypatch.setattr(
        catalog.httpx,
        "get",
        lambda *args, **kwargs: SimpleNamespace(raise_for_status=lambda: (_ for _ in ()).throw(RuntimeError())),
    )

    assert catalog.get_dept_courses("asci") == {}
