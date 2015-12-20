#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pyecs import *
from pyecs.application import main,profile,onHotswap
from pyecs.components import *

import pyecs
import pyecs.application

from collections import defaultdict
from testing import *

from funcy import partial
import mock

class TestApplication():
    @mock.patch('pyecs.application.Application')
    def test_main1(self,mocked_Application):
        main("__main__")
        mocked_Application.assert_called_once_with()

    @mock.patch('pyecs.application.Application')
    def test_main2(self,mocked_Application):
        main("anything-else")
        mocked_Application.assert_not_called()

    @mock.patch('cProfile.Profile')
    def test_profile(self,mocked_Profile):
        operation = mock.MagicMock()
        filename = "foobar"

        profile(operation,filename)

        operation.assert_called_once_with()

        mocked_Profile.assert_called_once_with()
        mocked_Profile.return_value.enable.assert_called_once_with()
        mocked_Profile.return_value.disable.assert_called_once_with()
        mocked_Profile.return_value.dump_stats.assert_called_once_with(filename)

    @mock.patch('pyecs.application.Application.spin')
    @mock.patch('pyecs.application.Entity')
    def test___init___autospin_default(self, mocked_Entity, mocked_spin):
        a = Application()
        assert Application.instance == a
        assert a.done == False
        assert hasattr(a,"entity") == True
        assert a.done == False
        mocked_spin.assert_called_once_with()
        mocked_Entity.assert_called_once_with()
        mocked_Entity.return_value.fire_callbacks.assert_called_once_with("setup")

    @mock.patch('pyecs.application.Application.spin')
    @mock.patch('pyecs.application.Entity')
    def test___init___auto_spin_True(self, mocked_Entity, mocked_spin):
        a = Application(auto_spin=True)
        assert Application.instance == a
        assert a.done == False
        assert hasattr(a,"entity") == True
        assert a.done == False
        mocked_spin.assert_called_once_with()
        mocked_Entity.assert_called_once_with()
        mocked_Entity.return_value.fire_callbacks.assert_called_once_with("setup")

    @mock.patch('pyecs.application.Application.spin')
    @mock.patch('pyecs.application.Entity')
    def test___init___auto_spin_False(self, mocked_Entity, mocked_spin):
        a = Application(auto_spin=False)
        assert Application.instance == a
        assert a.done == False
        assert hasattr(a,"entity") == True
        assert a.done == False
        mocked_spin.assert_not_called()
        mocked_Entity.assert_called_once_with()
        mocked_Entity.return_value.fire_callbacks.assert_called_once_with("setup")

    @mock.patch('pyecs.application.Entity')
    def test_setup_main_entity(self, mocked_Entity):
        a = Application(auto_spin=False)

        mocked_Entity.reset_mock()
        delattr(a, "entity")
        a.setup_main_entity()
        mocked_Entity.assert_called_once_with()
        assert hasattr(a, "entity")

    def test_register_events(self):
        a = Application(auto_spin=False)
        a.setup_main_entity() # generate new self.entity
        assert len(a.entity.callbacks["quit"])==0
        a.register_events()
        assert len(a.entity.callbacks["quit"])==1

    def test_on_quit(self):
        a = Application(auto_spin=False)
        a.done = False
        a.entity.fire_callbacks("quit",None)
        assert a.done == True

    @mock.patch('pyecs.application.Entity.fire_callbacks')
    def test_update(self, mocked_fire_callbacks):
        a = Application(auto_spin=False)
        dt = 1
        mocked_fire_callbacks.reset_mock()
        a.update(dt)
        mocked_fire_callbacks.assert_called_once_with("update",dt)

    @mock.patch('pyecs.application.Entity.fire_callbacks')
    def test_start(self, mocked_fire_callbacks):
        a = Application(auto_spin=False)
        dt = 1
        mocked_fire_callbacks.reset_mock()
        a.start()
        mocked_fire_callbacks.assert_called_once_with("start")

    @mock.patch('pyecs.application.Entity.fire_callbacks')
    def test_quit(self, mocked_fire_callbacks):
        a = Application(auto_spin=False)
        dt = 1
        mocked_fire_callbacks.reset_mock()
        a.quit()
        mocked_fire_callbacks.assert_called_once_with("quit",None)
    @mock.patch('pyecs.application.Entity.fire_callbacks')
    def test_on_hotswap(self, mocked_fire_callbacks):
        a = Application(auto_spin=False)
        dt = 1
        mocked_fire_callbacks.reset_mock()
        a.on_hotswap()
        mocked_fire_callbacks.assert_called_once_with("hotswap")

    @mock.patch('pyecs.application.time',new_callable=lambda:partial(lambda it:0.5*it.next(),generateNaturalIntegers()))
    def test_update_dt_0_5(self, mocked_time):
        a = Application(auto_spin=False)
        def update(dt):
            assert dt == 0.5
            update.called = True
            a.entity.fire_callbacks("quit",None)
        update.called = False
        a.entity.register_callback("update", update)
        a.spin()
        assert update.called == True

    @mock.patch('pyecs.application.time',new_callable=lambda:partial(lambda it:it.next(),generateNaturalIntegers()))
    def test_update_dt_1(self, mocked_time):
        a = Application(auto_spin=False)
        def update(dt):
            assert dt == 1
            update.called = True
            a.entity.fire_callbacks("quit",None)
        update.called = False
        a.entity.register_callback("update", update)
        a.spin()
        assert update.called == True

    @mock.patch('pyecs.application.onHotswap')
    def test_update_onHotswap(self, mocked_onHotswap):
        a = Application(auto_spin=False)
        def update(dt):
            update.called = True
            mocked_onHotswap.notify = True
            assert mocked_onHotswap.notify == True
            # if update.called > 10:
            #     a.entity.fire_callbacks("quit",None)

        def hotswap():
            hotswap.called = True
            a.entity.fire_callbacks("quit",None)

        update.called = False
        hotswap.called = False
        a.entity.register_callback("update", update)
        a.entity.register_callback("hotswap", hotswap)
        a.spin()
        assert update.called == True
        assert hotswap.called == True
    
    def test_update_start_quit(self):
        a = Application(auto_spin=False)
        def update(dt):
            a.entity.fire_callbacks("quit",None)
        def start():
            start.called = True
        def quit(event):
            quit.called = True

        a.entity.register_callback("update", update)
        a.entity.register_callback("start", start)
        a.entity.register_callback("quit", quit)
        
        start.called = False
        quit.called = False

        a.spin()

        assert start.called == True
        assert quit.called == True

    def test_onHotswap(self):
        onHotswap.notify = False
        onHotswap()
        assert onHotswap.notify == True
