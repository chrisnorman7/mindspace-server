def test_alert(con):
    msg = 'This is a test alert.'
    con.alert(msg)
    assert con.command_args == ('alert', msg)
    assert con.command_kwargs == {}


def test_message(con):
    msg = 'This is a test message.'
    con.message(msg)
    assert con.command_args == ('message', msg)
    assert con.command_kwargs == {}
