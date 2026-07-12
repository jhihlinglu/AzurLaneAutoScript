from module.exception import RequestHumanTakeover, ScriptError
from module.logger import logger
from module.os.map import OSMap


class OpsiZoneFarm(OSMap):
    def os_zone_farm(self):
        logger.hr('OS zone farm', level=1)

        if self.is_in_opsi_explore():
            logger.warning(f'OpsiExplore is still running, cannot do {self.config.task.command}')
            self.config.task_delay(server_update=True)
            self.config.task_stop()

        raw = str(self.config.OpsiZoneFarm_TargetZone).strip()
        # Support full-width comma（，）as delimiter
        zone_names = [z.strip() for z in raw.replace('，', ',').split(',') if z.strip() and z.strip() != '0']

        if not zone_names:
            raise RequestHumanTakeover('TargetZone is not set, please specify a zone ID')

        zones = []
        for name in zone_names:
            try:
                zone = self.name_to_zone(name)
                zones.append(zone)
            except ScriptError:
                logger.warning(f'Wrong zone_id input: {name}')
                raise RequestHumanTakeover(f'Wrong TargetZone input: {name}, task stopped')

        preserve = self.config.OpsiZoneFarm_ActionPointPreserve
        use_box = self.config.OpsiZoneFarm_UseActionPointBox
        zone_ids = ', '.join(str(z.zone_id) for z in zones)

        logger.hr(
            f'OS zone farm, zones=[{zone_ids}], preserve={preserve}, use_box={use_box}',
            level=1
        )

        while True:
            self.config.OS_ACTION_POINT_PRESERVE = preserve
            self.config.OS_ACTION_POINT_BOX_USE = use_box
            logger.attr('OS_ACTION_POINT_PRESERVE', self.config.OS_ACTION_POINT_PRESERVE)
            logger.attr('OS_ACTION_POINT_BOX_USE', self.config.OS_ACTION_POINT_BOX_USE)

            for zone in zones:
                logger.hr(f'Zone farm: {zone}', level=2)
                self.globe_goto(zone, types='SAFE', refresh=True)
                self.fleet_set(self.config.OpsiFleet_Fleet)
                self.os_order_execute(
                    recon_scan=False,
                    submarine_call=self.config.OpsiFleet_Submarine)
                self.run_auto_search()
                self.handle_after_auto_search()
                self.config.check_task_switch()
