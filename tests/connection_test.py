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


def test_confirm(con):
    msg = 'Are you sure you want to test?'
    ok_command = 'foo'
    ok_args = [1, 2, 3]
    ok_kwargs = {'hello': 'world'}
    cancel_command = 'bar'
    cancel_args = [4, 5, 6]
    cancel_kwargs = {'test': 'this'}
    con.confirm(msg, ok_command)
    assert con.command_args == (
        'confirm', msg, ok_command, [], {}, None, [], {}
    )
    con.confirm(msg, ok_command, cancel_command=cancel_command)
    assert con.command_args == (
        'confirm', msg, ok_command, [], {}, cancel_command, [], {}
    )
    assert con.command_kwargs == {}
    con.confirm(
        msg, ok_command, ok_args=ok_args, ok_kwargs=ok_kwargs,
        cancel_command=cancel_command, cancel_args=cancel_args,
        cancel_kwargs=cancel_kwargs
    )
    assert con.command_args == (
        'confirm', msg, ok_command, ok_args, ok_kwargs, cancel_command,
        cancel_args, cancel_kwargs
    )
    assert con.command_kwargs == {}


def test_urlopen(con):
    url = 'test'
    con.urlopen(url)
    assert con.command_args == ('urlopen', url)
    assert con.command_kwargs == {}
