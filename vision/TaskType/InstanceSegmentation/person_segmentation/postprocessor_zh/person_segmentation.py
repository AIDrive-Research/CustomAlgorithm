import cv2
import numpy as np

from postprocessor import Postprocessor as BasePostprocessor
from postprocessor.utils.image_utils.turbojpegutils import bytes_to_mat
from postprocessor.utils.unique_id_utils import get_object_id


class Postprocessor(BasePostprocessor):
    def __init__(self, source_id, alg_name):
        super().__init__(source_id, alg_name)
        self.mask_model_name = 'custom_segment'
        self.image_width, self.image_height = None, None
    
    @staticmethod
    def __mask_to_polygon(mask):
        if mask is None or mask.size == 0 or not mask.any():
            return None
        mask_uint8 = (mask > 0).astype(np.uint8) * 255
        contours, _ = cv2.findContours(mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if not contours:
            return None
        cnt = max(contours, key=cv2.contourArea)
        polygon = cnt.reshape(-1, 2)
        polygon_down = polygon[::2]
        return polygon_down.tolist()

    def _gen_mask_polygons(self, data):
        polygons = data.get('polygons', [])
        polygons_ = {}
        for polygon in polygons:
            polygons_[polygon['id']] = {
                'name': polygon['name'],
                'polygon': polygon['polygon'],
                'color': self.alert_color
            }
            self._set_ext(polygons_[polygon['id']])
        return polygons_
    
    def _process(self, result, filter_result):
        hit = False
        # Get the annotated detection region
        polygons = self._gen_polygons()
        model_name, targets = next(iter(filter_result.items()))
        polygons_mask = {}
        for target in targets:
            hit = True
            xyxy = target['xyxy']   
            mask = self._get_ext(target, 'mask', pop=True)
            if mask.any():
                polygon_points = self.__mask_to_polygon(mask)
                polygon_id = get_object_id()
                polygons_mask[polygon_id] = {
                    'name': None,
                    'polygon': polygon_points,
                    'color': self.non_alert_color
                }
            result['data']['bbox']['rectangles'].append(
                self._gen_rectangle(xyxy, self.alert_color, self.alert_label[0], target['conf']))
        result['hit'] = hit
        result['data']['bbox']['polygons'].update(polygons)
        result['data']['bbox']['polygons'].update(polygons_mask)
        return True

    def _filter(self, model_name, model_data):
        targets = []
        if self.image_height is None:
            draw_image = bytes_to_mat(self.draw_image)
            self.image_height, self.image_width = draw_image.shape[:2]
        model_conf = model_data['model_conf']
        engine_result = model_data['engine_result']
        for engine_result_ in engine_result:
            # Filter out objects with confidence below the threshold
            if not self._filter_by_conf(model_conf, engine_result_['conf']):
                continue
            # Filter out objects not in the label list
            label = self._filter_by_label(model_conf, engine_result_['label'])
            if not label:
                continue
            # Coordinate scaling
            xyxy = self._scale(engine_result_['xyxy'])
            # Filter out objects outside the polygon
            if not self._filter_by_roi(xyxy):
                continue
            mask = cv2.imdecode(np.frombuffer(engine_result_['mask'], np.uint8), cv2.IMREAD_GRAYSCALE)
            mask = cv2.resize(mask, (self.image_width, self.image_height), interpolation=cv2.INTER_NEAREST)
            # Generate a bounding box
            targets.append(self._gen_rectangle(
                xyxy, self.non_alert_color, label, engine_result_['conf'],
                mask=mask))
        return targets
