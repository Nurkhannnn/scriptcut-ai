def _create(client, video, name="Demo"):
    with video.open("rb") as fh:
        return client.post("/api/projects", data={"name": name}, files={"video": ("sample.mp4", fh, "video/mp4")})


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_create_rejects_non_video(client):
    r = client.post("/api/projects", data={"name": "x"}, files={"video": ("a.txt", b"hi", "text/plain")})
    assert r.status_code == 415


def test_full_cut_flow(client, sample_video):
    r = _create(client, sample_video)
    assert r.status_code == 201
    project = r.json()
    assert len(project["segments"]) == 5

    pid, first = project["id"], project["segments"][0]["id"]
    r = client.patch(f"/api/projects/{pid}/segments/{first}", json={"text": "Edited", "deleted": True})
    assert r.status_code == 200 and r.json()["text"] == "Edited"

    assert client.post(f"/api/projects/{pid}/cut").status_code == 202
    export = client.get(f"/api/projects/{pid}/export").json()  # TestClient runs background tasks before returning
    assert export["status"] == "done", export
    assert 7.0 < export["duration"] < 9.0

    dl = client.get(f"/api/projects/{pid}/export/download")
    assert dl.status_code == 200 and dl.content[4:8] == b"ftyp"


def test_cut_conflict_when_all_deleted(client, sample_video):
    project = _create(client, sample_video).json()
    for seg in project["segments"]:
        client.patch(f"/api/projects/{project['id']}/segments/{seg['id']}", json={"deleted": True})
    assert client.post(f"/api/projects/{project['id']}/cut").status_code == 409
