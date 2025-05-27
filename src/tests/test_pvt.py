import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope='module')
def client():
    return TestClient(app)


@pytest.mark.parametrize(
    "request_data, expected_response",
    [
        (
            {
                "pres": 100,
                "temp": 293,
                "oil": {
                    "mass": 10,
                    "dens": 800,
                    "heat_capacity": 4200,
                    "heat_conductivity": 0.603,
                    "solubility": 80
                },
                "wat": {
                    "mass": 10,
                    "dens": 1000,
                    "heat_capacity": 4200,
                    "heat_conductivity": 0.603,
                    "sali": 0
                },
                "gas": {
                    "mass": 10,
                    "dens": 1,
                    "heat_capacity": 4200,
                    "heat_conductivity": 0.603
                },
                "settings": {
                    "thermal": True,
                    "model_type": "Dead"
                }
            },
            {
                "oil": {
                    "vis": 0.00020721815086364336,
                    "fvf": 1.2954197903059899
                },
                "wat": {
                    "vis": 0.0032783065211337364,
                    "fvf": 1.240431844194427
                },
                "gas": {
                    "visc": 0.04974916953680915,
                    "dens": 0.019609659185788306
                }
            }
        )
    ]
)
def test_pvt_calc_return_valid_response(client: TestClient, request_data, expected_response):
    response = client.post("/pvt/calc", json=request_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "oil" in response_data
    assert "wat" in response_data
    assert "gas" in response_data
    oil = response_data["oil"]
    assert oil.keys() == expected_response["oil"].keys()
    assert oil["vis"] == pytest.approx(expected_response["oil"]["vis"])
    assert oil["fvf"] == pytest.approx(expected_response["oil"]["fvf"])
    wat = response_data["wat"]
    assert wat.keys() == expected_response["wat"].keys()
    assert wat["vis"] == pytest.approx(expected_response["wat"]["vis"])
    assert wat["fvf"] == pytest.approx(expected_response["wat"]["fvf"])
    gas = response_data["gas"]
    assert gas.keys() == expected_response["gas"].keys()
    assert gas["visc"] == pytest.approx(expected_response["gas"]["visc"])
    assert gas["dens"] == pytest.approx(expected_response["gas"]["dens"])