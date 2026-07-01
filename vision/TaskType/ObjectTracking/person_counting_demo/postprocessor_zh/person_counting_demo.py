from logger import LOGGER
from postprocessor import Postprocessor as BasePostprocessor
from postprocessor.utils.cv_utils.geo_utils import is_seg_intersect
from tracker import Tracker


class Postprocessor(BasePostprocessor):
    def __init__(self, source_id, alg_name):
        super().__init__(source_id, alg_name)
        self.strategy = None
        self.tracker = None
        self.max_retain = 0
        self.targets = {}

    def __is_rectangle_intersect_line(self, rectangle, line):
        """
        检查检测框是否与线段相交
        Args:
            rectangle: 目标检测框 [x1, y1, x2, y2]
            line: 线段坐标 [[x1, y1], [x2, y2]]
        Returns: True or False
        """
        x1, y1, x2, y2 = rectangle
        # 检测框的四条边
        rect_edges = [
            ((x1, y1), (x2, y1)),  # 上边
            ((x2, y1), (x2, y2)),  # 右边
            ((x2, y2), (x1, y2)),  # 下边
            ((x1, y2), (x1, y1))  # 左边
        ]
        # 检查线段是否与检测框的任意一条边相交
        for edge in rect_edges:
            if is_seg_intersect(edge, line):
                return True
        # 检查线段是否完全在检测框内部
        line_start, line_end = line
        if (x1 <= line_start[0] <= x2 and y1 <= line_start[1] <= y2 and
                x1 <= line_end[0] <= x2 and y1 <= line_end[1] <= y2):
            return True
        return False

    def __check_lost_target(self, tracker_result):
        for track_id in list(self.targets.keys()):
            if track_id not in tracker_result:
                self.targets[track_id]['lost'] += 1
            else:
                self.targets[track_id]['lost'] = 0
            if self.targets[track_id]['lost'] > self.max_retain:
                LOGGER.info('Target lost, source_id={}, alg_name={}, track_id={}, pre_target={}'.format(
                    self.source_id, self.alg_name, track_id, self.targets[track_id]['pre_target']))
                del self.targets[track_id]
        return True

    def _process(self, result, filter_result):
        hit = False
        if self.strategy is None:
            self.strategy = self.reserved_args['strategy']
        polygons = self._gen_polygons()
        lines = self._gen_lines()
        if self.tracker is None:
            self.tracker = Tracker(self.frame_interval)
            self.max_retain = self.tracker.track_buffer + 1
            LOGGER.info('Init tracker, source_id={}, alg_name={}, track_buffer={}'.format(
                self.source_id, self.alg_name, self.tracker.track_buffer))
        model_name, rectangles = next(iter(filter_result.items()))
        # 目标跟踪
        tracker_result = self.tracker.track(rectangles)
        # 检查丢失目标
        self.__check_lost_target(tracker_result)
        for track_id, rectangle in tracker_result.items():
            target = self.targets.get(track_id)
            if target is None:
                target = {
                    'lost': 0,
                    'pre_target': None,
                    # 记录每条线的状态：'free'(可计数) 或 'occupied'(已计数，需离开)
                    'line_states': {}
                }
                self.targets[track_id] = target
            if target['pre_target'] is not None:
                # 默认为非告警状态，如果任何线段触发则会被覆盖
                rectangle['color'] = self.non_alert_color
                for line_id, line in lines.items():
                    # 获取当前线段的状态
                    line_state = target['line_states'].get(line_id, 'free')
                    # 检查检测框是否与线段相交
                    is_intersect = self.__is_rectangle_intersect_line(
                        rectangle['xyxy'], line['line'])
                    if line_state == 'free':
                        # 可以进行跨线检测
                        result_ = self._cross_line_counting(
                            target['pre_target']['xyxy'], rectangle['xyxy'],
                            line['line'], line['ext']['direction'], self.strategy)
                        if result_ is not None:
                            hit = True
                            line['color'] = self.alert_color
                            self._set_ext(line, alert=True)
                            rectangle['color'] = self.alert_color
                            self._merge_cross_line_counting_result(
                                line['ext']['result'], result_)
                            # 标记为已计数状态，需要离开线段才能再次计数
                            target['line_states'][line_id] = 'occupied'
                            # 不break，继续检查其他线段
                    elif line_state == 'occupied':
                        # 已经计数过，检查检测框是否完全离开线段
                        if not is_intersect:
                            # 检测框完全离开线段，重置为可计数状态
                            target['line_states'][line_id] = 'free'
                        else:
                            # 检测框仍与线段相交，保持占用颜色但不计数
                            rectangle['color'] = self.non_alert_color
            else:
                rectangle['color'] = self.non_alert_color
            target['pre_target'] = rectangle
            result['data']['bbox']['rectangles'].append(rectangle)
        result['hit'] = hit
        result['data']['bbox']['polygons'].update(polygons)
        result['data']['bbox']['lines'].update(lines)
        return True
