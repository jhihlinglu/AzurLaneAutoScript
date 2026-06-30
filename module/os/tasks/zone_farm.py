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

        if self.config.OpsiZoneFarm_TargetZone == 0:
            raise RequestHumanTakeover('TargetZone is not set, please specify a zone ID')

        try:
            zone = self.name_to_zone(self.config.OpsiZoneFarm_TargetZone)
        except ScriptError:
            logger.warning(f'Wrong zone_id input: {self.config.OpsiZoneFarm_TargetZone}')
            raise RequestHumanTakeover('Wrong TargetZone input, task stopped')

        preserve = self.config.OpsiZoneFarm_ActionPointPreserve
        use_box = self.config.OpsiZoneFarm_UseActionPointBox

        logger.hr(
            f'OS zone farm, zone_id={zone.zone_id}, preserve={preserve}, use_box={use_box}',
            level=1
        )

        while True:
            self.config.OS_ACTION_POINT_PRESERVE = preserve
            self.config.OS_ACTION_POINT_BOX_USE = use_box
            logger.attr('OS_ACTION_POINT_PRESERVE', self.config.OS_ACTION_POINT_PRESERVE)
            logger.attr('OS_ACTION_POINT_BOX_USE', self.config.OS_ACTION_POINT_BOX_USE)

            self.globe_goto(zone, types='SAFE', refresh=True)
            self.fleet_set(self.config.OpsiFleet_Fleet)
            self.os_order_execute(
                recon_scan=False,
                submarine_call=self.config.OpsiFleet_Submarine)
            self.run_auto_search()
            self.handle_after_auto_search()
            self.config.check_task_switch()
