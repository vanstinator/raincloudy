from raincloudy.core import RainCloudy

raincloud = RainCloudy(username='justinvdhooft@gmail.com', password='5K7m#3gSZ8FrugBHMD11V6LJ71')

for controller in raincloud.controllers:
    print('\nController: ' + controller.name)
    for faucet in controller.faucets:
        print('\nFaucet: ' + faucet.name)
        for zone in faucet.zones:
            print('Zone: ' + zone.name)
            # zone.auto_watering = False
            # print(zone.manual_watering)

raincloud.controllers[0].name = 'Test This'
raincloud.controllers[1].name = 'Cool Bro'
raincloud.controllers[0].faucets[1].zone3.name = 'Le Sigh?'
raincloud.controllers[0].faucets[0].name = 'Ho!'