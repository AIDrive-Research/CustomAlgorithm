import kaldi_native_fbank as knf
import numpy as np

from logger import LOGGER
from model import RknnModel


class Model(RknnModel):
    default_args = {
        'num_frames': 300,
        'model_sample_rate': 16000,
        'min_duration': 0.4,
        'use_dB_normalization': True,
        'target_dB': -20,
        'feature_method': 'Fbank',
        'use_hf_model': False,
        'num_mel_bins': 80,
    }

    def __init__(self, acc_id, name, conf):
        super().__init__(acc_id, name, conf, ['model'])

    def _load_args(self, args):
        try:
            self.num_frames = int(args.get('num_frames', self.default_args['num_frames']))
            self.model_sample_rate = int(args.get('model_sample_rate', self.default_args['model_sample_rate']))
            self.min_duration = float(args.get('min_duration', self.default_args['min_duration']))
            self.use_db_normalization = self.__to_bool(
                args.get('use_dB_normalization', self.default_args['use_dB_normalization']))
            self.target_db = float(args.get('target_dB', self.default_args['target_dB']))
            self.feature_method = args.get('feature_method', self.default_args['feature_method'])
            self.use_hf_model = self.__to_bool(args.get('use_hf_model', self.default_args['use_hf_model']))
            self.num_mel_bins = int(args.get('num_mel_bins', self.default_args['num_mel_bins']))
            if self.num_frames <= 0:
                LOGGER.error('Invalid num_frames, value={}'.format(self.num_frames))
                return False
            if self.model_sample_rate <= 0:
                LOGGER.error('Invalid model_sample_rate, value={}'.format(self.model_sample_rate))
                return False
            if self.min_duration <= 0:
                LOGGER.error('Invalid min_duration, value={}'.format(self.min_duration))
                return False
            if self.num_mel_bins <= 0:
                LOGGER.error('Invalid num_mel_bins, value={}'.format(self.num_mel_bins))
                return False
            if 'Fbank' != self.feature_method:
                LOGGER.error('Unsupported feature_method, value={}'.format(self.feature_method))
                return False
            if self.use_hf_model:
                LOGGER.error('Unsupported use_hf_model, value={}'.format(self.use_hf_model))
                return False
            self.fbank_opts = self.__build_fbank_options(
                sample_frequency=self.model_sample_rate, num_mel_bins=self.num_mel_bins)
            return True
        except:
            LOGGER.exception('_load_args')
            return False

    @staticmethod
    def __to_bool(value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ['1', 'true', 'yes', 'on']
        return bool(value)

    @staticmethod
    def __build_fbank_options(sample_frequency, num_mel_bins):
        opts = knf.FbankOptions()
        opts.frame_opts.dither = 0.0
        opts.frame_opts.snip_edges = True
        opts.frame_opts.window_type = 'povey'
        opts.frame_opts.samp_freq = float(sample_frequency)
        opts.mel_opts.num_bins = int(num_mel_bins)
        return opts

    @staticmethod
    def __softmax(logits):
        logits = logits - np.max(logits)
        probs = np.exp(logits)
        return probs / (np.sum(probs) + 1e-12)

    def __fit_num_frames(self, feature):
        frame_len, feat_dim = feature.shape
        if frame_len == self.num_frames:
            return feature
        if frame_len > self.num_frames:
            # 这里直接截断前num_frames帧，保持输入尺寸稳定。
            return feature[:self.num_frames, :]
        # 帧数不足时在尾部补零，保持模型输入shape不变。
        padded = np.zeros((self.num_frames, feat_dim), dtype=np.float32)
        padded[:frame_len, :] = feature
        return padded

    def __extract_feature(self, audio_segment):
        samples = np.asarray(audio_segment, dtype=np.float32)
        online_fbank = knf.OnlineFbank(self.fbank_opts)
        # kaldi_native_fbank这里接收的是以16bit幅值为基准的浮点列表，因此需要先把[-1, 1]范围的音频放大回接近PCM幅值。
        online_fbank.accept_waveform(
            float(self.model_sample_rate),
            (samples * 32768.0).tolist())
        online_fbank.input_finished()
        frame_count = int(online_fbank.num_frames_ready)
        if frame_count <= 0:
            LOGGER.error('Extract feature failed, no frame generated')
            return None
        feature = np.stack([online_fbank.get_frame(i) for i in range(frame_count)]).astype(np.float32)
        # 做一次按维度中心化，降低不同录音音量和底噪带来的全局偏移。
        feature = feature - np.mean(feature, axis=0, keepdims=True)
        return feature

    @staticmethod
    def __normalize_db(samples, target_db):
        rms = np.sqrt(np.mean(samples ** 2) + 1e-12)
        if rms > 0:
            scalar = 10 ** (target_db / 20.0) / rms
            samples = samples * scalar
        return samples

    def __aed_infer(self, audio_float):
        try:
            samples = np.asarray(audio_float, dtype=np.float32)
            if samples.size == 0:
                LOGGER.warning('AED infer failed, empty audio input')
                return None, 0.0
            min_samples = int(self.model_sample_rate * self.min_duration)
            if samples.size < min_samples:
                LOGGER.warning('AED infer skipped, audio is too short, min_duration={}, sample_size={}'.format(
                    self.min_duration, samples.size))
                return None, 0.0
            if self.use_db_normalization:
                samples = self.__normalize_db(samples, self.target_db)
            feature = self.__extract_feature(samples)
            if feature is None:
                return None, 0.0
            feature = self.__fit_num_frames(feature)
            outputs = self._rknn_infer('model', [np.expand_dims(feature, axis=0)])
            if not outputs:
                LOGGER.error('AED infer failed, empty rknn output')
                return None, 0.0
            logits = np.asarray(outputs[0], dtype=np.float32).reshape(-1)
            if logits.size == 0:
                LOGGER.error('AED infer failed, empty logits')
                return None, 0.0
            probs = self.__softmax(logits)
            return probs
        except:
            LOGGER.exception('__aed_infer')
            return None

    @staticmethod
    def __load_bytes(data):
        if isinstance(data, np.ndarray):
            return np.asarray(data, dtype=np.float32)
        if isinstance(data, (bytes, bytearray)):
            int16_data = np.frombuffer(data, dtype=np.int16)
            return int16_data.astype(np.float32) / 32768.0
        raise TypeError('Unsupported audio data type: {}'.format(type(data)))

    def infer(self, data, **kwargs):
        infer_result = None
        if self.status:
            try:
                audio_float = self.__load_bytes(data)
                probs = self.__aed_infer(audio_float)
                if probs is not None:
                    label = int(np.argmax(probs))
                    conf_ = float(np.max(probs))
                    infer_result = {
                        'label': label,
                        'conf': conf_
                    }
            except:
                LOGGER.exception('infer')
        return infer_result
