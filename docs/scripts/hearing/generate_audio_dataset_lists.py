import argparse
import os

AUDIO_EXTENSIONS = {'.wav', '.mp3', '.flac', '.m4a', '.ogg'}


def normalize_label_name(dirname):
    """Convert `0_Blast` to `Blast`, while keeping `Blast` unchanged."""
    parts = dirname.split('_', 1)
    if len(parts) == 2 and parts[0].isdigit():
        return parts[1]
    return dirname


# 生成数据列表
def get_data_list(audio_path, list_path):
    sound_sum = 0
    audios = [
        name for name in sorted(os.listdir(audio_path))
        if os.path.isdir(os.path.join(audio_path, name))
    ]
    os.makedirs(list_path, exist_ok=True)

    train_list_path = os.path.join(list_path, 'train_list.txt')
    test_list_path = os.path.join(list_path, 'test_list.txt')
    label_list_path = os.path.join(list_path, 'label_list.txt')

    with open(train_list_path, 'w', encoding='utf-8') as f_train, \
            open(test_list_path, 'w', encoding='utf-8') as f_test, \
            open(label_list_path, 'w', encoding='utf-8') as f_label:
        for i, audio_dir in enumerate(audios):
            f_label.write(f'{normalize_label_name(audio_dir)}\n')
            class_dir = os.path.join(audio_path, audio_dir)
            sounds = [
                name for name in sorted(os.listdir(class_dir))
                if os.path.splitext(name)[1].lower() in AUDIO_EXTENSIONS
            ]
            for sound in sounds:
                sound_path = os.path.join(class_dir, sound).replace('\\', '/')
                if sound_sum % 10 == 0:
                    f_test.write(f'{sound_path}\t{i}\n')
                else:
                    f_train.write(f'{sound_path}\t{i}\n')
                sound_sum += 1
            print(f'Audio: {i + 1}/{len(audios)}, label={normalize_label_name(audio_dir)}, files={len(sounds)}')

    print(f'Generated: {train_list_path}')
    print(f'Generated: {test_list_path}')
    print(f'Generated: {label_list_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create train/test/label lists for AudioClassification-Pytorch.')
    parser.add_argument('--audio_path', default='dataset/hazardous_sound_detection/audioset', help='音频数据根目录，每个子目录为一个类别')
    parser.add_argument('--list_path', default='dataset/hazardous_sound_detection', help='输出 train_list.txt、test_list.txt、label_list.txt 的目录')
    args = parser.parse_args()
    get_data_list(args.audio_path, args.list_path)
