import os

from module.config.config import TaskEnd
from module.event.base import STAGE_FILTER, EventBase, EventStage
from module.exception import ScriptEnd, RequestHumanTakeover
from module.logger import logger


class EventClear(EventBase):
    def run(self, *args, **kwargs):
        # Filter map files
        stages = [EventStage(file) for file in os.listdir(f'./campaign/{self.config.Campaign_Event}')]
        stages = self.convert_stages(stages)
        logger.attr('Stage', [str(stage) for stage in stages])
        logger.attr('StageFilter', self.config.EventClear_StageFilter)
        STAGE_FILTER.load(self.config.EventClear_StageFilter)
        self.convert_stages(STAGE_FILTER)
        stages = [str(stage) for stage in STAGE_FILTER.apply(stages)]
        logger.attr('Filter sort', ' > '.join(stages))

        if not stages:
            logger.warning('No stage satisfy current filter')
            self.config.Scheduler_Enable = False
            self.config.task_stop()

        # Resume from last cleared stage (achievements are permanent, no daily reset needed)
        logger.info(f'LastStage: {self.config.EventClear_LastStage}')
        last = str(self.config.EventClear_LastStage).lower()
        last = self.convert_stages(last)
        if last in stages:
            stages = stages[stages.index(last) + 1:]
            logger.attr('Remaining stages', ' > '.join(stages))
        else:
            logger.info('Start from the beginning')

        if not stages:
            logger.info('All stages have been cleared, disabling task')
            self.config.Scheduler_Enable = False
            self.config.task_stop()

        # Run each stage until the achievement condition is met
        for stage in stages:
            stage = str(stage)
            # Force achievement-oriented settings for this task:
            # - MapAchievement drives MAP_CLEAR_ALL_THIS_TIME (kill all enemies before boss)
            # - RunCount=0 means no count limit (run until achievement triggers)
            # - StageIncrease=False so EventClear controls progression, not handle_map_stop()
            self.config.override(
                StopCondition_MapAchievement=self.config.EventClear_MapAchievement,
                StopCondition_RunCount=0,
                StopCondition_StageIncrease=False,
            )
            try:
                super().run(name=stage, folder=self.config.Campaign_Event, total=0)
            except TaskEnd:
                # Catch task switch from scheduler
                pass
            except ScriptEnd as e:
                if str(e) == 'Campaign name error':
                    task = self.config.task.command
                    logger.critical(
                        f'Cannot find stage "{stage}". '
                        f'Stage "{stage}" may not be unlocked yet. '
                        f'Use task "Event" to unlock it before using task "{task}"')
                    raise RequestHumanTakeover
                else:
                    raise

            # handle_map_stop() sets Scheduler_Enable=False when achievement is detected
            # (because StopCondition_StageIncrease=False). Re-enable here so that
            # task_switched() still sees EventClear as the active task and the for
            # loop can continue to the next stage.
            self.config.Scheduler_Enable = True

            if self.run_count > 0:
                # Battles were run this stage — check if oil caused an early stop
                # (triggered_stop_condition breaks the loop before achievement is confirmed)
                if self.get_oil() < max(500, self.config.StopCondition_OilLimit):
                    logger.info('Oil limit reached mid-stage, will retry this stage after oil recovery')
                    with self.config.multi_set():
                        self.config.task_delay(minute=(120, 240))
                    self.config.task_stop()
                # Achievement reached this session — record and advance
                with self.config.multi_set():
                    self.config.EventClear_LastStage = stage
                    self.config.task_delay(minute=0)
            else:
                # run_count == 0 has two possible meanings:
                # 1. triggered_map_stop() fired on map entry → stage already achieved → advance
                # 2. triggered_stop_condition() fired before first battle → oil was too low
                if self.get_oil() < max(500, self.config.StopCondition_OilLimit):
                    logger.info('Oil limit reached before entering stage, pausing')
                    with self.config.multi_set():
                        self.config.task_delay(minute=(120, 240))
                    self.config.task_stop()
                # Stage confirmed already achieved
                logger.info(f'Stage {stage} already achieved, advancing')
                self.config.EventClear_LastStage = stage

            if self.config.task_switched():
                self.config.task_stop()

        # All stages in filter have been cleared
        logger.hr('All stages cleared')
        self.config.Scheduler_Enable = False
        self.config.task_stop()
