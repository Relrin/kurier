import json
import tempfile

import pytest

from faker import Faker

from kurier.utils.history_manager import HistoryManager


fake = Faker()
TEMPFILE_OPTIONS = {
    "newline": "\n",
    "encoding": "utf-8"
}


def generate_state_data():
    return {
        "connection_url": "amqp://{}:{}@{}:{}vhost".format(
            fake.user_name(),
            fake.password(),
            fake.ipv4(),
            fake.random_int(5000, 9000)
        ),
        "request_exchange": "amqp.direct",
        "request_routing_key": fake.word(),
        "response_queue": fake.word(),
        "response_exchange": "amqp.direct",
        "response_routing_key": fake.word(),
        "properties": {},
        "headers": {},
        "body": fake.sentence(),
    }


def fill_history_manager(manager, amount):
    for _ in range(amount):
        state_data = generate_state_data()
        manager.AddState(state_data)


def test_new_history_manager_is_empty():
    manager = HistoryManager()
    assert manager.SavedStates == 0


def test_add_new_state():
    manager = HistoryManager()
    new_state = generate_state_data()

    assert manager.SavedStates == 0

    manager.AddState(new_state)
    assert manager.GetState(0) == new_state


def test_add_new_state_with_removing_old_state():
    manager = HistoryManager()
    fill_history_manager(manager, manager.MAX_STATES)

    assert manager.SavedStates == manager.MAX_STATES

    new_state = generate_state_data()
    oldest_state = manager._data[-1]

    manager.AddState(new_state)
    assert manager.SavedStates == manager.MAX_STATES
    assert oldest_state not in manager._data
    assert manager.GetState(0) == new_state


def test_get_state_to_history_manager():
    manager = HistoryManager()
    states_amount = 10
    fill_history_manager(manager, states_amount)

    assert manager.SavedStates == states_amount
    assert manager.GetState(0) == manager._data[0].GetDump()


def test_get_state_raises_an_index_error_for_too_big_index():
    manager = HistoryManager()
    states_amount = 10
    fill_history_manager(manager, states_amount)

    assert manager.SavedStates == states_amount
    with pytest.raises(IndexError):
        manager.GetState(states_amount + 1)


def test_remove_old_state():
    manager = HistoryManager()
    states_amount = 10
    fill_history_manager(manager, states_amount)

    assert manager.SavedStates == states_amount

    manager.RemoveOldState()
    assert manager.SavedStates == states_amount - 1


def test_removing_old_state_wont_be_applied_when_history_manager_is_empty():
    manager = HistoryManager()

    assert manager.SavedStates == 0

    manager.RemoveOldState()
    assert manager.SavedStates == 0


def test_manager_will_import_data_from_a_file():
    with tempfile.NamedTemporaryFile(mode="r+", **TEMPFILE_OPTIONS) as import_file:
        for _ in range(3):
            state = generate_state_data()
            state_dump = json.dumps(state) + TEMPFILE_OPTIONS["newline"]
            import_file.write(state_dump)

        import_file.seek(0)
        manager = HistoryManager()
        manager.ImportHistoryFromFile(import_file)

        assert manager.SavedStates == 3


def test_manager_wont_import_data_from_the_closed_file():
    with tempfile.NamedTemporaryFile(mode="r+", **TEMPFILE_OPTIONS) as import_file:
        import_file.close()
        manager = HistoryManager()
        manager.ImportHistoryFromFile(import_file)

        assert manager.SavedStates == 0


def test_manager_will_ignore_invalid_data_during_import_from_a_file():
    with tempfile.NamedTemporaryFile(mode="r+", **TEMPFILE_OPTIONS) as import_file:
        for _ in range(3):
            state = generate_state_data()
            state_dump = json.dumps(state) + TEMPFILE_OPTIONS["newline"]
            import_file.write(state_dump)

        import_file.write('{"KEY": "INVALID DATA"')

        import_file.seek(0)
        manager = HistoryManager()
        manager.ImportHistoryFromFile(import_file)

        assert manager.SavedStates == 3


def test_manager_will_export_data_into_the_file():
    with tempfile.NamedTemporaryFile(mode="r+", **TEMPFILE_OPTIONS) as import_file:
        with tempfile.NamedTemporaryFile(mode="w+", **TEMPFILE_OPTIONS, delete=False) as export_file:  # NOQA

            for _ in range(3):
                state = generate_state_data()
                state_dump = json.dumps(state) + TEMPFILE_OPTIONS["newline"]
                import_file.write(state_dump)

            import_file.seek(0)
            manager = HistoryManager()
            manager.ImportHistoryFromFile(import_file)

            assert manager.SavedStates == 3

            manager.ExportHistoryToFile(export_file)
            export_file.close()

            with open(export_file.name) as result_file:
                assert len(result_file.read().splitlines()) == 3

            export_file._closer.delete = True
            export_file._closer.close()


def test_manager_will_export_data_into_the_default_file():
    with tempfile.TemporaryDirectory() as app_directory:
        manager = HistoryManager(app_directory)

        for _ in range(3):
            state_data = generate_state_data()
            manager.AddState(state_data)

        assert manager.SavedStates == 3

        manager.ExportHistoryToDefaultFile()

        with open(manager._history_filepath) as result_file:
            assert len(result_file.read().splitlines()) == 3
