from tracking_load_faker.utils import faker_data, get_faker_data


def test_faker_data():
    @faker_data('gender')
    def gender_test(data=None):
        return data

    assert gender_test() == get_faker_data('gender')
