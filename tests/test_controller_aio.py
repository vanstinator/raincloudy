# -*- coding: utf-8 -*-
"""Test raincloudy.controller."""
from aioresponses import aioresponses
from aiohttp import ClientSession
from tests.test_base_aio import UnitTestBaseAsync
from tests.extras import CONTROLLER_NAME, CONTROLLER_SERIAL, CONTROLLER_TIMESTAMP


class TestRainCloudyControllerAsync(UnitTestBaseAsync):
    """Unit tests for controller attributes."""

    @aioresponses()
    async def test_errors_or_exceptions(self, mocked):
        """Tests for errors or exceptions."""
        from raincloudy.aio.controller import RainCloudyController

        self.add_methods(mocked)
        await self.rdy.login()

        controller = self.rdy.controllers[0]

        # make sure _parent is a RainCloudy.core object
        self.assertRaises(TypeError, RainCloudyController, None, None)

        # if _parent is not present, must return __repr__ with ID
        controller._parent = None
        objname = "<RainCloudyController: {}>".format(CONTROLLER_SERIAL)
        self.assertEquals(controller.__repr__(), objname)

        # try to create a Controller object without any faucets
        self.assertRaises(TypeError, RainCloudyController, self.rdy, CONTROLLER_SERIAL)

    @aioresponses()
    async def test_attributes(self, mocked):
        """Test controller attributes."""
        self.add_methods(mocked)
        await self.rdy.login()

        controller = self.rdy.controllers[0]

        self.assertTrue(hasattr(controller, "current_time"))
        self.assertTrue(hasattr(controller, "faucets"))
        self.assertTrue(hasattr(controller, "id"))
        self.assertTrue(hasattr(controller, "name"))
        self.assertTrue(hasattr(controller, "serial"))
        self.assertTrue(hasattr(controller, "status"))
        self.assertTrue(hasattr(controller, "update"))

        objname = "<RainCloudyController: {}>".format(CONTROLLER_NAME)
        self.assertEquals(controller.__repr__(), objname)

        self.assertEquals(controller.current_time, CONTROLLER_TIMESTAMP)
        self.assertEquals(controller.id, CONTROLLER_SERIAL)
        self.assertEquals(controller.name, CONTROLLER_NAME)
        self.assertEquals(controller.status, "Online")


# vim:sw=4:ts=4:et:
