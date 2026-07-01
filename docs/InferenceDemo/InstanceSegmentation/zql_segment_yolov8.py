import cv2
import numpy as np

from logger import LOGGER
from model import RknnModel
from utils.image_utils import opencv_to_bytes


class Model(RknnModel):
    default_args = {
        'max_wh': 7680,  # maximum box width and height
        'max_nms': 30000,  # maximum number of boxes
        'img_size': 640,
        'nms_thres': 0.45,
        'conf_thres': 0.25
    }

    def __init__(self, acc_id, name, conf):
        super().__init__(acc_id, name, conf, ['model'])

    def __process_mask(self, protos, masks_in, bboxes, shape, upsample=False):
        """
        Crop before upsample.
        proto_out: [mask_dim, mask_h, mask_w]
        out_masks: [n, mask_dim], n is number of masks after nms
        bboxes: [n, 4], n is number of masks after nms
        shape:input_image_size, (h, w)

        return: h, w, n
        """
        c, mh, mw = protos.shape  # CHW
        ih, iw = shape
        masks = self.__sigmoid(masks_in @ protos.astype(np.float32).reshape(c, -1)).reshape(-1, mh, mw)  # CHW
        downsampled_bboxes = bboxes.copy()
        downsampled_bboxes[:, 0] *= mw / iw
        downsampled_bboxes[:, 2] *= mw / iw
        downsampled_bboxes[:, 3] *= mh / ih
        downsampled_bboxes[:, 1] *= mh / ih
        masks = self.__crop_mask(masks, downsampled_bboxes)  # CHW
        if upsample:
            target_shape = shape[:2]
            resampled = np.zeros((masks.shape[0],) + target_shape)
            for i in range(masks.shape[0]):
                resampled[i] = cv2.resize(masks[i], (target_shape[1], target_shape[0]), interpolation=cv2.INTER_LINEAR)
            masks = resampled
        return np.where(masks > 0.5, 1, 0)

    @staticmethod
    def __sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def __crop_mask(masks, boxes):
        """
        "Crop" predicted masks by zeroing out everything not in the predicted bbox.
        Vectorized by Chong (thanks Chong).

        Args:
            - masks should be a size [h, w, n] tensor of masks
            - boxes should be a size [n, 4] tensor of bbox coords in relative point form
        """
        n, h, w = masks.shape
        x1, y1, x2, y2 = np.split(boxes[:, :, None], 4, 1)  # x1 shape(1,1,n)
        r = np.arange(w, dtype=x1.dtype)[None, None, :]  # rows shape(1,w,1)
        c = np.arange(h, dtype=x1.dtype)[None, :, None]  # cols shape(h,1,1)
        return masks * ((r >= x1) * (r < x2) * (c >= y1) * (c < y2))

    def _load_args(self, args):
        try:
            self.max_wh = args.get('max_wh', self.default_args['max_wh'])
            self.max_nms = args.get('max_nms', self.default_args['max_nms'])
            self.img_size = args.get('img_size', self.default_args['img_size'])
            self.nms_thres = args.get('nms_thres', self.default_args['nms_thres'])
            self.conf_thres = args.get('conf_thres', self.default_args['conf_thres'])
        except:
            LOGGER.exception('_load_args')
            return False
        return True
    
    '''-----------------------------------------yolov11_seg_post_process----------------------------------------'''
    def __dfl(self, position):
        # Distribution Focal Loss (DFL) - NumPy version
        x = np.array(position)
        n, c, h, w = x.shape
        p_num = 4
        mc = c // p_num
        y = x.reshape(n, p_num, mc, h, w)
        # Softmax along the mc dimension (axis=2)
        y_exp = np.exp(y - np.max(y, axis=2, keepdims=True))  # for numerical stability
        y = y_exp / np.sum(y_exp, axis=2, keepdims=True)
        # Create accumulator matrix and compute weighted sum
        acc_matrix = np.arange(mc).reshape(1, 1, mc, 1, 1).astype(np.float32)
        y = (y * acc_matrix).sum(axis=2)
        return y

    def __filter_boxes(self, boxes, box_confidences, box_class_probs, seg_part):
        """Filter boxes with object threshold.
        """
        box_confidences = box_confidences.reshape(-1)
        class_max_score = np.max(box_class_probs, axis=-1)
        classes = np.argmax(box_class_probs, axis=-1)

        _class_pos = np.where(class_max_score * box_confidences >= self.conf_thres)
        scores = (class_max_score * box_confidences)[_class_pos]

        boxes = boxes[_class_pos]
        classes = classes[_class_pos]
        seg_part = (seg_part * box_confidences.reshape(-1, 1))[_class_pos]

        return boxes, classes, scores, seg_part

    def __box_process(self, position, shape):
        grid_h, grid_w = position.shape[2:4]
        col, row = np.meshgrid(np.arange(0, grid_w), np.arange(0, grid_h))
        col = col.reshape(1, 1, grid_h, grid_w)
        row = row.reshape(1, 1, grid_h, grid_w)
        grid = np.concatenate((col, row), axis=1)
        stride = np.array([shape[1]//grid_h, shape[0] //grid_w]).reshape(1, 2, 1, 1)
        position = self.__dfl(position)
        box_xy  = grid +0.5 -position[:,0:2,:,:]
        box_xy2 = grid +0.5 +position[:,2:4,:,:]
        xyxy = np.concatenate((box_xy*stride, box_xy2*stride), axis=1)
        return xyxy

    def __post_process(self, input_data, agnostic=False, max_det=300):
        # input_data[0], input_data[4], and input_data[8] are detection box information
        # input_data[1], input_data[5], and input_data[9] are category score information
        # input_data[2], input_data[6], and input_data[10] are confidence score information
        # input_data[3], input_data[7], and input_data[11] are segmentation information
        # input_data[12] is the proto information
        
        proto = input_data[-1]
        proto_backup = proto
        boxes, scores, classes_conf, seg_part = [], [], [], []
        defualt_branch=3
        pair_per_branch = len(input_data)//defualt_branch
        for i in range(defualt_branch):
            boxes.append(self.__box_process(input_data[pair_per_branch*i], (self.img_size, self.img_size)))
            classes_conf.append(input_data[pair_per_branch*i+1])
            scores.append(np.ones_like(input_data[pair_per_branch*i+1][:,:1,:,:], dtype=np.float32))
            seg_part.append(input_data[pair_per_branch*i+3])

        def sp_flatten(_in):
            ch = _in.shape[1]
            _in = _in.transpose(0,2,3,1)
            return _in.reshape(-1, ch)

        boxes = np.concatenate([sp_flatten(_v) for _v in boxes])
        classes_conf = np.concatenate([sp_flatten(_v) for _v in classes_conf])
        scores = np.concatenate([sp_flatten(_v) for _v in scores])
        seg_part = np.concatenate([sp_flatten(_v) for _v in seg_part])

        # 根据阈值过滤
        boxes, classes, scores, seg_part = self.__filter_boxes(boxes, scores, classes_conf, seg_part)
        zipped = zip(boxes, classes, scores, seg_part)
        sort_zipped = sorted(zipped, key=lambda x: (x[2]), reverse=True)
        result = zip(*sort_zipped)
        n = boxes.shape[0]  # number of boxes
        if not n:
            return None, None, None, None
        elif n > self.max_nms:  # excess boxes
            boxes, classes, scores, seg_part = [np.array(x[:self.max_nms]) for x in result]
        else:
            boxes, classes, scores, seg_part = [np.array(x) for x in result]
        # nms
        nboxes, nclasses, nscores, nseg_part = [], [], [], []
        c = classes * (0 if agnostic else self.max_wh)
        keeps = self._nms_boxes(boxes + c.reshape(-1, 1), scores)
        real_keeps = keeps[:max_det]
        nboxes.append(boxes[real_keeps])
        nclasses.append(classes[real_keeps])
        nscores.append(scores[real_keeps])
        nseg_part.append(seg_part[real_keeps])
        if not nclasses and not nscores:
            return None, None, None, None
        boxes = np.concatenate(nboxes)
        classes = np.concatenate(nclasses)
        scores = np.concatenate(nscores)
        seg_part = np.concatenate(nseg_part)
        
        nmasks = self.__process_mask(proto_backup[0], seg_part, boxes, (self.img_size, self.img_size), upsample=True)
        nmasks = (nmasks * 255).astype(np.uint8)
        return nboxes[0], nclasses[0], nscores[0], nmasks

    def infer(self, data, **kwargs):
        """
        实例分割
        Args:
            data: 图像数据，ndarray类型，RGB格式（BGR格式需转换）
        Returns: infer_result
        """
        infer_result = []
        if self.status:
            try:
                image = data
                scale = 1
                raw_width, raw_height = image.shape[1], image.shape[0]
                if max(image.shape[:2]) != self.img_size:
                    scale = self.img_size / max(image.shape[:2])
                    if raw_height > raw_width:
                        image = cv2.resize(image, (int(raw_width * scale), self.img_size))
                    else:
                        image = cv2.resize(image, (self.img_size, int(raw_height * scale)))
                image, dw, dh = self._letterbox(image, (self.img_size, self.img_size))
                image = np.expand_dims(image, axis=0)
                outputs = self._rknn_infer('model', [image])
                boxes, classes, scores, masks = self.__post_process(outputs)
                if boxes is not None:
                    for i, box in enumerate(boxes):
                        obj = {
                            'label': int(classes[i]),
                            'conf': round(float(scores[i]), 2)
                        }
                        xyxy = [int(box[0] - dw), int(box[1] - dh), int(box[2] - dw), int(box[3] - dh)]
                        if scale != 1:
                            xyxy = [int(x / scale) for x in xyxy]
                        obj['xyxy'] = [xyxy[0] if xyxy[0] >= 0 else 0,
                                       xyxy[1] if xyxy[1] >= 0 else 0,
                                       xyxy[2] if xyxy[2] <= raw_width else raw_width,
                                       xyxy[3] if xyxy[3] <= raw_height else raw_height]
                        mask_shape = masks[i].shape
                        obj['mask'] = opencv_to_bytes(
                            masks[i][int(dh):int(mask_shape[0] - dh), int(dw):int(mask_shape[1] - dw)])
                        infer_result.append(obj)
            except:
                LOGGER.exception('infer')
        return infer_result