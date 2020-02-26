def test_alert(con):
    msg = 'This is a test alert.'
    con.alert(msg)
    assert con.command_args == ('alert', msg)
    assert con.command_kwargs == {}
