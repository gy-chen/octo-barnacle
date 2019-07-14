import pytest
import dotenv
from octo_barnacle.data.mark import create_file_app
from octo_barnacle.data.mark import ext

dotenv.load_dotenv()


@pytest.fixture
def app(app_config, sample_stickerset, sample_stickers):
    app = create_file_app(app_config)
    app.config['TESTING'] = True

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_file_api(client, sample_webp):
    image = client.get('/file/CAADBQADuQADOToIAV6R21Wc2_XvAg')
    assert image.get_data() == sample_webp
