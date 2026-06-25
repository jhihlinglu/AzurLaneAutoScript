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

        # Resume from last cleared stage
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

        for stage in stages:
            stage = str(stage)
            self.config.override(
                StopCondition_MapAchievement=self.config.EventClear_MapAchievement,
                StopCondition_RunCount=0,
                StopCondition_StageIncrease=False,
            )
            task_ended_early = False
            try:
                super().run(name=stage, folder=self.config.Campaign_Event, total=0)
            except TaskEnd:
                # task_switched() or event_time_limit inside CampaignRun
                task_ended_early = True
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

            if task_ended_early:
                # Save LastStage if any battles completed so we resume correctly
                if self.run_count > 0:
                    with self.config.multi_set():
                        self.config.Scheduler_Enable = True
                        self.config.EventClear_LastStage = stage
                self.config.task_stop()

            # Reliable achievement signal: handle_map_stop() sets Scheduler_Enable=False
            # when triggered_map_stop() fires (stage truly achieved).
            # Emotion control keeps Enable=True (emotion handler re-enables before stopping).
            stage_cleared = not self.config.Scheduler_Enable

            if not stage_cleared:
                # Stopped before achievement was confirmed (emotion control, oil stop, etc.)
                # Config NextRun/Enable already set by whichever handler stopped us.
                # Add oil delay on top if oil is also low.
                if self.get_oil() < max(500, self.config.StopCondition_OilLimit):
                    with self.config.multi_set():
                        self.config.task_delay(minute=(120, 240))
                self.config.task_stop()

            # Stage cleared — oil check before advancing
            if self.get_oil() < max(500, self.config.StopCondition_OilLimit):
                with self.config.multi_set():
                    self.config.Scheduler_Enable = True
                    self.config.EventClear_LastStage = stage
                    self.config.task_delay(minute=(120, 240))
                self.config.task_stop()

            if self.run_count == 0:
                logger.info(f'Stage {stage} already achieved, advancing')

            # Re-enable and record progress. Do NOT call task_delay(minute=0) here —
            # that would change NextRun and make task_switched() always return True,
            # breaking the loop after every stage. Let the loop continue naturally;
            # task_switched() will interrupt only when another task actually takes priority.
            with self.config.multi_set():
                self.config.Scheduler_Enable = True
                self.config.EventClear_LastStage = stage

            if self.config.task_switched():
                self.config.task_stop()

        logger.hr('All stages cleared')
        self.config.Scheduler_Enable = False
        self.config.task_stop()
