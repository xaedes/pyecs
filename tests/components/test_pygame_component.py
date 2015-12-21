#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pyecs import *
from pyecs.components import *

import pyecs
import pyecs.components

from collections import defaultdict, namedtuple
from testing import *

from funcy import partial
import mock
import pygame
from itertools import imap

class TestPygameComponent():
    @mock.patch('pygame.init')
    @mock.patch('pygame.display.set_mode')
    @mock.patch('pygame.display.set_caption')
    def test_setup(self, mocked_pygame_display_set_caption, mocked_pygame_display_set_mode, mocked_pygame_init):
        c = Pygame()
        c.caption = "Foo"
        assert hasattr(c,"screen") == False

        c.setup()
        assert hasattr(c,"screen") == True
        assert mocked_pygame_init.called
        assert mocked_pygame_display_set_mode.called
        mocked_pygame_display_set_caption.assert_called_once_with(c.caption)

    @mock.patch('pyecs.components.pygame_component.Pygame.setup')
    def test_setup_when_component_added(self, mocked_setup):
        mocked_setup = callback(mocked_setup)
        e = Entity()
        c = Pygame()

        # setup is called when component is added to entity
        mocked_setup.reset_mock()
        e.add_component(c)
        assert mocked_setup.called   

    @mock.patch('pyecs.components.pygame_component.Pygame.setup')
    def test_setup_callback(self, mocked_setup):
        mocked_setup = callback(mocked_setup)
        e = Entity()
        c = Pygame()
        e.add_component(c)
  
        # test callback
        mocked_setup.reset_mock()
        e.fire_callbacks("setup")
        assert mocked_setup.called 

    @mock.patch('pyecs.components.pygame_component.Pygame.setup')
    def test_setup_when_hotswap(self, mocked_setup):
        mocked_setup = callback(mocked_setup)
        e = Entity()
        c = Pygame()
        e.add_component(c)
  
        # test callback
        mocked_setup.reset_mock()
        e.fire_callbacks("hotswap")
        assert mocked_setup.called   

    @mock.patch('pygame.quit')
    def test_quit(self, mocked_pygame_quit):
        c = Pygame()
        mocked_pygame_quit.reset_mock()
        c.quit(None)
        assert mocked_pygame_quit.called

    @classmethod
    def _event(CLS,type):
        class Event():
            def __init__(self, type):
                self.type = type

        return Event(type)
                
    # @classmethod
    # def _pygame_event_get(CLS):
    _event_types = [pygame.QUIT, pygame.ACTIVEEVENT, pygame.KEYDOWN, pygame.KEYUP, 
            pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN,
            pygame.JOYAXISMOTION, pygame.JOYBALLMOTION, pygame.JOYHATMOTION, 
            pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN, pygame.VIDEORESIZE,
            pygame.VIDEOEXPOSE, pygame.USEREVENT]
        # return imap(CLS._event,iter(types))

    @mock.patch('pygame.display.flip')
    @mock.patch('pygame.mouse.get_pos')
    @mock.patch('pygame.mouse.get_pressed')
    @mock.patch('pygame.key.get_pressed')
    @mock.patch('pygame.event.get',new_callable=lambda:lambda:imap(TestPygameComponent._event,iter(TestPygameComponent._event_types)))
    @mock.patch('pyecs.components.pygame_component.Pygame.setup')
    def test_update(self, mocked_setup, mocked_pygame_event_get, mocked_pygame_key_get_pressed, mocked_pygame_mouse_get_pressed, 
                          mocked_pygame_mouse_get_pos, mocked_pygame_display_flip):
        mocked_setup = callback(mocked_setup)
        e = Entity()
        c = Pygame()
        e.add_component(c)
        c.screen = "foo"
        mocked_draw = mock.MagicMock()
        mocked_input = mock.MagicMock()
        e.register_callback("draw",mocked_draw)
        e.register_callback("input",mocked_input)
        def event_callback(type,event):
            assert type == event.type
            event_callback.called += 1
        for type in TestPygameComponent._event_types:
            e.register_callback(c.pygame_mappings[type],partial(event_callback, type))
        event_callback.called = 0
        e.fire_callbacks("update",0)
        assert event_callback.called == len(TestPygameComponent._event_types)
        mocked_input.assert_called_once_with(
            mocked_pygame_mouse_get_pos.return_value,
            mocked_pygame_mouse_get_pressed.return_value,
            mocked_pygame_key_get_pressed.return_value)
        mocked_draw.assert_called_once_with(c.screen)
        
        assert mocked_pygame_display_flip.called
        assert mocked_pygame_mouse_get_pos.called
        assert mocked_pygame_mouse_get_pressed.called
        assert mocked_pygame_key_get_pressed.called


