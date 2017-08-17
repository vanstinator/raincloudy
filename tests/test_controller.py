# -*- coding: utf-8 -*-
"""Test raincloudy.controller."""
from tests.test_base import UnitTestBase
from tests.helpers import (
    CONTROLLER_NAME, CONTROLLER_SERIAL, CONTROLLER_TIMESTAMP)


class TestRainCloudyController(UnitTestBase):
    """Unit tests for controller attributes."""

    def test_errors_or_exceptions(self):
        """Tests for errors or exceptions."""
        from raincloudy.controller import RainCloudyController

        controller = self.rdy.controller

        # make sure _parent is a RainCloudy.core object
        controller._parent = None
        self.assertRaises(TypeError, controller, '_verify_parent')

        # if _parent is not present, must return __repr__ with ID
        objname = "<RainCloudyController: {}>".format(CONTROLLER_SERIAL)
        self.assertEquals(controller.__repr__(), objname)

        # try to create a Controller object without any faucets
        self.assertRaises(TypeError, RainCloudyController,
                          self.rdy, CONTROLLER_SERIAL)

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


# vim:sw=4:ts=4:et:
