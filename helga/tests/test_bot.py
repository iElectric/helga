from mock import Mock
from unittest import TestCase

from helga import settings
from helga.bot import Helga


settings.DISABLE_AUTOBOT = True


class HelgaTestCase(TestCase):

    def setUp(self):
        self.helga = Helga(load=False)

    def test_join_channel(self):
        self.helga.join_channel('#all')

        assert '#all' in self.helga.channels

    def test_leave_channel(self):
        self.helga.join_channel('#all')
        self.helga.leave_channel('#all')

        assert '#all' not in self.helga.channels

    def test_set_topic(self):
        self.helga.set_topic('#all', 'everything is broken')

        assert self.helga.topics['#all'] == 'everything is broken'

    def test_nick(self):
        self.helga.client = Mock()
        self.helga.client.nickname = 'foo'

        assert self.helga.nick == 'foo'

    def test_nick_no_client(self):
        assert self.helga.nick == ''

    def test_get_current_nick_unknown_user(self):
        assert self.helga.get_current_nick('foo') == 'foo'

    def test_get_current_nick_is_current(self):
        self.helga.users = {'foo': ('foobar',)}

        assert self.helga.get_current_nick('foo') == 'foo'

    def test_get_current_nick_is_old_nick(self):
        self.helga.users = {'foo': ('foobar',)}

        assert self.helga.get_current_nick('foobar') == 'foo'

    def test_update_user_nick_adds_new_user(self):
        self.helga.update_user_nick(None, 'foo')

        assert self.helga.users['foo'] == set(['foo'])

    def test_update_user_nick_no_changes(self):
        user_set = {'foo': set(['foo'])}
        self.helga.users = user_set
        self.helga.update_user_nick('foo', 'foo')

        assert self.helga.users == user_set

    def test_update_user_nick_remaps(self):
        old = {'foobar': set(['foobar'])}
        new = {'foo': set(['foo', 'foobar'])}
        self.helga.users = old
        self.helga.update_user_nick('foobar', 'foo')

        assert self.helga.users == new

    def setup_handle_message(self, stfu_ret, ext_ret, is_silenced):
        self.helga.stfu = Mock()
        self.helga.stfu.dispatch.return_value = stfu_ret
        self.helga.stfu.is_silenced.return_value = is_silenced

        self.helga.extensions = Mock()
        self.helga.extensions.dispatch.return_value = ext_ret

        self.helga.client = Mock()

    def test_handle_message_does_nothing(self):
        self.setup_handle_message(None, None, True)
        self.helga.handle_message('foo', 'bar', 'baz', True)

        assert not self.helga.client.msg.called

    def test_handle_message_silencing_skips_extensions(self):
        self.setup_handle_message('OK', None, False)
        self.helga.handle_message('foo', 'bar', 'baz', True)

        assert not self.helga.extensions.dispatch.called

    def test_handle_message_sends_client_message_to_correct_channel(self):
        # Public
        self.setup_handle_message('OK', None, False)
        self.helga.handle_message('foo', 'bar', 'baz', True)
        self.helga.client.msg.assertCalledWith('bar', 'OK')

        # Private
        self.setup_handle_message('OK', None, False)
        self.helga.handle_message('foo', 'bar', 'baz', False)
        self.helga.client.msg.assertCalledWith('foo', 'OK')

    def test_handle_message_formats_output(self):
        self.setup_handle_message('OK: %(nick)s - %(botnick)s - %(channel)s', None, False)
        self.helga.client.nickname = 'helga'
        self.helga.handle_message('foo', 'bar', 'baz', True)

        self.helga.client.msg.assertCalledWith('bar', 'OK: foo - helga - bar')
