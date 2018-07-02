import pytest

from faker import Faker

from kurier.utils.history_manager import HistoryManager


fake = Faker()


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
        "headers": fake.pydict(),
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
