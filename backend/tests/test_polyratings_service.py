from services import polyratings


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def reset_polyratings_cache():
    polyratings._cache_professors = None
    polyratings._cache_ts = 0.0
    polyratings._course_index = {}


def test_get_professors_for_course_uses_quarter_equivalents_and_sorts(monkeypatch):
    reset_polyratings_cache()

    payload = {
        "result": {
            "data": [
                {
                    "id": "low-rated",
                    "firstName": "Alan",
                    "lastName": "Turing",
                    "courses": ["CSC 101"],
                    "overallRating": 3.9,
                    "numEvals": 10,
                },
                {
                    "id": "many-reviews",
                    "firstName": "Katherine",
                    "lastName": "Johnson",
                    "courses": ["CSC 101"],
                    "overallRating": 3.5,
                    "numEvals": 50,
                },
                {
                    "id": "other-course",
                    "firstName": "Margaret",
                    "lastName": "Hamilton",
                    "courses": ["CSC 357"],
                    "overallRating": 4.0,
                    "numEvals": 100,
                },
            ]
        }
    }

    monkeypatch.setattr(polyratings.httpx, "get", lambda *_args, **_kwargs: FakeResponse(payload))

    professors = polyratings.get_professors_for_course("CSC 1001")

    assert [prof.name for prof in professors] == ["Katherine Johnson", "Alan Turing"]
    assert professors[0].overall_score == 3.5
    assert professors[0].num_ratings == 50
    assert professors[0].polyratings_url == "https://polyratings.dev/professor/many-reviews"


def test_get_professors_for_course_returns_empty_list_when_fetch_fails(monkeypatch):
    reset_polyratings_cache()

    def raise_error(*_args, **_kwargs):
        raise RuntimeError("network unavailable")

    monkeypatch.setattr(polyratings.httpx, "get", raise_error)

    assert polyratings.get_professors_for_course("CSC 101") == []
