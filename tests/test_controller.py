# -*- coding: utf-8 -*-
"""Test raincloudy.controller."""
from tests.test_base import UnitTestBase
from tests.extras import (
    CONTROLLER_NAME, CONTROLLER_SERIAL, CONTROLLER_TIMESTAMP)


class TestRainCloudyController(UnitTestBase):
    """Unit tests for controller attributes."""

    def test_errors_or_exceptions(self):
        """Tests for errors or exceptions."""
        from raincloudy.controller import RainCloudyController
        controller = self.rdy.controller

        # make sure _parent is a RainCloudy.core object
        self.assertRaises(TypeError, RainCloudyController, None, None)

        # if _parent is not present, must return __repr__ with ID
        controller._parent = None
        objname = "<RainCloudyController: {}>".format(CONTROLLER_SERIAL)
        self.assertEquals(controller.__repr__(), objname)

        # try to create a Controller object without any faucets
        self.assertRaises(TypeError, RainCloudyController,
                          self.rdy, CONTROLLER_SERIAL)

        # check if has more than 1 faucet
        controller.faucets.append(1)
        self.assertRaises(TypeError, getattr, controller, 'faucet')

        # check if faucets does not exist
        delattr(controller, 'faucets')
        self.assertRaises(AttributeError, getattr, controller, 'faucet')

    def test_attributes(self):
        """Test controller attributes."""
        controller = self.rdy.controller

        self.assertTrue(hasattr(controller, 'current_time'))
        self.assertTrue(hasattr(controller, 'faucet'))
        self.assertTrue(hasattr(controller, 'faucets'))
        self.assertTrue(hasattr(controller, 'id'))
        self.assertTrue(hasattr(controller, 'lookup_attr'))
        self.assertTrue(hasattr(controller, 'name'))
        self.assertTrue(hasattr(controller, 'post'))
        self.assertTrue(hasattr(controller, 'serial'))
        self.assertTrue(hasattr(controller, 'status'))
        self.assertTrue(hasattr(controller, 'update'))

        objname = "<RainCloudyController: {}>".format(CONTROLLER_NAME)
        self.assertEquals(controller.__repr__(), objname)

        self.assertEquals(controller.current_time, CONTROLLER_TIMESTAMP)
        self.assertEquals(controller.id, CONTROLLER_SERIAL)
        self.assertEquals(controller.name, CONTROLLER_NAME)
        self.assertEquals(controller.status, 'Online')

    def test_post_actions(self):
        """Test post actions."""
        controller = self.rdy.controller
        controller.name = 'test'

# vim:sw=4:ts=4:et:
