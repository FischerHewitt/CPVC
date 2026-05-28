from services import polyratings


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def reset_polyratings_cache():
    polyratings._cache.reset()


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


def test_get_professors_for_static_semester_quarter_mapping(monkeypatch):
    reset_polyratings_cache()

    payload = {
        "result": {
            "data": [
                {
                    "id": "distributed",
                    "firstName": "Grace",
                    "lastName": "Hopper",
                    "courses": ["CSC 469"],
                    "overallRating": 3.8,
                    "numEvals": 12,
                },
            ]
        }
    }
    monkeypatch.setattr(polyratings.httpx, "get", lambda *_args, **_kwargs: FakeResponse(payload))

    professors = polyratings.get_professors_for_course("CSC 4669")

    assert [prof.name for prof in professors] == ["Grace Hopper"]


def test_get_professors_for_formerly_crosslisted_graphics_course(monkeypatch):
    reset_polyratings_cache()

    payload = {
        "result": {
            "data": [
                {
                    "id": "graphics",
                    "firstName": "Ivan",
                    "lastName": "Sutherland",
                    "courses": ["CPE 471"],
                    "overallRating": 3.9,
                    "numEvals": 14,
                },
            ]
        }
    }
    monkeypatch.setattr(polyratings.httpx, "get", lambda *_args, **_kwargs: FakeResponse(payload))

    professors = polyratings.get_professors_for_course("CSC 4710")

    assert [prof.name for prof in professors] == ["Ivan Sutherland"]


def test_get_professors_for_upper_division_trailing_zero_candidate(monkeypatch):
    reset_polyratings_cache()

    payload = {
        "result": {
            "data": [
                {
                    "id": "rendering",
                    "firstName": "Henri",
                    "lastName": "Gouraud",
                    "courses": ["CSC 473"],
                    "overallRating": 3.6,
                    "numEvals": 9,
                },
            ]
        }
    }
    monkeypatch.setattr(polyratings.httpx, "get", lambda *_args, **_kwargs: FakeResponse(payload))

    professors = polyratings.get_professors_for_course("CSC 4730")

    assert [prof.name for prof in professors] == ["Henri Gouraud"]


def test_get_professors_for_transition_to_advanced_math(monkeypatch):
    reset_polyratings_cache()

    payload = {
        "result": {
            "data": [
                {
                    "id": "proofs",
                    "firstName": "Emmy",
                    "lastName": "Noether",
                    "courses": ["MATH 248"],
                    "overallRating": 4.0,
                    "numEvals": 21,
                },
            ]
        }
    }
    monkeypatch.setattr(polyratings.httpx, "get", lambda *_args, **_kwargs: FakeResponse(payload))

    professors = polyratings.get_professors_for_course("MATH 2031")

    assert [prof.name for prof in professors] == ["Emmy Noether"]


def test_get_professors_for_ge_semester_course_uses_quarter_candidate(monkeypatch):
    reset_polyratings_cache()

    payload = {
        "result": {
            "data": [
                {
                    "id": "speech",
                    "firstName": "Mary",
                    "lastName": "Fisher",
                    "courses": ["COMS 101"],
                    "overallRating": 3.4,
                    "numEvals": 16,
                },
            ]
        }
    }
    monkeypatch.setattr(polyratings.httpx, "get", lambda *_args, **_kwargs: FakeResponse(payload))

    professors = polyratings.get_professors_for_course("COMS 1101")

    assert [prof.name for prof in professors] == ["Mary Fisher"]


def test_get_professors_for_ge_semester_course_indexes_course_strings_with_titles(monkeypatch):
    reset_polyratings_cache()

    payload = {
        "result": {
            "data": [
                {
                    "id": "advocacy",
                    "firstName": "bell",
                    "lastName": "hooks",
                    "courses": ["COMS126 - Argument and Advocacy"],
                    "overallRating": 3.9,
                    "numEvals": 18,
                },
            ]
        }
    }
    monkeypatch.setattr(polyratings.httpx, "get", lambda *_args, **_kwargs: FakeResponse(payload))

    professors = polyratings.get_professors_for_course("COMS 1126")

    assert [prof.name for prof in professors] == ["bell hooks"]


def test_get_professors_for_combined_course_option(monkeypatch):
    reset_polyratings_cache()

    payload = {
        "result": {
            "data": [
                {
                    "id": "capstone-i",
                    "firstName": "Barbara",
                    "lastName": "Liskov",
                    "courses": ["CSC 4160"],
                    "overallRating": 4.0,
                    "numEvals": 8,
                },
                {
                    "id": "capstone-ii",
                    "firstName": "Edsger",
                    "lastName": "Dijkstra",
                    "courses": ["CSC 4161"],
                    "overallRating": 3.7,
                    "numEvals": 11,
                },
            ]
        }
    }
    monkeypatch.setattr(polyratings.httpx, "get", lambda *_args, **_kwargs: FakeResponse(payload))

    professors = polyratings.get_professors_for_course("CSC 4160 and CSC 4161")

    assert [prof.name for prof in professors] == ["Edsger Dijkstra", "Barbara Liskov"]
